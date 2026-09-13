"""Translate public documentation; author/creator/modifier: Neil Mitchell.

Only Python's standard library is required. Model output is data, never code.
"""

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
META = "<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->"
NAV_START = "<!-- LANGUAGES:START -->"
NAV_END = "<!-- LANGUAGES:END -->"
NAV_RE = re.compile(re.escape(NAV_START) + r".*?" + re.escape(NAV_END) + r"\n*", re.S)
TOKEN = re.compile(r"ZXQKEEP\d{5}QXZ")
# Protect executable examples, URLs, HTML, code, and numerical release evidence.
PROTECTED = re.compile(
    r"^```[^\n]*\n.*?^```[^\n]*$|^~~~[^\n]*\n.*?^~~~[^\n]*$"
    r"|^\s*WINEPREFIX=[^\n]+|^Author / Creator / Last Modified By:[^\n]+"
    r"|<!--.*?-->|<[^>\n]+>|`+[^`\n]+`+"
    r"|(?<=\]\()[^\s)]+|https?://[^\s<>\])]+"
    r"|Neil Mitchell|Lau Setup|World of Warcraft|Wine Mono|/pyversion"
    r"|\b[\w.-]+\.(?:exe|mpq|disabled|zip|dll|json|py|cs|sh|txt|md|dbc)\b"
    r"|\b[A-Z][a-z]+(?:[A-Z][a-z0-9]*)+\b|\bPatch-[QMSY]\b"
    r"|\b[0-9a-fA-F]{40,64}\b|\b\d+(?:[.,]\d+)*(?:°|%|\+)?",
    re.M | re.S,
)
LINK = re.compile(r"(?<=\]\()([^\s)]+)|(?<=href=\")([^\"]+)|(?<=src=\")([^\"]+)")


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read(path):
    return path.read_text(encoding="utf-8-sig")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text, encoding="utf-8", newline="\n")
    temporary.replace(path)


def locales(root=ROOT):
    data = json.loads(read(root / "tools/translation-locales.json"))
    data = {k: v for k, v in data.items() if isinstance(v, dict)}
    supported = set(json.loads(read(root / "build/catalog.json"))["Locales"])
    if set(data) != supported | {"ptBR"} or "enUS" not in data:
        raise ValueError("Update translation-locales.json to cover exactly the catalog locales plus ptBR")
    tags = [v["tag"] for v in data.values()]
    if len(tags) != len(set(tags)) or any(not re.fullmatch(r"[a-z]{2}(?:-[A-Z]{2})?", t) for t in tags):
        raise ValueError("Locale tags must be unique safe language tags")
    return data


def sources(root=ROOT):
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
    return sorted(p for p in tracked if p and p.endswith((".md", ".txt"))
                  and ("/" not in p or p.startswith("docs/") or p == "wine/README.txt")
                  and p != "AGENTS.md" and not p.startswith("docs/i18n/"))


def destination(source, tag):
    return PurePosixPath("docs/i18n", tag, source).with_suffix(".md").as_posix()


def clean_source(text):
    return NAV_RE.sub("", text).strip() + "\n"


def mask(text):
    if TOKEN.search(text):
        raise ValueError("Source contains reserved translation placeholders")
    saved = []

    def replace(match):
        saved.append(match.group())
        return f"ZXQKEEP{len(saved) - 1:05d}QXZ"

    return PROTECTED.sub(replace, text), saved


def unmask(translated, original, saved):
    if not isinstance(translated, str) or not translated.strip():
        raise ValueError("Empty or non-text translation")
    if Counter(TOKEN.findall(translated)) != Counter(TOKEN.findall(original)):
        raise ValueError("Translation changed protected commands, links, or release facts")
    # A model must not introduce new active markup, commands, or destinations.
    if (re.search(r"https?://|<[^>]+>|`|\]\((?!ZXQKEEP\d{5}QXZ)", translated)
            or translated.count("](") != original.count("](")):
        raise ValueError("Translation introduced unprotected markup or a URL")
    plain = TOKEN.sub("", original)
    if len(TOKEN.sub("", translated)) < len(plain) * 0.2:
        raise ValueError("Translation appears truncated")
    if len(re.findall(r"[A-Za-z]{3,}", plain)) > 10 and translated == original:
        raise ValueError("Translation returned the English source unchanged")
    return TOKEN.sub(lambda m: saved[int(m.group()[7:12])], translated)


def chunks(text, limit=4000):
    # Split only between paragraphs after protecting multiline code blocks.
    current = ""
    for paragraph in re.split(r"(\n\s*\n)", text):
        if len(current) + len(paragraph) > limit and current:
            yield current
            current = ""
        current += paragraph
    if current:
        yield current


def stable_headings(text):
    seen = {}
    lines = []
    fenced = None
    for line in text.splitlines(keepends=True):
        fence = re.match(r"^(```|~~~)", line)
        if fence:
            fenced = None if fenced == fence[1] else fence[1]
        heading = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line) if not fenced else None
        if heading:
            title = re.sub(r"<[^>]+>", "", heading[1]).lower()
            slug = re.sub(r"[^\w\- ]", "", title).replace(" ", "-")
            count = seen.get(slug, 0)
            seen[slug] = count + 1
            lines.append(f'<a id="{slug + ("-" + str(count) if count else "")}"></a>\n\n')
        lines.append(line)
    return "".join(lines)


def rewrite_links(text, source, tag, source_files):
    current = destination(source, tag)

    def rewrite(match):
        url = match.group()
        if re.match(r"(?:[a-zA-Z][a-zA-Z0-9+.-]*:|//|#)", url):
            return url
        path, sep, fragment = url.partition("#")
        path, query_sep, query = path.partition("?")
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), path)) if not path.startswith("/") else path.lstrip("/")
        if resolved.startswith("../"):
            raise ValueError(f"Link escapes repository: {url}")
        target = destination(resolved, tag) if resolved in source_files else resolved
        return posixpath.relpath(target, posixpath.dirname(current)) + (query_sep + query if query_sep else "") + (sep + fragment if sep else "")

    return LINK.sub(rewrite, text)


MODEL = "translategemma:4b"
MODEL_DIGEST = "c49d986b0764f5881c476eb21435bb62b7abc62347aab3d4a6071e811be510a1"


def request_translation(text, language, model):
    if model != MODEL:
        raise ValueError("Only the pinned local translation model is allowed")
    name, tag = language["instruction"], language["tag"]
    if tag == "zh-CN":
        tag = "zh-Hans"
    elif tag == "zh-TW":
        tag = "zh-Hant"
    prompt = (
        f"You are a professional English (en) to {name} ({tag}) translator. "
        f"Your goal is to accurately convey the meaning and nuances of the original English text "
        f"while adhering to {name} grammar, vocabulary, and cultural sensitivities. "
        "Keep Markdown formatting and every ZXQKEEP00000QXZ-style placeholder exactly unchanged. "
        f"Produce only the {name} translation, without any additional explanations or commentary. "
        f"Please translate the following English text into {name}:\n\n\n{text}"
    )
    body = json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "keep_alive": "30m",
                       "options": {"temperature": 0, "num_ctx": 8192, "num_predict": 6000,
                                   "num_thread": 4}}).encode()
    request = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=body,
                                     headers={"Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=1800) as response:
                result = json.load(response)
            if not result.get("done") or result.get("done_reason") != "stop":
                raise ValueError("Local translation did not finish normally")
            return result["response"]
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise ValueError("Local Ollama translation service is unavailable") from None
            time.sleep(5)


def translate_one(source, locale, files, model, root=ROOT, translator=request_translation):
    tag = locale["tag"]
    output = root / destination(source, tag)
    state_path = root / "docs/i18n" / tag / ".translation-state.json"
    state = json.loads(read(state_path)) if state_path.exists() else {}
    original = clean_source(read(root / source))
    fingerprint = digest(original + json.dumps(locale, sort_keys=True) + model + read(Path(__file__)))
    cached = state.get(source, {})
    if cached.get("source") == fingerprint and output.exists() and cached.get("output") == digest(read(output)):
        return False
    english = posixpath.relpath(source, posixpath.dirname(destination(source, tag)))
    # Translate the visible provenance notice too; author metadata remains exact.
    prepared = META + f"\n\n> Automatic translation. [English source]({english}). If wording differs, the English source is authoritative.\n\n"
    content = stable_headings(original.replace(META, "").strip() + "\n")
    content = rewrite_links(content, source, tag, files)
    protected, saved = mask(prepared + content)
    translated_parts = []
    for chunk in chunks(protected):
        if not re.search(r"[A-Za-z]{2}", TOKEN.sub("", chunk)):
            translated_parts.append(chunk)
            continue
        leading = chunk[:len(chunk) - len(chunk.lstrip())]
        trailing = chunk[len(chunk.rstrip()):]
        result = leading + translator(chunk.strip(), locale, model).strip() + trailing
        # Validate each response before accepting any part of the document.
        unmask(result, chunk, saved)
        translated_parts.append(result)
    translated = "".join(translated_parts)
    result = unmask(translated, protected, saved)
    write(output, result.rstrip() + "\n")
    state[source] = {"source": fingerprint, "output": digest(read(output))}
    state.update({"Author": "Neil Mitchell", "Creator": "Neil Mitchell", "LastModifiedBy": "Neil Mitchell"})
    write(state_path, json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return True


def navigation(root=ROOT):
    data = locales(root)
    files = sources(root)
    documents = [("README.md", "en")]
    documents += [(destination(p, v["tag"]), v["tag"]) for v in data.values() if v["tag"] != "en"
                  for p in files if (root / destination(p, v["tag"])).exists()]
    for path, tag in documents:
        parent = posixpath.dirname(path) or "."
        choices = []
        for locale in data.values():
            target = "README.md" if locale["tag"] == "en" else destination("README.md", locale["tag"])
            label = locale["name"]
            if (root / target).exists():
                choices.append(f'[{label}]({posixpath.relpath(target, parent)})')
            else:
                choices.append(label)
        nav = NAV_START + "\n" + " · ".join(choices) + "\n" + NAV_END + "\n\n"
        text = nav + clean_source(read(root / path))
        write(root / path, text)
    # Navigation is deterministic and changes the output hash, not source freshness.
    for locale in data.values():
        state_path = root / "docs/i18n" / locale["tag"] / ".translation-state.json"
        if not state_path.exists():
            continue
        state = json.loads(read(state_path))
        for source in files:
            output = root / destination(source, locale["tag"])
            if source in state and output.exists():
                state[source]["output"] = digest(read(output))
        write(state_path, json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check catalog coverage and source inventory; no API calls")
    parser.add_argument("--navigation", action="store_true", help="Rebuild links to translations that exist")
    parser.add_argument("--source", help="Translate one tracked source document for a smoke check")
    parser.add_argument("--locale", help="Translate one catalog locale, such as ptBR")
    args = parser.parse_args()
    data, files = locales(), sources()
    if not files or "README.md" not in files:
        raise ValueError("No tracked documentation sources found")
    if args.check:
        print(f"Coverage OK: {len(data)} reading options; {len(files)} English source documents")
        print("Locales: " + ", ".join(data))
        return
    if args.navigation:
        navigation()
        return
    if args.source:
        if args.source not in files:
            raise ValueError("Source must be a tracked documentation file")
        files = [args.source]
    selected = {args.locale: data[args.locale]} if args.locale else data
    for key, locale in selected.items():
        if key == "enUS":
            continue
        for source in files:
            changed = translate_one(source, locale, files, MODEL)
            print(f"{key}: {source}: {'translated' if changed else 'unchanged'}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError) as error:
        print(f"Translation failed: {error}", file=sys.stderr)
        sys.exit(1)

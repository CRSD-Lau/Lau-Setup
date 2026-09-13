"""Translate public documentation; author/creator/modifier: Neil Mitchell.

Only Python's standard library is required. Google's free web translator supplies text, never executable code.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
META = "<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->"
NAV_START = "<!-- LANGUAGES:START -->"
NAV_END = "<!-- LANGUAGES:END -->"
NAV_RE = re.compile(re.escape(NAV_START) + r".*?" + re.escape(NAV_END) + r"\n*", re.S)
TOKEN = re.compile(r"ZXQKEEP\d{5}QXZ")
PROSE_BOUNDARY = re.compile(r"(" + TOKEN.pattern + r"|\n+|[\[\]()*|#!]+|^[ \t]*(?:[-+>]+)[ \t]+)", re.M)
# Protect executable examples, URLs, HTML, code, and numerical release evidence.
PROTECTED = re.compile(
    r"^```[^\n]*\n.*?^```[^\n]*$|^~~~[^\n]*\n.*?^~~~[^\n]*$"
    r"|The executable (?:is|remains) unsigned|(?:The|This) installer is unsigned|Windows packages are unsigned"
    r"|^\s*WINEPREFIX=[^\n]+|^Author / Creator / Last Modified By:[^\n]+"
    r"|<!--.*?-->|<[^>\n]+>|`+[^`\n]+`+"
    r"|(?<=\]\()[^\s)]+|https?://[^\s<>\])]+"
    r"|Neil Mitchell|Lau Setup|World of Warcraft|Wine Mono|/pyversion"
    r"|\b(?:Windows|Wine|Linux|Blizzard(?: Entertainment)?|Warmane|Wrath|Lau|Andre|Loriendal|Trimitor|Project Reforged|GitHub|WoW|SHA-256|64-bit|32-bit)\b"
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
    if any(v.get("google") not in {"en", "de", "es", "fr", "ko", "ru", "zh-CN", "zh-TW", "pt"} for v in data.values()):
        raise ValueError("Unknown Google target language")
    if len(tags) != len(set(tags)) or any(not re.fullmatch(r"[a-z]{2}(?:-[A-Z]{2})?", t) for t in tags):
        raise ValueError("Locale tags must be unique safe language tags")
    return data


def sources(root=ROOT):
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
    files = sorted(p for p in tracked if p and p.endswith((".md", ".txt"))
                  and ("/" not in p or p.startswith("docs/") or p == "wine/README.txt")
                  and p != "AGENTS.md" and not p.startswith("docs/i18n/"))
    outputs = [destination(p, "en") for p in files]
    if len(outputs) != len(set(outputs)):
        raise ValueError("Documentation filenames collide after converting text guides to Markdown")
    return files


def destination(source, tag):
    return PurePosixPath("docs/i18n", tag, source).with_suffix(".md").as_posix()


def clean_source(text):
    return NAV_RE.sub("", text).strip() + "\n"


def mask(text, locale=None):
    if TOKEN.search(text):
        raise ValueError("Source contains reserved translation placeholders")
    saved = []

    def replace(match):
        value = match.group()
        if locale and "unsigned" in value and not value.startswith(("`", "<")):
            if value.startswith("The executable"):
                value = locale["unsigned"]["executable"]
            elif value.startswith(("The installer", "This installer")):
                value = locale["unsigned"]["installer"]
            elif value.startswith("Windows packages"):
                value = locale["unsigned"]["windows"]
        saved.append(value)
        return f"ZXQKEEP{len(saved) - 1:05d}QXZ"

    return PROTECTED.sub(replace, text), saved


def unmask(translated, original, saved):
    if not isinstance(translated, str) or not translated.strip():
        raise ValueError("Empty or non-text translation")
    if Counter(TOKEN.findall(translated)) != Counter(TOKEN.findall(original)):
        raise ValueError("Translation changed protected commands, links, or release facts")
    # A provider must not introduce new active markup, commands, or destinations.
    if (re.search(r"https?://|<[^>]+>|`|\]\((?!ZXQKEEP\d{5}QXZ)", translated)
            or translated.count("](") != original.count("](")):
        raise ValueError("Translation introduced unprotected markup or a URL")
    plain = TOKEN.sub("", original)
    if len(plain) > 80 and len(TOKEN.sub("", translated)) < len(plain) * 0.2:
        raise ValueError("Translation appears truncated")
    if len(re.findall(r"[A-Za-z]{3,}", plain)) > 10 and translated == original:
        raise ValueError("Translation returned the English source unchanged")
    return TOKEN.sub(lambda m: saved[int(m.group()[7:12])], translated)


def chunks(text, limit=1800):
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


PROVIDER = "google-web"
TRANSLATION_REVISION = "5"


class GoogleResult(HTMLParser):
    """Read only the web translator's result and confirmed target language."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.parts = []
        self.target = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "input" and attrs.get("name") == "tl":
            self.target = attrs.get("value")
        if tag == "div" and attrs.get("class") in ("result-container", "t0"):
            self.depth = 1
        elif self.depth:
            if tag == "br":
                self.parts.append("\n")
            elif tag not in ("input", "img", "hr", "meta", "link"):
                self.depth += 1

    def handle_endtag(self, tag):
        if self.depth and tag not in ("br", "input", "img", "hr", "meta", "link"):
            self.depth -= 1

    def handle_data(self, data):
        if self.depth:
            self.parts.append(data)


def request_translation(text, language, provider, plain=False):
    if provider != PROVIDER:
        raise ValueError("Only the free Google web translator is configured")
    if len(text) > 2000:
        raise ValueError("Translation segment exceeds the Google web input limit")
    target = language["google"]
    url = "https://translate.google.com/m?" + urllib.parse.urlencode({"sl": "en", "tl": target, "q": unescape(text)})
    # A small steady request rate; no proxies, API keys, paid fallback or limit bypass.
    time.sleep(1)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=45) as response:
                page = response.read().decode("utf-8")
            parsed = GoogleResult()
            parsed.feed(page)
            if parsed.target is not None and parsed.target != target:
                raise ValueError(f"Google target rejected: {target} became {parsed.target}; existing pages retained")
            if parsed.target == target and parsed.parts:
                return "".join(parsed.parts)
            if attempt == 2:
                raise ValueError(f"Google returned no translation after 3 attempts ({target}, input: {text[:80]!r}); retry later")
        except urllib.error.HTTPError as error:
            if error.code == 429:
                raise ValueError("Google rate-limited translation; retry the workflow later. Existing pages retained.") from None
            if error.code < 500 or attempt == 2:
                raise ValueError(f"Google web translation HTTP {error.code}") from None
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise ValueError("Google web translation unavailable; retry later") from None
        time.sleep(5 * (attempt + 1))


def fingerprint(source, locale, files, provider, root):
    return digest(clean_source(read(root / source)) + json.dumps(locale, sort_keys=True)
                  + json.dumps(sorted(files)) + provider + TRANSLATION_REVISION)


def source_markdown(source, text):
    if not source.endswith(".txt"):
        return text
    # Text guides contain literal angle brackets and a shell command. Make those
    # visible as code when converting the guide to GitHub-rendered Markdown.
    text = text.replace(".mpq.disabled.<12-character hash>", "`.mpq.disabled.<12-character hash>`")
    return re.sub(r"(?m)^[ \t]*(WINEPREFIX=[^\n]+)$", r"```sh\n\1\n```", text)


def translate_prose(protected, locale, provider, translator, cache):
    """Keep protected spans and Markdown delimiters outside translated prose."""
    output = []
    for segment in PROSE_BOUNDARY.split(protected):
        if not segment or PROSE_BOUNDARY.fullmatch(segment) or not re.search(r"[A-Za-z]{2}", segment):
            output.append(segment)
            continue
        leading = segment[:len(segment) - len(segment.lstrip())]
        trailing = segment[len(segment.rstrip()):]
        prose = segment.strip()
        if len(prose) > 2000:
            split_at = prose.rfind(" ", 0, 1800)
            if split_at < 1:
                raise ValueError("Unbroken translation input exceeds Google web limit")
            output.append(leading + translate_prose(prose[:split_at], locale, provider, translator, cache)
                          + " " + translate_prose(prose[split_at + 1:], locale, provider, translator, cache) + trailing)
            continue
        cache_key = digest(prose + json.dumps(locale, sort_keys=True) + provider + TRANSLATION_REVISION)
        result = cache.get(cache_key)
        if result is None:
            result = translator(prose, locale, provider, True).strip()
        # Prose cannot create Markdown links, executable examples, or HTML.
        if re.search(r"[\[\]`<>|#*]|https?://|ZXQKEEP", result):
            raise ValueError(f"Prose translation introduced structure or a URL: {prose[:120]!r} -> {result[:180]!r}")
        unmask(result, prose, [])
        cache[cache_key] = result
        output.append(leading + result + trailing)
    return "".join(output)


def translate_context(chunk, locale, provider, translator, cache, saved):
    """Prefer full sentences; retry smaller paragraphs if provider changes structure."""
    if not re.search(r"[A-Za-z]{2}", TOKEN.sub("", chunk)):
        return chunk
    # HTML elements must retain their own text (e.g. slogan versus subtitle).
    html_tokens = [m.group() for m in TOKEN.finditer(chunk)
                   if saved[int(m.group()[7:12])].startswith("<")]
    if html_tokens:
        boundary = re.compile("(" + "|".join(map(re.escape, html_tokens)) + ")")
        return "".join(part if part in html_tokens else translate_context(part, locale, provider, translator, cache, saved)
                       for part in boundary.split(chunk) if part)
    key = digest(chunk + json.dumps(locale, sort_keys=True) + provider + TRANSLATION_REVISION)
    if key in cache:
        unmask(cache[key], chunk, saved)
        return cache[key]
    leading = chunk[:len(chunk) - len(chunk.lstrip())]
    trailing = chunk[len(chunk.rstrip()):]
    result = leading + translator(chunk.strip(), locale, provider).strip() + trailing if len(chunk.strip()) <= 2000 else ""
    try:
        unmask(result, chunk, saved)
    except ValueError:
        paragraphs = re.split(r"(\n\s*\n)", chunk)
        if len(paragraphs) > 1:
            result = "".join(translate_context(part, locale, provider, translator, cache, saved) for part in paragraphs)
        else:
            result = translate_prose(chunk, locale, provider, translator, cache)
        unmask(result, chunk, saved)
    cache[key] = result
    return result


def translate_one(source, locale, files, provider, root=ROOT, translator=request_translation):
    tag = locale["tag"]
    output = root / destination(source, tag)
    state_path = root / "docs/i18n" / tag / ".translation-state.json"
    state = json.loads(read(state_path)) if state_path.exists() else {}
    original = clean_source(read(root / source))
    source_hash = fingerprint(source, locale, files, provider, root)
    cached = state.get(source, {})
    if cached.get("source") == source_hash and output.exists() and cached.get("output") == digest(read(output)):
        return False
    english = posixpath.relpath(source, posixpath.dirname(destination(source, tag)))
    # Translate the visible provenance notice too; author metadata remains exact.
    prepared = META + f"\n\n> Automatic translation. [English source]({english}). If wording differs, the English source is authoritative.\n\n"
    content = stable_headings(source_markdown(source, original.replace(META, "").strip() + "\n"))
    content = rewrite_links(content, source, tag, files)
    protected, saved = mask(prepared + content, locale)
    cache_path = root / "docs/i18n" / tag / ".translation-segments.json"
    cache = json.loads(read(cache_path)) if cache_path.exists() else {}
    translated_parts = []
    for index, chunk in enumerate(chunks(protected), 1):
        if not re.search(r"[A-Za-z]{2}", TOKEN.sub("", chunk)):
            translated_parts.append(chunk)
            continue
        print(f"{tag}: {source}: translating section {index}", flush=True)
        result = translate_context(chunk, locale, provider, translator, cache, saved)
        # Validate each response before accepting any part of the document.
        unmask(result, chunk, saved)
        translated_parts.append(result)
    translated = "".join(translated_parts)
    result = unmask(translated, protected, saved)
    write(output, result.rstrip() + "\n")
    state[source] = {"source": source_hash, "output": digest(read(output))}
    state.update({"Author": "Neil Mitchell", "Creator": "Neil Mitchell", "LastModifiedBy": "Neil Mitchell"})
    write(state_path, json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    cache.update({"Author": "Neil Mitchell", "Creator": "Neil Mitchell", "LastModifiedBy": "Neil Mitchell"})
    write(cache_path, json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return True


def verify_complete(root=ROOT):
    files = sources(root)
    for locale in locales(root).values():
        if locale["tag"] == "en":
            continue
        state = json.loads(read(root / "docs/i18n" / locale["tag"] / ".translation-state.json"))
        for source in files:
            output = root / destination(source, locale["tag"])
            record = state.get(source, {})
            if (not output.is_file() or record.get("source") != fingerprint(source, locale, files, PROVIDER, root)
                    or record.get("output") != digest(read(output)) or META not in read(output)):
                raise ValueError(f"Missing, stale or modified translation: {locale['tag']}/{source}")
    print(f"All {len(files) * (len(locales(root)) - 1)} translated documents verified")


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
    parser.add_argument("--verify", action="store_true", help="Verify every locale and document before publication")
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
    if args.verify:
        verify_complete()
        return
    selected_files = files
    if args.source:
        if args.source not in files:
            raise ValueError("Source must be a tracked documentation file")
        selected_files = [args.source]
    selected = {args.locale: data[args.locale]} if args.locale else data
    for key, locale in selected.items():
        if key == "enUS":
            continue
        for source in selected_files:
            changed = translate_one(source, locale, files, PROVIDER)
            print(f"{key}: {source}: {'translated' if changed else 'unchanged'}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError) as error:
        print(f"Translation failed: {error}", file=sys.stderr)
        sys.exit(1)

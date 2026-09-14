"""Resume documentation translations. Author/creator/modifier: Neil Mitchell."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time

import translate_docs as t

METADATA = {"Author": "Neil Mitchell", "Creator": "Neil Mitchell", "LastModifiedBy": "Neil Mitchell"}
BASE_COOLDOWN = 3600
MAX_COOLDOWN = 86400
WORK_BUDGET = 45 * 60


def pending(root=t.ROOT):
    files = t.sources(root)
    result = []
    for key, locale in t.locales(root).items():
        if key == "enUS":
            continue
        path = root / "docs/i18n" / locale["tag"] / ".translation-state.json"
        state = json.loads(t.read(path)) if path.exists() else {}
        for source in files:
            output = root / t.destination(source, locale["tag"])
            record = state.get(source, {})
            if (not output.is_file() or record.get("source") != t.fingerprint(source, locale, files, t.PROVIDER, root)
                    or record.get("output") != t.digest(t.read(output)) or t.META not in t.read(output)):
                result.append((key, source))
    return result


def report(status, detail, ready=False):
    message = f"## Documentation translations: {status}\n\n{detail}\n"
    print(message, flush=True)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as stream:
            stream.write(message)
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as stream:
            stream.write(f"ready={str(ready).lower()}\n")


def utc(timestamp):
    return datetime.fromtimestamp(timestamp, timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


class BudgetReached(Exception):
    pass


def recover(root=t.ROOT, translator=t.request_translation, now=time.time, monotonic=time.monotonic):
    work = pending(root)
    if not work:
        report("current", "All translations are current. No provider requests were made.")
        return
    cache_dir = Path(os.environ["TRANSLATION_CACHE_DIR"])
    state_path = cache_dir / "cooldown.json"
    state = json.loads(t.read(state_path)) if state_path.exists() else {}
    until = state.get("until", 0)
    if until > now():
        report("waiting", f"{len(work)} documents pending. Next eligible attempt: **{utc(until)}**. "
               "The hourly recovery check will resume after that time; GitHub scheduling can be delayed. "
               "No provider requests were made. Existing published pages remain available.")
        return
    deadline = monotonic() + WORK_BUDGET

    def bounded_translation(*args):
        if monotonic() >= deadline:
            raise BudgetReached()
        return translator(*args)

    try:
        data, files = t.locales(root), t.sources(root)
        for key, source in work:
            t.translate_one(source, data[key], files, t.PROVIDER, root, bounded_translation)
        t.verify_complete(root)
    except t.TranslationDeferred as error:
        failures = min(int(state.get("failures", 0)) + 1, 6)
        delay = min(MAX_COOLDOWN, BASE_COOLDOWN * 2 ** (failures - 1))
        if error.retry_after is not None:
            delay = max(delay, error.retry_after)
        until = now() + delay
        t.write(state_path, json.dumps(dict(METADATA, until=until, failures=failures), indent=2) + "\n")
        hint = "Google supplied a retry delay." if error.retry_after is not None else "Google supplied no usable retry time; this is our cooldown, not a guaranteed Google reset."
        report("waiting", f"{error} {hint} Next eligible attempt: **{utc(until)}**. "
               "Accepted segments are checkpointed for the next automatic attempt. Publication is deferred until every document passes verification.")
        return
    except BudgetReached:
        report("pending", "This run reached its 45-minute work budget. Accepted segments are checkpointed; "
               "the next hourly check resumes them. Existing published pages remain available.")
        return
    t.write(state_path, json.dumps(dict(METADATA, until=0, failures=0), indent=2) + "\n")
    report("verified, awaiting publication", "All language and document integrity checks passed. The publish job must also succeed.", ready=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pending", action="store_true")
    args = parser.parse_args()
    if args.pending:
        work = pending()
        print(f"{len(work)} translated documents need updates.")
        if os.environ.get("GITHUB_OUTPUT"):
            with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as stream:
                stream.write(f"pending={str(bool(work)).lower()}\n")
        return
    recover()


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError) as error:
        report("failed", f"Integrity or configuration error: {error}. Existing pages retained; inspect the logs.")
        sys.exit(1)

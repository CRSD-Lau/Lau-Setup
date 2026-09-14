<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

# Repository translations

The **Translate documentation** GitHub Action uses **Google Translate's free website** to keep repository documentation available in every supported game language, plus **Brazilian Portuguese**. No API key, paid Cloud Translation account, subscription or model download is required.

Use the language links at the top of the README. GitHub displays the root README by default; visitors choose their language using these links. This workflow translates documentation, including installation guides and technical references. It does not translate GitHub's interface, issues, release descriptions, the separate website or the installer interface, and does not add a Portuguese game locale.

## Current beginner instructions

The 1.2.0 beginner steps in all 27 localized primary guides and the current notices in all 117 translated pages were updated directly while a full refresh of older technical text was blocked by HTTP 429. The English guides remain authoritative. The GitHub Action automatically retries the pending full refresh; current installer instructions and bundled interface translations do not depend on that service.

The authored temporary notices and beginner steps are retained in `tools/translation_zip_only_notices_120.py`. This self-contained repository script can reapply them without a translation-service request. Do not mark the older technical bodies freshly translated merely because these notices were updated. Once the complete refresh passes, review the result before retiring the temporary notices.

## Languages

Coverage is checked against `build/catalog.json`, with `ptBR` added for documentation. The reading options are English, German, Spanish for Spain and Mexico, French, Korean, Russian, Simplified Chinese, Traditional Chinese and Brazilian Portuguese.

Google's web language selector identifies `pt` as Portuguese (Brazil); Portuguese (Portugal) is a different target. Google provides one `es` target, so the Spain and Mexico pages use the same general Spanish translation. The Chinese targets are separate. Google target codes and native language names live in `tools/translation-locales.json`. Adding a game locale requires adding its documentation mapping; missing coverage fails validation.

## Automatic updates

Pushes changing English documentation, the catalog or translation tooling trigger the Action. Maintainers can also select **Actions → Translate documentation → Run workflow → main**. It discovers tracked Markdown and text files in the repository root and `docs/`, plus `wine/README.txt`. Generated translations and `AGENTS.md` are excluded. Text guides become rendered Markdown under `docs/i18n/<language>/`.

Only changed documents need translation. Source and output hashes and a segment cache avoid repeated requests. Bump `TRANSLATION_REVISION` when changing translation conventions. One worker translates languages sequentially, with a three-second pause before requests. Accepted segments are saved immediately to a recovery cache, including inside unfinished documents. An hourly GitHub Actions check (at minute 23, subject to GitHub scheduling delays) only starts recovery when documentation is stale. It makes no Google requests while a provider cooldown is active. No Copilot task or translation PR merge is needed. The free web interface is unofficial for automation and can change or block requests. There is no paid fallback. Existing published pages remain available when generation fails.

On HTTP 429 or a temporary network/server failure, the Action records a cooldown and stops contacting Google. It respects a usable `Retry-After` header; otherwise delays increase from one hour to two, four, eight, sixteen and twenty-four hours. The run summary shows the next eligible attempt in UTC. This is an earliest retry time, not a promise that Google will accept it. A waiting run can be green while publication is skipped: read the summary and the Publish job to distinguish waiting from published. Each run has a 45-minute work budget; the next scheduled check resumes cached segments. Integrity errors still fail visibly.

Recovery uses the GitHub Actions cache, which can be evicted; losing it may repeat work but cannot mark stale pages current. New source revisions still pass the full source/output checks. Scheduling can be delayed or disabled by GitHub (including inactivity on public repositories); **Run workflow** remains available and respects the same cooldown.

Standard GitHub-hosted runner execution is free for this public repository. Jobs are disabled if the repository becomes private. Small intermediate artifacts expire after one day; no model or large dependency is stored.

## Integrity and publication

Code, commands, URLs, version numbers, product names, credits and signature-status statements are protected. Relative document links point to the same language, while image and code links point to the originals. Stable English heading anchors preserve section links. Every page identifies itself as an automatic translation, links to its English source and retains Author, Creator and Last Modified By metadata for **Neil Mitchell**.

All nine translated reading options must pass source/output integrity checks before publication to `main`. Publication refuses a changed source revision and never force-pushes. Pull requests run offline translation and recovery tests with read-only access, so Google throttling cannot block unrelated code review. Real provider requests run only for trusted `main` updates or recovery. If branch protection later prevents committing, adapt publication to the approved PR process.

Machine translation still needs fluent-reader review. English remains authoritative. For durable corrections, update the English source or translation tooling; direct edits to generated files will be regenerated. Failed or partial batches do not replace existing documents.

## Native-language review

The [translation review matrix](docs/TRANSLATION-REVIEW.md) records human review of the current beginner guides. It starts every non-English language as unreviewed and deliberately leaves the source revision blank until a reviewer selects and reviews one. This record does not certify translation quality or replace the English source.

## Local use

Python 3.11 or newer is sufficient; no additional packages are required. Check structure without network access:

```sh
python -m unittest discover -s tests -p test_translate_docs.py -v
python -m unittest discover -s tests -p test_translation_recovery.py -v
python tools/translate_docs.py --check
```

Translate public documentation using the free Google website:

```sh
python tools/translate_docs.py --locale ptBR
python tools/translate_docs.py --navigation
```

References: [Google Translate](https://translate.google.com/), [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions). The separate [Google Cloud Translation API](https://cloud.google.com/translate/pricing) is a billed service and is not used here.

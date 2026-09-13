<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

# Repository translations

The **Translate documentation** GitHub Action uses **Google Translate's free website** to keep repository documentation available in every supported game language, plus **Brazilian Portuguese**. No API key, paid Cloud Translation account, subscription or model download is required.

Use the language links at the top of the README. GitHub displays the root README by default; visitors choose their language using these links. This workflow translates documentation, including installation guides and technical references. It does not translate GitHub's interface, issues, release descriptions, the separate website or the installer interface, and does not add a Portuguese game locale.

## Languages

Coverage is checked against `build/catalog.json`, with `ptBR` added for documentation. The reading options are English, German, Spanish for Spain and Mexico, French, Korean, Russian, Simplified Chinese, Traditional Chinese and Brazilian Portuguese.

Google's web language selector identifies `pt` as Portuguese (Brazil); Portuguese (Portugal) is a different target. Google provides one `es` target, so the Spain and Mexico pages use the same general Spanish translation. The Chinese targets are separate. Google target codes and native language names live in `tools/translation-locales.json`. Adding a game locale requires adding its documentation mapping; missing coverage fails validation.

## Automatic updates

Pushes changing English documentation, the catalog or translation tooling trigger the Action. Maintainers can also select **Actions → Translate documentation → Run workflow → main**. It discovers tracked Markdown and text files in the repository root and `docs/`, plus `wine/README.txt`. Generated translations and `AGENTS.md` are excluded. Text guides become rendered Markdown under `docs/i18n/<language>/`.

Only changed documents need translation. Source and output hashes and a segment cache avoid repeated requests. Bump `TRANSLATION_REVISION` when changing translation conventions. Language jobs run one at a time, with a pause between requests. A rate limit stops the affected job; retry later. The free web interface is unofficial for automation and can change or block requests. There is no paid fallback. Existing published pages remain available when generation fails.

Standard GitHub-hosted runner execution is free for this public repository. Jobs are disabled if the repository becomes private. Small intermediate artifacts expire after one day; no model or large dependency is stored.

## Integrity and publication

Code, commands, URLs, version numbers, product names, credits and signature-status statements are protected. Relative document links point to the same language, while image and code links point to the originals. Stable English heading anchors preserve section links. Every page identifies itself as an automatic translation, links to its English source and retains Author, Creator and Last Modified By metadata for **Neil Mitchell**.

All nine translated reading options must pass source/output integrity checks before publication to `main`. Publication refuses a changed source revision and never force-pushes. Pull requests run unit checks and a real Brazilian Portuguese README smoke translation with read-only access. If branch protection later prevents committing, adapt publication to the approved PR process.

Machine translation still needs fluent-reader review. English remains authoritative. For durable corrections, update the English source or translation tooling; direct edits to generated files will be regenerated. Failed or partial batches do not replace existing documents.

## Local use

Python 3.11 or newer is sufficient; no additional packages are required. Check structure without network access:

```sh
python -m unittest discover -s tests -p test_translate_docs.py -v
python tools/translate_docs.py --check
```

Translate public documentation using the free Google website:

```sh
python tools/translate_docs.py --locale ptBR
python tools/translate_docs.py --navigation
```

References: [Google Translate](https://translate.google.com/), [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions). The separate [Google Cloud Translation API](https://cloud.google.com/translate/pricing) is a billed service and is not used here.

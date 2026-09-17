# Lau Setup 1.4.1 installer-only compatibility hotfix

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

## What changes

Lau Setup 1.4.1 recognizes installed `enGB`, `ptBR`, and `itIT` 3.3.5a clients. It preserves the client-selected locale and writes only the normal Lau-managed root and matching active-locale targets.

The release catalog maps those three clients to the existing verified English **visual** assets. This avoids a false “missing matching language files” rejection while keeping the mapping visible, reviewable, and testable in release metadata.

## What does not change

- Game release remains **3.0.9 Lau**; `/pyversion` remains **3.0.9**.
- The nine existing localized game locales and their assets are unchanged.
- This does not install a base language pack, alter `WTF\\Config.wtf`, rename archives, or add Portuguese or Italian game-text translations.
- **No DBC edits.**
- Existing server-specific visual reports and map/loading-screen reports remain backlog items.

## Validation performed and production scope

- 74 Windows isolated regression groups passed, including install, repeat-install, option-switch, interrupted-operation, exact restore, and configured-locale coverage for `enGB`, `ptBR`, and `itIT`.
- Readback tests prove English visual source assets reach only the selected locale’s managed targets.
- The packaged ZIP and source archive were verified before publication.

Runtime validation for a representative real `enGB`, `ptBR`, and `itIT` client is intentionally deferred to production feedback for this edge-case installer hotfix. Report the exact client folder layout, locale, selected options, installer log and a screenshot if a compatibility path fails.

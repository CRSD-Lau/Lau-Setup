# Lau Setup 1.4.1 hotfix announcement

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

Use this exact Markdown in the existing PizzaWarriors and Wrath HD Discord release posts after the 1.4.1 package and GitHub release are published.

```md
## Lau Setup 1.4.1 hotfix

`enGB`, `ptBR`, and `itIT` 3.3.5a clients are now accepted by Lau Setup instead of being stopped with a missing matching-language-files message.

This is an installer-only compatibility hotfix. Those clients keep their own locale and receive the existing English visual layer where Lau needs a visual asset. It does not alter `Config.wtf`, rename client archives, install a language pack, or add Portuguese or Italian game-text translations.

The game release stays `3.0.9 Lau`; `/pyversion` is unchanged. No DBC edits.

Download: https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip
Release notes: https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.1
```

Character count of the fenced announcement body: **706** (well below Discord's 2,000-character limit).

The release package and checksum are verified. Real `enGB`, `ptBR`, and `itIT` startup coverage is intentionally deferred to production feedback for this edge-case hotfix; keep the compatibility boundaries above intact when editing the two posts.

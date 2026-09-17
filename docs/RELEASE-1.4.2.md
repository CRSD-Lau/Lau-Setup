# Lau Setup 1.4.2 Wine launcher compatibility hotfix

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

## What changes

Lau Setup's Linux launcher now treats Wine 11.0 and Wine Mono 10.4.1 as a tested **baseline**, not exact-only version strings or minimum versions. Any parseable Wine and Wine Mono version can start Lau Setup without editing `lau_wine.py`, including older, newer, WineHQ staging, development, and distribution-suffixed versions. Older prefixes that have Wine Mono installed but expose no Mono version now warn and continue instead of being falsely rejected.

Wine 11.0 / Wine Mono 10.4.1 remains the validated baseline. Every other runtime combination prints a clear terminal warning with the detected Wine and Mono versions; it is allowed, not certified.

## Safety retained

- Missing Wine Mono or unreadable Wine information still stops before Lau Setup starts and names the detected or missing runtime.
- Existing 64-bit prefix, normal-user, path, process, local-storage, lock, and transaction safety checks are unchanged.
- Game release remains **3.0.9 Lau**; `/pyversion` is unchanged. **No DBC edits.**

## Validation

- New launcher unit coverage accepts the 11.0 / 10.4.1 baseline, older and newer stable Wine/Mono, WineHQ staging-style strings, and a real installed-Mono directory without registry version metadata; it rejects missing Mono and unparsable Wine values.
- Python syntax, package-layout checks, and the existing Windows installer regression suite must pass before publication.

This hotfix still needs a complete real Linux/Wine execution and exact restore against a newer WineHQ staging environment before that environment can be called certified. The warning is intentional until that evidence exists.

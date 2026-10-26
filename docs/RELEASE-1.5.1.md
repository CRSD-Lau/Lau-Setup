# Lau Setup 1.5.1 / Game 3.1.0

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

This installer-only hotfix resolves the Windows false block reported in issue #47. When the normal .NET process-module query cannot identify a WoW-named process, Setup now retries with Windows limited-information process access. A process confirmed to have exited during enumeration is ignored. An unidentified process that is still live continues to stop installation, preserving the existing closed-client safety boundary.

Game release 3.1.0 is unchanged. This release changes no game executable payload, MPQ, DBC, model, texture, map, loading screen or addon. The three standalone Patch-Y 3.1.0 downloads and their public hashes remain unchanged. Issues #46 and #49 remain open because Steam/Proton is outside the supported Wine integration target and the reported OneDrive failure has not been reproduced with affected diagnostics.

## Validation

- The Windows installer suite passes 81/81 in isolated disposable fixtures using the released catalog-pinned WoW 3.3.5a build 12340 executable. The source matched its catalog size and SHA-256 before use.
- Regression coverage forces the original process-module query to fail, proves the limited-information fallback finds the isolated running client, and proves a confirmed exited-process race is ignored.
- Platform-neutral Python checks pass; Linux-native filesystem and process-host tests remain Linux-only.
- The release package must contain exactly `LauSetup.exe`, `LauSetup.sh`, `lau_wine.py`, `lau-languages.json` and `README.txt`, with Neil Mitchell metadata and exact source-byte readback.
- The executable is unsigned. Automated fixtures do not replace live installation/restore or in-game visual acceptance. Existing game 3.1.0 visual acceptance and limitations remain recorded in the [game-release scope](RAID-VISUAL-RELEASE.md).

Download and extract the complete `LauSetup.zip` from the 1.5.1 GitHub release. Close WoW before selecting the folder that directly contains `WoW.exe`. Keep `LauSetupBackups` for exact restore. Windows opens `LauSetup.exe`; supported Linux/Wine environments use the included launcher.

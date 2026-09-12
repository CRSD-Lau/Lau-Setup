# Lau Setup 1.1.1 · Game release 3.0.5 Lau

## Wider raid warnings

- Sindragosa Frost Breath: **75° → 90° total** (7.5° extra per side).
- Rotface Slime Spray: **25° → 60° total** (17.5° extra per side).
- Applied to all six HD/Non-HD editions and available with all nine client locales. Other indicators, Consecration settings, localized tables and artwork are unchanged.

These are buffered visual warnings informed by Warmane raid footage and spell-hit logs. They do not change server damage or mechanics, or claim an exact damage boundary.

## Updating an existing installation

Download the new **LauSetup.exe** or **LauSetup-Wine.zip** first. Close WoW, select the same folder and visual choices, then click **Install upgrade**. The installer compares actual file hashes: older 3.0.4 patches are replaced, while an exact 3.0.5 install is reported as already installed. `/pyversion` reports **3.0.5 Lau** after updating. Old downloaded installers retain their old catalog.

Windows and Wine downloads include the same rebuilt setup executable. For Wine, extract all four files together and use `LauSetup.sh` as described in the included README. Existing runtime requirements are unchanged.

## Verification

All 38 Windows regression groups passed, including 108 locale/edition/map plans. All six editions passed actual 3.0.4-to-3.0.5 upgrade, repeat-install and exact rollback checks. New payloads passed anonymous download/hash checks; an isolated core installation from GitHub and rollback passed. Each edition preserves every member except four model/geometry files and the version TOC.

Wine launcher code is unchanged and the ZIP contains the exact rebuilt EXE. Earlier Wine 11.0 / Mono 10.4.1 runtime evidence is retained; fresh Wine execution was unavailable because the Docker engine did not start. New cone geometry is statically verified, not newly certified in-game.

Download checksums, source and the detailed validation report are attached. Keep `LauSetupBackups` for recovery.

Author / Creator / Last Modified By: Neil Mitchell

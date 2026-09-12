# Lau Setup 1.1.3 · Game release 3.0.7 Lau

## Larger Halion meteor-fire warnings

Promotes tester-approved **test v2**: Halion's red ground-marker radius is **50% larger than release 3.0.6**, around trails and landing fire. Test v3 is not included. Coldflame, colors, animation tracks, native flames, Consecration and the Sindragosa/Rotface cones are unchanged. All six editions and nine client languages are supported.

The tester confirmed v2 after correcting an unupdated patch. This is a visual warning buffer, not a change to server damage or a certification of every position or encounter.

## Update with the new installer

Download **LauSetup.exe** or **LauSetup-Wine.zip** from this release first. Close WoW, select the same client and visuals, then click **Install upgrade**. Old installers retain old catalogs. `/pyversion` reports **3.0.7 Lau**.

Existing 3.0.6 and test v2 users receive the update. Setup compares actual file hashes, including one-byte changes with unchanged size and timestamp; only exact current files count as already installed. Backups and Restore previous install remain available.

Windows requires .NET Framework 4.8. Wine users extract all four files and run `LauSetup.sh` as a normal user with the supported existing Wine/Mono prefix. No runtime installers are bundled.

## Validation

Windows and Wine installer regression, six-edition upgrades, repeat detection, one-byte checks, rollback and public-download checks are recorded in VALIDATION.json. The Halion models and skins are byte-identical to test v2. Only their geometry/bounds and the version TOC differ from 3.0.6; Coldflame and other archive members are unchanged.

[Website changelog and installation help](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

# Lau Setup 1.1.2 · Game release 3.0.6 Lau

## Blue Coldflame, red meteor fire

- **Marrowgar Coldflame:** light blue circles with the existing inward glow and clockwise animation, including heroic.
- **Halion meteor fire:** fire red circles around trails and landing fire with the existing clockwise animation.
- All six HD/Non-HD editions and nine client languages. Native flames, durations, Consecration choices and the 90° Sindragosa / 60° Rotface cones are unchanged.

[Animated color previews and full changelog](https://wrath-multilingual-hd.vercel.app/#changelog). The previews are illustrative mockups, not in-game recordings. Server damage and mechanics are unchanged; warning edges remain visual buffers.

## Already installed? Download the new installer first

Download **LauSetup.exe** or **LauSetup-Wine.zip** from this release. Close WoW, choose the same folder and visual settings, then click **Install upgrade**. Old downloaded installers keep their old embedded catalog.

Setup hashes the actual files. Older 3.0.5 files are replaced; even a one-byte change with identical file size and timestamp is detected. Only exact new files are treated as already installed. `/pyversion` reports **3.0.6 Lau**. Backups and Restore previous install remain available.

Wine users: extract all four files together and run `LauSetup.sh` as your normal user with your existing 64-bit Wine 11.0 / Mono 10.4.1 prefix. Python 3.9+ and local Linux storage are required. Windows needs .NET Framework 4.8. Runtimes are not bundled.

## Fresh verification on Windows and Wine

- 38 regression groups per platform, including 108 locale/edition/map plans each.
- All six actual 3.0.5-to-3.0.6 upgrades, repeat no-op installs and exact rollback on both platforms.
- One-byte same-size/same-timestamp changes detected and repaired independently in root and locale Y on both platforms.
- Anonymous GitHub payload downloads, actual core installations and rollback on Windows and Wine.
- 15 Linux host-safety tests and the exact four-file Wine launcher under a normal user; Windows form render checked.
- Three marker M2 texture references and the version TOC changed per edition; two color textures added. All other members preserved byte for byte.

These installer checks do not certify every Linux distribution or every in-game encounter. The executable remains unsigned. Detailed evidence, checksums and source are attached.

Author / Creator / Last Modified By: Neil Mitchell

---

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

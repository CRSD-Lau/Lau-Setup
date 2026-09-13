# Lau Setup 1.3.0 — automatic extra-patch backups

- Click Install upgrade as usual: recognized extra upgrade patches are backed up automatically and setup continues.
- Restore previous install returns those extra files as well as the managed files.
- Unknown readable patches stay in place. Unreadable archives, protected stock files and changed backups retain their safety checks.
- Game release remains 3.0.8. No DBC edits.

See [beginner steps](START-HERE.txt) and [1.3.0 release notes](docs/RELEASE-1.3.0.md).

# Lau Setup 1.2.1 — large MPQ compatibility fix

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

Download and extract the latest **LauSetup.zip**. Windows opens **LauSetup.exe**; Linux/Wine uses **LauSetup.sh** with the existing supported environment. The game remains **3.0.8 Lau**. No DBC edits.

- Fixes the false unsupported-layout rejection of large classic MPQ hash tables, including the 524,288-entry archive supplied by Andre. Tables now stream in bounded chunks instead of using an arbitrary entry-count cap.
- Preserves bounds, malformed-entry, cancellation, timeout and known-patch conflict checks.
- Clarifies the warning to **Possible extra upgrade patch** in all ten interface languages. A file with its original download name can trigger this warning too; it is separate from the large-table bug.
- Installer update only: all 28 game assets and their hashes are unchanged.

See [beginner steps](START-HERE.txt) and [1.2.1 release notes](docs/RELEASE-1.2.1.md).

---

# Lau Setup 1.2.0 — shared download and interface languages

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> **First time installing?** Use [Start here](START-HERE.txt). Older entries below retain their original release instructions.

One `LauSetup.zip` includes the Windows executable, Linux/Wine safety launcher and bundled translations. The interface detects the system language, offers ten languages including Brazilian Portuguese, and remembers a manual selection. Changing interface language preserves the selected client and options. WoW's detected locale still controls game patch selection.

The current release publishes only `LauSetup.zip` as an installer download; the duplicate Wine ZIP and standalone EXE assets were removed. Primary guides now begin with exact numbered Windows and separate Linux/Wine steps, folder selection, option meanings and recovery help. All 27 localized primary guides include current beginner steps.

Documentation follow-up: the website now has one shared download card. Current guides include plain-language setup and recovery FAQs; historical hotfix details remain below. This documentation update does not change the installer binary or game files.

Linux prerequisites remain unchanged. Game release 3.0.8, its nine game locales, all 28 game assets and their hashes remain unchanged; no DBC edits. Validation passed 62 Windows and 62 Wine regression groups, 50 Windows and 21 normal-user Wine interface states, 185 translation keys across ten languages, and 31 package, translation, and host tests. See [1.2.0 release notes](docs/RELEASE-1.2.0.md) and [shared-package guide](docs/UNIVERSAL-INSTALLER.md).

---

# Lau Setup 1.1.8 Hotfix — renamed-patch checks

Setup 1.1.8 Hotfix checks active root and client-locale MPQs for renamed Patch-Y markers and exact copies of catalog patches before downloading and again before installation. A possible conflict or unreadable/unsupported archive stops installation with its filename; setup does not delete it. Keep a backup and resolve the named archive outside Data before retrying. Expected Q/M/S/Y placements and disabled files are excluded. Game files remain 3.0.8; no DBC edits.

Windows and Wine each passed 60 regression groups, including 108 locale/edition/map plans, renamed/malformed archives, cancellation, a conflict introduced during staging, interrupted operations and exact rollback. Fresh release payloads passed on/off/on and stacked rollback on both platforms. The raw Patch-Y ZIP, game executable and DBC bytes are unchanged. See [scan coverage and limits](docs/MPQ-SCANNING.md).

---

# Lau Setup 1.1.7 Hotfix - Patch-S re-enable cleanup

- Re-enabling New spell visuals reuses a disabled Patch-S when its SHA-256 and size match the selected release, avoiding that download.
- The plain disabled copy moves into the verified transaction backup outside Data, even if active Patch-S already matches. Different disabled files remain recoverable through Restore previous install.
- Applies to root and active-locale Patch-S. Off still uses the plain `.mpq.disabled` filename. Existing hash-suffixed archives are left intact.
- Game payloads remain 3.0.8 Lau. Windows and Wine each passed 50 regression groups, real-file on/off/on switching and exact rollback.

---

# Lau Setup 1.1.6 Hotfix - Switch options with existing disabled Patch-S

Fixes the 1.1.5 message "A different disabled Patch-S already exists" when turning New spell visuals off after an earlier install.

Setup keeps both files automatically. The current S file always becomes `.mpq.disabled`. If a different older disabled copy is already there, Setup first preserves that older copy as `.mpq.disabled.<12-character hash>`. An identical saved copy is reused. Both versions are retained. A hash-named copy whose contents do not match the older file being preserved still stops the operation for inspection.

This applies to root and active-locale S files, including the sequence **all three flags on -> New spell visuals off**, repeated switches and rollback. The map choice is retained.

Download the new EXE or Wine ZIP and retry your selection. You do not need to delete or rename the existing disabled copy to resolve the ordinary collision shown by 1.1.5.

To undo the full install, use **Restore previous install**. To manually re-enable a saved S file, close WoW and remove `.disabled` and any following hash, restoring its original `.mpq` filename. Never overwrite a different active file. Manual changes can stop managed rollback on file drift; keep your backups. Files removed by installers before 1.1.5 still need recovery through their backups.

Game release remains **3.0.8 Lau** and every game payload is unchanged. All 90-degree cones, meteor-fire radius and Coldflame are preserved.

Windows and Wine checks include 46 regression groups, all nine locales, existing disabled files, repeated on/off switches, tampered-copy protection, interruption recovery and exact rollback. Fresh public downloads are tested with real On/Off release files and an older disabled copy present. This is installer validation, not new in-game encounter validation.

[Raw six-edition Patch-Y ZIP](https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.1.4/Lau-Patch-Y-3.0.8-All-Editions.zip)

[Installation help and changelog](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

# Lau Setup 1.1.5 Hotfix - Keep disabled Patch-S files

Turning off **New spell visuals** now preserves the root and active-locale Patch-S files beside their original locations as `.mpq.disabled`, rather than leaving them only in installer backups. Their bytes are verified before and after the change. WoW does not load the disabled filename.

- A different existing `.disabled` copy blocks the install; it is never overwritten.
- An identical disabled copy is reused and preserved.
- Turning the option on installs the selected release's active S files and keeps disabled copies.
- Repeat installs, rollback and interruption recovery cover both active and disabled paths.

To re-enable a disabled file manually, close WoW and remove only the `.disabled` suffix. Do not overwrite a different active file. To undo the complete Lau installation, use **Restore previous install**; deleting only Patch-Y does not undo Q/M/executable or other changes. Manual file changes can cause managed rollback to stop on drift, so keep the backups.

**Already affected by an older installer?** This update does not automatically extract old backups. Use Restore previous install to recover those files, working backwards through any stacked installs, before reinstalling with the new setup. Keep LauSetupBackups.

Game release remains **3.0.8 Lau**. All MPQs are unchanged: 90-degree breaths/Slime Spray, approved +50% Halion meteor-fire radius and Coldflame are preserved. Download the new EXE or Wine ZIP for the installer fix.

Windows and Wine validation is included in VALIDATION.json. Tests cover all nine locales, disabled-copy collisions, on/off transitions, repeated installation, interruption at every move/restore step, file drift and exact rollback. The fix does not claim new in-game encounter validation.

[Raw six-edition Patch-Y ZIP (unchanged 3.0.8)](https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.1.4/Lau-Patch-Y-3.0.8-All-Editions.zip)

[Installation help and changelog](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

# Lau Setup 1.1.4 · Game release 3.0.8 Lau

## All breath and Slime Spray warnings are now 90°

Following Warmane tester confirmation, Halion (both realms), Saviana Ragefire, Sartharion, ICC Rimefang and Rotface Slime Spray now use **90° total cones**, matching Sindragosa's existing 90° warning. This applies to all six editions and nine client languages, including the existing normal/heroic spell mappings.

Only cone width changes. Range, animation timing, native spell effects and spell tables are preserved. The approved 50% larger Halion meteor-fire radius, light blue Coldflame, colors and Consecration are unchanged. These are visual warning buffers; server damage and mechanics are unchanged. Uneven terrain can still clip flat cones.

## Updating

Download **LauSetup.exe** or **LauSetup-Wine.zip** from this release first. Close WoW, select the same client and visuals, then click **Install upgrade**. Old installers retain their old catalogs. Check `/pyversion` for **3.0.8 Lau**.

Setup verifies actual SHA-256 hashes, so previous releases and even one-byte changes with unchanged size and timestamp are detected. Only exact current files count as already installed. Backups and Restore previous install remain available.

Windows requires .NET Framework 4.8. Wine users extract all four files and run `LauSetup.sh` as a normal user with the supported existing Wine/Mono prefix. Runtime installers are not bundled.

## Validation

See VALIDATION.json for Windows and Wine regression, six-edition upgrades from 3.0.7, repeat detection, one-byte checks, rollback and public-download checks. Geometry checks verify 90° cones, preserved range, valid bounds and triangle winding in every edition. Exactly eleven existing archive members change: five models, their five skins and the version TOC. All other members are byte-identical to 3.0.7.

The width decision follows reported Warmane testing. This release is not an every-encounter or exact server-boundary certification.

[Website changelog and installation help](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

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

# Lau Setup 1.4.0 / Game 3.0.9 Lau

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

The stable release uses one [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) for Windows and supported Linux/Wine. Extract the whole ZIP before starting. Windows opens LauSetup.exe; Linux uses LauSetup.sh with the existing supported Wine prefix.

## Your existing game, your choice of visuals

1. Close WoW. Click **Browse...** and choose the folder containing **WoW.exe**, not Data.
2. Click **Next**. Setup detects the game language and HD/Non-HD client. Interface language remains available on every step.
3. Choose your extras. Patch-Y is selected for the detected client. All extras start off: **Compatible WoW.exe + loading screens**, **Enhanced Consecration**, **New spell visuals** (existing HD models required), and **Upgrade maps and minimap**. Installed map upgrades are kept.
4. Click **Next**, review the folder, choices, Install/Keep existing states and download size, then click **Install upgrade**.
5. Wait for **Finished**, start WoW and use `/pyversion` to confirm **3.0.9 Lau**.

## What changed since stable 1.3.0

- Four-step wizard, manual/automatic language selection, clearer review and progress through download, staging, installation and verification.
- Approved dark layout with aligned controls, numbered steps and dividers, rounded folder field, placeholder and Browse button. Neil and Andre approved the visual candidate.
- Optional executable and loading screens share one checkbox. Off keeps both unchanged. Maps work independently.
- Maps combine Lau world/minimap textures with Trimitor WDM 2.4.5 dungeon/raid maps and its beta cave expansion, including required WDM/!Astrolabe support files.
- Unrelated and renamed duplicate patches remain in place. Empty Patch-V is backed up; nonempty Patch-V stays with a nonblocking compatibility warning.
- All six Patch-Y editions report 3.0.9 and are compacted for distribution, saving 58,774,086 bytes in total compared with 3.0.8. Setup does not compact player files or backups.

## Backups and compatibility

Files replaced by Setup are verified and backed up in LauSetupBackups. Restore previous install returns the exact original files. Keep backups and use Setup 1.4.0 or newer to restore map-support addon transactions. Unlisted addons and SavedVariables remain untouched; selected WDM support files and the active-language Patch-T can be replaced with backups.

Windows requires .NET Framework 4.8. Linux/Wine requires the documented Wine 11.0 / Wine Mono 10.4.1 environment, Python 3.9+, fonts, a 64-bit prefix and local Linux storage. See [the Wine guide](../wine/README.txt).

## DBC changes

**No Patch-Y DBC edits.** The optional map component adds upstream DungeonMap, DungeonMapChunk, WorldMapArea, WorldMapTransforms, AreaTable and WMOAreaTable overrides. See [table hashes and provenance](dbc/map-pack-1.4.0.json) and [DBC changelog](../DBC-CHANGELOG.md). The final wizard polish changes no game archives.

## Validation and limits

The release validation file records Windows and normal-user Wine regression tests, six real 3.0.8-to-3.0.9 edition upgrades, repeat-install detection, exact restore, recovery, language and packaged layout checks. See [VALIDATION.json](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/VALIDATION.json).

Installer validation does not certify every client patch combination or encounter. Cave maps remain upstream beta; report navigation or floor-switching problems with the exact client and options. New feature experiments are separate from this stable release.

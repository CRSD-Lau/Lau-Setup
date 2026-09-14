# Technical reference

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

[Back to Lau Setup](../README.md)

> **First time installing?** Use [Start here](../START-HERE.txt). This reference is for build, recovery, and verification details.

## Build and verification

Run `tools/build.ps1` on Windows with the .NET Framework compiler installed. The 1.2.0 source bundle includes the application, embedded catalog and translations, build/package scripts, documentation, and regression harnesses. `tools/test_localization.ps1` checks language resolution, saved preferences and live interface switching without a game installation. `tools/test.ps1 -ClientExecutable <path-to-WoW.exe>` runs transaction, download, path, process, recovery and GUI tests using isolated copies of an externally supplied build 12340 reference executable. The source bundle excludes that executable, game payloads and private source indexes. `tools/build.ps1 -Release` refuses a catalog that has not passed the publication gate.

For the shared 1.2.0 release, build with `tools/build.ps1 -OutputDirectory dist/universal-1.2.0`, then run `python tools/package_universal.py`. `python tools/translate_installer.py verify` checks the bundled translations offline. `python -m unittest discover -s tests -p "test_universal_package.py"` checks package contents and Linux language precedence. Release validation recorded 62 Windows and 62 Wine regression groups, 50 Windows and 21 normal-user Wine interface states, 185 keys in ten interface languages, and 31 package, translation, and host tests. See the [shared-package guide](UNIVERSAL-INSTALLER.md) for supported platforms and the distinction between installer language and game locale.

`build/catalog.json` names every asset and download segment by size and SHA-256, together with observed GitHub Release URLs. The catalog pins the repository, release tag and hash-named file. The installer downloads anonymously and checks every redirect before following it. No GitHub account, signed-in browser or API credential is required by the installer. In the full development checkout, `tools/refresh_github_catalog.py` associates uploaded assets without changing hashes, and `tools/verify-public.ps1` verifies every segment and reconstructed asset through the same downloader used by the app.

## File placement and recovery in 1.4.0

Patch-Y goes to the root Data folder and the active game locale. Optional new-spell assets and localized tables use the corresponding Patch-S paths. Turning new spell visuals off preserves the scoped S files as disabled copies.

Compatible WoW.exe and loading screens are one optional choice. Off keeps the current executable and Patch-Q. On backs up and replaces WoW.exe plus matching root/locale loading Q archives. Maps are independent: Patch-M supplies world/minimap textures, the active locale's Patch-T supplies upstream map data, and an exact WDM/!Astrolabe allowlist supplies addon support. Existing localized M/N archives, unlisted addon files and SavedVariables remain in place.

One client lock covers downloading, staging and installation. Downloads, staged files and installed destinations are hash-verified. Existing files and recovery journals are retained under LauSetupBackups/transactions. Addon backup storage uses short names; journals retain original paths. A failed commit restores originals when safe. Interrupted installs/restores remain recoverable, including a missing WoW.exe.

Restore refuses files changed after installation. Managed paths are exact allowlisted root/locale Q/M/S/T/Y paths, WoW.exe and selected map-support addon files. Arbitrary and renamed duplicate patches are not scanned or removed. An empty Patch-V is the backup-only exception; a nonempty V stays with a warning. Traversal, alternate streams, linked paths and hardlink hazards retain their safety checks. Setup never extracts arbitrary archive entries into the client filesystem.

## Release boundaries

The installer is unsigned. Windows and Wine installer tests, sampled GUI checks and the retained game-data baseline are recorded separately in VALIDATION.json. Wine 1.1.0 checks use Wine 11.0 / Wine Mono 10.4.1 and local Docker overlay storage; the nested-mount test mocks device identity because that container cannot create mounts. These checks do not certify every Linux distribution/filesystem, display scale, encounter or third-party client modification. Raw Patch-Y edition ZIPs are available on GitHub Releases. See [known limitations](../KNOWN-LIMITATIONS.md) for current scope and assumptions.


## 3.0.6 color update / Setup 1.1.2

Each of the six Y archives changes three M2 members and the !PYAndre TOC, and adds two BLP textures. `Spells/PW_Coldflame_Ground.m2` now references `Spells/PW_Coldflame_Blue.blp`; `Spells/PW_HalionMeteor_Ground.m2` and `Spells/PW_HalionMeteor_Ring.m2` reference `Spells/PW_Halion_Red.blp`. Only texture descriptor 4's filename length/offset changes in each original model; the new path is appended. Native particle textures (indices 0–3), skins, geometry, global animation tracks, bounds and DBC bytes are unchanged. The shared white texture remains unchanged for other indicators.

The new textures preserve the existing opaque 8×8 DXT1 BLP2 format and all four mip levels. Only the RGB565 endpoint changes: light blue decodes as (120,216,248,255), red as (248,68,40,255). Quantization is inherent to the existing texture format. Both Halion models use the same red texture. Consecration and model-edition choices remain independent.

Update decisions compare actual SHA-256 and size, not release labels or timestamps. Regression tests modify one byte without changing file size or timestamp in each Y placement, require exactly one repair operation, verify the repaired hash, then restore the previous release. An old EXE embeds the old catalog, so upgrading requires downloading the new EXE/ZIP first.

## 3.0.7 Halion radius / Setup 1.1.3

Promotes exact test-v2 bytes for `Spells/PW_HalionMeteor_Ground.m2`, `Spells/PW_HalionMeteor_Ring.m2` and their `00.skin` files. Mesh X/Y coordinates are 1.5 times 3.0.6. Z/UVs/normals and animation/particle tracks are preserved. Model bounds (offset 160), sequence bounds (sequence +32), and skin submesh bounds (submesh +20) reflect the enlarged geometry. TOC version changes from 3.0.6 to 3.0.7. Exactly five existing members change per edition; no added or removed members. Test v3 geometry is excluded. Coldflame and all other members match 3.0.6. User relayed tester acceptance of v2; broad encounter certification is not claimed.

## 3.0.8 all cones / Setup 1.1.4

All six editions use 90 degree total fan geometry. Legacy model filenames and all DBC rows remain unchanged to preserve spell routing. Changes: PW_White_Fan60_60yd_Glowing (Halion both realms), PW_White_Fan60_30yd_Glowing (Saviana), PW_White_Fan60_100y_Glowing (ICC Rimefang), and PW_Rotface_SlimeSpray_Fan25_Room (Rotface) widen from 60 to 90; PW_White_Fan82_60yd_Glowing (Sartharion) widens from 82 to 90. PW_White_Fan75_60yd_Glowing (Sindragosa) is already 90 and is byte-identical.

For each modified model, only vertex XY (48-byte vertex stride) and bounds change. Angle about +X scales by 90/old-angle; each vertex radius and Z are preserved. Model bounds at offset 160, sequence bounds at sequence+32, and skin submesh bounds at submesh+20 are updated. UVs, normals, animation and particle tracks remain unchanged. Ten model/skin members and two version strings in the TOC change per edition; no members are added or removed. All other members, including Halion meteor-fire test-v2 geometry and Coldflame, match 3.0.7 byte for byte.

## Setup 1.1.5 disabled Patch-S preservation

Only root and active-locale S paths gain the .disabled suffix. Each disable creates a hash-pinned local staged copy before deactivating S; both paths are journaled, with at most eleven destinations. Rollback restores original active files and removes only newly created disabled copies. Pre-existing identical disabled copies remain outside the transaction and are preserved. Conflicting files or directories block planning. Re-enabling installs catalog S assets and does not consume the disabled copies. Existing journals remain readable. No arbitrary local source paths are accepted: each local copy must match its paired S deactivation operation.

## Setup 1.1.6 disabled-copy collisions

The current active S file always takes the plain .mpq.disabled name. Before replacing a different existing disabled file, Setup stages its bytes into a sibling ending in the first 12 characters of its SHA-256; full SHA-256 and length are checked before any reuse. This keeps names within the existing Windows path limits. Conflicting archive contents fail closed. The active S, plain disabled file, and newly created archival copy are journaled independently, with at most thirteen entries; rollback restores all originals. Local sources are restricted to paired S deactivation or disabled-file replacement operations. Old journals remain readable.

## Setup 1.1.7 re-enable cleanup

Enabling new spells journals removal of the plain root and active-locale disabled S files. The transaction moves their verified original bytes into its before backup outside Data. If a disabled file matches the catalog SHA-256 and size, it is staged locally for the matching S destination and excluded from downloads. Local sources must be paired with the exact disabled-file removal and catalog asset. Active S already matching still produces a cleanup transaction. Existing hash-suffixed archives are not swept. Previous journals remain readable. On/off/on, source drift, interruptions at every new commit/restore step, all locales and stacked restoration are covered.


## Current backup behavior (Setup 1.3.0)

**Before Setup replaces or moves an existing game file, it preserves the original automatically.** Keep `LauSetupBackups` in your game folder; **Restore previous install** uses it to put the originals back. Unrelated files stay in place.

Setup leaves unrelated MPQs alone and does not parse them for conflicts. If you rename patch-y.mpq to patch-lau.mpq, that copy stays in place; manage renamed duplicates yourself. Setup backs up files it replaces. Empty Data\patch-v.mpq is the only additional automatic cleanup; nonempty V stays with a warning.

## Historical Setup 1.1.8 renamed-patch preflight

The manual-move behavior below describes 1.1.8 and is superseded by automatic backups in 1.3.0.

Setup 1.1.8 Hotfix checks active root and client-locale MPQs for renamed Patch-Y markers and exact copies of catalog patches before downloading and again before installation. A possible conflict or unreadable/unsupported archive stops installation with its filename; setup does not delete it. Keep a backup and resolve the named archive outside Data before retrying. Expected Q/M/S/Y placements and disabled files are excluded. Game files remain 3.0.8; no DBC edits.

`app/MpqScan.cs` implements bounded classic hash-table probes in managed C#, with no archive extraction, decompression, external process or native parser. It runs during plan creation, under the client lease before GUI downloads, at transaction preflight and after staging immediately before commit. It does not change restoration semantics or expand the write allowlist. Files remain vulnerable to unrelated external changes after a check; close WoW and avoid concurrent manual changes.

See [scanner limits](../KNOWN-LIMITATIONS.md#setup-118-overlap-detection). Windows and Wine regression cases include missing-listfile detection, normal placements, generic shared members, disabled/other-locale files, current-catalog copies, malformed/bounded tables, pre-transaction drift and cancellation.


Setup 1.4.0 also accepts game-language codes regardless of letter case (`enus`, `ENUS` and `enUS` all select enUS), without changing Config.wtf. The window shows both the installer version and game release.

**Patch-V:** Empty `Data\patch-v.mpq` files (any letter case) are backed up automatically. Recognized Lau upgrade copies are also backed up. An unidentified nonempty Patch-V stays in place with a compatibility warning; installation continues, even if the scanner cannot parse it. A filename alone cannot identify the unstable HD building patch because unrelated mods can also use V. **Restore previous install** returns backed-up files.

Maps and loading screens are independent options. Maps include Lau’s maps/minimaps plus Trimitor WDM dungeon, raid and cave maps and their required support addons. Selected map-support files are backed up before replacement; personal settings and unrelated addons remain untouched.
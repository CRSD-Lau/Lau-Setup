# Technical reference

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

[Back to Lau Setup](../README.md)

## Build and verification

Run `tools/build.ps1` on Windows with the .NET Framework compiler installed. The public source bundle contains the application, embedded catalog, build script, and documentation. The full development checkout additionally contains `tools/test.ps1` for transaction, download, path, process, recovery, and GUI regression tests; those tests use isolated fixtures and a local reference executable. `tools/build.ps1 -Release` refuses a catalog that has not passed the publication gate. The test harness, payload generation, and native game tests depend on private local source paths and are not part of the public source bundle.

`build/catalog.json` names every asset and download segment by size and SHA-256, together with observed GitHub Release URLs. The catalog pins the repository, release tag and hash-named file. The installer downloads anonymously and checks every redirect before following it. No GitHub account, signed-in browser or API credential is required by the installer. In the full development checkout, `tools/refresh_github_catalog.py` associates uploaded assets without changing hashes, and `tools/verify-public.ps1` verifies every segment and reconstructed asset through the same downloader used by the app.

## File placement

| Component | Destination |
|---|---|
| Compatible executable | `WoW.exe` |
| Selected regional Q | Identical copies in root `Data/patch-q.mpq` and active locale `Data/<locale>/patch-<locale>-Q.MPQ` |
| Selected edition Y | Identical copies in root `Data/patch-y.mpq` and active locale `Data/<locale>/patch-<locale>-Y.MPQ` |
| New spell assets, when selected | Root `Data/patch-s.mpq` |
| Matching localized spell tables, when selected | Active locale `Data/<locale>/patch-<locale>-S.MPQ` |
| Optional maps/minimap | Root `Data/patch-m.mpq`; the superseded active-locale M is backed up |

Core Q retains the release's LoadingScreens.dbc, localized Map.dbc and loading images byte for byte. It omits the added world-map definitions and world-map artwork. Full map mode uses the original regional Q and shared M without repacking them. The two S placements contain different archives. Turning new spells off backs up and removes the scoped root/locale S pair. HD detection requires the matching existing root and locale F patches.

## Recovery design

One client lock covers downloading, staging and installation. Files are verified before staging and again after placement. Existing files move into `LauSetupBackups/transactions/<id>/before/`, preserving their bytes and timestamps; the journal is written durably before commit. A failed commit restores originals when safe. Interrupted commits and interrupted restores remain discoverable when the app is reopened, even without WoW.exe.

Restore refuses files changed by another update and keeps the backup for manual resolution. Only exact root/active-locale Q/M/S/Y paths and WoW.exe are accepted. Traversal, alternate streams and reparse points are rejected; writable resumed files must have one hardlink. Journal and assembly temporaries use unique names and exclusive creation. The application never enumerates an archive into the client filesystem.

## Release boundaries

The installer is unsigned. Windows and Wine installer tests, sampled GUI checks and the retained game-data baseline are recorded separately in VALIDATION.json. Wine 1.1.0 checks use Wine 11.0 / Wine Mono 10.4.1 and local Docker overlay storage; the nested-mount test mocks device identity because that container cannot create mounts. These checks do not certify every Linux distribution/filesystem, display scale, encounter or third-party client modification. Existing manual Google Drive releases remain available; new raw-file uploads are deferred while rate limited.


## 3.0.6 color update / Setup 1.1.2

Each of the six Y archives changes three M2 members and the !PYAndre TOC, and adds two BLP textures. `Spells/PW_Coldflame_Ground.m2` now references `Spells/PW_Coldflame_Blue.blp`; `Spells/PW_HalionMeteor_Ground.m2` and `Spells/PW_HalionMeteor_Ring.m2` reference `Spells/PW_Halion_Red.blp`. Only texture descriptor 4's filename length/offset changes in each original model; the new path is appended. Native particle textures (indices 0–3), skins, geometry, global animation tracks, bounds and DBC bytes are unchanged. The shared white texture remains unchanged for other indicators.

The new textures preserve the existing opaque 8×8 DXT1 BLP2 format and all four mip levels. Only the RGB565 endpoint changes: light blue decodes as (120,216,248,255), red as (248,68,40,255). Quantization is inherent to the existing texture format. Both Halion models use the same red texture. Consecration and model-edition choices remain independent.

Update decisions compare actual SHA-256 and size, not release labels or timestamps. Regression tests modify one byte without changing file size or timestamp in each Y placement, require exactly one repair operation, verify the repaired hash, then restore the previous release. An old EXE embeds the old catalog, so upgrading requires downloading the new EXE/ZIP first.

## 3.0.7 Halion radius / Setup 1.1.3

Promotes exact test-v2 bytes for `Spells/PW_HalionMeteor_Ground.m2`, `Spells/PW_HalionMeteor_Ring.m2` and their `00.skin` files. Mesh X/Y coordinates are 1.5 times 3.0.6. Z/UVs/normals and animation/particle tracks are preserved. Model bounds (offset 160), sequence bounds (sequence +32), and skin submesh bounds (submesh +20) reflect the enlarged geometry. TOC version changes from 3.0.6 to 3.0.7. Exactly five existing members change per edition; no added or removed members. Test v3 geometry is excluded. Coldflame and all other members match 3.0.6. User relayed tester acceptance of v2; broad encounter certification is not claimed.

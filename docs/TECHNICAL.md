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

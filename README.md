# Lau Setup

Author: Neil Mitchell  
Creator: Neil Mitchell  
Last Modified By: Neil Mitchell

Small Windows installer for the Lau 3.0.4 Q/S/Y upgrade. The user selects an existing WoW 3.3.5a build 12340 folder, confirms visual options, and installs. See START-HERE.txt for the user instructions.

Installer 1.0.1 improves contrast for supporting text and disabled controls, and increases footer text size. Game payloads and installation behavior are unchanged. Linux/Wine and macOS are not yet supported; see [platform feasibility and the required checks](PLATFORM-FEASIBILITY.md).

**[Download LauSetup.exe](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.exe)**

1. Close World of Warcraft.
2. Download and open **LauSetup.exe**, then choose your WoW folder.
3. Choose your visuals and click **Install upgrade**.

Start WoW and type `/pyversion` to confirm the edition. Enhanced Consecration is selected by default; uncheck it for the stock appearance. Upgraded maps and minimap textures are optional. Your existing addons, settings, fonts and login artwork are preserved.

The base download is about 472 MB for an English HD client with new spell visuals, or 259 MB for a non-HD client. Optional maps add a larger download. The installer displays the amount for your chosen language and options before installation. No manual archive placement or renaming is needed.

The public deliverable is LauSetup.exe. It has an embedded, immutable catalog and uses the installed .NET Framework 4.8 runtime. No administrator privilege, full client, personal UI, account credentials, analytics, remote scripts, or runtime toolchain is bundled. The installer interface is in English; the game keeps its detected language.

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

The installer is unsigned. It has been built and exercised on the current Windows host; runtime game checks use isolated Docker/Wine clients. Native file/hash/text checks and sampled visual inspection are recorded separately. They do not certify every zone, encounter, third-party client modification, or Windows configuration. Existing manual Google Drive releases remain available. New installer builds are published only after their public-download and native-runtime gates pass.

# Lau Setup

Author: Neil Mitchell  
Creator: Neil Mitchell  
Last Modified By: Neil Mitchell

Small Windows and Wine installer for the Lau 3.0.4 Q/S/Y upgrade. Select an existing WoW 3.3.5a build 12340 folder, confirm visual options, and install. See START-HERE.txt for Windows instructions and [the Wine guide](wine/README.txt) for Linux.

Installer 1.1.0 adds Wine 11 / Wine Mono 10.4.1 support through a Linux launcher with host process, path and locking checks. It also uses the release site's W-and-shield icon for the executable and window, selects fonts available on Wine, and checks Windows .NET Framework 4.8 before opening setup. Game payloads remain unchanged. Lutris, Proton and macOS integration are outside this release.

**[Download LauSetup.exe](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.exe)**

**[Download LauSetup-Wine.zip for Linux](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup-Wine.zip)** — extract it and run `WINEPREFIX="/path/to/existing/prefix" sh LauSetup.sh`. Requires Wine 11.0, Wine Mono 10.4.1, a 64-bit prefix and Python 3.9+. Use the supplied launcher; direct Wine execution refuses client operations without its Linux safety helper. Close every WoW instance across all prefixes.

1. Close World of Warcraft.
2. Download and open **LauSetup.exe**, then choose your WoW folder.
3. Choose your visuals and click **Install upgrade**.

Start WoW and type `/pyversion` to confirm the edition. Enhanced Consecration is selected by default; uncheck it for the stock appearance. Upgraded maps and minimap textures are optional. Your existing addons, settings, fonts and login artwork are preserved.

The base download is about 472 MB for an English HD client with new spell visuals, or 259 MB for a non-HD client. Optional maps add a larger download. The installer displays the amount for your chosen language and options before installation. No manual archive placement or renaming is needed.

The Windows download uses the installed .NET Framework 4.8 runtime and offers Microsoft's official download page when it is missing. The Wine bundle uses Wine Mono and includes a small Python standard-library safety helper. Runtime installers are not bundled. No administrator privilege, full client, personal UI, account credentials or analytics are included. The installer interface is English; game content retains all nine supported client locales.

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

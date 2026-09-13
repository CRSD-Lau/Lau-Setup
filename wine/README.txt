Lau Setup 1.2.1 shared Windows/Linux release
Author / Creator / Last Modified By: Neil Mitchell

Game data remains Lau 3.0.8. This package contains one LauSetup folder with
exactly LauSetup.exe, LauSetup.sh, lau_wine.py, lau-languages.json and this
README.txt. Keep those five files together after extraction.

## Start here on Windows

You need Windows 10/11 and your existing WoW 3.3.5a game (build 12340).
This ZIP is an upgrade, not the complete game.

1. Close WoW completely.
2. If you have not already done so, right-click LauSetup.zip, choose Extract
   All, and open the extracted LauSetup folder.
3. Double-click LauSetup.exe. Its File Explorer type is Application.
4. Click Choose folder… and select the game folder that directly contains
   WoW.exe, not its Data folder or a launcher folder.
5. Leave Enhanced Consecration on for the custom look, or turn it off for the
   original look. New spell visuals is available only with compatible HD
   models. Upgrade maps and minimap is optional and adds a download.
6. Click Install upgrade and wait until it finishes. Start WoW and type
   /pyversion; it should show 3.0.8 Lau.

Already installed means your selected files match this release; no game update
is needed. To undo an installation, close WoW, reopen Lau Setup, choose the
same game folder and click Restore previous install. Keep LauSetupBackups.

Cannot find the app? Open the extracted folder, not the ZIP. If setup rejects
a folder, find the one containing WoW.exe. If .NET is missing, use the Microsoft
.NET Framework 4.8 prompt and then reopen setup.

Setup follows your system language. Interface language lets you select and
save another language; Automatic follows your computer again. This changes
setup text only, not your game's language or files.

## Start here on Linux / Wine

1. Download `LauSetup.zip` and extract it. Keep the five files in its
   `LauSetup/` folder together.
2. Before starting, use an existing WoW 3.3.5a build 12340 client on local
   Linux storage, and close every WoW instance in every Wine prefix.
3. Your existing environment must have Wine 11.0, Wine Mono 10.4.1, a 64-bit
   prefix, Python 3.9+, and the fonts listed below. Lau Setup does not create
   or repair these prerequisites.
4. In the extracted `LauSetup` folder, run:

   WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh

   Replace the example path with your existing Wine prefix path.

5. In Lau Setup, choose **Choose folder…** and select the game folder that
   directly contains `WoW.exe`, not its `Data` folder. Select your options,
   choose **Install upgrade**, and wait for completion. **Enhanced
   Consecration** starts on; **New spell visuals** needs detected compatible HD
   models; **Upgrade maps and minimap** is optional. If setup says **Already
   installed**, the selected files already match this release and no game
   update is needed.
6. Start WoW and type `/pyversion`. To undo an installation, close WoW, reopen
   setup with the same game folder, and choose **Restore previous install**.

Linux requirements and limits
- Wine 11.0, an existing 64-bit prefix, and Wine Mono 10.4.1 in that prefix.
- Python 3.9+ for the standard-library host safety helper.
- Liberation Sans or DejaVu Sans and Wine's complete font package for controls.
- Korean and Chinese interface text needs Wine-visible Noto Sans CJK fonts
  (`fonts-noto-cjk` on typical Debian/Ubuntu systems). Lau Setup auto-selects
  them when available and never installs fonts or other prerequisites.
- Local Linux storage, ordinary host process visibility, and a normal user;
  never sudo/root. Network shares, Windows-mounted drives, symlinked paths,
  hardlinks, ambiguous casing, and process-hiding sandboxes are rejected.
- The prefix may contain the 32-bit game client. Lau Setup never creates,
  converts, or upgrades the prefix; changes its Wine/Mono/DXVK runtime or
  registry configuration; or changes a game launcher. The application stores
  its saved interface-language choice only in that Wine user's app data.
  Proton, Lutris and macOS are not supported.

Always use LauSetup.sh on Linux. Starting LauSetup.exe directly under Wine
refuses client operations because it lacks the host path, process, and
cross-prefix lock guard. Keep WoW closed until Setup completes. The guard
reduces races but cannot stop another program launched afterward.

If the launcher cannot start, confirm that `LauSetup.exe`, `lau_wine.py`, and
`lau-languages.json` are still in the extracted `LauSetup` folder. If it says
WoW is running, close every WoW instance in every prefix and retry. If it
rejects your game folder, select the folder that directly contains `WoW.exe`.
If it reports missing matching language files, use the fully installed locale
already active in that client; changing configuration does not add a game
language pack. If an interrupted install needs restoring, choose the same
client folder and select **Restore previous install**. Keep
`LauSetupBackups`; if restore stops because another update changed a named game
file, keep all files and backups. Report the exact message, filename, and a
screenshot at https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose; do not
delete or force-replace files to bypass the check.

Possible extra upgrade patch? A file with its original download name can
trigger this too. Close WoW, keep a backup, and move only the named extra file
outside Data, then retry. Setup chooses the right edition. Do not rename an HD
download into an original-model client. If unsure, report the file first.

Cannot safely check patch? Download the latest setup; 1.2.1 fixes the old
large-table restriction. If it still stops, keep the archive and backups and
report the exact message and filename through the link above.

Interface language
The interface has ten languages: English (US), German, French, Spanish
(Spain), Spanish (Mexico), Portuguese (Brazil), Korean, Russian, Simplified
Chinese and Traditional Chinese. On Linux it follows LC_ALL, then LC_MESSAGES,
then LANG; GNU LANGUAGE supplies a preferred list only when that category is
not C or POSIX. A missing category is treated as C. Use
`sh LauSetup.sh --language fr-FR` to select and save that manual choice. Use
`sh LauSetup.sh --language auto` to save Automatic and return to the host/system
language. The launcher passes only validated argv and does not
write Wine registry settings; LauSetup.exe owns the saved preference in Wine
user app data.
All ten interface languages are bundled, but fluent human review remains the
limit for translation quality.

Interface language is separate from game locale. The nine unchanged supported
game locales are enUS, deDE, frFR, esES, esMX, koKR, ruRU, zhCN and zhTW.

Historical 1.2.0 validation passed 62 Wine regression groups. Thirty-five groups ran before the
busy-state completion fix; the affected GUI group and remaining 26 ran after
it, followed by final localization and packaged-window checks. Twenty-one
normal-user Wine interface states and all ten bundled interface languages were
checked. This is not certification for every Linux distribution, filesystem,
display scale, Wine version, translation nuance, or game encounter.

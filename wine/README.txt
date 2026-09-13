Lau Setup 1.2.0 local shared Windows/Linux candidate
Author / Creator / Last Modified By: Neil Mitchell

Game data remains Lau 3.0.8. This package contains one LauSetup folder with
exactly LauSetup.exe, LauSetup.sh, lau_wine.py, lau-languages.json and this
README.txt. Keep those five files together after extraction.

Windows
Open LauSetup.exe. It is the native installer and requires .NET Framework 4.8.

Linux with Wine
1. Use an existing WoW 3.3.5a build 12340 client on a local Linux filesystem.
2. Close every WoW instance, including games in other Wine prefixes.
3. In the extracted LauSetup folder, run:

   WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh

4. Choose the existing game folder and install. Automatic backups and Restore
   previous install remain available.

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

Validation scope: isolated Wine 11.0 / Wine Mono 10.4.1 clients, fixture and
real-payload install/restore tests, two-prefix safety tests and sampled GUI
checks. This is not certification for every Linux distribution, filesystem,
display scale, Wine version or game encounter.

This is a local 1.2.0 candidate. Public release links remain on 1.1.8 until
separate release validation and publishing are complete.

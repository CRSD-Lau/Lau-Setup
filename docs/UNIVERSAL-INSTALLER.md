# Lau Setup shared Windows/Linux package

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell

`LauSetup.zip` is the Lau Setup 1.3.0 release ZIP for Windows and Linux.
Extract it intact: it contains one `LauSetup/` folder with `LauSetup.exe`,
`LauSetup.sh`, `lau_wine.py`, `lau-languages.json`, and `README.txt`.

## Start here

### Windows

1. Close WoW completely. Right-click `LauSetup.zip`, choose **Extract All**,
   and open the extracted `LauSetup` folder.
2. Double-click `LauSetup.exe` (its File Explorer type is **Application**).
3. Choose **Choose folder…**, then select the folder that directly contains
   `WoW.exe`, not its `Data` folder or a launcher folder.
4. **Enhanced Consecration** starts on; **New spell visuals** needs detected
   compatible HD models; **Upgrade maps and minimap** is optional. Choose
   **Install upgrade** and wait for completion.
5. If setup says **Already installed**, the selected files already match this
   release and no game update is needed. Otherwise start WoW and type
   `/pyversion`. To undo an installation, close WoW, reopen setup with the
   same folder, and choose **Restore previous install**.

### Linux / Wine

Use the same ZIP, but first prepare the supported existing Wine environment
listed below. Close every WoW instance in every prefix, extract the ZIP, and
run `WINEPREFIX="/absolute/path/to/prefix" sh LauSetup.sh` from the extracted
`LauSetup` folder. Never start the EXE directly under Wine: the shell launcher
supplies the host process, filesystem, and cross-prefix locking guard. Once it
opens setup, follow the same **Choose folder…**, option, and **Install upgrade**
steps above.

If Windows cannot find `LauSetup.exe`, open the extracted `LauSetup` folder;
the file type should be **Application**. If setup rejects a folder, select the
folder containing `WoW.exe` directly. If WoW is running, close it and retry.
Windows uses the Microsoft .NET Framework 4.8 prompt when that runtime is missing.

Linux still requires Wine 11.0, a 64-bit prefix with Wine Mono 10.4.1, Python
3.9+, local Linux storage, visible host processes, and a normal non-root user.
Korean and Chinese interfaces also require Wine-visible Noto Sans CJK fonts
(`fonts-noto-cjk` is the usual Debian/Ubuntu package); Lau Setup selects them
automatically when available. It never installs fonts or other prerequisites.
The package does not install, upgrade, or edit Wine, Mono, DXVK, game launchers,
or prefix registry settings. Existing Wine limitations remain: no Proton,
Lutris, macOS, network shares, Windows-mounted drives, symlinked clients, or
hidden-process sandboxes are supported.

The interface selects one of ten UI languages from the host locale: English,
German, French, Spanish (Spain), Spanish (Mexico), Portuguese (Brazil), Korean,
Russian, Simplified Chinese, or Traditional Chinese. GNU `LC_ALL`, then
`LC_MESSAGES`, then `LANG` determine the category; `LANGUAGE` is its preferred
list when that category is not `C` or `POSIX`. `sh LauSetup.sh --language fr-FR`
selects and saves that manual choice. `--language auto` saves Automatic and
returns the interface to the host/system language. With no locale
category, the launcher treats the host as `C` and ignores `LANGUAGE`. Windows starts from its UI language.
All ten interface languages are bundled, but fluent human review remains the
limit for translation quality.
The saved interface choice is maintained only in the Wine user's app data by
the Windows application. The Linux launcher never changes Wine runtime or
registry configuration.

Interface language is separate from the game locale. Lau Setup continues to
detect and preserve the nine supported 3.3.5a game locales: enUS, deDE, frFR,
esES, esMX, koKR, ruRU, zhCN, and zhTW.

Build a release only after placing the built input EXE at
`dist/release-1.3.0/LauSetup.exe` and generating `app/translations.json`:

```powershell
python tools/package_universal.py --exe dist/release-1.3.0/LauSetup.exe --output dist/release-1.3.0/LauSetup.zip
```

For an isolated build, pass `--exe`, `--translations`, and
`--output`. The packager copies those input bytes exactly, accepts only the five
listed files, stamps ZIP metadata as Neil Mitchell, and gives the shell launcher
an executable Unix mode. It bundles no game payloads or Wine runtime.

Release validation passed 62 Windows and 62 Wine regression groups, 50 Windows
and 21 normal-user Wine interface states, 185 translation keys across ten
languages, and 31 package, translation, and host tests.
Game release 3.0.8, its nine locales, 28 game assets, and DBC data are unchanged.

# Lau Setup shared Windows/Linux package

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell

`dist/universal-1.2.0/LauSetup.zip` is the local 1.2.0 candidate ZIP for Windows and Linux.
Extract it intact: it contains one `LauSetup/` folder with `LauSetup.exe`,
`LauSetup.sh`, `lau_wine.py`, `lau-languages.json`, and `README.txt`.

On Windows, open `LauSetup.exe`. It needs .NET Framework 4.8 and is the native
installer. On Linux, use an existing supported Wine prefix and run
`WINEPREFIX="/absolute/path/to/prefix" sh LauSetup.sh`. Do not start the EXE
directly under Wine: the shell launcher supplies the host process, filesystem,
and cross-prefix locking guard.

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
`dist/universal-1.2.0/LauSetup.exe` and generating `app/translations.json`:

```powershell
python tools/package_universal.py
```

For an isolated release candidate, pass `--exe`, `--translations`, and
`--output`. The packager copies those input bytes exactly, accepts only the five
listed files, stamps ZIP metadata as Neil Mitchell, and gives the shell launcher
an executable Unix mode. It bundles no game payloads or Wine runtime.

This candidate does not alter public 1.1.8 release links. Publish and replace
those links only after the separate release validation is complete.

# Lau Setup shared Windows/Linux package

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell

`LauSetup.zip` is the Lau Setup 1.4.0 release ZIP for Windows and Linux.
Extract it intact: it contains one `LauSetup/` folder with `LauSetup.exe`,
`LauSetup.sh`, `lau_wine.py`, `lau-languages.json`, and `README.txt`.

## Start here

### Windows

1. Close WoW completely. Right-click `LauSetup.zip`, choose **Extract All**,
   and open the extracted `LauSetup` folder.
2. Double-click `LauSetup.exe` (its File Explorer type is **Application**).
4. Click Browse... and select the game folder containing WoW.exe,
   then click Next. Do not select Data or a launcher folder.
5. Your visuals shows a fixed Patch-Y HD or Patch-Y Non-HD selection based
   on your client. Optional extras start off. Enable Enhanced Consecration
   for Lau's ground effect, New spell visuals for upgraded spells (HD only),
   or Upgrade maps and minimap for sharper maps and an extra download.
   Already installed map upgrades are kept. Click Next.
6. Review Your choices: Patch-Y (Lau’s version), followed by each enabled
   extra. The review also lists WoW.exe, Patch-Q artwork, matching language
   patches, download size and automatic backups. Back lets you make changes.
7. Click Install upgrade and wait for Finished, then click Finish. Start WoW
   and type /pyversion to check 3.0.9 Lau. If your selection is already
   installed, click Finish; no game-file changes are needed.

Interface language stays at the top of every step. Choose your language if
Automatic detects it incorrectly. Your manual choice is remembered; choose
Automatic to follow your system again. This changes setup text, not the game.
Next does not download or change game files. Install upgrade performs the update.

### Linux / Wine

Use the same ZIP, but first prepare the supported existing Wine environment
listed below. Close every WoW instance in every prefix, extract the ZIP, and
run `WINEPREFIX="/absolute/path/to/prefix" sh LauSetup.sh` from the extracted
`LauSetup` folder. Never start the EXE directly under Wine: the shell launcher
supplies the host process, filesystem, and cross-prefix locking guard. Once it
opens setup, follow the same **Game folder → Your visuals → Review → Finished**
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
`dist/release-1.4.0/LauSetup.exe` and generating `app/translations.json`:

```powershell
python tools/package_universal.py --exe dist/release-1.4.0/LauSetup.exe --output dist/release-1.4.0/LauSetup.zip
```

For an isolated build, pass `--exe`, `--translations`, and
`--output`. The packager copies those input bytes exactly, accepts only the five
listed files, stamps ZIP metadata as Neil Mitchell, and gives the shell launcher
an executable Unix mode. It bundles no game payloads or Wine runtime.

Release evidence is recorded in [1.4.0 release notes](RELEASE-1.4.0.md) and
VALIDATION.json alongside the release downloads. Installer translations are
bundled and work offline. Full translated-document refresh has a separate
rate-limit follow-up; fluent human review remains the language-quality limit.
Game release 3.0.9 compacts six Patch-Y editions without Patch-Y DBC edits. The optional map component adds documented upstream table overrides; see DBC-CHANGELOG.md. Nine game locales remain supported.

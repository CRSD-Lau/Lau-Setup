# Lau Setup 1.2.0

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell

**[Download LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.2.0/LauSetup.zip)** for Windows or Linux/Wine. This is the only installer download. Setup downloads the game files needed for your choices.

You need an existing **WoW 3.3.5a game, build 12340**. The download is an upgrade, not a full game, language pack or HD model base.

## Start here on Windows

1. **Close WoW completely.**
2. Download **LauSetup.zip**, right-click it and choose **Extract All**. Open the extracted **LauSetup** folder.
3. Double-click **LauSetup.exe**. Its File Explorer type is **Application**. Keep the five extracted files together.
4. Click **Choose folder…** and select the game folder that directly contains **WoW.exe**, not its **Data** folder or your launcher folder.
5. **Enhanced Consecration** starts on for the custom appearance; turn it off for the original look. **New spell visuals** is available only when compatible HD models are detected. **Upgrade maps and minimap** is optional and adds a download.
6. Click **Install upgrade** and wait until it finishes. Start WoW and type **/pyversion**; it should show **3.0.8 Lau**.

If setup says **Already installed**, your selected files already match this release and no game update is needed. To update an older installation, use these same steps with the same game folder.

**If you get stuck:** open the extracted folder if you cannot find the app; choose the folder containing WoW.exe if setup rejects your selection; close the game if setup says it is running. Windows 10/11 requires .NET Framework 4.8: use the Microsoft download prompt if it is missing, then reopen setup. For other errors, [report the exact message and a screenshot](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose).

**To undo:** close WoW, reopen Lau Setup, choose the same folder and click **Restore previous install**. Keep **LauSetupBackups** in the game folder.

## Linux / Wine

Use the same ZIP with an existing supported Wine environment. Close every WoW instance across all prefixes, extract the ZIP and open a terminal in its **LauSetup** folder. Run as your normal user:

```bash
WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh
```

Replace the example path with the path to your existing Wine prefix. Once setup opens, follow Windows steps 4–6 above. Use **LauSetup.sh**, not the EXE directly: the launcher checks the Linux environment before starting setup.

You need Wine 11.0, Wine Mono 10.4.1, an existing 64-bit prefix, Python 3.9+, the documented fonts and supported local Linux storage. Korean and Chinese text requires Wine-visible Noto Sans CJK fonts. Setup does not install runtimes or fonts. Read the [Linux guide](https://github.com/CRSD-Lau/Lau-Setup/blob/main/wine/README.txt) before starting; Proton, Lutris and macOS integration are not included.

## What changed

- One shared ZIP contains the Windows executable, Linux/Wine launcher and bundled translations.
- Setup detects the Windows display language or Linux host language preferences. **Interface language** changes setup text immediately and remembers your manual choice. **Automatic** follows the system again.
- Ten interface languages: English, German, French, Spanish (Spain), Spanish (Mexico), Korean, Russian, Simplified Chinese, Traditional Chinese and Brazilian Portuguese.
- Interface language is separate from WoW's nine supported game locales. Portuguese interface text does not add Portuguese game data.
- Beginner instructions now lead the primary guides, with technical details below them. Current download guidance uses the shared ZIP throughout the repository, website and Discord.

**No DBC edits. Game release 3.0.8 and every game asset hash remain unchanged.** This is an installer release; existing game files do not need to change just to use the new setup interface.

## Other files on this release

You only need **LauSetup.zip** to install. **START-HERE.txt** is a separate copy of the beginner guide. **LauSetup-source-1.2.0.zip** is for developers. The **Patch-Y All-Editions ZIP** is an optional manual-install package. **SHA256SUMS.txt**, the detached game ZIP checksum and **VALIDATION.json** are verification information.

## Validation and translation notes

The exact checks and hashes are in **VALIDATION.json** and **SHA256SUMS.txt**. Coverage includes 62 Windows regression groups; 62 Wine groups across staged runs, including the affected GUI group and remaining checks rerun after the fix; 50 Windows and 21 normal-user Wine interface states; all 185 translation keys in ten languages; and 31 package, translation and host tests. Beginner documentation and the final packages were checked separately.

Translations are bundled; setup makes no translation-service requests. Current notices in all 117 translated guides and beginner steps in all 27 translated primary guides have been updated. A full refresh of older technical translation bodies remains pending because the external Google service returned HTTP 429. Fluent-reader corrections are welcome. These interface checks do not certify every Linux distribution or new in-game behavior.

[Website and help](https://wrath-multilingual-hd.vercel.app/) · [Community roadmap](https://github.com/users/CRSD-Lau/projects/2)

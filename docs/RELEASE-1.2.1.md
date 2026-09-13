# Lau Setup 1.2.1

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell

**[Download LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.2.1/LauSetup.zip)** for Windows or Linux/Wine. This is the only installer download. Setup downloads the game files needed for your choices.

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

- Fixes the false unsupported-layout rejection of large classic MPQ hash tables, including the 524,288-entry archive supplied by Andre. Tables now stream in bounded chunks instead of using an arbitrary entry-count cap.
- Preserves bounds, malformed-entry, cancellation, timeout and known-patch conflict checks.
- Clarifies the warning to **Possible extra upgrade patch** in all ten interface languages. A file with its original download name can trigger this warning too; it is separate from the large-table bug.
- Installer update only: all 28 game assets and their hashes are unchanged.

## Other files on this release

You only need **LauSetup.zip** to install. **START-HERE.txt** is a separate copy of the beginner guide. **LauSetup-source-1.2.1.zip** is for developers. The **Patch-Y All-Editions ZIP** is an optional manual-install package. **SHA256SUMS.txt**, the detached game ZIP checksum and **VALIDATION.json** are verification information.

## Validation and translation notes

Windows and Wine each passed 66 regression groups, including large tables, end-of-table markers and malformed bounds. All 185 translation keys across ten languages and 16 package/translation tests passed. Packaged interface checks are recorded in VALIDATION.json. The supplied archive passes the new reader; this does not certify every archive member or game encounter.

Translations are bundled; setup makes no translation-service requests. Current notices in all 117 translated guides and beginner steps in all 27 translated primary guides have been updated. A full refresh of older technical translation bodies remains pending because the external Google service returned HTTP 429. Fluent-reader corrections are welcome. These interface checks do not certify every Linux distribution or new in-game behavior.

[Website and help](https://wrath-multilingual-hd.vercel.app/) · [Community roadmap](https://github.com/users/CRSD-Lau/projects/2)

# Lau Setup 1.3.0

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

Extra upgrade files no longer require manual moving. Click **Install upgrade**: setup backs up recognized extra upgrade patches in **LauSetupBackups** and continues. **Restore previous install** puts them back.

## First time? Do this

1. Close World of Warcraft.
2. Download **LauSetup.zip**. Windows and Linux use the same ZIP.
3. Extract the whole ZIP. Keep all five files together in the LauSetup folder.
4. Windows: double-click **LauSetup.exe**. Linux with the supported Wine environment: run **LauSetup.sh**. See [Linux instructions](../wine/README.txt).
5. Click **Choose folder** and select your existing WoW 3.3.5a folder containing **WoW.exe**.
6. Choose the visuals you want and click **Install upgrade**. Wait for completion, then start the game normally.

You do not need the source ZIP, raw game patch ZIP, or checksum files for normal setup. Setup follows your system language; the language menu lets you change it.

## What happens to my files?

**Before Setup replaces or moves an existing game file, it preserves the original automatically.** Keep `LauSetupBackups` in your game folder; **Restore previous install** uses it to put the originals back. Unrelated files stay in place.

Most users do not need to rename patches. The supplied `WoW.exe` supports additional patch names, but Setup uses its standard Q/M/S/Y names. For example, if you renamed an identical `patch-y.mpq` to `patch-lau.mpq`, Setup recognizes the contents, backs up `patch-lau.mpq`, and installs the selected `patch-y.mpq`. Restore returns the backed-up file under its original name. A name change alone does not make it a different patch; support for additional names does not guarantee every custom name or loading order.

Recognized extra copies are moved into a verified backup, including files kept under their original download names. Your addons and personal settings stay in place. Keep **LauSetupBackups** in your selected game folder so Restore can work.

Unknown readable patches stay in place. Setup still stops if it cannot safely read an archive, if a protected stock archive contains conflicting content, or if files change during installation. Keep those files and [report the exact message](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose).

## Validation

Windows and normal-user Wine each passed 76 regression groups. The packaged interface passed 60 Windows previews and 28 Wine previews without text overflow. A real released Patch-Y file was automatically backed up and restored byte-for-byte while the supplied Patch-Armadura.mpq stayed unchanged. All 186 interface strings are present in ten languages. Release verification is recorded in the attached **VALIDATION.json**. Automated install and recovery tests use isolated clients; these checks do not replace in-game visual acceptance. See [scanner scope](MPQ-SCANNING.md).

## DBC changes

**No DBC edits.** Game release remains **3.0.8**. All 28 game asset entries, nine game locales and the raw game ZIP are unchanged. This is an installer release.

Full translated-document bodies remain pending the Google rate limit. All 117 translated snapshot notices now describe 1.3.0 and automatic backups; the existing six-hour follow-up will finish the full refresh.

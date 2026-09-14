<!-- LANGUAGES:START -->
[English](README.md) · [Deutsch](docs/i18n/de/README.md) · [Español (España)](docs/i18n/es-ES/README.md) · [Español (México)](docs/i18n/es-MX/README.md) · [Français](docs/i18n/fr/README.md) · [한국어](docs/i18n/ko/README.md) · [Русский](docs/i18n/ru/README.md) · [简体中文](docs/i18n/zh-CN/README.md) · [繁體中文](docs/i18n/zh-TW/README.md) · [Português (Brasil)](docs/i18n/pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

<p align="center">
  <a href="https://wrath-multilingual-hd.vercel.app/"><img src="docs/assets/social-preview.png" alt="Wrath HD — gold W shield on an icy blue background" width="100%" /></a>
</p>

<h1 align="center">Lau Setup</h1>
<p align="center"><strong>Your client. Your language. Your Wrath.</strong><br />The Windows and Linux/Wine installer for the Lau visual upgrade.</p>
<p align="center">
  <a href="https://github.com/CRSD-Lau/Lau-Setup/releases/latest">Latest release</a> ·
  <a href="https://wrath-multilingual-hd.vercel.app/">Website &amp; gallery</a> ·
  <a href="https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose">Report a problem</a> ·
  <a href="https://github.com/users/CRSD-Lau/projects/2">Community roadmap</a>
</p>

---

Multilingual spell text, widescreen loading artwork, custom ground indicators and optional HD maps for **WoW 3.3.5a, build 12340**. Choose your existing client and visuals; Lau Setup downloads the required files, verifies them, places the patches and backs up the originals.

**Installer 1.4.0 test candidate (not stable) · Game release 3.0.8 Lau · Ten interface languages · Nine game locales**

## Download and start here

**[Download LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)**. This is the one installer download for Windows and Linux/Wine.

### Windows

1. **Close WoW completely.**
2. Download **LauSetup.zip**, right-click it, choose **Extract All**, and open the extracted `LauSetup` folder.
3. Double-click `LauSetup.exe` (its File Explorer type is **Application**).
4. **Game folder:** select **Choose folder…**, choose the folder directly containing `WoW.exe`, then click **Next**.
5. **Your visuals:** the fixed **Patch-Y HD** or **Patch-Y Non-HD** selection matches your detected client. Extras start off: choose **Enhanced Consecration** for Lau’s ground effect, **New spell visuals** for upgraded spells (existing HD models required), and **Upgrade maps and minimap** for sharper maps. Existing map upgrades are kept. **Compatible WoW.exe + loading screens** is one optional checkbox, off by default; leave it off to keep both unchanged. Click **Next**.
6. **Review:** check **Your choices**—for example, **Patch-Y (Lau’s version) + Enhanced Consecration + New Spells + Map Upgrade**. The screen explicitly says **Install** or **Keep existing** for **WoW.exe** and **Patch-Q** artwork, and lists matching language patches, download size and automatic backups. Use **Back** to change choices.
7. Click **Install upgrade**, wait for **Finished**, then click **Finish**. Start WoW and type `/pyversion`; it should show **3.0.8 Lau**. If your selection is already installed, **Finish** closes setup without changing game files.

**Wrong interface language?** Use **Interface language** at the top of any step. The manual choice is remembered; **Automatic** follows your system again. It changes setup text only. **Next** does not download or change game files.

### Linux / Wine

Use the same ZIP, but first prepare an existing supported environment: Wine 11.0, Wine Mono 10.4.1, a 64-bit prefix, Python 3.9+, the documented fonts, and local Linux storage. Close every WoW instance in every prefix, extract the ZIP, then run this from the `LauSetup` folder:

```sh
WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh
```

Never start `LauSetup.exe` directly under Wine. When setup opens, use the same **Game folder → Your visuals → Review → Finished** steps above. For recovery, close WoW, choose the same game folder, and select **Restore previous install**.

## Common setup messages

Setup 1.4.0 also accepts game-language codes regardless of letter case (`enus`, `ENUS` and `enUS` all select enUS), without changing Config.wtf. The window shows both the installer version and game release.

**Patch-V:** Empty `Data\patch-v.mpq` files (any letter case) are backed up automatically. Recognized Lau upgrade copies are also backed up. An unidentified nonempty Patch-V stays in place with a compatibility warning; installation continues, even if the scanner cannot parse it. A filename alone cannot identify the unstable HD building patch because unrelated mods can also use V. **Restore previous install** returns backed-up files.


- **Cannot find `LauSetup.exe`** — extract the ZIP first, then open the extracted `LauSetup` folder. Its File Explorer type is **Application**.
- **Choose the folder containing `WoW.exe`** — choose the game folder itself, not `Data`, a launcher folder, a drive root, network share, or linked folder.
- **.NET Framework 4.8 is missing** — use the Microsoft runtime prompt, then reopen setup.
- **Missing matching language files** — use the client whose active game locale is fully installed. Changing a config value does not install a language pack.
- **WoW is running** — close it and retry. Under Wine, close every WoW instance in every prefix.
- **An interrupted install needs restoring first** — choose the same client folder, select **Restore previous install**, and keep `LauSetupBackups` in place.
- **A game file was changed by another update** — restore stops to preserve that file. Keep all files and backups, then [report the exact message, filename, and a screenshot](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose). Do not delete or force-replace files to bypass the check.
- **Other patches** — Setup leaves them alone. Renamed duplicate patches are your responsibility. Files Setup replaces are backed up in `LauSetupBackups`.
- **Cannot safely check patch** — first download the latest setup; 1.2.1 fixes the old large-table restriction. If it still stops, keep the named archive and your backups. [Report the exact message, filename, and a screenshot](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose); do not force-replace files to bypass the check.

For prior hotfix behavior and historical indicator changes, see the [changelog](CHANGELOG.md). Setup checks actual SHA-256 hashes; an older installer keeps its embedded catalog, so download and extract the current `LauSetup.zip` before updating.

## Package and requirements

**[Download LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)** once for Windows or Linux/Wine. Extract it intact: the `LauSetup/` folder contains the Windows executable, the Linux/Wine safety launcher, bundled translations, and its README.

| Windows | Linux / Wine |
| :--- | :--- |
| Open `LauSetup.exe` · Windows 10 / 11 · .NET Framework 4.8 | Run `LauSetup.sh` · Wine 11.0 · Wine Mono 10.4.1 · 64-bit prefix · Python 3.9+ |
| [Windows guide](START-HERE.txt) | [Wine guide and prerequisites](wine/README.txt) |

Game files download during setup. An English core installation is about **472 MB** with HD models and new spell visuals, or **259 MB** with original models. Optional maps add a larger download; setup shows the total before you install.

[SHA-256 checksums](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/SHA256SUMS.txt) · [Release notes](https://github.com/CRSD-Lau/Lau-Setup/releases/latest) · [Validation report](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/VALIDATION.json)

> **Bring your existing client.** This is an upgrade, not a full game client, language pack or HD model base. Runtime installers are not bundled. The installer interface has ten languages; game content supports nine unchanged locales.

## One setup. The details handled.

| Choose your visuals | Keep control of your installation |
| :--- | :--- |
| Enhanced or stock Consecration | Client language and model detection |
| New spell visuals for compatible HD clients | Only the required files downloaded |
| Optional HD maps and minimap textures | SHA-256 verification before installation |
| Regional widescreen loading artwork | Automatic backups and resumable downloads |
| Localized spell names, ranks and tooltips | Restore and interrupted-operation recovery |

<p align="center"><img src="docs/assets/installer-windows.png" alt="Lau Setup on Windows: choose a WoW folder, select visuals, install or restore" width="836" /></p>

Your addons, SavedVariables, fonts, login artwork, realm settings and unrelated patches stay in place. No personal UI, credentials or analytics are included.

## Ten interface languages; nine game locales

The installer interface automatically follows your Windows display language or Linux host locale. You can choose any interface language manually; the selection is saved, and **Automatic** follows the system again. This affects setup text only.

English (US) · Deutsch · Français · Español (España) · Español (México) · Português (Brasil) · 한국어 · Русский · 简体中文 · 繁體中文

Game locales (unchanged): English · Français · Deutsch · 한국어 · Русский · 简体中文 · 繁體中文 · Español (España) · Español (México)

`enUS` · `frFR` · `deDE` · `koKR` · `ruRU` · `zhCN` · `zhTW` · `esES` · `esMX`

Setup follows your client's active locale. Install the appropriate language files and fonts before changing the configuration. Changing a config value alone does not install a language pack.

## Your files are backed up automatically

**Before Setup replaces or moves an existing game file, it preserves the original automatically.** Keep `LauSetupBackups` in your game folder; **Restore previous install** uses it to put the originals back. Unrelated files stay in place.

Setup leaves unrelated MPQs alone and does not parse them for conflicts. If you rename patch-y.mpq to patch-lau.mpq, that copy stays in place; manage renamed duplicates yourself. Setup backs up files it replaces. Empty Data\patch-v.mpq is the only additional automatic cleanup; nonempty V stays with a warning.

## Restore with your backups

Close WoW, reopen setup through the same launcher, choose the same game folder, and select **Restore previous install**. Keep `LauSetupBackups` inside the client folder: it contains the originals and recovery records.

An interrupted install or restore can be recovered even if `WoW.exe` is temporarily missing. If another update changed the installed files, restore stops and preserves the backup for resolution. Once this installer adds the map upgrade, it retains it during edition changes; restore the previous installation to undo that upgrade.

## Tested, with clear limits

Setup 1.4.0 is in development: the wizard keeps 1.1.7-style handling of unrelated patches. See [current scope and validation](docs/RELEASE-1.4.0.md). Earlier release evidence below does not validate this candidate.

Setup 1.2.0 passed **62 regression groups on Windows and 62 on Wine**. Wine ran 35 groups before the busy-state completion fix, then the affected GUI group and the remaining 26 after it; final Wine localization and packaged-window checks also passed. The validation records 50 Windows and 21 normal-user Wine interface states, 185 keys across all ten bundled interface languages, and 31 package, translation, and host tests. Game release 3.0.8, its nine locales, 28 game assets, and DBC data are unchanged.

Wine was tested with **Wine 11.0 / Wine Mono 10.4.1** on local Linux storage, including the supplied launcher as a normal user. Halion meteor-fire geometry matches tester-approved v2 exactly. Coldflame, animation tracks, native fire and spell tables remain byte-identical to 3.0.7. Website animations are illustrative mockups. These tests do not certify every Linux distribution or in-game encounter.

Lutris, Proton and macOS integrations are outside this release. The executable is unsigned.

## Known limitations and feature requests

Read [Known limitations and assumptions](KNOWN-LIMITATIONS.md) before suggesting a feature: Warmane server control, DLL/native-code scope, protected Lua actions, indicator accuracy and timing, DBC dependencies, and platform/recovery limits.

## For contributors

- [Build, archive placement and recovery design](docs/TECHNICAL.md)
- [Contribution and bug-report guidance](CONTRIBUTING.md)
- [Implementation review](REVIEW.md)
- [Platform scope and feasibility](PLATFORM-FEASIBILITY.md)

Game payloads are distributed through GitHub Releases. This repository contains the installer source, catalog, launcher and documentation; you do not need to clone it to install the upgrade.

## Built on community work

**Andre** — Patch-Y baselines · **Loriendal & Trimitor** — HD client foundation · **Project Reforged contributors** — HD artwork · **Blizzard** — original game, artwork and localized text · **Lau** — ground indicators, compatibility, adaptations, testing and release tooling.

[Full credits](https://wrath-multilingual-hd.vercel.app/credits) · [Screenshots and installation help](https://wrath-multilingual-hd.vercel.app/)

<sub>Unofficial community project. Not affiliated with or endorsed by Blizzard Entertainment. Original game and third-party artwork remain the property of their respective owners.</sub>

## DBC change tracking

See the [DBC changelog](DBC-CHANGELOG.md) for individual table/record/field edits and comparison evidence. **3.0.7 → 3.0.8 had no DBC edits**: the 90° indicator update changed model geometry. Setup 1.1.5–1.1.8 also leave the DBC data unchanged.

Maps and loading screens are independent options. Maps include Lau’s maps/minimaps plus Trimitor WDM dungeon, raid and cave maps and their required support addons. Selected map-support files are backed up before replacement; personal settings and unrelated addons remain untouched.
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

**Installer 1.2.0 · Game release 3.0.8 Lau · Ten interface languages · Nine game locales**

## Download and start here

**[Download LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)**. This is the one installer download for Windows and Linux/Wine.

### Windows

1. **Close WoW completely.** Right-click `LauSetup.zip`, choose **Extract All**, and open the extracted `LauSetup` folder.
2. Double-click `LauSetup.exe` (its File Explorer type is **Application**).
3. Select **Choose folder…**, then choose the game folder that directly contains `WoW.exe`—not its `Data` folder or a launcher folder.
4. **Enhanced Consecration** starts on; **New spell visuals** needs detected compatible HD models; **Upgrade maps and minimap** is optional. Select **Install upgrade** and wait for completion.
5. If setup says **Already installed**, the selected files already match this release and no game update is needed. Otherwise start WoW and type `/pyversion`.

### Linux / Wine

Use the same ZIP, but first prepare an existing supported environment: Wine 11.0, Wine Mono 10.4.1, a 64-bit prefix, Python 3.9+, the documented fonts, and local Linux storage. Close every WoW instance in every prefix, extract the ZIP, then run this from the `LauSetup` folder:

```sh
WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh
```

Never start `LauSetup.exe` directly under Wine. When setup opens, use the same **Choose folder…**, options, and **Install upgrade** steps above. For recovery, close WoW, choose the same game folder, and select **Restore previous install**.

**Stuck?** Extract the ZIP before looking for `LauSetup.exe`; select the folder that contains `WoW.exe` directly; close WoW if setup says it is running; and use the Microsoft .NET Framework 4.8 prompt if Windows reports that runtime is missing.

## Renamed-patch checks

Setup 1.1.8 Hotfix checks active root and client-locale MPQs for renamed Patch-Y markers and exact copies of catalog patches before downloading and again before installation. A possible conflict or unreadable/unsupported archive stops installation with its filename; setup does not delete it. Keep a backup and resolve the named archive outside Data before retrying. Expected Q/M/S/Y placements and disabled files are excluded. Game files remain 3.0.8; no DBC edits.

The supplied executable retains the inspected Billy patch-naming implementation. Setup still manages its own Q/M/S/Y at fixed names; do not rename those files.

## Patch-S stays recoverable

**Setup 1.1.7 Hotfix:** re-enabling New spell visuals reuses a matching disabled Patch-S and moves the plain disabled copy into `LauSetupBackups`, so Data does not retain an active/disabled duplicate. Different copies are preserved in the transaction backup. Switching off still uses `.mpq.disabled`. Use **Restore previous install** for recovery.

## 90° breath and Slime Spray warnings

**3.0.8 Lau:** all supported breath indicators and Rotface Slime Spray are **90° total**, following Warmane tester confirmation. Covers Halion in both realms, Saviana Ragefire, Sartharion, ICC Rimefang and Sindragosa. Range and animation timing are preserved. The approved larger Halion meteor-fire radius and light blue Coldflame are unchanged.

**Already installed?** Download **LauSetup.zip** first, extract it, select the same folder and visuals, then install. Setup checks actual SHA-256 hashes: even a one-byte change with the same size and timestamp is detected. Only matching new files count as already installed. `/pyversion` reports **3.0.8 Lau**. Older installers keep their embedded catalog.

[Animated color previews and changelog](https://wrath-multilingual-hd.vercel.app/#changelog)

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

## Restore with your backups

Close WoW, reopen setup through the same launcher, choose the same game folder, and select **Restore previous install**. Keep `LauSetupBackups` inside the client folder: it contains the originals and recovery records.

An interrupted install or restore can be recovered even if `WoW.exe` is temporarily missing. If another update changed the installed files, restore stops and preserves the backup for resolution. Once this installer adds the map upgrade, it retains it during edition changes; restore the previous installation to undo that upgrade.

## Tested, with clear limits

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

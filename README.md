<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

<p align="center">
  <a href="https://wrath-multilingual-hd.vercel.app/"><img src="docs/assets/social-preview.png" alt="Wrath HD — gold W shield on an icy blue background" width="100%" /></a>
</p>

<h1 align="center">Lau Setup</h1>
<p align="center"><strong>Your client. Your language. Your Wrath.</strong><br />The Windows and Linux/Wine installer for the Lau visual upgrade.</p>
<p align="center">
  <a href="https://github.com/CRSD-Lau/Lau-Setup/releases/latest">Latest release</a> ·
  <a href="https://wrath-multilingual-hd.vercel.app/">Website &amp; gallery</a> ·
  <a href="https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose">Report a problem</a>
</p>

---

Multilingual spell text, widescreen loading artwork, custom ground indicators and optional HD maps for **WoW 3.3.5a, build 12340**. Choose your existing client and visuals; Lau Setup downloads the required files, verifies them, places the patches and backs up the originals.

**Installer 1.1.6 · Game release 3.0.8 Lau · Nine client languages**

## Patch-S stays recoverable

**Setup 1.1.6 Hotfix:** turning off New spell visuals keeps Patch-S as `.mpq.disabled` beside its original path. The current file always receives the plain .mpq.disabled name; any older disabled copy is preserved under a short hash-suffixed name. Older installations can recover Patch-S through **Restore previous install**.

## 90° breath and Slime Spray warnings

**3.0.8 Lau:** all supported breath indicators and Rotface Slime Spray are **90° total**, following Warmane tester confirmation. Covers Halion in both realms, Saviana Ragefire, Sartharion, ICC Rimefang and Sindragosa. Range and animation timing are preserved. The approved larger Halion meteor-fire radius and light blue Coldflame are unchanged.

**Already installed?** Download **Setup 1.1.6** first, select the same folder and visuals, then install. Setup checks actual SHA-256 hashes: even a one-byte change with the same size and timestamp is detected. Only matching new files count as already installed. `/pyversion` reports **3.0.8 Lau**. Old installers keep their old embedded catalog.

[Animated color previews and changelog](https://wrath-multilingual-hd.vercel.app/#changelog)

## Download

| Windows | Linux / Wine |
| :--- | :--- |
| **[Download LauSetup.exe](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.exe)** | **[Download LauSetup-Wine.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup-Wine.zip)** |
| Windows 10 / 11 · .NET Framework 4.8 | Wine 11.0 · Wine Mono 10.4.1 · 64-bit prefix |
| About **156 KB** | About **80 KB** · Python 3.9+ |
| [Windows guide](START-HERE.txt) | [Wine guide and prerequisites](wine/README.txt) |

Game files download during setup. An English core installation is about **472 MB** with HD models and new spell visuals, or **259 MB** with original models. Optional maps add a larger download; setup shows the total before you install.

[SHA-256 checksums](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/SHA256SUMS.txt) · [Release notes](https://github.com/CRSD-Lau/Lau-Setup/releases/latest) · [Validation report](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/VALIDATION.json)

> **Bring your existing client.** This is an upgrade, not a full game client, language pack or HD model base. Runtime installers are not bundled. The installer UI is English; game content supports nine locales.

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

## Get started

1. **Close WoW completely.** On Wine, close every WoW instance across all prefixes.
2. **Launch setup and choose your client folder.** Windows: open `LauSetup.exe`. Linux: extract all four files from the Wine ZIP and use the launcher below.
3. **Choose your visuals and install.** Enhanced Consecration starts checked; uncheck it for the stock appearance. New spell visuals require a compatible HD model base. Maps are optional.
4. **Launch WoW and run `/pyversion`.** Confirm the installed edition before heading into game.

On Linux, run this from the extracted folder with your existing prefix:

```sh
WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh
```

Use the launcher as your normal user. It checks Linux paths, running games, free space and installer locks across prefixes. Use local Linux storage; linked folders, network shares and Windows-mounted drives are unsupported. The [Wine guide](wine/README.txt) lists fonts and all prerequisites.

On Windows, setup offers Microsoft's official .NET Framework 4.8 download page if the runtime is missing. The tested Wine configuration uses **Wine Mono**, not the Windows .NET installer.

## Nine client languages

English · Français · Deutsch · 한국어 · Русский · 简体中文 · 繁體中文 · Español (España) · Español (México)

`enUS` · `frFR` · `deDE` · `koKR` · `ruRU` · `zhCN` · `zhTW` · `esES` · `esMX`

Setup follows your client's active locale. Install the appropriate language files and fonts before changing the configuration. Changing a config value alone does not install a language pack.

## Restore with your backups

Close WoW, reopen setup through the same launcher, choose the same client and select **Restore previous install**. Keep `LauSetupBackups` inside the client folder: it contains the originals and recovery records.

An interrupted install or restore can be recovered even if `WoW.exe` is temporarily missing. If another update changed the installed files, restore stops and preserves the backup for resolution. Once this installer adds the map upgrade, it retains it during edition changes; restore the previous installation to undo that upgrade.

## Tested, with clear limits

Release 1.1.6 passed **46 regression groups on Windows and on Wine**, including 108 locale/edition/map plans per platform. Game-release 3.0.8 previously passed six-edition upgrades and one-byte detection on both platforms; its payloads are unchanged. Setup 1.1.6 also covers the all-flags-on to New Spells off sequence with older disabled copies, repeated switches and exact rollback. Public payloads were downloaded anonymously and hash-verified; actual core installation and rollback were tested.

Wine was tested with **Wine 11.0 / Wine Mono 10.4.1** on local Linux storage, including the supplied launcher as a normal user. Halion meteor-fire geometry matches tester-approved v2 exactly. Coldflame, animation tracks, native fire and spell tables remain byte-identical to 3.0.7. Website animations are illustrative mockups. These tests do not certify every Linux distribution or in-game encounter.

Lutris, Proton and macOS integrations are outside this release. The executable is unsigned.

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

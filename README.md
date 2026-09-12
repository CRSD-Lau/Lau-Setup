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

**Installer 1.1.1 · Game release 3.0.5 Lau · Nine client languages**

## Updated cone warnings

Game release **3.0.5 Lau** widens Sindragosa from **75° to 90° total** and Rotface from **25° to 60° total** in all six editions. These are buffered visual warnings informed by Warmane footage and logs; server mechanics are unchanged.

**Updating from 3.0.4?** Download the new EXE or Wine ZIP first, choose the same client and visuals, then install. Setup checks actual file hashes, updates the older patches and reports `/pyversion` as 3.0.5. Older downloaded installers retain their older embedded catalog. [Changelog](https://wrath-multilingual-hd.vercel.app/#changelog).

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

Release 1.1.1 passed **38 Windows regression groups**, including 108 locale/edition/map plans. All six editions passed actual **3.0.4-to-3.0.5 upgrade, repeat-install and exact rollback** checks. New payloads were downloaded anonymously and hash-verified; a core installation from GitHub and rollback also passed.

The Wine launcher is unchanged and its ZIP contains the same rebuilt EXE. **Wine runtime evidence comes from 1.1.0** (Wine 11.0 / Mono 10.4.1, 38 groups and native safety checks); fresh Wine execution was unavailable for this update. Earlier game checks cover preserved files. The new cone geometry is statically verified and deliberately buffered, not newly certified against server damage boundaries.

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

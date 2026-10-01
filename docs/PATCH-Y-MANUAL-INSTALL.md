# Install Patch-Y without Lau Setup

Author: Neil Mitchell  
Creator: Neil Mitchell  
Last Modified By: Neil Mitchell

Download one manual ZIP from the [Patch-Y 3.1.0 release](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/payload-3.1.0). No installer is required. These are the same MPQ bytes used by Lau Setup 1.5.0.

| Your existing client | Download |
| --- | --- |
| HD model pack, upgraded spell visuals | [HD — New spell visuals](https://github.com/CRSD-Lau/Lau-Setup/releases/download/payload-3.1.0/Patch-Y-3.1.0-HD-New-Spells.zip) |
| HD model pack, original spell visuals | [HD — Original spell visuals](https://github.com/CRSD-Lau/Lau-Setup/releases/download/payload-3.1.0/Patch-Y-3.1.0-HD-Original-Spells.zip) |
| Original models / Non-HD / SD | [Non-HD / SD](https://github.com/CRSD-Lau/Lau-Setup/releases/download/payload-3.1.0/Patch-Y-3.1.0-Non-HD.zip) |

All three include Lau's enhanced Consecration. The New spell visuals ZIP also includes both required Patch-S companions. The ZIPs do not include an HD model pack, game executable, loading screens, maps, addons or an entire game client.

## Before copying

Use a complete WoW 3.3.5a client, build 12340. HD editions require the existing matching model pair `Data/patch-f.mpq` and `Data/<locale>/patch-<locale>-F.MPQ`; use Non-HD for original models. Keep your existing compatible executable. These ZIPs do not convert another client version or add support for a different server.

1. Close WoW and extract the ZIP into a temporary folder **outside your game folder**.
2. Find your active client locale in `WTF/Config.wtf` (`SET locale`), and confirm the matching `Data/<locale>/locale-<locale>.mpq` exists. For an English US client, the locale is `enUS`.
3. Back up the exact files you will replace to a folder **outside `Data`**, keeping their paths. Preserve any previous `LauSetupBackups`. Resolve any known renamed copies of old Patch-Y before installing, so they do not override the new files. Do not remove unrelated patches.

## Copy the files

For **every edition**, make two copies of the ZIP's `patch-y.mpq`:

| Source | Destination in your game folder |
| --- | --- |
| `patch-y.mpq` | `Data/patch-y.mpq` |
| The same `patch-y.mpq`, renamed for your locale | `Data/<locale>/patch-<locale>-Y.MPQ` |

For example, English US uses `Data/patch-y.mpq` **and** `Data/enUS/patch-enUS-Y.MPQ`. Both files must contain the same bytes. Enable file extensions in your file manager before renaming.

For **HD — New spell visuals**, also copy:

| Source | Destination in your game folder |
| --- | --- |
| `patch-s.mpq` | `Data/patch-s.mpq` |
| `patch-LOCALE-S.MPQ`, renamed for your locale | `Data/<locale>/patch-<locale>-S.MPQ` |

For **HD — Original spell visuals** or **Non-HD / SD**, disable the previous new-spells pair if present: back up and move the known `Data/patch-s.mpq` and `Data/<locale>/patch-<locale>-S.MPQ` outside `Data`. Do not remove the HD Patch-F model files from an HD client. If these filenames contain other custom work, resolve that combination before replacing them.

Only change the active locale folder. Supported client locale names are `deDE`, `enGB`, `enUS`, `esES`, `esMX`, `frFR`, `itIT`, `koKR`, `ptBR`, `ruRU`, `zhCN`, and `zhTW`. Patch-Y contains nine localized text sets; `enGB`, `itIT`, and `ptBR` use the existing English visual-text fallback. Do not change your client language just to install the patch.

## Check and restore

Start WoW and confirm `/pyversion` reports **3.1.0 Lau**. Verify the edition in game. Packaging does not add new gameplay acceptance: the existing release's edition/encounter limits still apply. To undo a manual installation, close WoW and restore the exact files from your manual backup; remove only files newly added by this manual installation.

The release supplies [ZIP checksums](https://github.com/CRSD-Lau/Lau-Setup/releases/download/payload-3.1.0/SHA256SUMS-Patch-Y.txt). Each ZIP also contains a manifest describing MPQ hashes and installation paths. On Windows, `Get-FileHash -Algorithm SHA256 'C:\path\to\download.zip'` reports a ZIP's checksum.

## Credits

Andre and the Patch-Y community; Loriendal and Trimitor's HD client foundation; Project Reforged contributors; Blizzard's original game, assets and localized text; Suppository and the contributors credited in the adopted visual source; and Lau / Lausudo (Neil Mitchell) for the documented adaptations, integration, testing and packaging. See the [full edit and attribution breakdown](../MPQ-EDIT-BREAKDOWN.md).

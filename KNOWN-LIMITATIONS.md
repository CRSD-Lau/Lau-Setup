# Known limitations and assumptions

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

[Back to Lau Setup](README.md) · [Recommendations and feature requests](https://github.com/CRSD-Lau/Lau-Setup/discussions/1) · [DBC change history](DBC-CHANGELOG.md)

Read this before proposing a feature. Lau Setup installs a client-side visual upgrade for **WoW 3.3.5a build 12340**. It is not a server modification framework. The boundaries below describe the current project; outside scope does not necessarily mean technically impossible.

> **Need installation help?** Use [Start here](START-HERE.txt) before relying on these technical limits.

## What we can and cannot change

| Request | Current boundary |
| --- | --- |
| Improve supported ground indicators, textures, models or localized client tables | Within scope, subject to file dependencies and testing. A visual improvement must not be described as a change to server damage or mechanics. |
| Improve installation, backups, accessibility or documentation | Within scope. Preserve unrelated files and verify installation and recovery. |
| Change Warmane damage, hit detection, ability duration, targeting or encounter scripts | Outside our control. Warmane runs its own server code; this project has no access to change or deploy that code. An MPQ or addon cannot make the server adopt different mechanics. |
| Add custom C++ code to Warmane's core | Not something this release can deliver. Changes to a separately controlled test server do not change Warmane. |
| Inject a DLL, hook the client or add new native engine behavior | Outside the supported patch/addon workflow. This requires a separate engineering and compatibility investigation, not just a DBC edit. No DLL injection framework or general client-hook support is provided. |
| Unlock protected Lua actions or missing game APIs | Not a supported feature. Editable addon Lua and protected client actions are different things. Rewriting Lua does not itself grant permissions or create an API the client does not expose. Report the exact action/API before assuming a workaround exists. |
| Supply a full client, another language pack or an HD model base | Not included. Bring an existing compatible client with the required language files, fonts and model configuration. |

The compatible `WoW.exe` supplied by setup has a specific role in the approved loading renderer, archive capacity and large-address support. Its inclusion is **not** a promise of arbitrary executable or DLL modifications. Likewise, not every Lua file is protected or uneditable: ordinary addon and UI changes can be feasible within the client's supported behavior.

## Indicators are visual guidance

- **Warmane is the runtime reference for Warmane reports.** AzerothCore and isolated clients help check file integrity and behavior in those environments. They cannot prove Warmane's custom hit detection, timing or encounter behavior.
- **A drawn edge is not a guaranteed safe boundary.** The supported breaths and Slime Spray use 90° total cones following tester feedback. Halion meteor-fire uses the accepted test-v2 enlargement. These are visual warnings based on observations, not measurements from Warmane's server source.
- **Terrain can clip flat indicators.** A flat ground mesh can intersect slopes, steps and uneven surfaces. Enlarging or raising it does not guarantee terrain-following projection everywhere.
- **Effect lifetime needs encounter evidence.** Pursuit/ghost feedback has included effects disappearing after one or two seconds. Changing a texture, shape or looping animation alone does not prove that the client will keep the effect instance alive for the full pursuit. A timing fix needs footage and event evidence for that specific ability; do not treat a mockup or experimental build as a confirmed fix.
- **Mockups are illustrative.** Website/chat animations demonstrate appearance. They are not recordings or proof of in-game rendering, duration or coverage.

For boundary or timing reports, include the encounter, ability, difficulty, client edition, `/pyversion`, and a clip showing the lead-up and damage or effect ending. Screenshots are useful, but perspective and overlapping effects limit exact radius measurements.

## DBC and patch compatibility

DBC tables are connected data, not independent switches. Adding a visual can require matching spell, visual, kit, effect and model references. Replacing a complete table can also replace its localized text and conflict with another patch supplying the same table.

The localization dependency was a real issue during this project's development. Andre and Lau worked through it together. The [historical DBC audit](DBC-CHANGELOG.md) separates the reported development timeline from retained archive evidence: Andre's baseline omitted `Spell.dbc`, not every DBC. Do not assume that copying an English table into another locale is safe.

- Use the edition matching your current HD/original-model configuration. New spell visuals require the compatible HD dependencies; detection does not certify every third-party model pack.
- If you remove or disable the HD model patches after installation, rerun the latest setup for the resulting configuration. An installed HD edition does not dynamically convert itself. Mismatched assets may produce missing or incorrect visuals and can require investigation of crashes; neither a crash nor crash-free behavior is guaranteed.
- Root and active-locale placements have distinct roles. In particular, the two S archives are different. Follow the [placement guide](docs/TECHNICAL.md#file-placement), not a generic instruction to duplicate every MPQ.
- Unrelated patches are preserved, but preservation is not a compatibility guarantee. Another archive overriding the same data can change the result.
- Game content supports nine locales. The installer interface supports ten languages, follows the system in Automatic mode, and saves a manual selection. Changing `Config.wtf` alone does not install another game language's files or fonts.

## Installer and recovery assumptions

Close WoW fully before installation or restore. Use the exact intended client folder and keep `LauSetupBackups` intact.

Setup compares actual file hashes with its **embedded catalog**. A one-byte change can be detected even when size and timestamp match, but an old installer still knows only its old catalog. Download the latest installer when upgrading. Setup does not continuously monitor a client after it exits or automatically reconcile later manual patch changes.

Turning New spell visuals off preserves the scoped S files as `.mpq.disabled`. Re-enabling uses matching disabled bytes when available and moves the plain disabled copy into the verified transaction backup. Older hash-suffixed copies are retained. See the [current recovery implementation](docs/TECHNICAL.md#setup-117-re-enable-cleanup).

**Before Setup replaces or moves an existing game file, it preserves the original automatically.** Keep `LauSetupBackups` in your game folder; **Restore previous install** uses it to put the originals back. Unrelated files stay in place.

Restore depends on the backups and recovery records. It stops when later changes make automatic restoration unsafe. It cannot promise recovery of files whose only backup was deleted. Removing Patch-Y alone is not a full rollback of the executable and other patches installed by setup. Use **Restore previous install** for the managed transaction.

## Platform and validation limits

The documented Windows target is Windows 10/11 with .NET Framework 4.8. The tested Linux configuration uses Wine 11.0, Wine Mono 10.4.1, an existing 64-bit prefix and Python 3.9+. Runtime installers are not bundled. Follow the [Wine prerequisites](wine/README.txt); use local Linux storage. Linked folders, network shares and Windows-mounted drives are outside the supported Wine path configuration.

Lutris, Proton, Steam Deck-specific integration and macOS are not supported integration targets in this release. This does not assert that every other environment is impossible; it means we have not established support for it. Windows packages are unsigned.

Builds, hash checks, installer regression tests, Wine tests and in-game testing answer different questions. Passing one does not replace the others. Visual checks are sampled, not certification of every zone, encounter, display scale, Linux distribution or third-party client modification. Consult each release's validation report for what was actually checked.

## Before requesting a feature

Describe the player-visible problem, your setup and the evidence. Proposals within the supported scope are welcome in [Ideas](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas); reproducible defects belong in [Issues](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose).

For DLL, native-code, protected-action or server-dependent proposals, identify the dependency explicitly. They need feasibility work and appropriate control of the affected system before implementation can be promised. Please do not file them as simple missing DBC options.


## Setup 1.1.8 overlap detection

The scanner reads classic MPQ version 0/1 headers and hash tables without extraction or native DLL loading. Known Patch-Y member-name combinations detect renamed copies even without a listfile. Exact current-catalog Q/M/S/Y copies are also detected by size and SHA-256. Modified Q/M/S files and unknown renamed members can evade these checks; this is not a universal conflict detector or proof of archive loading priority.

Scans cover root Data and the active locale only. Expected managed paths and filenames not ending in .mpq are excluded. Limits are 2,048 candidate archives and a one-minute cooperative time budget (individual storage calls can take longer). Setup 1.2.1 streams hash tables in 64 KiB chunks without the old entry-count cap, while checking table bounds and every member index. Unsupported, malformed or inaccessible candidate archives stop the install for review. Setup 1.3.0 moves recognized extra upgrade archives into verified backups; Restore previous install returns them. Unknown readable archives stay in place. Protected stock archives and unreadable files are not moved automatically. Separate HDD and broad filesystem benchmarks remain future work.


Setup 1.4.0 also accepts game-language codes regardless of letter case (`enus`, `ENUS` and `enUS` all select enUS), without changing Config.wtf. The window shows both the installer version and game release.

**Old Patch-V present?** Install normally. Setup automatically moves `Data\patch-v.mpq` (any letter case), the retired HD beta building patch, into its verified `LauSetupBackups` transaction. This includes empty leftover files. You do not need to rename, delete or move it yourself. **Restore previous install** puts the original file back. Other unrecognized archives retain their existing checks; this is not a promise that every custom patch is compatible.

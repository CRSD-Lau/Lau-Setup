# Lau Setup 1.5.0 / Patch-Y 3.1.0

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

This release brings Neil's raid-tested Patch-Y into the HD new-spells, HD original-spells and SD editions. Consecration is included by default. It also adds the adopted Coldflame, Swarming Shadows, Meteor Strike trails and selected Trial of the Crusader effects.

The optional **Compatible WoW.exe + loading screens** choice adds 77 newly reviewed HD 16:9 loading backgrounds. Neil approved the pack after representative in-game testing at 16:9. Eight catalog backgrounds keep their original artwork and can retain side bars: Black Temple, Eastern Kingdoms, Kalimdor, Outland, PvP Battleground, generic Raid, Ruined City and Sunwell. The new images are 1672×940 or 1672×941 source artwork, not native 4K. The other 77 compositions retain their original subjects and framing while extending the scenery to 16:9. [Loading-pack detail and evidence](LOADING-HD16X9-PACK.md).

The optional map package resolves competing WorldMapArea tables behind the Caverns of Time fallback. It retains all existing Lau map records. Setup recognizes the previous map package and includes it in the update.

The installer explains rejected folders, offers another folder selection, and copies a redacted support report on request. Review distinguishes current files, fresh installation and files needing an update or repair. It links to [contributor examples in the HD Discord](https://discord.com/channels/858041817043042364/1352616642491842580).

Andre's supplied Halion skin restores tank-positioning material batches while preserving the model and breath cone. The restored marks have archive and material-batch checks; targeted in-game confirmation has not been recorded.

## DBC changes

This is a DBC-changing release. Four Patch-Y tables change: Spell, SpellVisual, SpellVisualKit and SpellVisualEffectName. Existing spell routes are changed for the named abilities, new effect/kit records are added, and Slime Pool gets a dedicated visual cloned from 118 so unrelated spells retain their existing behavior. Consecration uses the accepted custom model and scale.

The root map WorldMapArea table gains 53 cave records while all 159 existing records remain unchanged. Duplicate WorldMapArea members are removed from all nine locale-T map archives. The Halion skin restoration itself has no DBC edits.

The optional loading pack changes `LoadingScreens.HasWideScreen` (zero-based field 3) from 0 to 1 on 61 of 92 rows. IDs, paths, strings and all other fields are preserved; rows for the eight original exceptions are unchanged. [Exact row IDs and Q archive hashes](dbc/loading-3.1.0.json).

[Record/field history and reasons](../DBC-CHANGELOG.md) · [Six 3.0.9 edition comparisons](dbc/raid-visuals-3.1.0-candidate.json) · [Map rows and hashes](dbc/caverns-3.1.0-candidate.json).

## Credits and readiness

**Neil Mitchell / Lau / Lausudo**: Lau edits, integration, HD/SD adaptations, loading-art adaptation, installer improvements, packaging and validation. **Suppository and the contributors listed in the source patch**: adopted visual sources. **Andre**: the supplied Halion mark restoration. Existing community credits remain intact. [Source visual examples](https://discord.com/channels/858041817043042364/1352616642491842580) require Discord access.

Windows and isolated Docker/Wine automated validation passed. Docker covered 94 Linux tests, 60 interface renders, and six real-payload install/repair/restore cases on Wine 9.0 and 11.0 with Mono 10.4.1. Neil accepted the 77-image pack after representative in-game testing at 16:9 and confirmed the Caverns map correction. The eight original loading screens and the untested raid visual combinations remain explicit limits. Discord examples remain uninspected. [Docker validation](DOCKER-VALIDATION-1.5.0-CANDIDATE.json) · [Full scope, credits and remaining checks](RAID-VISUAL-RELEASE.md).

Download and extract the complete [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip). This is the small online installer; the separate [game 3.1.0 payload release](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/payload-3.1.0) carries the files Setup downloads. Close WoW, select the folder containing `WoW.exe`, review your optional choices, install, and confirm `/pyversion` shows **3.1.0 Lau**. Keep `LauSetupBackups` for **Restore previous install**. Windows opens `LauSetup.exe`; Linux/Wine uses the included launcher and its documented prerequisites.

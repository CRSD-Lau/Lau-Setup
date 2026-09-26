# Lau Setup 1.5.0 / Patch-Y 3.1.0 candidate

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

This local candidate brings Neil's raid-tested Patch-Y into the HD new-spells, HD original-spells and SD editions. Consecration is included by default. It also adds the imported Coldflame, Swarming Shadows, Meteor Strike trails and selected Trial of the Crusader effects.

The optional map package resolves competing WorldMapArea tables behind the Caverns of Time fallback. It retains all existing Lau map records. Setup recognizes the previous map package and includes it in the update.

The installer explains rejected folders, offers another folder selection, and copies a redacted support report on request. Review distinguishes current files, fresh installation and files needing an update or repair. It links to [contributor examples in the HD Discord](https://discord.com/channels/858041817043042364/1352616642491842580).

Andre's supplied Halion skin restores tank-positioning material batches while preserving the model and breath cone. In-game placement remains a release gate.

## DBC changes

This is a DBC-changing release. Four Patch-Y tables change: Spell, SpellVisual, SpellVisualKit and SpellVisualEffectName. Existing spell routes are changed for the named abilities, new effect/kit records are added, and Slime Pool gets a dedicated visual cloned from 118 so unrelated spells retain their existing behavior. Consecration uses the accepted custom model and scale.

The root map WorldMapArea table gains 53 cave records while all 159 existing records remain unchanged. Duplicate WorldMapArea members are removed from all nine locale-T map archives. The Halion skin restoration itself has no DBC edits.

[Record/field history and reasons](../DBC-CHANGELOG.md) · [Six old-edition comparisons](dbc/raid-visuals-3.1.0-candidate.json) · [Map rows and hashes](dbc/caverns-3.1.0-candidate.json).

## Credits and readiness

**Neil Mitchell / Lau / Lausudo**: Lau edits, integration, HD/SD adaptations, installer improvements, packaging and validation. **Suppository and his listed contributors**: imported visual sources. **Andre**: the supplied Halion mark restoration. Existing community credits remain intact.

This candidate is not the published stable download. Publication awaits the recorded in-game and platform validation gates. [Full scope, credits and remaining checks](RAID-VISUAL-RELEASE.md).

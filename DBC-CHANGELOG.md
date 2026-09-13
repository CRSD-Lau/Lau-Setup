# DBC changelog

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

Track client DBC edits separately from model, texture and installer changes. Game versions and installer versions are separate: `/pyversion` reports the game edition.

## 3.0.7 → 3.0.8 — no DBC edits

Released with [Setup 1.1.4](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.1.4). All **42 DBC comparisons passed byte-for-byte**: seven tables in each of the six Patch-Y editions. There are no added/deleted tables, changed records, changed fields, or changed string blocks.

| Table | Record edits | Field edits | Result |
| --- | ---: | ---: | --- |
| CreatureDisplayInfo.dbc | 0 | 0 | Identical |
| CreatureModelData.dbc | 0 | 0 | Identical |
| Spell.dbc | 0 | 0 | Identical |
| SpellVisual.dbc | 0 | 0 | Identical |
| SpellVisualEffectName.dbc | 0 | 0 | Identical |
| SpellVisualKit.dbc | 0 | 0 | Identical |
| SpellVisualKitModelAttach.dbc | 0 | 0 | Identical |

[Full comparison evidence](docs/dbc/3.0.7-to-3.0.8.json) records each edition's source/destination MPQ SHA-256, each DBC's before/after SHA-256, size, row count and field count. The MPQ hashes were checked against the release catalogs. The other 22 catalog assets, including locale Q and shared S assets, are unchanged.

### What actually changed in 3.0.8

Five existing cone models were widened to **90° total** by editing their `.m2` geometry and corresponding `00.skin` bounds. Existing DBC bindings were retained.

| Model stem | Previous angle | New angle |
| --- | ---: | ---: |
| PW_Rotface_SlimeSpray_Fan25_Room | 60° | 90° |
| PW_White_Fan60_60yd_Glowing | 60° | 90° |
| PW_White_Fan60_30yd_Glowing | 60° | 90° |
| PW_White_Fan60_100y_Glowing | 60° | 90° |
| PW_White_Fan82_60yd_Glowing | 82° | 90° |

Filenames retain historical angle labels; the geometry determines the displayed angle. Sindragosa was already 90° and did not change in this transition. This brought all supported breath and Slime Spray indicators to 90°. Range and animation timing were unchanged. Halion meteor-fire radius, Coldflame colors and Consecration were unchanged.

Each edition changed exactly **11 archive members**: five `.m2` files, five `.skin` files and the `!pyandre.toc` game-version label from 3.0.7 to 3.0.8. Every other listed content member is identical. MPQ container bookkeeping is outside the content-member comparison.

This verifies client file changes, not Warmane's server mechanics or an exact damage boundary.

## Setup 1.1.5, 1.1.6 and 1.1.7 — no DBC edits

These are installer hotfixes. Their game payloads remain 3.0.8, with unchanged DBC data. The latest hotfix changes Patch-S installation, preservation and reuse, not its internal DBC contents.

## Required entry for future releases

Every release must add an entry here and a **DBC changes** section to its GitHub release notes, including installer-only releases. Explicitly state **No DBC edits** when applicable. Compare against the preceding stable game release, not an unpublished test build. Do not describe a model/texture edit as a DBC edit.

For each actual DBC edit, record one row per field (or a linked machine-readable row-level diff for large localization changes):

| Game transition | Table | Record ID | Field name / zero-based index | Old value | New value | Editions / locales | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VERSION → VERSION | TABLE.dbc | ID | Named field [index] | Previous value | New value | Affected variants | Purpose |

Also record added/deleted records and tables, schema changes, and string-value edits. Decode string values rather than reporting string-block offset churn as content changes. Specify field-index convention and schema source; label unknown fields rather than guessing. Attach before/after archive and table hashes, the comparison method, and validation limits. Never claim a comparison passed without evidence.

Older transitions before 3.0.7 have not yet been audited in this log. Unrelated test releases are not covered by the 3.0.7 → 3.0.8 comparison.

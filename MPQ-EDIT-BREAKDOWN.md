# Lau MPQ edit breakdown

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

This document separates the changes made for Lau Setup from the assets inherited
from Andre, the HD client foundation, Project Reforged, Blizzard, and the optional
Trimitor map component. It covers the current stable **Setup 1.4.0 / game 3.0.9
Lau** payload and the retained Patch-Y history from the Andre handoff onward.

This is the short answer: Lau Setup does not replace every MPQ in a client. It
installs one selected Patch-Y edition, and it can install optional Q, S, M, and T
components. Lau's verified Patch-Y changes are DBC routing and localization,
specific raid-warning geometry, two marker colors, a Halion radius increase, the
version marker, and lossless release compaction. Most files inside Patch-Y are
inherited assets and must not be described as newly authored by Lau.

## What Setup can place in the client

| Installed path | When used | Contents and provenance |
| --- | --- | --- |
| `Data/patch-y.mpq` and `Data/<locale>/patch-<locale>-Y.MPQ` | Always; both destinations receive the same selected Y archive | Andre-based Patch-Y plus the verified Lau changes documented below |
| `Data/patch-q.mpq` and `Data/<locale>/patch-<locale>-Q.MPQ` | Optional **Compatible WoW.exe + loading screens** | Matching loading screens and regional artwork; this component is not part of the Patch-Y authorship comparison |
| `Data/patch-s.mpq` | Optional **New spell visuals** | Shared spell models, textures, and other visual assets from the supported HD spell component |
| `Data/<locale>/patch-<locale>-S.MPQ` | Optional **New spell visuals** | Localized spell tables matching the root S assets; this is a different archive from root Patch-S |
| `Data/patch-m.mpq` | Optional **Upgrade maps and minimap** | Shared world-map and minimap textures from the existing Lau map selection |
| `Data/<locale>/patch-<locale>-T.MPQ` | Optional **Upgrade maps and minimap** | Trimitor WDM 2.4.5 stable dungeon/raid maps plus the selected 2.4.5 beta cave data, repacked without changing the selected upstream member bytes |

Setup also installs an allowlisted set of WDM and `!Astrolabe` addon support
files with the map option. Those files are not MPQs. The compatible `WoW.exe` is
also not an MPQ edit.

The installer backs up files it replaces, verifies destination hashes, and can
restore the exact prior installation. Root and locale Y are identical copies.
Root and locale S serve different roles and are not interchangeable.

## The six Patch-Y editions

The player receives exactly one of these editions. HD detection fixes the HD or
Non-HD family; **New spell visuals** and **Enhanced Consecration** select the
available variant within that family.

| Edition | Current members | Current archive size | Difference controlled by the option |
| --- | ---: | ---: | --- |
| HD, New Spells Off, Consecration Off | 508 | 47,561,296 bytes | Stock Consecration appearance; no HD-new-spell selection |
| HD, New Spells Off, Consecration On | 508 | 47,561,314 bytes | Lau Consecration appearance |
| HD, New Spells On, Consecration Off | 507 | 47,470,879 bytes | HD new-spell routing; stock Consecration appearance |
| HD, New Spells On, Consecration On | 507 | 47,470,883 bytes | HD new-spell routing and Lau Consecration appearance |
| Non-HD, Consecration Off | 500 | 46,608,600 bytes | Non-HD basis; stock Consecration appearance |
| Non-HD, Consecration On | 500 | 46,608,605 bytes | Non-HD basis; Lau Consecration appearance |

Each current Y archive contains seven DBC tables, one `!PYAndre` Lua file, one
TOC, two text provenance/version files, and a large inherited collection of
models, skins, and textures. Depending on the edition, the archive contains
146–147 M2 models, 147 SKIN files, and 194–201 BLP textures. A member being
present does not by itself mean Lau authored or edited it.

The exact current archive hashes and download sizes are pinned in
[`build/catalog.json`](build/catalog.json). The detailed DBC comparison is in
the [DBC changelog](DBC-CHANGELOG.md) and the linked machine-readable evidence.

## Verified Lau Patch-Y changes

### Andre handoff to retained multilingual Lau baseline

Andre supplied the Patch-Y baseline and intentionally omitted `Spell.dbc` to
avoid localization conflicts. The retained Andre archives already contain six
other visual/model DBCs and the bulk of the models, skins, and textures.

The Lau adaptation added a compatible `Spell.dbc`, connected fifteen accepted
raid spell records to the indicator visuals, and added the supporting
SpellVisual, SpellVisualKit, SpellVisualEffectName, and attachment records. The
Consecration-On editions change the Consecration model reference from
`spells\consecration_impact_base.mdx` to `spells\Flamezone.mdx` and its scale
word from `1065353216` (1.0) to `1075838976` (2.5). The multilingual rebuild
populated compatible localized/fallback spell text while preserving the
numeric visual links. Lau and Andre debugged that localization dependency
together.

The retained artifact evidence maps this completed multilingual baseline to
published game 3.0.4, although the remembered development milestones used
overlapping early labels. The audit therefore names hashes and retained
artifacts instead of inventing a missing release assignment.

For every record ID, field index, old value, new value, and added row, see
[`docs/dbc/history/INDIVIDUAL-EDITS.md`](docs/dbc/history/INDIVIDUAL-EDITS.md).
That report also explains which Spell data came from the HD Patch-S or stock
client basis so inherited rows are not presented as Lau-authored records.

The handoff audit is complete for the seven DBC tables. The retained evidence
does not prove a member-by-member non-DBC diff for the unrecovered early broken
build, so no additional early M2, SKIN, or BLP authorship is claimed here.

### Game 3.0.5: wider Sindragosa and Rotface warnings

Applied to all six editions:

- Sindragosa Frost Breath widened from 75° to 90° total.
- Rotface Slime Spray widened from 25° to 60° total.
- Only X/Y mesh geometry and the required model/submesh bounds changed. Range,
  Z coordinates, UVs, normals, animation, particles, and DBC routing stayed
  unchanged.

Exactly five existing members changed in each edition:

- `Spells/PW_White_Fan75_60yd_Glowing.m2`
- `Spells/PW_White_Fan75_60yd_Glowing00.skin`
- `Spells/PW_Rotface_SlimeSpray_Fan25_Room.m2`
- `Spells/PW_Rotface_SlimeSpray_Fan25_Room00.skin`
- `Interface/AddOns/!PYAndre/!PYAndre.toc` for the version label

Every other archive member was byte-identical to game 3.0.4.

### Game 3.0.6: light-blue Coldflame and red Halion meteor fire

Applied to all six editions:

- Marrowgar Coldflame uses a new opaque light-blue marker texture.
- Halion meteor trails and landing fire use one shared new opaque red marker
  texture.
- Existing native particles, animation, geometry, skins, bounds, and DBC bytes
  were preserved.

Four existing members changed:

- `Spells/PW_Coldflame_Ground.m2`
- `Spells/PW_HalionMeteor_Ground.m2`
- `Spells/PW_HalionMeteor_Ring.m2`
- `Interface/AddOns/!PYAndre/!PYAndre.toc`

Two members were added:

- `Spells/PW_Coldflame_Blue.blp` — decoded DXT1 color `(120, 216, 248, 255)`
- `Spells/PW_Halion_Red.blp` — decoded DXT1 color `(248, 68, 40, 255)`

The three M2 edits only redirect texture descriptor 4 from the shared white
texture to the corresponding new BLP path. Every unrelated member was
byte-identical to game 3.0.5.

### Game 3.0.7: larger Halion meteor-fire radius

The tester-approved v2 geometry increased the X/Y size of Halion's meteor
ground and ring markers by 50%. Z coordinates, UVs, normals, animation, particle
tracks, Coldflame, and unrelated members were preserved.

Exactly five existing members changed in each edition:

- `Spells/PW_HalionMeteor_Ground.m2`
- `Spells/PW_HalionMeteor_Ground00.skin`
- `Spells/PW_HalionMeteor_Ring.m2`
- `Spells/PW_HalionMeteor_Ring00.skin`
- `Interface/AddOns/!PYAndre/!PYAndre.toc`

### Game 3.0.8: all retained breath and Slime Spray warnings at 90°

The following models were widened by editing X/Y vertices and model, sequence,
and skin-submesh bounds. Radius and Z were preserved.

| Model | Encounter/use | Previous | New |
| --- | --- | ---: | ---: |
| `PW_Rotface_SlimeSpray_Fan25_Room` | Rotface Slime Spray | 60° | 90° |
| `PW_White_Fan60_60yd_Glowing` | Halion, both realms | 60° | 90° |
| `PW_White_Fan60_30yd_Glowing` | Saviana Ragefire | 60° | 90° |
| `PW_White_Fan60_100y_Glowing` | ICC Rimefang | 60° | 90° |
| `PW_White_Fan82_60yd_Glowing` | Sartharion | 82° | 90° |

Each listed M2 and its matching `00.skin` changed, plus the `!PYAndre.toc`
version label: eleven existing members per edition. Sindragosa's
`PW_White_Fan75_60yd_Glowing` was already 90° from game 3.0.5 and remained
byte-identical. UVs, normals, animation, particle tracks, DBC rows, the approved
Halion radius, and the Coldflame/Halion colors were unchanged.

The exact member lists and all 42 byte-identical DBC comparisons are recorded
in [`docs/dbc/3.0.7-to-3.0.8.json`](docs/dbc/3.0.7-to-3.0.8.json).

### Game 3.0.9: version marker and lossless archive compaction

No gameplay, geometry, texture, or DBC content was changed. The embedded
`Interface/AddOns/!PYAndre/!PYAndre.toc` version marker was updated to 3.0.9,
then all six Y archives were compacted for download. The compaction removed
58,774,086 bytes of unused MPQ container space across the six editions without
changing the extracted member set or member bytes after the version update.

Setup compacts only the distributed Patch-Y payloads. It never compacts a
player's existing MPQs or backups.

## Optional components that are not Patch-Y authorship

### New spell Patch-S pair

The root `patch-s.mpq` contains shared spell visual assets. The active-locale S
archive contains the matching localized tables. Lau Setup selects, verifies,
backs up, disables, re-enables, and restores this pair, but installer transaction
work is not an internal MPQ content edit. These assets are also the data basis
used to construct compatible HD New-Spells-On Spell rows in Patch-Y.

### Loading Patch-Q pair

The root and active-locale Q destinations receive identical bytes for the
selected client language. They contain loading screens and regional artwork and
are coupled to the optional compatible executable in Setup 1.4.0. They are not
part of the Andre-to-Lau Patch-Y diff.

### Map Patch-M and Patch-T

The optional map component is separate from Patch-Y:

- Root Patch-M contains the large world-map/minimap texture set.
- Active-locale Patch-T contains 2,190 selected upstream WDM members.
- Patch-T includes `DungeonMap.dbc`, `DungeonMapChunk.dbc`, `WorldMapArea.dbc`,
  `WorldMapTransforms.dbc`, `AreaTable.dbc`, and `WMOAreaTable.dbc`.
- Where the stable and cave sources both provide `WorldMapArea.dbc`, the cave
  version intentionally wins. Cave maps remain upstream beta.
- The selected upstream member bytes and provenance are recorded per locale in
  [`docs/dbc/map-pack-1.4.0.json`](docs/dbc/map-pack-1.4.0.json).

This packaging and compatibility work is part of Lau Setup, but the Trimitor
map data is credited upstream and is not represented as a Lau-authored map or
DBC edit.

## What these edits do not change

- They do not change Warmane server mechanics, hitboxes, damage, timing, or AI.
- The ground indicators are visual warnings and may not be exact damage
  boundaries.
- Flat geometry can clip or disappear on uneven terrain.
- Static MPQ, hash, DBC, and geometry checks do not replace in-game encounter
  testing.
- Installer versions and game payload versions are separate. Installer-only
  releases can change backup or UI behavior while leaving every MPQ byte
  unchanged.

## Evidence map

| Question | Evidence |
| --- | --- |
| What files can Setup install, and where? | [`docs/TECHNICAL.md`](docs/TECHNICAL.md) and `app/Core.cs` |
| What are the exact current asset hashes and sizes? | [`build/catalog.json`](build/catalog.json) |
| Which DBC records and fields changed? | [`DBC-CHANGELOG.md`](DBC-CHANGELOG.md) and [`docs/dbc/history/INDIVIDUAL-EDITS.md`](docs/dbc/history/INDIVIDUAL-EDITS.md) |
| Were later releases DBC-identical? | [`docs/dbc/history/3.0.4-through-3.0.8.json`](docs/dbc/history/3.0.4-through-3.0.8.json) |
| What changed in 3.0.7 → 3.0.8? | [`docs/dbc/3.0.7-to-3.0.8.json`](docs/dbc/3.0.7-to-3.0.8.json) |
| Where did the optional map tables come from? | [`docs/dbc/map-pack-1.4.0.json`](docs/dbc/map-pack-1.4.0.json) |
| What are the release-level behavior and validation limits? | [`CHANGELOG.md`](CHANGELOG.md), [`docs/RELEASE-1.4.0.md`](docs/RELEASE-1.4.0.md), and [`KNOWN-LIMITATIONS.md`](KNOWN-LIMITATIONS.md) |

## Credits and attribution boundary

**Andre** supplied the Patch-Y baselines. **Loriendal and Trimitor** supplied the
HD client foundation. **Project Reforged contributors** supplied HD artwork.
**Blizzard** supplied the original game, artwork, and localized text. **Trimitor
WDM** supplied the optional dungeon, raid, and beta cave map component. **Lau**
is credited for the verified adaptations and edits listed in this document,
compatibility work, testing, packaging, and release tooling.

# Optional merged map pack for Setup 1.4.0

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell

The single maps/minimaps checkbox installs Lau's existing shared map archive
plus map-only localized content from [Trimitor WDM](https://github.com/Trimitor/WDM-patch).
Classic/TBC dungeon and raid maps use 2.4.5-stable. The optional upstream cave
expansion uses 2.4.5-beta; it is included in this combined candidate and requires
in-game acceptance. Loading screens and executable replacement share one optional checkbox; maps remain independent.

## Contents and provenance

- Existing shared Lau Maps asset is unchanged.
- Nine localized Patch-T archives combine the upstream locale M and N archives.
  Each has 2,190 content members. The sole overlapping name is WorldMapArea.dbc;
  the cave expansion's version wins. Every output member was extracted and
  compared by SHA-256 to its selected upstream member.
- The map-only archives contain no LoadingScreens.dbc, Map.dbc or loading images.
- WDM and !Astrolabe support addons contain 115 files from WDM-addons commit
  621d4de79f9b9a24586a9d7cdce0f57d8c78e395. All 102 active TOC/XML file references
  resolve. Original credits and included license files are preserved.
- New payload download tag: payload-maps-1.4.0. All 116 unique segments were
  downloaded from their public URLs and verified by size and SHA-256.

## Files and recovery

Setup writes Data/patch-m.mpq, the detected language's Patch-T, and only the
compiled WDM/!Astrolabe file allowlist. Existing localized M/N archives are kept.
Existing Patch-T and selected support files are backed up before replacement.
Unlisted addon files and SavedVariables are untouched. Internal addon backups
use short names to avoid Windows path-length failures; the journal retains the
original path for Restore. Use Setup 1.4.0 or newer for these backups.

## DBC scope and acceptance

This optional component supplies DungeonMap, DungeonMapChunk, WorldMapArea,
WorldMapTransforms, AreaTable and WMOAreaTable overrides. It copies upstream
bytes without custom table edits. Patch-Y remains game version 3.0.8, but it
would be inaccurate to say this map addition introduces no DBC changes.

Static checks do not establish client patch precedence. Player testing must
check world/minimap textures, Classic/TBC dungeon and raid maps, cave maps,
floor switching and navigation, and coexistence with old combined Patch-Q.
Do not mark that acceptance complete based on installer or archive tests.

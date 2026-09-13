# Editing the Lady Deathwhisper visuals

Author / Creator / Last Modified By: Neil Mitchell

## Source layout

`editing/native/Creature/Banshee` contains the original native model, four skin LODs and textures. `editing/native/Spells` contains the native double-ring texture and the red DXT3 texture used for the arrows. Keep these as pristine inputs. `tools/build_model.py` appends marker geometry and writes `dist/model`; it never writes to a game client. `tools/model_utils.py` provides the M2 array and WDBC helpers. `tools/build_lady_payload.py` edits each baseline's own tables and packs verified per-edition MPQs using `tools/mpq.py`.

The generated private path is `Creature\PW_DW_Banshee\Banshee.mdx` (the physical model is `.M2`). No shared Banshee asset is overwritten.

## Ring and arrow adjustments

In `tools/build_model.py`:

- **Circle color:** RGB565 endpoint multipliers `.40`, `.78`, and unchanged blue tint `DoubleRing128.blp`. They preserve the DXT1 block indices, original ring shape and mip chain. Change these multipliers to adjust tint; keep channels within their 5/6/5-bit ranges.
- **Circle size:** the first `parts` quad uses coordinates from `-1.5` to `1.5`. This is model space, multiplied by display scale 1.2; it is not a certified game damage radius.
- **Circle thickness/opacity:** edit the source ring texture's shape/intensity and regenerate valid mip levels with a BLP-capable tool. Changing quad size alone scales both ring thickness and diameter.
- **Arrow locations:** `for tip in [1.8, 2.6, 3.4]` positions the three tips along model +X. Update both the solid and glow loops together.
- **Arrow shape:** each six-vertex polygon uses tip offsets and Y widths (`.48` / `.35`). Its four triangles create the chevron. Increase width/thickness through these vertices, preserving triangle winding.
- **Arrow color:** `PW_DW_Red.blp` is a native-format DXT3 texture with a full mip chain. Use a compatible BLP editor, retaining format and mipmaps. Tiny placeholder textures previously rendered incorrectly and should not replace it.
- **Arrow glow:** `(1.12, .12)` and `(1.24, .045)` set expansion and brightness of the two faint additive copies. Brightness is baked into separate RGB565 texture endpoints; it is not driven by the `alpha` tuple field in the geometry loop.
- **Height:** ring/arrow Z offsets plus the common `z + .2` position the geometry above the root. Test clipping and bobbing while moving. Both the body and markers inherit native root animation.

For body scale, edit `set_f32(disp,4,1.2)` in `tools/build_lady_payload.py`. For body colors, edit the native Banshee BLP input textures. Always rebuild from native inputs; running geometry edits on an already-modified M2 would append duplicates.

## Model invariants

The build keeps the native skeleton, original geometry and animation data, appends 58 vertices / 38 triangles for the default ring and arrows, and updates all four `.skin` files. Original bone bytes and each skin's maximum-bone setting are asserted unchanged. New vertices bind to native root bone 0. Full-opacity lookup references native opacity track 5. Each skin's new vertex lookup starts at its own lookup count, which can differ from the M2 vertex count. Preserve that distinction, per-LOD bone limits, model/submesh bounds and texture/material references.

## Exact DBC scope (zero-based fields)

| Table | Edit |
|---|---|
| CreatureDisplayInfo | Row 31553: field 1 private model ID, field 4 scale 1.2, field 6 BansheeSkin, fields 7/8 zero |
| CreatureModelData | Clone native Banshee row 144 into a fresh ID; field 2 private model path |
| SpellVisual | Row 15116: fields 3/5 zero, field 4 remains 90011 |
| SpellVisualKit | Row 90011 clones Frost Beacon kit 90002, retains ID 90011; direct effect fields 3–14 zero |
| SpellVisualEffectName | Clone native effect 6519 into a fresh ID; private name, scale fields 4/5/6 = 1 |
| SpellVisualKitModelAttach | Remove attachments for kit 90011; clone donor 8004 with fresh ID, kit 90011 and new effect ID |

IDs are allocated as the maximum existing ID plus one for each edition. Do not copy a whole DBC from another edition. The build preserves each edition's strings and unrelated rows, plus the Sindragosa donors. `Spell.dbc` stays byte-identical: no aura duration or gameplay edits. The native beacon donor uses `spells\catmark_red.mdx`.

## Rebuild on Windows

Prerequisites: Python 3, Windows .NET Framework 4.8 compiler, and an x64 **Unicode-path StormLib DLL** (the wrapper uses UTF-16 file paths). StormLib is a build dependency and is not placed in WoW. Use a trusted build of StormLib and its upstream license. No Python packages are needed.

Download and extract the original `Lau-Patch-Y-3.0.8-All-Editions.zip` from the stable v1.1.7 release. Locate the directory containing the six `Y-*.mpq` files. The branch's `build/catalog.json` provides the expected baseline hashes.

```powershell
$env:STORMLIB_DLL = 'C:\BuildTools\StormLib.dll'
python tools\build_model.py
python tools\build_lady_payload.py 'C:\Baselines\3.0.8' build\catalog.json
.\tools\build-test.ps1
```

Outputs: `dist/LauSetup.exe`, `dist/payload`, `dist/catalog.json`, `dist/baseline.json`, and `dist/scope-validation.json`. Ship the EXE and entire payload folder together. Do not ship build fixtures, a personal WoW.exe, account files or local logs. See `tools/package-test.py` for the release ZIP and checksum manifest.

Run the installer regression harness with **absolute paths** and a new isolated fixture directory. The fixture WoW.exe is only read locally and copied into the test directory; it is never included in the distribution:

```powershell
.\dist\LadyTestTests.exe 'C:\TestFixtures\Lady-Run1' 'C:\Baselines\3.0.8' 'C:\MyWoW\WoW.exe' 'C:\Lau-Setup\dist\payload'
```

After geometry changes, inspect all LODs and actual game rendering again. After payload changes, rerun archive scope/readback checks, rebuild the embedded installer catalog, and rerun install/restore tests. Create a new prerelease identifier; retain the prior test and backup paths for rollback.

## What cannot be fixed here

This is a client visual package. It cannot force Warmane to expose accurate spirit targets or keep an aura alive until despawn. A persistent circle on the Banshee is supported because it belongs to the creature model; a persistent player chase marker is not implemented.

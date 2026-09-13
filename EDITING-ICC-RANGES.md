# Editing the ICC player-circle experiment

Author / Creator / Last Modified By: Neil Mitchell

This branch builds the Windows test for [ticket #27](https://github.com/CRSD-Lau/Lau-Setup/issues/27). Read [Andre's test instructions](ICC-RANGE-TEST.md) before changing the visual hooks. The intended ring radius is 12 yards; its runtime size and usefulness have not been accepted in game.

## Asset and build chain

`editing/range-circles` retains the native `Range_Circle_White_Small_50` model, skin and texture already distributed in Lau Patch-Y, plus its PNG editing reference. These are inherited project assets, not newly authored artwork. `tools/build_range_model.py` verifies the three native input hashes, enlarges the four-vertex model and creates three colour variants beneath `dist/model/Spells/Lau_ICC_RangeTest`. It preserves the donor's bones, animation tracks and render settings, updates model/sequence/submesh bounds for the enlarged geometry, and rewrites the texture path to the private namespace.

`tools/build_range_payload.py` verifies each supported 3.0.8 archive against `build/catalog.json`, reads that edition's own tables, allocates private visual records, adds the generated models, and reads the finished MPQ back with StormLib. Every unrelated member must remain byte-identical. It writes six complete replacement Patch-Y archives, an embedded test catalog, the baseline catalog and a detailed scope report. The Windows installer chooses the matching edition and replaces only root Patch-Y and active-locale Patch-Y through the existing verified backup/restore engine.

## Cues and limitations

| Cue | Spell IDs | Visual attachment |
| --- | --- | --- |
| Cyan-blue heroic BPC carrier | 73001 | Clone Shadow Prison visual 15404; a private StateKit tests whether the player area-aura state renders. It may be hidden or absent on Warmane. |
| Purple Empowered Shock Vortex | 72038, 72815, 72816, 72817 | Clone visual 15204 and its CastKit 14056; attach to the player force-casting the burst. This is a resolution-time cue. |
| Red Blood Nova | 72378, 73058 | Clone parent visual 15283 and ImpactKit 14140; test the selected target's impact visual. Keep boss casting artwork and the dummy/damage chain unchanged. |

The direct Vortex and Nova cues are not certified advance warnings. The reference server implementation can dispatch Blood Nova damage directly from the selected-target parent, bypassing dummy spell 72379. That is why this test attaches to the parent rather than relying on the dummy. Warmane's implementation is not proven identical. The boss Shadow Prison aura 72998 and Blood Nova dummy/damage spells 72379, 72380 and 72438–72440 are untouched.

These conclusions are based on the [TrinityCore BPC script](https://github.com/TrinityCore/TrinityCore/blob/3.3.5/src/server/scripts/Northrend/IcecrownCitadel/boss_blood_prince_council.cpp), [Saurfang script](https://github.com/TrinityCore/TrinityCore/blob/3.3.5/src/server/scripts/Northrend/IcecrownCitadel/boss_deathbringer_saurfang.cpp), and the [12340 DBC definitions](https://github.com/wowdev/WoWDBDefs/tree/master/definitions). They are implementation references, not evidence from Andre's realm.

## Size, colour and data scope

The donor quad half-width is 2.8592245579 model units. The retained 512-pixel PNG's bright visible ring reaches 249.5 pixels from the centre against a 255.5-pixel texture half-width, using alpha and maximum RGB thresholds of 64. `QUAD_HALF_WIDTH = 12 / (249.5 / 255.5)` produces a 12.2885771543-unit quad half-width and an intended visible radius of 12 model units. The square's corner radius is not the circle radius. Confirm the result against 10/12/14-yard player separation in game, including different races and forms.

Change the `CUES` RGB multipliers in `build_range_model.py` to retint the DXT5 colour endpoints; alpha, block indices and mip levels are retained. Do not treat model units as a verified yard measurement or lengthen spell duration to manufacture an aura. Changing circle size, geometry, attachment or effect scaling requires a new runtime calibration and test identifier.

Only `Spell.dbc` field **131**, the first visual link, changes on seven existing spells. Field 132, gameplay fields and spell strings remain unchanged. The other four DBC tables receive three new rows each; all their original rows are preserved. [DBC-CHANGES](docs/dbc/icc-range-test1.md) records exact IDs, field values and hashes for all six editions, with the full [JSON evidence](docs/dbc/icc-range-test1.json).

## Build and validate on Windows

Prerequisites: Python 3.11+, .NET Framework 4.8's C# compiler and a trusted x64 **Unicode-path StormLib DLL**. StormLib is a build dependency and is not shipped. No third-party Python packages are required. Obtain the original six 3.0.8 MPQs and keep their filenames as `Y-<edition>.mpq`; the checked-in stable catalog is the authority for bytes and hashes.

Run from this branch's repository root, substituting your own absolute paths:

```powershell
$env:STORMLIB_DLL = 'C:\BuildTools\StormLib.dll'
python tools\build_range_model.py
python tools\build_range_payload.py 'C:\Baselines\3.0.8' build\catalog.json
python tools\test_range_payload.py
.\tools\build-range-test.ps1
.\dist\RangeTestTests.exe 'C:\TestFixtures\ICC-Run1' 'C:\Baselines\3.0.8' 'C:\MyWoW\WoW.exe' 'C:\Lau-Setup\dist\payload'
```

The fixture directory must be new and empty. The harness reads the chosen executable and copies it only into the isolated fixture; never package that copy. Finish the shared regression run, exact DBC report and release package using the same unchanged build:

```powershell
.\tools\run-range-core-tests.ps1 -Output 'C:\TestFixtures\ICC-Core1' -FixtureExe 'C:\MyWoW\WoW.exe'
python tools\document-range-test.py
python tools\package-range-test.py --installer-results 'C:\TestFixtures\ICC-Run1\validation.json' --core-results 'C:\TestFixtures\ICC-Core1\run\results.json' --core-provenance 'C:\TestFixtures\ICC-Core1\core-provenance.json'
```

The package builder requires passing results bound to the current source, catalogs, payload and installer, and rejects stale evidence. If any build input changes, rebuild and repeat the relevant validation before packaging.

Ship the complete ZIP, not the EXE alone. It contains the offline installer, configuration, six tested payload files, instructions, DBC evidence, validation and checksums. Build dependencies, baseline archives, test executables, fixtures, personal paths and account data are excluded. Keep this experimental release separate from stable Lau Setup and leave the ticket in Testing until Andre reports encounter results.

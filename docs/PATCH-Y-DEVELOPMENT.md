# Develop Patch-Y visual changes

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

[Back to Lau Setup](../README.md) · [Source layout](../patch-y/README.md) ·
[Current MPQ edit breakdown](../MPQ-EDIT-BREAKDOWN.md)

This workflow lets contributors inspect the raw members of one released
Patch-Y edition, propose a narrow visual change and prove the exact archive
scope before opening a pull request. It never writes a WoW client.

## Requirements

- Python 3.11 or newer.
- Windows: a trusted x64 Unicode `StormLib.dll`, exposed through
  `STORMLIB_DLL`.
- Linux: StormLib 9.22 (`libstorm9`/`libstorm-dev`) or an explicit
  `STORMLIB_LIBRARY` path.
- About 900 MB of temporary space for the verified release ZIP, six extracted
  baseline MPQs and six candidate MPQs.

StormLib is a build dependency only. Do not copy it into Patch-Y or a game
client.

## Fork, inspect and branch

1. Fork and clone `CRSD-Lau/Lau-Setup`, then create a focused branch.
2. Fetch the exact public baseline:

   ```text
   python tools/patch_y.py fetch
   ```

3. Verify all six MPQs and every member against `patch-y/baseline.json`:

   ```text
   python tools/patch_y.py verify-baseline
   ```

4. Extract one edition for read-only inspection:

   ```text
   python tools/patch_y.py inspect Y-HD-NewSpells-On-Consecration-On
   ```

   The raw tree appears under `patch-y/.work/inspect/` and stays ignored by
   Git. Never edit this extracted baseline in place.

## Declare a change

Put changes shared by all editions in `patch-y/overlays/common`. Put a truly
edition-specific change in the matching `patch-y/overlays/editions/<edition>`
directory. Add source files below that overlay and declare every operation in
its `manifest.json`.

Every operation also requires a non-empty `servers` list using IDs from
`patch-y/servers.json`. Server targeting is independent from the six visual
editions: do not apply one realm's DBC IDs, timing assumptions or geometry to
another server merely because both run client build 12340. The current profiles
are `warmane` and `wowcircle`. WoW Circle's faster Halion twilight cutters and
larger meteor-strike fire radiuses are documented differences; exact values
still require evidence from the named realm/build.

Ridepad's [UwU Logs server registry](https://github.com/Ridepad/uwu-logs/blob/685c8f3d726ef2a27f9860b9ed9033b44d7930b5/config/servers_main.json)
confirms distinct Warmane realm names and WoW Circle x1/x4/x5/x100 identities.
It is evidence for naming and separation, not proof that two realms share DBC
rows, animation timing or visual radiuses. If a PR targets another private
server, add a reviewed profile to `servers.json` with its exact public name,
realm/build identifiers, known database differences and evidence source.

Supported operations are:

- `add`: add a new member; include `source` and `sourceSha256`.
- `replace`: replace one exact baseline member; also include its
  `expectedBeforeSha256`.
- `delete`: remove one exact member with an `expectedBeforeSha256`.
- `dbc`: apply explicit WDBC field changes. Each edit requires the record ID,
  descriptive field name, zero-based field index, value type, old/new values
  and reason.
- `transform`: run a reviewed, parameterized recipe against one exact baseline
  member. Supported recipes scale XY vertices, rewrite M2/SKIN bounds, replace
  fixed-width embedded texture references, or recolor opaque DXT1 endpoints.

Allowed public member types are M2/MDX, SKIN, BLP, DBC, Lua, TOC and text.
Paths are ASCII, relative, case-unique and traversal-free. A build fails if two
overlays touch the same member in one edition or if a pre-change hash differs.

Opaque DBC `add` and `replace` operations are rejected. Use structured `dbc`
operations so reviewers can see the record and old/new value. An exceptional
whole-table replacement needs its own proposal, schema change and provenance
review before the public tool can accept it.

## Build and prove the candidate

Use a short lowercase development label. It is written into `!PYAndre.toc`,
so `/pyversion` distinguishes the candidate from stable 3.0.9.

```text
python tools/patch_y.py build --server warmane --label my-change
python tools/patch_y.py verify --server warmane
python tools/patch_y.py diff --server warmane
```

The build copies the verified baseline outside Git, applies only declared
operations, compacts the staged archive, reopens it and compares every member.
The diff command writes compact Markdown and JSON proof under
`patch-y/.work/`. Complete candidate MPQs remain ignored.

## Test safely

Archive and hash checks prove file scope, not appearance or encounter
accuracy. For runtime testing:

1. Fully close WoW and use an isolated test client, never a personal active
   client.
2. Back up the existing root and active-locale Patch-Y files outside `Data`.
3. Install one matching candidate MPQ at both Patch-Y destinations.
4. Confirm the development label with `/pyversion`.
5. Test the named encounter, difficulty, terrain, camera angles and movement.
6. Capture screenshots or video and restore the exact original files.

Visual indicators do not change Warmane damage, hitboxes, timing or AI. Flat
geometry can clip on uneven terrain. State clearly which runtime cases were
and were not tested.

## Pull-request evidence

A visual PR must include:

- The encounter/ability and user-visible problem.
- The exact server, realm/build and relevant database or timing evidence.
- The affected editions and declared source operations.
- Asset provenance and applicable permission.
- The generated scope report and commands run.
- Test client, locale, `/pyversion`, difficulty and visual evidence.
- An explicit list of untested encounters, editions or platforms.

CI repeats the hash-pinned build without secrets and uploads only compact
scope reports. Merging a source change does not make it stable: public release
promotion still requires the installer/catalog, DBC history, rollback,
Windows/Wine and in-game acceptance gates.

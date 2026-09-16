# Develop Patch-Y visual changes

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

[Back to Lau Setup](../README.md) · [Source layout](../patch-y/README.md) ·
[Windows beginner quick start](PATCH-Y-QUICKSTART-WINDOWS.md) ·
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
`patch-y/servers.json`. A target can represent a server or a specific realm;
its `targetType` makes that distinction explicit. Targeting is independent
from the six visual editions: do not apply one target's DBC IDs, timing
assumptions or geometry to another merely because both run client build 12340.
The current registered targets are `warmane` and `wowcircle`. WoW Circle's
faster Halion twilight cutters and larger meteor-strike fire radiuses are
documented differences; exact values still require evidence for the exact
server or realm/build tested. If a PR needs another target, add a narrowly
reviewed profile to `servers.json` with `targetType`, its public display name,
and the known database or encounter differences. Do not add unrelated server
directories or external server-list references.

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
- The exact server or realm/build and relevant database or timing evidence.
- The affected editions and declared source operations.
- Asset provenance and applicable permission.
- The generated scope report and commands run.
- Test client, locale, `/pyversion`, difficulty and visual evidence.
- An explicit list of untested encounters, editions or platforms.

CI repeats the hash-pinned build without secrets and uploads only compact
scope reports. Merging a source change does not make it stable: public release
promotion still requires the installer/catalog, DBC history, rollback,
Windows/Wine and in-game acceptance gates.

## Windows commands

The guided launcher is the easiest Windows path:

```powershell
.\tools\patch-y.ps1
```

If local PowerShell policy blocks scripts, use the included double-clickable
`tools\Patch-Y-Start.cmd`, or run:

```powershell
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\tools\patch-y.ps1
```

Direct commands remain available for contributors who prefer them:

```powershell
py -3.11 tools\patch_y.py fetch
py -3.11 tools\patch_y.py inspect Y-HD-NewSpells-On-Consecration-On
py -3.11 tools\patch_y.py build --server warmane --label my-change
py -3.11 tools\patch_y.py verify --server warmane
py -3.11 tools\patch_y.py diff --server warmane
```

## Linux commands

Install Python 3.11+ and the pinned StormLib package described above, then run:

```bash
python3 tools/patch_y.py fetch
python3 tools/patch_y.py inspect Y-HD-NewSpells-On-Consecration-On
python3 tools/patch_y.py build --server warmane --label my-change
python3 tools/patch_y.py verify --server warmane
python3 tools/patch_y.py diff --server warmane
```

## Troubleshooting

- **`python` or `py` not found:** install Python 3.11 or newer. On Windows,
  select **Add python.exe to PATH** in the installer, close PowerShell and open
  it again.
- **StormLib not found:** on Windows, select the x64 Unicode `StormLib.dll`
  when the launcher asks, or set `STORMLIB_DLL` to its full path. Do not copy
  the DLL into the repository or WoW client.
- **Wrong DLL architecture or `%1 is not a valid Win32 application`:** use an
  x64 StormLib build with x64 Python. Do not mix 32-bit and 64-bit files.
- **Baseline hash mismatch:** delete only `patch-y/.cache`, then fetch again.
  Do not substitute another Patch-Y ZIP.
- **Not enough disk space:** keep at least 900 MB free for the ZIP, extracted
  baselines and candidates.
- **Invalid or case-colliding path:** use an ASCII MPQ member path, preserve
  its exact spelling and slashes, and do not use `..`, drive letters or two
  paths that differ only by case.
- **Build says an old value or hash differs:** stop and inspect the selected
  3.0.9 baseline. Do not remove the guard value to force the build.

## Glossary

- **MPQ member:** one file stored inside an MPQ archive, addressed by its
  internal path.
- **Overlay:** the small tracked set of declared additions, replacements,
  deletions or transformations applied over the pinned baseline.
- **Edition:** one of the six Patch-Y combinations of HD/new-spell and
  Consecration options.
- **Server profile:** a registered build target in `servers.json`; despite the
  historical field name, its `targetType` may be `server` or `realm`.
- **DBC operation:** a structured change to named fields in a specific DBC
  record, including guarded old and new values.
- **Scope report:** generated JSON/Markdown proof of exactly which MPQ members
  changed and which remained byte-identical.
- **`/pyversion`:** the in-game command used to confirm the loaded Patch-Y
  candidate and development label.

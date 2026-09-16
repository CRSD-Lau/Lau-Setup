# Patch-Y contributor source

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

This directory makes the six released Patch-Y editions inspectable and
buildable without committing six duplicate trees of inherited binary game
assets. The exact **3.0.9 Lau** release is the immutable baseline. Git tracks
its complete member manifest, reviewable source overlays, transforms and tests.

New to Git or command-line tools? Start with the
[Windows beginner quick start](../docs/PATCH-Y-QUICKSTART-WINDOWS.md). Use the
[Patch-Y development guide](../docs/PATCH-Y-DEVELOPMENT.md) as the complete
technical reference.

## What is tracked

- `baseline.json` pins the public release ZIP, all six MPQs and every extracted
  member by size and SHA-256.
- `servers.json` registers explicit server or realm targets and their known
  database or encounter differences. Every non-empty overlay operation names
  its targets.
- `overlays/common` applies a declared change to every edition.
- `overlays/editions/<edition>` holds changes for one exact edition.
- `lib/patch_y_source` contains the cross-platform archive, DBC, model and
  texture helpers used by `tools/patch_y.py`.
- `examples` shows the operation format. Example hashes are placeholders and
  are never loaded by the build.

Downloaded baselines, extracted working trees, candidate MPQs and reports are
written only below ignored `.cache` and `.work` directories. Do not commit
them. A normal pull request changes source overlays and generated proof, not a
complete MPQ.

## Baseline and attribution

Patch-Y 3.0.9 contains inherited work from Andre, the HD client foundation,
Project Reforged and Blizzard as well as Lau's verified adaptations. The
baseline release is fetched from GitHub and is not copied into Git history.
See [the MPQ edit breakdown](../MPQ-EDIT-BREAKDOWN.md) for the exact authorship
boundary and [the DBC changelog](../DBC-CHANGELOG.md) for record-level history.

Binary submissions must identify their source and applicable permission.
Never submit a client, account data, WTF/SavedVariables, personal patches or
private test fixtures.

The current baseline targets Warmane. WoW Circle is tracked separately because
its Halion twilight cutters move faster and its meteor-strike fire radiuses are
larger. The profile records that difference without inventing unverified
numeric values; a WoW Circle change must supply evidence for the exact server
or realm/build tested.

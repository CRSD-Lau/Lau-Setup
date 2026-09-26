# Loading-screen framing — v2 staged correction

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

This supersedes the first broad native-framing test for [issue #34](https://github.com/CRSD-Lau/Lau-Setup/issues/34). Neil rejected that approach in-game because its 16:9 framing produced black sidebars on ICC and other HD loading screens.

The v2 candidate restores the pack's pre-test 16:9 fullscreen behavior for every loading screen except ICC. It adds a scoped full-UV path only when all of these are true:

- the display is exactly 16:9;
- the current `LoadingScreens.dbc` ID is `250` (Icecrown Citadel); and
- ICC's Wide asset loaded successfully.

If the Wide asset is missing, ICC retains the earlier route. At other aspects, and for every other loading ID, the candidate retains the established behavior. This is a staged local candidate, not an installed client change or a published release.

## Candidate and static evidence

`tools/build_icc_widescreen_executable.py` builds only from the compatible prior executable hashes and writes a fresh staged output. The candidate executable is 7,705,600 bytes with SHA-256:

```text
3038275f00c30aea568cb2517b21a289b1a8a58e241e7ff8e69b62116b507fb3
```

The companion Patch-Q candidate is SHA-256:

```text
146707c7040043311ab4ce07eaf3988d76008d3a1c5ec03d4ba65ba37665326c
```

The executable proof permits the restored two five-byte detours plus the scoped helper range, preserves the archive-reserve fix, and reports all other bytes identical. The MPQ proof records the one ICC DBC flag change and the added ICC Wide texture. See [ICC widescreen test plan](ICC-WIDESCREEN-TEST.md) for the precise scope and acceptance checks.

## Staged test boundary

The v2 restore is intended to replace only the staged executable, root Patch-Q, and active-locale Patch-Q. It does not change maps, Caverns artifacts, Patch-Y, or other client assets. A fresh three-file restore fixture has not yet been created for v2.

The release ZIP is unchanged and unpublished; `PublicReady=false`. The current live WoW process was not touched. Static archive, byte, and texture-decode checks do not establish in-game rendering or release readiness.

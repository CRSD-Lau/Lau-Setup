# Loading-screen framing test fix

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

This separate test fix addresses [issue #34](https://github.com/CRSD-Lau/Lau-Setup/issues/34). It is not yet incorporated in the packaged Setup 1.5.0 candidate. The previously recorded Docker results refer to that earlier package, not to an in-game run of this executable.

The supplied compatible executable contains a custom `.ldwide` modification which selects full-screen loading geometry near a 16:9 aspect ratio and substitutes UV coordinates. The full Icecrown artwork is present in Patch-Q; its `LoadingScreens.dbc` record uses the same non-wide flag as the stock record. Replacing images or changing that DBC is unnecessary for this executable repair.

`tools/fix_loading_screen_framing.py` accepts only the exact input SHA-256 `6993049f1338b32a0423612093a8c7c6895b112504b83d6826d4c2174692cd37`. It restores two five-byte instruction sites, changing eight bytes in total:

| File offset | Before | After | Purpose |
| --- | --- | --- | --- |
| `0x9a02` | `e8f9299f00` | `e899dfffff` | Call the native loading-background routine at `0x4085a0` |
| `0x7a15` | `e8e64a9f00` | `680064ab00` | Push the native UV-coordinate table at `0xab6400` |

The second instruction is a **push**, not a call into a data table. All other executable bytes, including the archive-list reserve-floor fix in the same added section, are retained. The resulting 7,705,600-byte executable has SHA-256 `a6767f7ed4d1f7c67c144eed7bf9707cd270d95af200f4accd0c6fc66ca14889`.

**No DBC or artwork edits are part of this loading-screen fix.** The separately installed Caverns candidate still makes the documented WorldMapArea changes.

## Validation and reproduction

[Isolated instruction validation](LOADING-FRAMING-VALIDATION.json) passed 32 executions of the original and repaired x86 paths across 4:3, 16:10, 16:9 and 21:9, with both texture flags and both background-presence states as applicable. The tests verify native UV-table selection, stack balance and retained registers. They stub the native draw/get/set functions and do not render the game. Exact input rejection and byte preservation also passed.

The standalone validator requires Python with `pefile` and `unicorn` (validation used Unicorn 2.1.4). It is separate from the installer and does not run or inject into a game process:

```text
python tools/fix_loading_screen_framing.py --source original-WoW.exe --output test-WoW.exe --proof framing-proof.json
python tools/validate_loading_framing.py original-WoW.exe test-WoW.exe validation.json
```

A backed-up local test installation changes exactly the executable and the two Caverns M/T archives. Restore was tested on an isolated three-file fixture, including refusal before any write when a destination has changed. In-game acceptance and integration into a newly packaged release candidate remain pending.

## In-game acceptance

Cold-start the test client at its usual 16:9 resolution. Enter ICC and check that the complete loading image remains visible at the intended proportions, with no clipped logo, missing edges or displaced loading bar. Black side bars are expected where a 4:3 image is fitted. Check another previously affected loading screen as well. Representative 4:3, 16:10 and ultrawide checks remain part of broader release acceptance.

For the Caverns fix, open the map inside Caverns of Time and check the cave floors and entrances rather than only the outdoor Tanaris map. It should no longer fall back to Kalimdor. Check one other cave map for regression.

Issue #34 and the Caverns issue #32 remain open until their in-game checks pass. The release catalog and public downloads must not be marked verified from instruction emulation or archive checks alone.

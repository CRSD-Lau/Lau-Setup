# BPC Floor Markers — Test 3

Author/Creator/Modifier: Neil Mitchell

This Windows-only test adds 25 small, muted, room-fixed floor decals labelled
`M1`–`M10`, `H1`–`H5`, and `R1`–`R10` in the
Blood Prince Council chamber: ten melee stage points, five healer anchors, and
ten ranged anchors inferred from the supplied position plan. Every marker
centre is at least 13 yards from every other marker centre, providing a one-yard
margin over the 12-yard Vortex knockback threshold. The closest pair is
measured automatically during the build and recorded in `POSITION-SEPARATION.json`.
It does not add player
circles and does not alter DBCs, spells, gameplay, addons, SavedVariables, or
the client executable.

## Install

1. Close WoW completely.
2. Extract this ZIP outside the WoW folder and run `LauBpcFloorMarkersTest.exe`.
3. Select the root folder containing `WoW.exe` and choose **Apply BPC floor-marker test**.
4. Enter the BPC room and judge placement, visibility, and clutter in a real
   25-player setup. The installer checks hashes, backs up only the root and
   active-language Patch-Y files, and verifies the installed bytes.

Use **Restore previous Patch-Y** in the same program to revert exactly the two
files it changed. Restore the earlier range-circle Test 1 first if it is still
installed; this test intentionally accepts only the stable Lau 3.0.8 baseline
or its own installed files.

## What Andre should check

- The 10 melee points remain on the stage and do not obscure the fight.
- The five healer and 10 ranged anchors match the planner layout.
- The muted, floor-matching labels are readable without turning the room into a
  field of circles.
- No marker is floating, clipped into the floor, or visible outside BPC.

The archive and installer checks prove the reversible file scope. They do not
replace visual acceptance in the live BPC room.

# ICC 12-yard circles — Test 1 for Andre

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

This is an experimental Windows build for **Blood Prince Council** and **Deathbringer Saurfang**, based on Lau game release **3.0.8**. It tests whether the client can display useful player-centred circles through existing spell visuals. The intended radius is **12 yards**, or **24 yards across**.

**The rings are not yet proven advance warnings.** Direct Empowered Shock Vortex and Blood Nova effects may appear only when the ability hits. Heroic BPC additionally tests Shadow Prison as a carrier for circles throughout the encounter. Record an absent, late, misplaced or incorrectly scaled ring as a failed experiment; do not rely on it to decide that a position is safe.

## Install on Windows

1. Use a working Lau **3.0.8** client. The installer recognises all six supported visual editions automatically. Restore any Lady, Halion or other experimental Patch-Y build first. It refuses custom/unknown or mismatched editions.
2. Close that WoW client completely.
3. Extract the **entire** test ZIP into a separate folder. Keep `LauIccRangeTest.exe`, its `.config` file and the `payload` folder together. Do not copy the six payload files into WoW yourself.
4. Open **LauIccRangeTest.exe**, choose the intended WoW folder, and click **Apply ICC range-circle test**.
5. Wait for the installed-and-verified message. Launch WoW normally. `/pyversion` remains **3.0.8**; use the installer and this test package name to identify Test 1.

The installer uses .NET Framework 4.8 and runs offline. This package targets Windows only. It contains no replacement WoW executable, Q/M/S patches, addons, DBM changes, account settings or personal files.

The only game files replaced are the already installed `Data\patch-y.mpq` and `Data\<active locale>\patch-<locale>-Y.MPQ`. They must match the supported baseline or this exact test build. This installer replaces the complete Patch-Y archives; the build separately verifies that unrelated archive contents are unchanged. Original bytes are backed up through Lau's verified transaction system.

## What to record

The test uses **cyan-blue** for the heroic Shadow Prison carrier, **purple** for Empowered Vortex, and **red** for Blood Nova.

Keep the existing DBM 12-yard range radar visible as a comparison. A screenshot alone is not enough to establish timing; record a short clip that starts before the cast and includes the impact and cleanup.

| Encounter test | Questions for Andre |
| --- | --- |
| Heroic BPC: Shadow Prison carrier | Do circles appear beneath players, including yourself? Are they present while standing still as well as moving? Do they stay during the Empowered Vortex spread window? Do they follow the correct player and disappear on death, reset and leaving the encounter? |
| BPC: Empowered Shock Vortex | Does the burst marker appear? Is it centred on the player producing the vortex? Does it arrive during the cast or only at the explosion? Check the behaviour separately in normal and heroic modes. |
| DBS: Blood Nova | Does the marker appear on the selected Nova player, the boss, every splash victim, or nowhere? Is there any useful lead time before damage? Does it follow movement or stay at the burst location? |
| Scale and readability | Compare another player's centre at approximately 10, 12 and 14 yards; include different races/forms and camera angles. Check clutter with a full raid and clipping into the floor. |

Judge the **other player's centre against your ring edge**. Two 12-yard rings can overlap even when those players are more than 12 yards apart. The rendered ring does not change server targeting or damage radius. Only clients with this test installed see its artwork.

Post results to [ticket #27](https://github.com/CRSD-Lau/Lau-Setup/issues/27), including realm, difficulty, raid size, game locale, HD/new-spell/Consecration settings, the cue tested and a clip. The ticket remains in **Testing** until the requested behaviour has been evaluated.

## Restore

Close WoW, open this same test installer, select the same client, and click **Restore previous Patch-Y**. Wait for the verified-restore message. Keep the `LauSetupBackups` directory intact. Restore uses only this test's own backup and refuses to overwrite files that changed afterward. If it reports an unrelated interrupted installation, recover that operation using the installer that created it.

Archive integrity and installer tests establish safe installation and rollback. Andre's encounter tests establish whether these particular visual hooks are useful. The stable Lau release is unchanged.

[Editing and rebuilding](EDITING-ICC-RANGES.md) · [Test release](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/icc-player-range-circles-test1)

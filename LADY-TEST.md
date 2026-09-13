# Lady Deathwhisper — Banshee test 1

Author / Creator / Last Modified By: Neil Mitchell

Windows prerelease for Andre to test. This is a visual-only experiment based on Lau Patch-Y 3.0.8. Original Patch-Y credit: Andre. Native game assets remain Blizzard assets.

## Install and restore

1. Start with an unmodified Lau 3.0.8 installation. All six Patch-Y editions and the installer's nine locales are recognized. Do not install the stable bundle over a customized client just to bypass a rejection.
2. Extract the entire test ZIP. Keep `LauSetup.exe` beside the `payload` folder.
3. Close WoW. Run `LauSetup.exe`, choose the client folder, and select **Apply Lady test**.
4. Launch WoW. `/pyversion` still reports 3.0.8; the test installer identifies this experiment separately.
5. To undo, close WoW, reopen this installer and choose **Restore previous Patch-Y**. Keep `LauSetupBackups` in the client folder for recovery.

The installer accepts only exact supported baseline/test hashes, preserves your installed edition, and replaces only root `Data/patch-y.mpq` and active-locale `Data/<locale>/patch-<locale>-Y.MPQ`. It rejects mismatched editions or customized Patch-Y files. It does not install WoW.exe, DBM, addons, realm settings, personal UI, other boss experiments, maps or model packs. It is unsigned and requires Windows with .NET Framework 4.8. This test package is not a Wine release.

## Included visuals

- Vengeful Shade display 31553 uses the native Banshee at scale 1.2.
- A blue double-ring glow and three red forward-pointing chevrons are attached to the creature's native root.
- Deathwhisper's existing summon-recipient visual uses the native Frost Beacon overhead icon.

**The beacon is not a confirmed chase-target indicator.** It retains aura 71363's server-controlled duration, approximately six seconds in the local test. It does not persist until the spirit despawns. Warmane target correspondence and full-raid visibility remain unverified. The bottom ring is a visibility cue, not a measured explosion radius. No server mechanics or spell durations change. The DBM detection/sound experiment is excluded.

## Andre's test checklist

- Confirm Banshee size, animation and texture appearance on your chosen edition.
- Inspect the ring and all three arrows at near/far camera distances and low/high model detail.
- Check movement, turning, slopes and overlap with 25-player spell effects and multiple spirits.
- Record which player receives the beacon versus whom the spirit pursues, and when the beacon disappears.
- Confirm unrelated boss visuals remain as before. Record client edition, locale and this test version with feedback.
- Restore using the installer and verify the previous appearance returns.

On a local GM server, `.npc add temp 38222` spawns a temporary Vengeful Shade at your position. This alone does not reproduce encounter targeting. `.aura 71363` is a local visual check, not a Warmane chase test.

## Validation boundary

The original Banshee candidate was rendered in a real isolated WoW client and Neil accepted its appearance. This package rebases only those changes onto each 3.0.8 edition. Archive member readback and DBC row preservation are checked per edition. Isolated Windows installer tests cover install, repeat, drift rejection and exact restore. These checks do not certify all six editions visually in-game or a 25-player Warmane encounter.

See [EDITING-LADY.md](EDITING-LADY.md) for source and rebuilding instructions. `VALIDATION.json` and `SHA256SUMS.txt` accompany the release.

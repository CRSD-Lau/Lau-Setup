# Halion radius test

Author / Creator / Last Modified By: Neil Mitchell

Branch: `test/halion-radius-30`. Private experiment, based on game release 3.0.6.

Only `PW_HalionMeteor_Ground` and `PW_HalionMeteor_Ring` ground geometry is enlarged by 30 percent in X/Y. The corresponding model and skin bounds are updated. Z, UVs, motion tracks, native particles, textures, Coldflame and every other archive member are unchanged. This is a warning buffer, not a change to server damage.

Extract the entire Windows ZIP, close WoW, open `LauSetup.exe`, select the existing client and click **Apply Halion +30% test**. Keep the payload folder beside the EXE. No network download or SDK is needed. Windows requires .NET Framework 4.8, as with normal Setup.

The installer accepts all six original 3.0.6 editions or this exact test. It keeps the edition already installed and only replaces root/active-locale Patch-Y. It refuses unknown/custom Patch-Y, mixed editions, missing placements or mismatched HD models. It will not run normal installation choices or install WoW.exe, maps or models.

Use **Restore previous Patch-Y** to undo this test. Its restore action selects only a backup whose changes match this test's Y hashes; unrelated backups are not restored. Backups use the existing `LauSetupBackups` transaction system.

`/pyversion` remains 3.0.6 because addon metadata is unchanged. The test installer detects the exact archive hashes and reports if this test is already installed. One-byte unknown changes are rejected, rather than silently overwritten.

In-game acceptance is pending. Compare the ring with the no-damage position from the screenshot. Public installers, website and release assets remain unchanged.

# Patch-Y beginner quick start for Windows

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

[Back to Lau Setup](../README.md) ·
[Full technical guide](PATCH-Y-DEVELOPMENT.md) ·
[Source layout](../patch-y/README.md)

You do not need to know Python programming to contribute a visual change.
Python runs the existing Patch-Y tools; you will use the guided launcher and
edit one small JSON manifest.

The tools never install files into a WoW client. Candidate MPQs are created
under the ignored `patch-y/.work` folder. In-game testing is a separate,
deliberate step using an isolated client.

## 1. Install the three requirements once

1. Install [GitHub Desktop](https://desktop.github.com/).
2. Install 64-bit Python 3.11 or newer from
   [python.org](https://www.python.org/downloads/windows/). On the first
   installer screen, select **Add python.exe to PATH**.
3. Obtain the x64 Unicode `StormLib.dll` from the official
   [StormLib 9.22 release](https://github.com/ladislav-zezula/StormLib/releases/tag/v9.22),
   which matches the version pinned in Patch-Y CI. Keep it in a separate tools
   folder, not in this repository and not in your WoW client. The launcher
   will ask you to select it.

You also need about 900 MB of temporary free space.

## 2. Fork and create a branch with GitHub Desktop

1. Open [CRSD-Lau/Lau-Setup](https://github.com/CRSD-Lau/Lau-Setup) and click
   **Fork**.
2. In your fork, click **Code**, then **Open with GitHub Desktop**.
3. Choose a local folder and click **Clone**.
4. In GitHub Desktop, select **Current branch** → **New branch**.
5. Use a focused name such as `visual/halion-cutter-width`.

Never make a contribution directly on `main`.

## 3. Start the guided helper

Open the cloned folder, open `tools`, and double-click
`Patch-Y-Start.cmd`. Choose **Check Python and StormLib**, then select your
`StormLib.dll` when prompted.

Use the same menu to:

1. Fetch the verified 3.0.9 baseline.
2. Inspect an edition.
3. Build candidates.
4. Verify candidates.
5. Prepare the Markdown and JSON proof for a pull request.

The first fetch downloads about 277 MB. Future commands reuse the verified
ignored cache.

## 4. Worked example: add one shared BLP texture

This example adds a new texture called `HalionCutterGuide.blp` to all six
editions. Substitute your own approved asset and internal MPQ path.

1. Put your finished file here:

   ```text
   patch-y/overlays/common/files/Spells/HalionCutterGuide.blp
   ```

2. In PowerShell, calculate its SHA-256:

   ```powershell
   (Get-FileHash -Algorithm SHA256 -LiteralPath '.\patch-y\overlays\common\files\Spells\HalionCutterGuide.blp').Hash.ToLower()
   ```

3. Open `patch-y/overlays/common/manifest.json`. Replace its empty
   `operations` array with this operation, inserting the hash printed above:

   ```json
   "operations": [
     {
       "action": "add",
       "servers": ["warmane"],
       "member": "Spells\\HalionCutterGuide.blp",
       "source": "files/Spells/HalionCutterGuide.blp",
       "sourceSha256": "paste-the-lowercase-sha256-here",
       "reason": "Add a reviewed Halion cutter guide texture for visual testing."
     }
   ]
   ```

4. Keep `warmane` only if that is the registered target for your change. If
   your evidence and test are for WoW Circle, use `wowcircle`. In the PR,
   separately state the exact server or realm/build you tested. Do not assume
   that timing, DBC values or visual radius match another target.
5. Start `Patch-Y-Start.cmd`, choose **Prepare pull-request proof**, enter the
   target and a label such as `halion-guide`, and wait for `PASS`.
6. The review files are:

   ```text
   patch-y/.work/patch-y-diff-warmane.md
   patch-y/.work/patch-y-diff-warmane.json
   ```

   Candidate MPQs stay under `patch-y/.work/candidate/warmane/` and must not
   be committed.

An `add` operation is appropriate only for a genuinely new MPQ member. To
replace an inherited member, copy `patch-y/examples/replace-texture.json` and
include the original member's `expectedBeforeSha256`. DBC files must use the
structured DBC operation example; opaque whole-table replacements are blocked.

## 5. Test without risking your normal client

1. Fully close WoW.
2. Make a separate test-client copy.
3. Back up and hash its existing Patch-Y files outside `Data`.
4. Install only the matching candidate in the root and active-locale Patch-Y
   destinations.
5. Log in and confirm your development label with `/pyversion`.
6. Test the named encounter, ability, difficulty, terrain, camera angles and
   movement on the exact server or realm/build named in the PR.
7. Capture screenshots or video, record what was not tested, then restore the
   original files.

A successful build proves archive scope. It does not prove that a visual is
correct in game.

## 6. Commit and open the pull request

In GitHub Desktop:

1. Review the changed files. Do not include `.cache`, `.work`, MPQs, clients,
   account data or SavedVariables.
2. Write a short summary and click **Commit to** your branch.
3. Click **Push origin**, then **Create Pull Request**.
4. Complete every Patch-Y field in the PR template. Include asset provenance,
   exact server or realm/build, affected editions, `/pyversion`, generated
   scope proof, screenshots/video, test-client details and anything not tested.

## Troubleshooting and glossary

The [technical guide](PATCH-Y-DEVELOPMENT.md#troubleshooting) contains fixes
for missing Python, StormLib loading and architecture errors, hash mismatches,
disk space and invalid paths. Its [glossary](PATCH-Y-DEVELOPMENT.md#glossary)
defines MPQ member, overlay, edition, server profile, DBC operation, scope
report and `/pyversion`.

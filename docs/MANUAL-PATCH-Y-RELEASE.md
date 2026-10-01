# Standalone Patch-Y release contract

Author: Neil Mitchell  
Creator: Neil Mitchell  
Last Modified By: Neil Mitchell

Neil requires manual Patch-Y downloads **every time the game version changes**, alongside Lau Setup. This is a mandatory release gate, not an optional follow-up. Installer-only releases reuse the existing game-version downloads.

## Required artifacts

Every published `payload-X.Y.Z` release must include:

- `Patch-Y-X.Y.Z-HD-New-Spells.zip`, including the required Patch-S companions.
- `Patch-Y-X.Y.Z-HD-Original-Spells.zip`.
- `Patch-Y-X.Y.Z-Non-HD.zip`.
- `SHA256SUMS-Patch-Y.txt` and `manual-downloads.json`.

Use the exact SHA-256/size-pinned catalog bytes. Do not rebuild game content, copy personal clients or increment the game version merely to package existing files. Keep Author, Creator and Last Modified By as Neil Mitchell. ZIP contents are allowlisted; guides retain community attribution, locale placement, model prerequisites and manual backup/restore instructions.

## Build and publish

The `Standalone Patch-Y downloads` GitHub Actions workflow runs when a game payload or stable installer release is published. It reads the released catalog. If the payload tag predates final public URLs, it resolves the matching final installer tag and requires unchanged game version, MPQ/part hashes, sizes and locale mapping. It builds all packages, verifies contents and metadata, uploads missing assets, downloads them again, and adds manual links to the game release's notes. It rejects different existing assets rather than overwriting published downloads. If the installer tag has not yet been published, the payload-triggered run fails safely; publishing the matching installer triggers a new attempt.

For backfills, retry after a failed run, or releases created with `GITHUB_TOKEN` (which do not trigger another workflow), explicitly dispatch:

```powershell
gh workflow run patch-y-manual.yml --repo CRSD-Lau/Lau-Setup --ref main -f release_tag=payload-X.Y.Z
```

Do not mark the game release complete until that run succeeds. Publication of hash-named installer parts alone is insufficient.

Local build and verification, using the final public catalog:

```powershell
python tools/package_patch_y_manual.py build --catalog build/catalog.json --output dist/manual-X.Y.Z --cache build/manual-cache --version X.Y.Z
python tools/package_patch_y_manual.py verify --catalog build/catalog.json --output dist/manual-X.Y.Z --version X.Y.Z
python tools/publish_patch_y_manual.py --catalog build/catalog.json --output dist/manual-X.Y.Z --repo CRSD-Lau/Lau-Setup --tag payload-X.Y.Z
```

`--payload-dir` may provide a local directory of existing hash-named parts; every part and assembled MPQ is still checked. No personal-client path is needed.

## Finish the public release

1. Confirm all three public ZIPs download and their bytes match the local checksums and catalog member hashes.
2. Update the manual install guide and current installer release notes with the new game download links. Preserve installer and game version separation and prior release notes.
3. Update the Wrath HD website manual downloads with `python sync_manual_downloads.py --version X.Y.Z`; keep `installer.upgradeRelease` and manual version in agreement. Run site tests and deploy to the existing Vercel project.
4. Verify the deployed desktop/mobile links and no-JavaScript fallback. Carry the direct manual download option into any user-authorized release announcement.
5. Record archive verification separately from gameplay acceptance. Unchanged packaging carries forward existing gameplay evidence; it does not establish new visual compatibility.

Adding manual packages for 3.1.0 makes **no DBC edits** and changes no MPQ bytes. Future game-content changes still require the existing record-level DBC changelog and validation gates.

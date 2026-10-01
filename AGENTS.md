# Lau Setup release requirements

Author: Neil Mitchell  
Creator: Neil Mitchell  
Last Modified By: Neil Mitchell

Preserve personal clients, unrelated patches, settings and active worktrees. Test installs only with isolated fixtures. Installer version and game version are separate.

Every game-version release must also publish standalone manual Patch-Y ZIPs for HD new spell visuals (with both required Patch-S companions), HD original spell visuals and Non-HD/SD. Package the exact catalog-pinned MPQ bytes. Publish checksums and a manifest, verify fresh public downloads, and update the manual guide, release notes and website links. See `docs/MANUAL-PATCH-Y-RELEASE.md`; do not call a game release complete with installer downloads alone. Installer-only releases reuse the existing game-version ZIPs.

For every future release, update DBC-CHANGELOG.md and add a DBC changes section to GitHub release notes. Log table, record ID, field name/index, old/new values, editions, reason and hash-backed evidence; explicitly say No DBC edits for installer-only or packaging-only releases.

Author, Creator and Last Modified By metadata must name Neil Mitchell. Preserve the original Patch-Y and community attribution. New gameplay acceptance is separate from packaging, CI and archive checks.

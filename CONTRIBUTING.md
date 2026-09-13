# Contributing to Lau Setup

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

Thanks for helping improve installation and recovery for the Wrath community.

## Report a problem

Use the [bug-report form](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose). Include the installer version, platform, client locale, selected visuals, expected behavior and steps to reproduce. For in-game issues, include `/pyversion`, the boss or ability, difficulty and a screenshot. Wine reports should include Wine and Wine Mono versions.

Remove account names, passwords, tokens and personal paths from screenshots or excerpts. Do not upload your client, WTF folder, SavedVariables or entire logs. Keep local backups if recovery is pending.

## Propose a change

Keep pull requests focused. Explain the user-visible problem, the change and the checks you ran. Test file operations only in isolated fixtures, never in an active personal game client.

Preserve the archive allowlist, hash checks, backup journals, process checks and cross-prefix locking. Do not change game payload records as part of a documentation or interface update.

The [technical reference](docs/TECHNICAL.md) explains the public build and the tests that require private local fixtures. Clearly separate a successful build, fixture testing and actual in-game validation in your PR.

## Artwork and attribution

Keep the established W-and-shield branding and upstream credits intact. Include the source and applicable permissions for proposed artwork. Do not introduce personal client state into public assets.

## DBC release records

Every game or installer release must update [DBC-CHANGELOG.md](DBC-CHANGELOG.md) and include a **DBC changes** section in its GitHub release notes. For actual DBC edits, list table, record ID, named field and zero-based index, old/new values, affected editions/locales, and reason, with before/after hashes and comparison evidence. For unchanged DBCs, explicitly record **No DBC edits**. Separate geometry, texture and installer edits from DBC changes. See the changelog for the required format and validation boundaries.

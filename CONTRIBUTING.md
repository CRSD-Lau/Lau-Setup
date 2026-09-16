# Contributing to Lau Setup

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

Thanks for helping improve installation and recovery for the Wrath community.

> **Installing for the first time?** Follow [Start here](START-HERE.txt) before collecting a bug report.

## Community roadmap

Follow the [Community roadmap](https://github.com/users/CRSD-Lau/projects/2) to see work as issues and pull requests automatically feed the board through **Backlog**, **Ready**, **In progress**, **Testing** and **Done**. **Testing** cards include acceptance checklists and collect the evidence needed to finish validation; use [Ideas](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas) to discuss proposals before filing an issue. [Release notes](https://github.com/CRSD-Lau/Lau-Setup/releases) remain the authority for what shipped in each version.

## Report a problem

Use the [bug-report form](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose). Include the installer version, platform, client locale, selected visuals, expected behavior and steps to reproduce. For in-game issues, include `/pyversion`, the boss or ability, difficulty and a screenshot. Wine reports should include Wine and Wine Mono versions.

Remove account names, passwords, tokens and personal paths from screenshots or excerpts. Do not upload your client, WTF folder, SavedVariables or entire logs. Keep local backups if recovery is pending.

## Propose a change

Start with [Known limitations and assumptions](KNOWN-LIMITATIONS.md). Use [Ideas](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas) for recommendations; identify any server, native-code or protected-action dependency before proposing an implementation.

Keep pull requests focused. Explain the user-visible problem, the change and the checks you ran. Test file operations only in isolated fixtures, never in an active personal game client.

Preserve the archive allowlist, hash checks, backup journals, process checks and cross-prefix locking. Do not change game payload records as part of a documentation or interface update.

The [technical reference](docs/TECHNICAL.md) explains the public build and the tests that require private local fixtures. Clearly separate a successful build, fixture testing and actual in-game validation in your PR.

For Patch-Y mechanics and visual work, beginners should start with the [Windows quick start](docs/PATCH-Y-QUICKSTART-WINDOWS.md); the [public Patch-Y development workflow](docs/PATCH-Y-DEVELOPMENT.md) is the full technical reference. Every operation must name its registered target, and the PR must identify the exact server or realm/build plus relevant database, timing or radius evidence. Submit declared source overlays and generated scope proof, not complete MPQs. CI rebuilds all affected editions from the hash-pinned 3.0.9 baseline and rejects undeclared member or DBC changes. A merged source PR is still a candidate until the normal in-game and release gates pass.

## Artwork and attribution

Keep the established W-and-shield branding and upstream credits intact. Include the source and applicable permissions for proposed artwork. Do not introduce personal client state into public assets.

Patch-Y includes inherited Blizzard, Andre, HD-client and Project Reforged assets. Do not claim inherited work as newly authored or commit extracted baseline trees. New binary assets need provenance and applicable redistribution permission.

## DBC release records

Every game or installer release must update [DBC-CHANGELOG.md](DBC-CHANGELOG.md) and include a **DBC changes** section in its GitHub release notes. For actual DBC edits, list table, record ID, named field and zero-based index, old/new values, affected editions/locales, and reason, with before/after hashes and comparison evidence. For unchanged DBCs, explicitly record **No DBC edits**. Separate geometry, texture and installer edits from DBC changes. See the changelog for the required format and validation boundaries.

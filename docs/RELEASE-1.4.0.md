# Lau Setup 1.4.0 — work in progress

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell

## Scope
Build the beginner-friendly wizard using Setup 1.1.7 as the reference for installation behavior: leave unrelated MPQs alone. This supersedes earlier requirements to scan or automatically remove renamed Lau patches. Retain current backup/recovery safeguards and the shared Windows/Linux ZIP.

## Required behavior
- Game folder → Options → Review and install → Finished; Next alone does not change files.
- Automatic interface-language detection, a persistent manual selector, case-insensitive game locale resolution, and installer version 1.4.0 separately from game 3.0.9 in the footer.
- Fixed Patch-Y HD / Non-HD based on the detected client.
- Separate optional checkboxes, initially off: Enhanced Consecration, Compatible WoW.exe + loading screens (one combined option), maps/minimaps, and New Spell Visuals (requires existing HD models).
- Merge Trimitor WDM Classic/TBC dungeon/raid and cave maps into Lau's maps option, including required WDM/!Astrolabe support files. Maps must work independently of loading screens and executable replacement.
- Review explicitly lists Patch-Y and all selected options; unchecked EXE/artwork remain unchanged. Explain replaced files are backed up in LauSetupBackups.
- Do not parse/classify arbitrary patches or remove renamed duplicate patches. Players manage their own renamed duplicates.
- Preserve the separately requested empty Patch-V backup exception. Nonempty V stays, with a nonblocking compatibility warning and no parsing.
- Preserve unrelated addons, custom files and SavedVariables. Selected WDM support files may be updated with verified backups; do not claim every addon file is untouched.
- One clean LauSetup.zip serves Windows and supported Linux/Wine; no duplicate platform download cards.

## Completion gates
- [ ] Final Windows and normal-user Wine transaction, recovery, option and language tests.
- [ ] Verify final packaged UI and shared ZIP.
- [ ] Verify map payload member parity, required addon dependencies, and map-only content separation.
- [ ] Andre/player testing: maps, dungeon/cave navigation, old combined Q compatibility, and chosen executable.
- [ ] Publish installer and verify downloads; retain draft PR until approved.
- [ ] Align repository documentation, changelogs, website sections and existing Discord release posts.

## Current status
In progress on draft PR #28. Test1 is older and does not implement this revised scope. Test2 and its download fix test3 were published as prereleases. Test4 combined EXE and loading screens. Test5 adds game 3.0.9, compact archives, the approved mockup layout, responsive option choices and installation progress; stable 1.4.0 is not released. Local map-content parity passed for all nine game locales; all 102 addon TOC/XML references resolve across 115 packaged files. New independent map install/restore and interruption regressions pass locally; final Windows/Wine/package checks are underway.

Patch-Y now reports 3.0.9, and all six archives are compacted before packaging. This saves 58,774,086 bytes in total while leaving player backups untouched. No Patch-Y DBC edits. The optional map pack introduces upstream map DBC overrides: do not describe this addition as having no DBC changes. The cave expansion is upstream beta and still needs in-game acceptance.

Keep this ticket In progress until release and public-surface verification are complete. The existing translation-rate-limit follow-up remains active. Prior website changes were blocked by automatic approval review; public website/Discord alignment is still pending.

# Raid visual release candidate

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

Status: local candidate built and validated on Windows, not published. Candidate versions: Lau Setup 1.5.0 / Patch-Y 3.1.0.

## Agreed scope

Neil clarified on 26 September 2026 that this release should carry his complete **Patch-Y**, not his wider HD client patch stack. It includes the existing Lau visuals plus his raid-tested Consecration, Marrowgar Coldflame, Blood Queen Lana'thel Swarming Shadows, Halion Meteor Strike trails, Gormok Fire Bomb, Jaraxxus Legion Flame and Acidmaw/Dreadscale Slime Pool.

Consecration is standard. The installer offers HD with or without the new-spell pack and Non-HD/SD, retaining edition-specific data. Legacy Consecration-On/Off catalog identifiers remain readable and both select the standard visuals in this release.

Also included in the candidate work: Caverns of Time map packaging correction, actionable client-folder errors, user-initiated redacted diagnostics, clearer current/upgrade/repair status, restoration of Halion tank-positioning marks, and a link to actual visual examples.

## Credits

**Lau / Lausudo — Neil Mitchell:** Lau-specific visual edits and integration, preservation of unrelated spell routes, HD/SD adaptations, release packaging, installer changes, map packaging correction and validation. The raid-tested configuration and release selection are Neil's.

**Suppository and the contributors listed in the supplied patch:** the imported visual source. The original description credits Suppository, Kupi, Thiesant, Rorifer, Loriendal, Sl1msh, Rexbe, Andre, Merfin, palms, Lau and an anonymous contributor. This release preserves those credits; it does not attribute every source asset to one person without evidence.

**Andre (andrecolacoml2):** the Halion tank-mark restoration supplied in [issue #39](https://github.com/CRSD-Lau/Lau-Setup/issues/39#issuecomment-5681283458). Its model and texture are identical to the public baseline; the supplied skin restores material batches without changing the breath-cone model.

Existing credits for the HD foundation, Project Reforged and Blizzard remain in the project. Contributor names describe actual contributions, not ownership of the entire inherited client.

## Validation and release gates

- Neil reported successful raiding with the personal HD build on 26 September. This validates that configuration; it does not certify newly restored Halion marks or the other editions.
- Three staged editions have exact archive-member and DBC comparisons against the hash-pinned public 3.0.9 baseline. Their HD new-spells edition matches the accepted personal archive apart from the supplied Halion skin and the new version label.
- Independent review confirmed the three-byte Halion skin change selects bounded material batches, with unchanged model geometry, texture and breath-cone files.
- Windows validation passed 80 installer cases, 72 real Patch-Y upgrade/restore cases, both-placement byte-repair checks in all three editions, and the full-size enGB map upgrade/restore test. The Python suite ran 74 cases with one archive-integration case skipped; the separate real archive builds and comparisons passed. [Validation record](VALIDATION-1.5.0-CANDIDATE.json).
- Wine runtime validation for this candidate remains pending because the Docker Linux engine was unavailable. The prior release's Wine baseline is not claimed as a new candidate pass.
- Caverns of Time map selection and Halion marks still require targeted in-game checks. HD spells-off and SD visual acceptance remain separate checks.
- Neil supplied the [Lady Deathwhisper forum ID in the HD Discord](https://discord.com/channels/858041817043042364/1352616642491842580) for Suppository's images. Setup links to that source directly. Discord access is required; the images have not been independently inspected from the currently logged-out browser session and are not presented as screenshots of every Lau-specific change.
- Publication follows the validated candidate, complete DBC change history, final credits, download guidance and release announcement.

No personal client, addon profiles, account data or settings are included in the release.

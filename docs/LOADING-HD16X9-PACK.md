# HD 16:9 loading-screen pack — 77 accepted backgrounds

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell

Neil requested crisp 16:9 loading artwork across the whole client, preserving every original composition without cropping, zooming or stretching. Extend the side scenery with AI where necessary, retaining the original style, subject proportions, logo and decorative bands.

## Source coverage

The inspected protected client supplied the source Q catalog, which contains 92 LoadingScreens rows mapping to 85 distinct backgrounds. All 85 paths resolve in the inspected archive set; 27 already have Wide routes. The source references prefer the existing HD Wide artwork where present and retain the base references for comparison. Texture storage dimensions are converted to their intended display proportions before editing: base 4:3 and existing Wide 16:10. Raw decodes are retained.

The complete inventory records competing archive payloads rather than treating filename order as proof of precedence. The shared 3.0.9 Q baseline SHA-256 is `d477b60836c37ccfabefc8186b0745484cefdcee74b3c6ba768fdcba9c59312e`. The shared 3.1.0 Q candidate SHA-256 is `aec7d51c5f77ab34a87d705564c718a6bbd9426daf5252a885f93442a4095534`. zhCN and zhTW use distinct Q archives so their 17 locale-specific base aliases remain byte-identical. Root and active-locale Q placements use the Q asset selected for the client's locale. [All locale hashes](dbc/loading-3.1.0.json).

The local review workspace is intentionally excluded from the public source package. Its relative evidence layout was:

- `inventory/generation-manifest.json`: 85 indexed source references, archive provenance and row mappings.
- `artwork-jobs.json` and `artwork/*/prompt.txt`: individual preservation prompts and provenance.
- `review.html`: source/candidate comparison page, including the eight original exceptions.
- `renderer/current-approved-renderer-plan.json`: current native rendering candidate and mechanical evidence.

## Rendering

The first installed native-framing experiment restored uncropped artwork but exposed the client's 16:10 Wide frame, producing side bars on Neil's 16:9 display. The ICC-only replacement was staged but never installed; it is superseded by this complete-pack request.

For an entirely 16:9 Wide asset set, the native renderer can use a 16:9 Wide aspect constant while retaining native full UV and aspect fitting. The verified candidate is SHA-256 `4218fef354f875d1d27aae9cc6a93c75aaadaa1f0beea1204172793cd39e0505`. Relative to the currently installed native-framing test (`a6767f7e…`), only three bytes differ. Both native geometry branches remain intact, and the archive-reserve fix remains unchanged.

The renderer proof was calibrated against the observed old 90%-width viewport on 16:9 and the stock full-frame 4:3 behavior. Its corrected harness executes the real normalized-aspect provider. An earlier experimental `64/27` constant was rejected after a bad emulator stub was identified; never package that executable. Neil subsequently confirmed the accepted 77-image set displays correctly in game at 16:9.

## Build, DBC changes and accepted coverage

`tools/build_loading_hd16x9_executable.py` produces the exact staged executable from one of two known input hashes. The reviewed build uses 77 images and intentionally retains the original routes for eight exceptions. It adds or replaces only the derived `*Wide.blp` members, changes `LoadingScreens.HasWideScreen` (zero-based field 3) from 0 to 1 on 61 rows, and preserves every row ID, name, path, string and other field. Original base artwork remains identical. [Exact row and archive evidence](dbc/loading-3.1.0.json).

Neil selected the built-in image tool for the full artwork run, accepting its observed 1672×941 output. Each final image records its actual native dimensions and passes individual visual review. No image API or API key is involved. Never describe the 4096×2048 BLP storage dimensions as native generated-art resolution.

The built-in image tool produced 77 reviewed backgrounds (1672×940 or 1672×941). Eight targets were rejected and keep their original artwork: BlackTemple (11), EasternKingdom (27), Kalimdor (40), Outland (55), PvpBattleground (57), Raid (59), RuinedCity (63), and Sunwell (70). Some of these originals can retain side bars. All 77 new images passed decode, opacity, dimension, SHA-256, prompt-provenance and Neil Mitchell metadata checks. Neil accepted their in-game appearance at 16:9. `artwork-progress.json` records exact coverage, and `review.html` compares each original with its candidate. No substitute images were silently supplied.

The accepted 77-image build produced read-back verified Q archives. The shared Q proof records 54 added Wide members, 26 replaced Wide members, 71 unchanged prior members, 92 checked DBC rows and 61 changed `HasWideScreen` fields. zhCN and zhTW preserve 17 additional original base aliases each; three original screens also use compatibility-padded Wide files. Loading-only install/restore fixtures passed full and partial installation, running-client refusal, unexpected-source refusal, automatic rollback after an interrupted replacement, and preservation of unrelated map files. The fixture checks are separate from Neil's in-game visual acceptance.

The accepted installation concerns only the compatible `WoW.exe`, root Q and active-locale Q. The eight original exceptions remain at their native behavior; no claim of a 16:9 rewrite is made for them. Other display ratios require their own visual acceptance. This release does not include a full HD client, personal addons or settings.

Issue #32 was closed following Neil's Caverns confirmation. Neil accepted the 77-image loading result in game; any issue status should reflect the published release record. Existing contributor credits remain, with Neil Mitchell credited for adaptation and integration; original Warcraft artwork and marks remain Blizzard's.

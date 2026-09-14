# Stable 1.4.0 final review

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell

The final wizard diff changes rendering/layout, text and translation bindings. It does not change the test5 installation engine, downloader or embedded 3.0.9 catalog. Folder placeholders remain separate from the actual selected path. Browse retains the normal folder dialog and validation. Language changes update placeholder/tooltips without changing client selection. Footer adapts at narrow widths; the native 100-preview matrix has no detected text/button clipping. Neil and Andre approved the Windows visual result.

Final Windows regression: 73 groups passed, including 108 locale/edition/map install plans, recovery/interruption guards, options, language switching and upgrades/no-op/exact rollback for all six actual 3.0.8 editions. The first attempt used an excessively long test-output root and hit Windows MAX_PATH; the same suite passed from a short isolated fixture root. This is recorded as a fixture limitation, not hidden as a successful first run.

Wine, source-package, public release and coordinated surface results are recorded in the stable VALIDATION.json. No personal client was modified. The previous review below is historical.

# Wizard 1.4.0 review

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell

Reviewed the wizard diff against the existing install/restore transaction. No
transaction scope, MPQ detection, payload bytes, path checks or commit guards
were changed. Next checks/prepares a plan and navigates; only Install upgrade
enters the download/transaction path. Restore remains reachable when WoW.exe
is missing. Manual language changes re-render the summary without changing
client locale or options.

Fixed during review: hidden progress control shifted auto-assigned layout
rows and clipped navigation; grid rows are now explicit. Restore captures
checkbox values on the UI thread and refreshes the plan/download display.
GUI tests now install a stable WinForms synchronization context and enable
cross-thread detection instead of allowing asynchronous test continuations
onto worker threads. Eight option combinations, all ten live interface
languages and Back/Next/install/restore passed on Windows. Wine release checks
and final package evidence are recorded separately in VALIDATION.json.

Public release and website/Discord verification remain required. This source
review is not an in-game acceptance result. Older review history follows.

---

# Installer review

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell

## Historical 1.2.0 validation evidence

Installer 1.2.0 validation recorded 62 regression groups on Windows and 62 on
Wine. The Wine run is staged: 35 groups ran before the busy-state completion
fix, then the affected GUI group and the remaining 26 ran after it, followed by
final localization and packaged-window checks. The evidence also records 50
Windows and 21 normal-user Wine interface states, 185 keys across ten bundled
interface languages, and 31 package, translation, and host tests. Game release
3.0.8, its nine locales, 28 game assets, and DBC data are unchanged. This is
installer validation; it does not certify every Linux distribution or in-game
encounter.

Reviewed the new application against the GStack review checklist, including an independent read-only security review. All identified implementation issues were addressed within the authorized installer work:

- A missing executable could prevent selecting the client for crash recovery. Folder selection now discovers and validates recovery records before inspecting WoW.exe. A GUI regression test covers the missing-executable case.
- Downloads occurred before the operation lock. One lease now covers the download cache through commit; pending recovery is checked inside that lease.
- Predictable writable temporaries could follow NTFS hardlinks. Journal and assembly temporaries now use GUID names with CreateNew. Resumed partial files are opened exclusively and their link count is checked before any truncation or write. An actual hardlink regression test proves the unrelated file remains unchanged.
- A tampered restore journal could create a lock under another root before validation. Size, location, root, locale, entries and scoped paths are now validated before acquiring the restore lock. A regression test proves no foreign lock is created.
- Interrupted restoration did not have its own resumable state. RESTORING is journaled before mutation and recognized throughout the UI and recovery path. Fault injection after every restore step passes.
- Installed/restored map options could remain stale in the UI. Client detection is refreshed after each successful operation. The GUI test installs the map selection, verifies its retained state, restores, and verifies the prior state.

The GitHub migration additionally pins the repository, release tag and file name in the embedded catalog. Redirects are followed manually so each HTTPS destination is checked before a request, including credentials and port checks. The old Google Drive HTML confirmation parser has been removed. Added tests cover catalog URL tampering, a redirected resumable transfer, and rejected redirect destinations.

An independent review of the migration found that Python optimization could remove publishing checks written as assertions. Upload, catalog-refresh and release-gate checks now raise explicit exceptions. The uploader also resolves each source and requires it to remain directly inside the payload directory. Publishing guard tests pass under `python -O` for file paths, sizes, hashes and remote URL/digest tampering.

Historical 2026-09-11 regression suite: `reports/tests-20260911-200603/results.json`; 38 test groups passed, including 108 actual fixture install/restore combinations, all commit/restore interruption points, path/junction/hardlink protection, process and file locks, corruption/drift, HTTP range handling, cancellation, offline assembly, and GUI install/restore using the real versioned executable. It is retained as prior-release evidence, not the latest complete 1.2.0 suite.

The 1.0.1 UI review covers brighter supporting text, larger footer text and custom disabled-control painting. Native Enabled semantics remain in place; only disabled appearance is drawn manually. The initial, ready and busy Windows previews were visually inspected. Core.cs, Downloader.cs and all game payloads remain byte-identical to v1.0.0. Its game/network evidence is retained; the Windows regression suite is rerun for this update. The Wine feasibility probe did not pass form construction and does not establish platform support.

Publication checks and final binary metadata are separate gates. See the release VALIDATION.json for evidence scope, including which checks were retained from the unchanged game baseline.

## Installer 1.1.0

The Wine implementation followed a three-opinion Council and two peer reviews.
It keeps the C# transaction engine and requires a live authenticated Linux
helper for Wine path inspection, host process checks and cross-prefix locking.
The helper rejects links, ambiguous casing, restricted process visibility and
unsupported filesystems. Wine drive mappings are accepted only after native
target inspection. The process policy conservatively requires all WoW
instances to be closed. Repeated checks reduce races; they do not lock out
unrelated programs or eliminate hostile concurrent filesystem changes.

The focused implementation review found nested mount coverage and lock release
after a root rename gaps. Both were fixed: managed paths and their nearest
existing ancestors must stay on the client's local filesystem, and release
uses the saved native path and token without requiring the root to still exist.
The corresponding native tests pass.

Free-space checks now query the actual Linux cache and client filesystems,
instead of Wine's mapped drive root. Actual Wine download and install tests
with zero reported free space reject the operation and preserve original files.

Validation includes 38 groups on Windows and 38 on Wine, 15 native helper tests,
8 Wine safety cases including two prefixes and helper loss after a move, a
fresh anonymous GitHub install/rollback under Wine, and a normal-user launcher
and fixture transaction. The W-and-shield ICO is copied byte for byte from the
existing release site's favicon. UI snapshots cover initial, ready and busy
states; the Windows prerequisite branch was reviewed and the installed-runtime
path exercised. No Windows machine lacking .NET was modified for a test.
The final code also repeats core installation and exact rollback with the
previously downloaded and rehashed GitHub payload bytes.

## Setup 1.1.7 review

Reviewed the current diff for path scope, local-source trust, download selection, preflight/commit drift checks, transaction backups and rollback compatibility. No unresolved findings. Local reuse is limited to the catalog-matching root/active-locale S pair; disabled files move through the existing verified backup journal. Both platforms passed 50 regression groups and actual release-file on/off/on with exact stacked rollback. No game payload changes.


## Setup 1.1.8 review

Reviewed the managed MPQ reader for bounds, integer overflow, read-only file access, root/active-locale scope, false positives from shared DBCs, candidate limits, cancellation and transaction ordering. Added a recheck after staging and a regression for a conflict introduced during staging. Invalid archive errors name the affected file. No new native dependency, extraction, archive mutation or expanded write allowlist is introduced. See [scan coverage and limits](docs/MPQ-SCANNING.md) and the release validation report.

## 1.2.1 scanner review

The table reader uses bounded chunks and continuous cipher state rather than loading the full table or collecting every hash in a set. Every table entry is still validated. Current validation is in docs/RELEASE-1.2.1.md and the release VALIDATION.json; older results above retain their original scope.

## 1.3.0 automatic-backup review

Three independent reviews and two peer reviews selected the existing verified transaction for recognized extra patches. Scope guards protect stock archives, unrelated files and inactive locales. Full-set revalidation precedes even no-op completion; pending recovery keeps priority in the interface. Regression coverage includes changed files, forged journals, cancellation, interrupted moves, historical catalog recovery and GUI install/restore. See docs/RELEASE-1.3.0.md for release evidence.

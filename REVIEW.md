# Installer review

Author: Neil Mitchell  
Creator: Neil Mitchell  
Last Modified By: Neil Mitchell

Reviewed the new application against the GStack review checklist, including an independent read-only security review. All identified implementation issues were addressed within the authorized installer work:

- A missing executable could prevent selecting the client for crash recovery. Folder selection now discovers and validates recovery records before inspecting WoW.exe. A GUI regression test covers the missing-executable case.
- Downloads occurred before the operation lock. One lease now covers the download cache through commit; pending recovery is checked inside that lease.
- Predictable writable temporaries could follow NTFS hardlinks. Journal and assembly temporaries now use GUID names with CreateNew. Resumed partial files are opened exclusively and their link count is checked before any truncation or write. An actual hardlink regression test proves the unrelated file remains unchanged.
- A tampered restore journal could create a lock under another root before validation. Size, location, root, locale, entries and scoped paths are now validated before acquiring the restore lock. A regression test proves no foreign lock is created.
- Interrupted restoration did not have its own resumable state. RESTORING is journaled before mutation and recognized throughout the UI and recovery path. Fault injection after every restore step passes.
- Installed/restored map options could remain stale in the UI. Client detection is refreshed after each successful operation. The GUI test installs the map selection, verifies its retained state, restores, and verifies the prior state.

The GitHub migration additionally pins the repository, release tag and file name in the embedded catalog. Redirects are followed manually so each HTTPS destination is checked before a request, including credentials and port checks. The old Google Drive HTML confirmation parser has been removed. Added tests cover catalog URL tampering, a redirected resumable transfer, and rejected redirect destinations.

An independent review of the migration found that Python optimization could remove publishing checks written as assertions. Upload, catalog-refresh and release-gate checks now raise explicit exceptions. The uploader also resolves each source and requires it to remain directly inside the payload directory. Publishing guard tests pass under `python -O` for file paths, sizes, hashes and remote URL/digest tampering.

Latest complete regression suite: `reports/tests-20260911-154011/results.json`; 38 test groups passed, including 108 actual fixture install/restore combinations, all commit/restore interruption points, path/junction/hardlink protection, process and file locks, corruption/drift, HTTP range handling, cancellation, offline assembly, and GUI install/restore using the real versioned executable.

Publication checks, final binary metadata and full native runtime results are separate release gates. See WORK.md for their current status.

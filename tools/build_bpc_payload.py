"""Build six scoped BPC static-floor-marker Patch-Y archives.

Only the BPC middle-section root/group WMOs and private marker assets are
added.  No DBC, spell, executable, account, or SavedVariables content changes.
Author/Creator/Modifier: Neil Mitchell.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

from range_mpq import add_or_replace, dll, opened, snapshot


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PRIVATE_PREFIX = "Spells\\Lau_BPC_FloorMarkers"
WMO_PREFIX = "World\\WMO\\Dungeon\\IcecrownRaid"
MARKER_LABELS = tuple([f"M{index}" for index in range(1, 11)] + [f"H{index}" for index in range(1, 6)] + [f"R{index}" for index in range(1, 11)])
EXPECTED_MEMBERS = {
    *(f"{PRIVATE_PREFIX}\\{label}{suffix}" for label in MARKER_LABELS for suffix in (".m2", "00.skin", ".blp")),
    f"{WMO_PREFIX}\\IcecrownRaid_middle_section.wmo",
    f"{WMO_PREFIX}\\IcecrownRaid_middle_section_023.wmo",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def reset(path: Path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def updates():
    model_root = DIST / "model"
    wmo_root = DIST / "wmo"
    result = {}
    for path in model_root.rglob("*"):
        if path.is_file():
            result[str(path.relative_to(model_root)).replace("/", "\\")] = path.read_bytes()
    for path in wmo_root.rglob("*"):
        if path.is_file():
            result[str(path.relative_to(wmo_root)).replace("/", "\\")] = path.read_bytes()
    if set(result) != EXPECTED_MEMBERS:
        raise ValueError(f"Unexpected BPC payload member set: {sorted(result)}")
    return result


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: build_bpc_payload.py BASELINE_DIRECTORY CATALOG_JSON")
    baseline_dir, catalog_path = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    catalog = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
    baseline_catalog = json.loads(json.dumps(catalog))
    editions = sorted(key for key in catalog["Assets"] if key.startswith("Y-"))
    if len(editions) != 6:
        raise ValueError(f"Expected six Y editions, got {editions}")
    payload_dir, work_dir = DIST / "payload", DIST / "payload-work"
    reset(payload_dir)
    reset(work_dir)
    member_updates = updates()
    results = []
    for edition in editions:
        baseline = baseline_dir / f"{edition}.mpq"
        expected = baseline_catalog["Assets"][edition]
        baseline_bytes = baseline.read_bytes()
        if len(baseline_bytes) != expected["Bytes"] or digest(baseline_bytes) != expected["Sha256"]:
            raise ValueError(f"Stable 3.0.8 baseline mismatch: {edition}")
        before = snapshot(baseline)
        collisions = sorted(member for member in member_updates if member in before)
        if collisions:
            raise ValueError(f"BPC test unexpectedly overwrites baseline members: {collisions}")
        target = payload_dir / f"{edition}.mpq"
        shutil.copy2(baseline, target)
        archive = opened(target, 0)
        try:
            for index, (member, data) in enumerate(sorted(member_updates.items())):
                local = work_dir / f"{edition}-{index}.bin"
                local.write_bytes(data)
                add_or_replace(archive, local, member)
                local.unlink()
        finally:
            dll.SFileCloseArchive(archive)
        after = snapshot(target)
        wanted = dict(before)
        wanted.update(member_updates)
        if after != wanted:
            raise AssertionError(f"Exact MPQ readback failed for {edition}")
        output_bytes = target.read_bytes()
        output_hash = digest(output_bytes)
        output_part = payload_dir / f"{output_hash}.bin"
        shutil.copy2(target, output_part)
        catalog["Assets"][edition] = {
            "Id": edition, "Sha256": output_hash, "Bytes": len(output_bytes),
            "Parts": [{"Sha256": output_hash, "Bytes": len(output_bytes), "FileName": output_part.name, "Url": None}],
        }
        results.append({
            "edition": edition,
            "baseline_archive_sha256": digest(baseline_bytes),
            "output_archive_sha256": output_hash,
            "output_archive_bytes": len(output_bytes),
            "added": sorted(member_updates),
            "added_member_hashes": {member: digest(data) for member, data in sorted(member_updates.items())},
            "changed_existing_members": [],
            "unrelated_members_byte_identical": True,
            "archive_snapshot_readback_exact": True,
        })
        print(f"PASS exact BPC scope/readback {edition} -> {output_hash}")
    catalog["PublicReady"] = False
    (DIST / "catalog.json").write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    (DIST / "baseline.json").write_text(json.dumps(baseline_catalog, indent=2) + "\n", encoding="utf-8")
    validation = {
        "Author": "Neil Mitchell", "Creator": "Neil Mitchell", "LastModifiedBy": "Neil Mitchell",
        "prototype": "BPC fixed floor-marker Test 3",
        "no_dbc_edits": True,
        "no_spell_or_gameplay_edits": True,
        "scope": "BPC middle-section group 023 plus 25 private muted one-yard labelled marker models",
        "labelled_markers": list(MARKER_LABELS),
        "position_source": "supplied BPC 25-player layout image",
        "marker_count": 25,
        "position_separation": json.loads((DIST / "bpc-floor-marker-separation.json").read_text(encoding="utf-8")),
        "build_dependency": {
            "stormlib_sha256": digest(Path(os.environ["STORMLIB_DLL"]).read_bytes()),
            "stormlib_embedded_in_payload": False,
        },
        "results": results,
    }
    (DIST / "scope-validation.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

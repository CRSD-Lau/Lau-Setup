"""Build Setup 1.5.0 / game 3.1.0 loading assets from hash-pinned inputs.

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell

Inputs are read-only. Pass a directory with core-<locale>.mpq for all nine
locales, the approved 77-screen candidate MPQ, and the approved WoW.exe.
The output directory must be new and must not contain any input file.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import shutil
import struct
from pathlib import Path

from PIL import Image, PngImagePlugin

from build_caverns_release import Mpq, LOCALES, member_hashes
from loading_release_codec import (
    META, TABLE, assert_blp, encode_blp, normalized_path,
    parse_loading_dbc, wide_member_path,
)

SOURCE_HASHES = {
    "deDE": "d477b60836c37ccfabefc8186b0745484cefdcee74b3c6ba768fdcba9c59312e",
    "enUS": "d477b60836c37ccfabefc8186b0745484cefdcee74b3c6ba768fdcba9c59312e",
    "esES": "d477b60836c37ccfabefc8186b0745484cefdcee74b3c6ba768fdcba9c59312e",
    "esMX": "d477b60836c37ccfabefc8186b0745484cefdcee74b3c6ba768fdcba9c59312e",
    "frFR": "d477b60836c37ccfabefc8186b0745484cefdcee74b3c6ba768fdcba9c59312e",
    "koKR": "d477b60836c37ccfabefc8186b0745484cefdcee74b3c6ba768fdcba9c59312e",
    "ruRU": "d477b60836c37ccfabefc8186b0745484cefdcee74b3c6ba768fdcba9c59312e",
    "zhCN": "6cc47ec31ac489149577d491aa3e2baa42d0894af6786616a40d4a5813720f4a",
    "zhTW": "962577c0d1206222fb581a8bfe38077e2b7fdd9211ec9c810ef6560d0241360a",
}
APPROVED_CANDIDATE_SHA256 = "aec7d51c5f77ab34a87d705564c718a6bbd9426daf5252a885f93442a4095534"
APPROVED_CANDIDATE_PROOF_SHA256 = "d1d9c8a0a9f5dae149f26fe7589a30598a5ac2fe3aa85e0afcac7b4d3a26f5ee"
APPROVED_EXE_SHA256 = "4218fef354f875d1d27aae9cc6a93c75aaadaa1f0beea1204172793cd39e0505"
APPROVED_ARTWORK_MANIFEST_SHA256 = "b20934cdf6aa2ee181f3c34881c85da6b000ad26731f434e9c7687cf00503f63"
MISSING_INDICES = {11, 27, 40, 55, 57, 59, 63, 70}
FALLBACK_NAMES = {
    "loadscreenblacktemple.blp",           # 11
    "loadscreenpvpbattleground.blp",        # 57
    "loadscreenraid.blp",                   # 59
    "loadscreenruinedcity.blp",             # 63
    "loadscreensunwell.blp",                # 70
}
COMPAT_NAMES = {
    "loadscreeneasternkingdom.blp": 27,
    "loadscreenkalimdor.blp": 40,
    "loadscreenoutland.blp": 55,
}
TABLE_KEY = TABLE.lower()


def digest_file(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_file(path: Path, expected: str) -> None:
    if not path.is_file() or digest_file(path) != expected:
        raise ValueError(f"Hash-pinned input differs: {path.name}")


def approved_artwork_provenance(path: Path) -> list[dict]:
    check_file(path, APPROVED_ARTWORK_MANIFEST_SHA256)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    entries = manifest.get("entries")
    if not isinstance(entries, list) or len(entries) != 77 or manifest.get("approved_count") != 77:
        raise ValueError("Approved artwork manifest lacks 77 entries")
    expected = set(range(85)) - MISSING_INDICES
    if {entry.get("index") for entry in entries} != expected:
        raise ValueError("Approved artwork indices differ")
    result = []
    for entry in sorted(entries, key=lambda item: item["index"]):
        dimensions = entry.get("native_dimensions")
        png_hash = entry.get("sha256")
        if entry.get("approved") is not True or not isinstance(dimensions, list) or len(dimensions) != 2 or not all(isinstance(value, int) and value > 0 for value in dimensions) or not isinstance(png_hash, str) or len(png_hash) != 64:
            raise ValueError(f"Approved artwork entry {entry.get('index')} invalid")
        result.append({"index": entry["index"], "nativeDimensions": dimensions,
                       "approvedPngSha256": png_hash})
    return result


def verify_approved_candidate_proof(path: Path) -> None:
    check_file(path, APPROVED_CANDIDATE_PROOF_SHA256)
    proof = json.loads(path.read_text(encoding="utf-8"))
    if (proof.get("candidate_q_sha256") != APPROVED_CANDIDATE_SHA256 or
        proof.get("generated_entries") != 77 or
        len(proof.get("compatibility_wide_assets", [])) != 3 or
        proof.get("dbc", {}).get("all_ids_names_paths_other_fields_preserved") is not True):
        raise ValueError("Approved candidate proof does not bind the accepted 77+3 assets and DBC")


def row_map(data: bytes) -> dict[int, dict]:
    rows = parse_loading_dbc(data)
    if len(rows) != 92 or len({normalized_path(row["path"], "DBC") for row in rows}) != 85:
        raise ValueError("LoadingScreens coverage differs from 92 rows / 85 paths")
    return {row["id"]: row for row in rows}


def table_changes(old: bytes, new: bytes) -> list[dict]:
    before, after = row_map(old), row_map(new)
    if before.keys() != after.keys() or len(old) != len(new):
        raise ValueError("DBC IDs or length changed")
    changed = []
    allowed_bytes = set()
    for row_id, original in before.items():
        current = after[row_id]
        if any(original[key] != current[key] for key in ("index", "offset", "name", "path")):
            raise ValueError(f"DBC row {row_id} identity changed")
        name = Path(original["path"]).name.lower()
        expected = original["flag"] if name in FALLBACK_NAMES or name in COMPAT_NAMES else 1
        if current["flag"] != expected:
            raise ValueError(f"DBC row {row_id} HasWideScreen mismatch")
        if current["flag"] != original["flag"]:
            changed.append({"recordId": row_id, "field": "HasWideScreen", "fieldIndex": 3,
                            "old": original["flag"], "new": current["flag"]})
            allowed_bytes.update(range(original["offset"] + 12, original["offset"] + 16))
    if any(old[i] != new[i] for i in range(len(old)) if i not in allowed_bytes):
        raise ValueError("DBC changed outside approved HasWideScreen fields")
    return sorted(changed, key=lambda item: item["recordId"])


def extract_candidate(mpq: Mpq, source: Path, candidate: Path, output: Path,
                      reuse_assets: Path | None):
    english = member_hashes(mpq, source)
    approved = member_hashes(mpq, candidate)
    if english.keys() - approved.keys():
        raise ValueError("Approved candidate dropped an English member")
    changed = {key for key in english.keys() & approved.keys() if english[key] != approved[key]}
    added = approved.keys() - english.keys()
    wide_keys = (changed | added) - {TABLE_KEY}
    if len(wide_keys) != 80 or TABLE_KEY not in changed or any(not key.endswith("wide.blp") for key in wide_keys):
        raise ValueError("Approved candidate is not the 80-Wide/one-DBC approved delta")
    archive = mpq.open(candidate)
    original = mpq.open(source)
    try:
        old_table, new_table = mpq.read(original, TABLE), mpq.read(archive, TABLE)
        dbc_changes = table_changes(old_table, new_table)
        rows = row_map(old_table)
        expected_wide = {normalized_path(wide_member_path(row["path"]), "Wide") for row in rows.values()
                         if Path(row["path"]).name.lower() not in FALLBACK_NAMES}
        if wide_keys != expected_wide:
            raise ValueError("Approved Wide members do not cover exactly the 77 new and three compatibility paths")
        asset_dir = output / "assets"
        asset_dir.mkdir()
        assets = {}
        for index, key in enumerate(sorted(wide_keys)):
            target = asset_dir / f"{index:03d}.blp"
            previous = reuse_assets / target.name if reuse_assets else None
            if previous and previous.is_file():
                if digest_file(previous) != approved[key]:
                    raise ValueError(f"Reused approved BLP {target.name} hash differs")
                shutil.copyfile(previous, target)
            else:
                blob = mpq.read(archive, mpq.names(archive)[key])
                assert_blp(blob)
                target.write_bytes(blob)
            assets[key] = target
        if {digest_file(asset) for asset in assets.values()} != {approved[key] for key in wide_keys}:
            raise ValueError("Extracted approved BLP hashes differ")
        return assets, old_table, new_table, dbc_changes, english, approved
    finally:
        mpq.close_archive(original)
        mpq.close_archive(archive)


def pad_locale_wide(blob: bytes, destination: Path) -> dict:
    """Keep the locale's complete original 16:10 artwork at 90% canvas width."""
    with Image.open(io.BytesIO(blob)) as image:
        image.load()
        native = list(image.size)
        picture = image.convert("RGB").resize((2304, 1440), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (2560, 1440), (0, 0, 0))
    canvas.paste(picture, (128, 0))
    meta = PngImagePlugin.PngInfo()
    for key, value in META.items():
        meta.add_text(key, value)
    png = destination.with_suffix(".png")
    canvas.save(png, pnginfo=meta)
    with Image.open(png) as check:
        check.load()
        if check.size != (2560, 1440) or check.crop((128, 0, 2432, 1440)).tobytes() != picture.tobytes():
            raise ValueError("Locale compatibility canvas failed readback")
        if check.getpixel((0, 720)) != (0, 0, 0) or check.getpixel((2559, 720)) != (0, 0, 0):
            raise ValueError("Locale compatibility bars are not black")
    png_hash = digest_file(png)
    converted = encode_blp(png, png_hash)
    assert_blp(converted)
    destination.write_bytes(converted)
    return {"originalWideSha256": digest(blob), "originalStorageDimensions": native,
            "canvasDimensions": [2560, 1440], "pictureBox": [128, 0, 2432, 1440],
            "canvasPngSha256": png_hash, "wideSha256": digest(converted)}


def copy_english_locale(locale: str, source: Path, candidate: Path, output: Path,
                        original_table: bytes, changed_table: bytes, changes: list[dict],
                        before: dict, after: dict) -> dict:
    if SOURCE_HASHES[locale] != SOURCE_HASHES["enUS"]:
        raise ValueError("English copy requires byte-identical source MPQ")
    destination = output / f"patch-{locale}-q.mpq"
    shutil.copyfile(candidate, destination)
    check_file(destination, APPROVED_CANDIDATE_SHA256)
    changed_existing = {key for key in before.keys() & after.keys() if before[key] != after[key]}
    added = after.keys() - before.keys()
    if (len(added) != 54 or len(changed_existing) != 27 or
        any(key != TABLE_KEY and not key.endswith("wide.blp") for key in changed_existing)):
        raise ValueError("Approved English member delta differs")
    if table_changes(original_table, changed_table) != changes or after[TABLE_KEY] != digest(changed_table):
        raise ValueError("Approved English DBC change differs")
    return {"source": source.name, "sourceSha256": SOURCE_HASHES[locale],
            "output": destination.name, "bytes": destination.stat().st_size,
            "sha256": APPROVED_CANDIDATE_SHA256, "sourceMembers": len(before), "outputMembers": len(after),
            "addedWideMembers": len(added), "replacedWideMembers": len(changed_existing - {TABLE_KEY}),
            "unchangedPriorMembers": len(before) - len(changed_existing),
            "unchangedPriorMembersVerified": True, "chineseBaseAliases": {},
            "chineseBaseAliasesByteIdentical": True,
            "dbcBeforeSha256": digest(original_table), "dbcAfterSha256": digest(changed_table),
            "dbcChangedRows": changes, "compatibilityWide": {}, "index57NativeFallback": True}


def create_locale(mpq: Mpq, locale: str, source: Path, assets: dict,
                  table: bytes, output: Path, expected_changes: list[dict], english_members: dict) -> dict:
    before = member_hashes(mpq, source)
    locale_unique = before.keys() - english_members.keys()
    if locale in ("zhCN", "zhTW"):
        if len(locale_unique) != 17 or any(not key.endswith(".blp") or key.endswith("wide.blp") for key in locale_unique):
            raise ValueError(f"{locale} Chinese base aliases differ from the expected 17")
    elif locale_unique:
        raise ValueError(f"{locale} has unexpected members beyond English source")
    source_archive = mpq.open(source)
    names = mpq.names(source_archive)
    original_table = mpq.read(source_archive, TABLE)
    source_changes = table_changes(original_table, table)
    if source_changes != expected_changes:
        mpq.close_archive(source_archive)
        raise ValueError(f"{locale} source DBC differs from approved row changes")
    local_assets = dict(assets)
    compatibility = {}
    paths = {normalized_path(row["path"], "DBC"): row["path"] for row in row_map(original_table).values()}
    canonical_wide = {normalized_path(wide_member_path(path), "Wide"): wide_member_path(path)
                      for path in paths.values()}
    if locale in ("zhCN", "zhTW"):
        for basename, index in COMPAT_NAMES.items():
            base = next(path for path in paths.values() if Path(path).name.lower() == basename)
            member = wide_member_path(base)
            key = normalized_path(member, "locale Wide")
            if key not in names:
                mpq.close_archive(source_archive)
                raise ValueError(f"{locale} lacks original Wide for compatibility index {index}")
            old_blob = mpq.read(source_archive, names[key])
            target = output / "assets" / f"{locale}-{index:03d}.blp"
            compatibility[str(index)] = pad_locale_wide(old_blob, target)
            local_assets[key] = target
    destination = output / f"patch-{locale}-q.mpq"
    table_file = output / "assets" / f"{locale}-LoadingScreens.dbc"
    table_file.write_bytes(table)
    archive = mpq.create(destination, 1 << math.ceil(math.log2(len(names) + len(assets) + 8)))
    temp = output / "assets" / f"{locale}-member.tmp"
    try:
        for key, name in sorted(names.items()):
            if key == TABLE_KEY:
                mpq.add(archive, table_file, name)
            elif key in local_assets:
                mpq.add(archive, local_assets[key], name)
            else:
                temp.write_bytes(mpq.read(source_archive, name))
                mpq.add(archive, temp, name)
        for key, asset in sorted(local_assets.items()):
            if key not in names:
                mpq.add(archive, asset, canonical_wide[key])
    finally:
        mpq.close_archive(archive)
        mpq.close_archive(source_archive)
        temp.unlink(missing_ok=True)
    after = member_hashes(mpq, destination)
    expected_keys = before.keys() | local_assets.keys()
    if after.keys() != expected_keys:
        raise ValueError(f"{locale} output member set differs")
    allowed = set(local_assets) | {TABLE_KEY}
    unchanged = before.keys() - allowed
    if any(before[key] != after[key] for key in unchanged):
        raise ValueError(f"{locale} changed an unrelated or localized member")
    if any(before[key] != after[key] for key in locale_unique):
        raise ValueError(f"{locale} changed a Chinese base alias")
    if any(after[key] != digest_file(asset) for key, asset in local_assets.items()):
        raise ValueError(f"{locale} Wide readback mismatch")
    if after[TABLE_KEY] != digest(table):
        raise ValueError(f"{locale} DBC readback mismatch")
    check = mpq.open(destination)
    try:
        changes = table_changes(original_table, mpq.read(check, TABLE))
    finally:
        mpq.close_archive(check)
    if changes != expected_changes:
        raise ValueError(f"{locale} DBC field readback mismatch")
    original_wide_57 = next(wide_member_path(row["path"]) for row in row_map(original_table).values()
                            if Path(row["path"]).name.lower() == "loadscreenpvpbattleground.blp")
    if normalized_path(original_wide_57, "57 Wide") in after:
        raise ValueError(f"{locale} index 57 Wide must remain absent")
    return {"source": source.name, "sourceSha256": SOURCE_HASHES[locale],
            "output": destination.name, "bytes": destination.stat().st_size,
            "sha256": digest_file(destination), "sourceMembers": len(before), "outputMembers": len(after),
            "addedWideMembers": len(after.keys() - before.keys()),
            "replacedWideMembers": len({key for key in before.keys() & local_assets.keys() if before[key] != after[key]}),
            "unchangedPriorMembers": len(unchanged), "unchangedPriorMembersVerified": True,
            "chineseBaseAliases": {key: before[key] for key in sorted(locale_unique)},
            "chineseBaseAliasesByteIdentical": True,
            "dbcBeforeSha256": digest(original_table), "dbcAfterSha256": after[TABLE_KEY],
            "dbcChangedRows": changes, "compatibilityWide": compatibility,
            "index57NativeFallback": True}


def build(args) -> dict:
    source_dir, candidate, candidate_proof, exe, artwork_manifest, output = (path.resolve() for path in
        (args.source_dir, args.approved_candidate, args.approved_candidate_proof,
         args.approved_exe, args.approved_artwork_manifest, args.output))
    reuse_assets = args.reuse_assets_dir.resolve() if args.reuse_assets_dir else None
    if output.exists() or any(output == path or output in path.parents for path in (source_dir, candidate, exe, artwork_manifest)):
        raise ValueError("Output must be fresh and must not contain an input")
    if source_dir.name.lower() == "data" and source_dir in output.parents:
        raise ValueError("Output must not be inside a client Data directory")
    sources = {locale: source_dir / f"core-{locale}.mpq" for locale in LOCALES}
    for locale, path in sources.items():
        check_file(path, SOURCE_HASHES[locale])
    check_file(candidate, APPROVED_CANDIDATE_SHA256)
    check_file(exe, APPROVED_EXE_SHA256)
    verify_approved_candidate_proof(candidate_proof)
    artwork = approved_artwork_provenance(artwork_manifest)
    mpq = Mpq(args.stormlib)
    output.mkdir(parents=True)
    assets, old_table, table, changes, english_members, candidate_members = extract_candidate(
        mpq, sources["enUS"], candidate, output, reuse_assets)
    results = {}
    for locale in LOCALES:
        if locale in ("zhCN", "zhTW"):
            results[locale] = create_locale(mpq, locale, sources[locale], assets, table, output, changes, english_members)
        else:
            results[locale] = copy_english_locale(locale, sources[locale], candidate, output,
                                                  old_table, table, changes, english_members, candidate_members)
        check_file(sources[locale], SOURCE_HASHES[locale])
    staged_exe = output / "WoW.exe"
    shutil.copyfile(exe, staged_exe)
    check_file(staged_exe, APPROVED_EXE_SHA256)
    check_file(candidate, APPROVED_CANDIDATE_SHA256)
    report = {**META, "gameVersion": "3.1.0", "status": "MPQ_MEMBER_AND_DBC_READBACK_PASS",
              "acceptedInGame": "77 new screens approved by user in English client",
              "builder": "tools/build_loading_release.py",
              "inputs": {"approvedCandidate": candidate.name, "approvedCandidateSha256": APPROVED_CANDIDATE_SHA256,
                         "approvedCandidateProof": candidate_proof.name,
                         "approvedCandidateProofSha256": APPROVED_CANDIDATE_PROOF_SHA256,
                         "approvedExecutable": exe.name, "approvedExecutableSha256": APPROVED_EXE_SHA256,
                         "approvedArtworkManifest": artwork_manifest.name,
                         "approvedArtworkManifestSha256": APPROVED_ARTWORK_MANIFEST_SHA256,
                         "sourceMpqSha256": SOURCE_HASHES},
              "loadingScenes": {"totalDistinct": 85, "newWideApproved": 77,
                                "originalPreserved": [11, 27, 40, 55, 57, 59, 63, 70],
                                "compatibilityPadded": [27, 40, 55], "missingNativeWide": [57],
                                "newWideStorageDimensions": [4096, 2048],
                                "nativeArtwork": artwork,
                                "storageDimensions": [4096, 2048]},
              "dbc": {"table": "LoadingScreens", "field": "HasWideScreen", "fieldIndex": 3,
                      "beforeSha256": results["enUS"]["dbcBeforeSha256"],
                      "afterSha256": digest(table), "changedRows": changes,
                      "idsNamesPathsAndOtherFieldsUnchanged": True},
              "outputs": {"executable": {"file": staged_exe.name, "bytes": staged_exe.stat().st_size,
                                         "sha256": APPROVED_EXE_SHA256}, "locales": results}}
    (output / "proof.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--approved-candidate", type=Path, required=True)
    parser.add_argument("--approved-candidate-proof", type=Path, required=True)
    parser.add_argument("--approved-exe", type=Path, required=True)
    parser.add_argument("--approved-artwork-manifest", type=Path, required=True)
    parser.add_argument("--stormlib", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--reuse-assets-dir", type=Path,
                        help="Optional prior extraction: each asset is reused only after candidate-member SHA-256 matches")
    result = build(parser.parse_args())
    print(json.dumps({"status": result["status"],
                      "outputs": {locale: item["sha256"] for locale, item in result["outputs"]["locales"].items()}}, indent=2))


if __name__ == "__main__":
    main()

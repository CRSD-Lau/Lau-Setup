"""Build a staged 16:9 loading-screen Patch-Q override without live writes.

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell

The generated-image manifest is deliberately an approval boundary.  Every
inventory entry must have one approved 16:9 PNG before this program opens an
output MPQ.  See --help for the manifest contract.
"""
import argparse
import hashlib
import io
import json
import math
import struct
import sys
from pathlib import Path

from PIL import Image

from build_caverns_release import Mpq, member_hashes


META = {"Author": "Neil Mitchell", "Creator": "Neil Mitchell", "LastModifiedBy": "Neil Mitchell"}
TABLE = r"DBFilesClient\LoadingScreens.dbc"
KNOWN_SOURCE_SHA256 = "d477b60836c37ccfabefc8186b0745484cefdcee74b3c6ba768fdcba9c59312e"
STORAGE_SIZE = (4096, 2048)
MINIMUM_SIZE = (1280, 720)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def file_sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def load_json(path, label):
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Cannot read {label}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def decoded_string(block, offset, label):
    if not isinstance(offset, int) or offset < 0 or offset >= len(block):
        raise ValueError(f"{label} string offset outside string block")
    end = block.find(b"\0", offset)
    if end < 0:
        raise ValueError(f"{label} string is not NUL terminated")
    return block[offset:end].decode("utf-8", "strict")


def parse_loading_dbc(data):
    if len(data) < 20:
        raise ValueError("LoadingScreens DBC is shorter than its header")
    signature, count, fields, record_size, string_size = struct.unpack_from("<4s4I", data)
    if signature != b"WDBC" or fields != 4 or record_size != 16:
        raise ValueError("Unexpected LoadingScreens DBC schema")
    records_end = 20 + count * record_size
    if records_end < 20 or records_end + string_size != len(data):
        raise ValueError("LoadingScreens DBC has invalid structural bounds")
    strings = data[records_end:]
    rows = []
    ids = set()
    for index in range(count):
        offset = 20 + index * record_size
        row = list(struct.unpack_from("<4I", data, offset))
        if row[0] in ids:
            raise ValueError(f"Duplicate LoadingScreens ID {row[0]}")
        ids.add(row[0])
        path = decoded_string(strings, row[2], f"LoadingScreens ID {row[0]}")
        rows.append({"index": index, "offset": offset, "id": row[0], "name": decoded_string(strings, row[1], f"LoadingScreens ID {row[0]}"), "path": path, "flag": row[3]})
    return rows


def normalized_path(value, label):
    if not isinstance(value, str) or not value or "/" in value or value.startswith("\\") or ".." in value.split("\\"):
        raise ValueError(f"Invalid {label} path")
    return value.lower()


def wide_member_path(base):
    prefix, separator, extension = base.rpartition(".")
    if not separator or not prefix or extension.lower() != "blp":
        raise ValueError(f"Loading-screen member must end in .blp: {base}")
    return prefix + "Wide." + extension


def inventory_entries(manifest):
    entries = manifest.get("entries")
    coverage = manifest.get("coverage", {})
    if not isinstance(entries, list) or len(entries) != 85:
        raise ValueError("Source inventory must contain exactly 85 entries")
    if coverage.get("dbc_rows") != 92 or coverage.get("distinct_dbc_paths") != 85 or coverage.get("missing_distinct_paths") != 0:
        raise ValueError("Source inventory coverage is not the expected 92 rows / 85 paths")
    by_index, by_path = {}, {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("index"), int):
            raise ValueError("Inventory entry lacks integer index")
        index = entry["index"]
        path = normalized_path(entry.get("path"), "inventory")
        row_ids = entry.get("row_ids")
        preferred = entry.get("preferredsourcePNG")
        if index in by_index or path in by_path or not isinstance(entry.get("id"), str) or not isinstance(row_ids, list) or not row_ids or not all(isinstance(row_id, int) for row_id in row_ids) or not isinstance(preferred, str):
            raise ValueError("Inventory has duplicate/index/path or incomplete entry")
        by_index[index], by_path[path] = entry, entry
    if set(by_index) != set(range(85)):
        raise ValueError("Inventory indices must be exactly 0 through 84")
    return by_index, by_path


def approved_images(manifest, inventory):
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        raise ValueError("Generated-image manifest requires entries")
    result, output_paths = {}, set()
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("index"), int):
            raise ValueError("Generated-image entry lacks integer index")
        index = entry["index"]
        if index not in inventory or index in result:
            raise ValueError("Generated-image manifest has unknown or duplicate index")
        if entry.get("approved") is not True:
            raise ValueError(f"Generated image {index} is not approved")
        output_path, prompt_path = entry.get("output_path"), entry.get("prompt_path")
        dimensions = entry.get("native_dimensions")
        if not isinstance(output_path, str) or not isinstance(prompt_path, str) or not isinstance(dimensions, list) or len(dimensions) != 2 or not all(isinstance(value, int) for value in dimensions):
            raise ValueError(f"Generated image {index} violates the output_path/approved/native_dimensions/prompt_path contract")
        image_path, prompt = Path(output_path), Path(prompt_path)
        if not image_path.is_file() or image_path.suffix.lower() != ".png" or not prompt.is_file():
            raise ValueError(f"Generated image {index} or its prompt artifact is absent")
        resolved_image = image_path.resolve()
        if resolved_image in output_paths:
            raise ValueError(f"Generated image manifest reuses output_path for index {index}")
        output_paths.add(resolved_image)
        try:
            with Image.open(image_path) as image:
                if image.format != "PNG":
                    raise ValueError(f"Generated image {index} is not PNG")
                before_hash = file_sha(image_path)
                image.load()
                actual = image.size
                if image.convert("RGBA").getchannel("A").getextrema() != (255, 255):
                    raise ValueError(f"Generated image {index} contains transparency")
                if file_sha(image_path) != before_hash:
                    raise ValueError(f"Generated image {index} changed while it was decoded")
        except OSError as error:
            raise ValueError(f"Generated image {index} cannot be decoded: {error}") from error
        if tuple(dimensions) != actual or actual[0] < MINIMUM_SIZE[0] or actual[1] < MINIMUM_SIZE[1] or abs(actual[0] / actual[1] - 16 / 9) > 0.002:
            raise ValueError(f"Generated image {index} is not approved true 16:9 at at least 1280x720")
        result[index] = {"path": image_path.resolve(), "prompt_path": prompt.resolve(), "dimensions": list(actual), "sha256": before_hash}
    if set(result) != set(inventory):
        missing = sorted(set(inventory) - set(result))
        raise ValueError(f"Generated-image manifest does not cover every inventory entry; missing {missing}")
    return result


def encode_blp(png_path, expected_sha256):
    if file_sha(png_path) != expected_sha256:
        raise ValueError(f"Generated image changed after approval: {png_path}")
    with Image.open(png_path) as source:
        source.load()
        image = source.convert("RGB").resize(STORAGE_SIZE, Image.Resampling.LANCZOS)
    if file_sha(png_path) != expected_sha256:
        raise ValueError(f"Generated image changed during conversion: {png_path}")
    offsets, sizes, blocks, offset = [0] * 16, [0] * 16, [], 148
    for level in range(13):
        stream = io.BytesIO()
        image.save(stream, format="DDS", pixel_format="DXT1")
        dds = stream.getvalue()
        if dds[:4] != b"DDS " or dds[84:88] != b"DXT1":
            raise ValueError("Pillow did not produce DXT1 DDS")
        block = dds[128:]
        expected = max(1, (image.width + 3) // 4) * max(1, (image.height + 3) // 4) * 8
        if len(block) != expected:
            raise ValueError("Unexpected DXT1 mip size")
        offsets[level], sizes[level] = offset, len(block)
        blocks.append(block)
        offset += len(block)
        image = image.resize((max(1, image.width // 2), max(1, image.height // 2)), Image.Resampling.LANCZOS)
    payload = struct.pack("<4sI4B2I", b"BLP2", 1, 2, 0, 0, 1, *STORAGE_SIZE) + struct.pack("<16I", *offsets) + struct.pack("<16I", *sizes) + b"".join(blocks)
    if len(payload) != offset:
        raise ValueError("BLP packing length mismatch")
    return payload


def assert_blp(data):
    if len(data) < 148 or data[:4] != b"BLP2" or struct.unpack_from("<2I", data, 12) != STORAGE_SIZE:
        raise ValueError("Encoded BLP header differs")
    offsets = struct.unpack_from("<16I", data, 20)
    sizes = struct.unpack_from("<16I", data, 84)
    expected_offset = 148
    for level in range(13):
        width, height = max(1, 4096 >> level), max(1, 2048 >> level)
        expected = max(1, (width + 3) // 4) * max(1, (height + 3) // 4) * 8
        if offsets[level] != expected_offset or offsets[level] + sizes[level] > len(data) or sizes[level] != expected:
            raise ValueError("Encoded BLP mip bounds differ")
        expected_offset += expected
    if expected_offset != len(data) or any(offsets[level] or sizes[level] for level in range(13, 16)):
        raise ValueError("Encoded BLP has noncontiguous or unexpected unused mip data")
    with Image.open(io.BytesIO(data)) as image:
        image.load()
        if image.size != STORAGE_SIZE:
            raise ValueError("Encoded BLP does not decode at storage dimensions")


def reject_output(source, output, protected_client_root):
    protected_client_root = protected_client_root.resolve(strict=True)
    if not protected_client_root.is_dir():
        raise ValueError("Protected client root must be an existing directory")
    if source == output or source in output.parents:
        raise ValueError("Refusing output alias or output under the source archive")
    # The source is expected to be read from a client Data folder; output may never be written there.
    source_client_root = source.parent.parent
    if (output == source_client_root or source_client_root in output.parents or
            output == protected_client_root or protected_client_root in output.parents):
        raise ValueError("Refusing staged output inside the live client tree")
    if output.exists():
        raise ValueError("Refusing existing staged output directory")


def verify_source(mpq, source, inventory):
    if not source.is_file() or file_sha(source) != KNOWN_SOURCE_SHA256:
        raise ValueError("Source Patch-Q hash does not match the approved known source")
    before = member_hashes(mpq, source)
    archive = mpq.open(source)
    try:
        names = mpq.names(archive)
        table = mpq.read(archive, TABLE)
    finally:
        mpq.close_archive(archive)
    rows = parse_loading_dbc(table)
    nonempty = [row for row in rows if row["path"]]
    paths = {normalized_path(row["path"], "DBC") for row in nonempty}
    inventory_paths = {normalized_path(entry["path"], "inventory") for entry in inventory.values()}
    if len(rows) != 92 or len(nonempty) != 92 or len(paths) != 85 or paths != inventory_paths:
        raise ValueError("Source DBC does not match the 92-row/85-path inventory")
    for entry in inventory.values():
        actual_ids = sorted(row["id"] for row in nonempty if normalized_path(row["path"], "DBC") == normalized_path(entry["path"], "inventory"))
        if actual_ids != sorted(entry["row_ids"]):
            raise ValueError(f"Source DBC row IDs differ for inventory index {entry['index']}")
    return before, names, table, rows


def validation_report(source, inventory_manifest, generated_manifest, mpq=None):
    inventory, paths = inventory_entries(inventory_manifest)
    generated = approved_images(generated_manifest, inventory)
    report = {**META, "status": "INPUT_COVERAGE_PASS", "source_q": str(source), "source_q_sha256": file_sha(source),
              "inventory_entries": len(inventory), "generated_entries": len(generated), "required_dbc_rows": 92,
              "distinct_paths": 85, "generated_images": [{"index": index, "output_path": str(info["path"]), "prompt_path": str(info["prompt_path"]), "approved": True, "native_dimensions": info["dimensions"], "sha256": info["sha256"]} for index, info in sorted(generated.items())]}
    if mpq:
        before, names, table, rows = verify_source(mpq, source, inventory)
        report.update({"source_members": len(before), "source_loading_rows": len(rows), "source_nonempty_rows": len([row for row in rows if row["path"]])})
    return inventory, generated, report


def build(args):
    source, output = args.source_q.resolve(), args.output.resolve()
    inventory_manifest = load_json(args.source_inventory_manifest, "source inventory manifest")
    generated_manifest = load_json(args.generated_image_manifest, "generated-image manifest")
    mpq = Mpq(args.stormlib)
    inventory, generated, report = validation_report(source, inventory_manifest, generated_manifest, mpq)
    if args.validate_inputs:
        print(json.dumps(report, indent=2))
        return
    reject_output(source, output, args.protected_client_root)
    # No archive or output write has occurred before all source and approval checks above.
    source_sha_before_build = file_sha(source)
    before, names, old_dbc, rows = verify_source(mpq, source, inventory)
    staged_blps = {}
    for index, entry in sorted(inventory.items()):
        blob = encode_blp(generated[index]["path"], generated[index]["sha256"])
        assert_blp(blob)
        target = wide_member_path(entry["path"])
        key = normalized_path(target, "derived Wide")
        if key in staged_blps:
            raise ValueError("Derived Wide member collision")
        staged_blps[key] = (target, blob)
    changed_dbc = bytearray(old_dbc)
    for row in rows:
        struct.pack_into("<I", changed_dbc, row["offset"] + 12, 1)
    changed_dbc = bytes(changed_dbc)
    changed_rows = [row["id"] for row in rows if struct.unpack_from("<I", old_dbc, row["offset"] + 12)[0] != 1]
    if changed_rows and len(changed_rows) > 92:
        raise ValueError("Unexpected LoadingScreens DBC flag delta")
    output.mkdir(parents=True)
    asset_dir = output / "derived-wide-blp"
    asset_dir.mkdir()
    for index, entry in sorted(inventory.items()):
        target, blob = staged_blps[normalized_path(wide_member_path(entry["path"]), "derived Wide")]
        path = asset_dir / f"{index:03d}-{Path(target).name}"
        path.write_bytes(blob)
    dbc_path = output / "LoadingScreens.dbc"
    dbc_path.write_bytes(changed_dbc)
    target_q = output / "patch-q-loading-hd16x9.mpq"
    archive = mpq.create(target_q, 1 << math.ceil(math.log2(len(names) + len(staged_blps) + 8)))
    source_archive = mpq.open(source)
    try:
        temp = output / "member.tmp"
        for key, name in sorted(names.items()):
            if key == TABLE.lower():
                mpq.add(archive, dbc_path, name)
            elif key in staged_blps:
                target, _ = staged_blps[key]
                mpq.add(archive, asset_dir / f"{next(index for index, entry in inventory.items() if normalized_path(wide_member_path(entry['path']), 'derived Wide') == key):03d}-{Path(target).name}", target)
            else:
                temp.write_bytes(mpq.read(source_archive, name))
                mpq.add(archive, temp, name)
        for key, (name, _) in sorted(staged_blps.items()):
            if key not in names:
                mpq.add(archive, asset_dir / f"{next(index for index, entry in inventory.items() if normalized_path(wide_member_path(entry['path']), 'derived Wide') == key):03d}-{Path(name).name}", name)
    finally:
        mpq.close_archive(source_archive)
        mpq.close_archive(archive)
        temp.unlink(missing_ok=True)
    after = member_hashes(mpq, target_q)
    allowed = {TABLE.lower(), *staged_blps}
    changed_members = {key for key in before.keys() & after.keys() if before[key] != after[key]}
    if changed_members - allowed or before.keys() - after.keys() or after.keys() - before.keys() - set(staged_blps):
        raise ValueError("Candidate MPQ changed unrelated members")
    target_archive = mpq.open(target_q)
    try:
        readback = mpq.read(target_archive, TABLE)
    finally:
        mpq.close_archive(target_archive)
    new_rows = parse_loading_dbc(readback)
    if len(new_rows) != 92 or any(row["flag"] != 1 for row in new_rows):
        raise ValueError("Candidate LoadingScreens rows are not all Wide")
    allowed_dbc_bytes = {row["offset"] + byte for row in rows for byte in range(12, 16)}
    if any(old_dbc[offset] != readback[offset] for offset in range(len(old_dbc)) if offset not in allowed_dbc_bytes):
        raise ValueError("Candidate LoadingScreens changed bytes outside HasWideScreen")
    for old, new in zip(rows, new_rows):
        if (old["id"], old["name"], old["path"]) != (new["id"], new["name"], new["path"]):
            raise ValueError("Candidate LoadingScreens changed an ID, name, or path")
    for key, (name, blob) in staged_blps.items():
        if after.get(key) != sha(blob):
            raise ValueError(f"Candidate Wide member differs: {name}")
        archive = mpq.open(target_q)
        try:
            assert_blp(mpq.read(archive, name))
        finally:
            mpq.close_archive(archive)
    if file_sha(source) != source_sha_before_build:
        raise ValueError("Read-only source Q changed while building")
    report.update({"status": "STAGED_MEMBER_AND_DBC_PARITY_PASS_IN_GAME_PENDING", "runtime": "PENDING_USER_VISUAL_ACCEPTANCE",
                   "candidate_q": str(target_q), "candidate_q_sha256": file_sha(target_q), "source_members": len(before),
                   "candidate_members": len(after), "added_wide_members": sorted(name for key, (name, _) in staged_blps.items() if key not in before),
                   "replaced_wide_members": sorted(name for key, (name, _) in staged_blps.items() if key in before),
                   "unchanged_prior_members": len(before) - len(changed_members), "changed_existing_members": sorted(changed_members),
                   "dbc": {"table": "LoadingScreens", "rows": 92, "distinct_paths": 85, "field": "HasWideScreen", "index": 3,
                           "changed_row_ids": changed_rows, "all_ids_names_paths_other_fields_preserved": True},
                   "wide_assets": [{"index": index, "output_path": str(generated[index]["path"]), "approved": True, "native_dimensions": generated[index]["dimensions"], "prompt_path": str(generated[index]["prompt_path"]), "member": wide_member_path(entry["path"]), "blp_sha256": sha(staged_blps[normalized_path(wide_member_path(entry["path"]), "derived Wide")][1])} for index, entry in sorted(inventory.items())]})
    (output / "build-proof.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=__doc__, epilog="""Generated-image manifest contract:\n  {\"entries\": [{\"index\": 0, \"output_path\": \"<approved-image.png>\", \"approved\": true,\n                \"native_dimensions\": [1920, 1080], \"prompt_path\": \"<prompt.txt>\"}]}\nAll 85 indices 0..84 occur exactly once. Files must exist, prompt artifacts must exist,\ndimensions must match the decoded PNG, and each PNG must be >=1280x720 and 16:9 ±0.002.""")
    parser.add_argument("--source-q", required=True, type=Path, help="Read-only Patch-Q matching the known source SHA-256")
    parser.add_argument("--source-inventory-manifest", required=True, type=Path)
    parser.add_argument("--generated-image-manifest", required=True, type=Path)
    parser.add_argument("--stormlib", required=True, type=Path)
    parser.add_argument("--protected-client-root", required=True, type=Path,
                        help="Existing client root that staged output must never enter")
    parser.add_argument("--output", required=True, type=Path, help="Fresh staged directory outside the source client Data directory")
    parser.add_argument("--validate-inputs", action="store_true", help="Report coverage and approvals without conversion or writes")
    args = parser.parse_args()
    try:
        build(args)
    except (OSError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()

"""Build the optional Caverns map fix without writing a game client.

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell

Input archives are immutable. The root Maps archive keeps every existing
WorldMapArea record and adds the 53 caves records; each localized MapDetails
archive omits that competing table. All other decompressed members are checked.
"""

import argparse
import ctypes as C
from ctypes import wintypes as W
import hashlib
import json
import math
from pathlib import Path
import struct


TABLE = "DBFilesClient\\WorldMapArea.dbc"
LOCALES = ("deDE", "enUS", "esES", "esMX", "frFR", "koKR", "ruRU", "zhCN", "zhTW")
META = {"Author": "Neil Mitchell", "Creator": "Neil Mitchell", "LastModifiedBy": "Neil Mitchell"}
PART_SIZE = 96 * 1024 * 1024


def digest_file(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def rows(data):
    signature, count, fields, size, strings = struct.unpack_from("<4s4I", data)
    if signature != b"WDBC" or len(data) != 20 + count * size + strings or size != fields * 4:
        raise ValueError("Invalid WorldMapArea DBC structure")
    result = {}
    for index in range(count):
        record = struct.unpack_from("<" + "I" * fields, data, 20 + index * size)
        if record[0] in result:
            raise ValueError("Duplicate WorldMapArea record ID")
        result[record[0]] = record
    return result


def string_at(data, offset):
    count, size = struct.unpack_from("<II", data, 4)[0], struct.unpack_from("<I", data, 16)[0]
    record_size = struct.unpack_from("<I", data, 12)[0]
    strings = data[20 + count * record_size:]
    if offset >= size:
        raise ValueError("WorldMapArea string offset outside block")
    end = strings.find(b"\0", offset)
    if end < 0:
        raise ValueError("Unterminated WorldMapArea string")
    return strings[offset:end]


def merge_tables(root_data, cave_data):
    original = rows(root_data)
    caves = rows(cave_data)
    count, fields, record_size, string_size = struct.unpack_from("<4I", root_data, 4)
    cave_count, cave_fields, cave_record_size, _ = struct.unpack_from("<4I", cave_data, 4)
    if (fields, record_size) != (cave_fields, cave_record_size) or fields != 11:
        raise ValueError("WorldMapArea schemas differ")
    strings = bytearray(root_data[20 + count * record_size:])
    if len(strings) != string_size:
        raise ValueError("Root string block size differs")
    names = {}
    for record in original.values():
        names[string_at(root_data, record[3])] = record[3]
    additions = []
    for record_id, record in caves.items():
        if record_id in original:
            continue
        name = string_at(cave_data, record[3])
        if name not in names:
            names[name] = len(strings)
            strings.extend(name + b"\0")
        updated = list(record)
        updated[3] = names[name]
        additions.append(tuple(updated))
    header = struct.pack("<4s4I", b"WDBC", count + len(additions), fields, record_size, len(strings))
    records = root_data[20:20 + count * record_size] + b"".join(struct.pack("<" + "I" * fields, *record) for record in additions)
    result = header + records + strings
    merged = rows(result)
    if len(merged) != cave_count or any(merged[k] != v for k, v in original.items()):
        raise ValueError("Original WorldMapArea rows were modified")
    for record_id in caves.keys() - original.keys():
        actual, expected = merged[record_id], caves[record_id]
        if actual[:3] != expected[:3] or actual[4:] != expected[4:] or string_at(result, actual[3]) != string_at(cave_data, expected[3]):
            raise ValueError(f"Added WorldMapArea row differs: {record_id}")
    return result


class Mpq:
    def __init__(self, dll_path):
        self.dll = C.WinDLL(str(Path(dll_path).resolve()), use_last_error=True)
        self.open_archive = self.bind("SFileOpenArchive", [C.c_wchar_p, W.DWORD, W.DWORD, C.POINTER(W.HANDLE)], C.c_bool)
        self.close_archive = self.bind("SFileCloseArchive", [W.HANDLE], C.c_bool)
        self.create_archive = self.bind("SFileCreateArchive", [C.c_wchar_p, W.DWORD, W.DWORD, C.POINTER(W.HANDLE)], C.c_bool)
        self.open_file = self.bind("SFileOpenFileEx", [W.HANDLE, C.c_char_p, W.DWORD, C.POINTER(W.HANDLE)], C.c_bool)
        self.get_file_size = self.bind("SFileGetFileSize", [W.HANDLE, C.POINTER(W.DWORD)], W.DWORD)
        self.read_file = self.bind("SFileReadFile", [W.HANDLE, C.c_void_p, W.DWORD, C.POINTER(W.DWORD), C.c_void_p], C.c_bool)
        self.close_file = self.bind("SFileCloseFile", [W.HANDLE], C.c_bool)
        self.add_file = self.bind("SFileAddFileEx", [W.HANDLE, C.c_wchar_p, C.c_char_p, W.DWORD, W.DWORD, W.DWORD], C.c_bool)

    def bind(self, name, arguments, result):
        function = getattr(self.dll, name)
        function.argtypes = arguments
        function.restype = result
        return function

    @staticmethod
    def require(value, operation):
        if not value:
            raise RuntimeError(f"{operation} failed, Win32 error {C.get_last_error()}")

    def open(self, path, writable=False):
        handle = W.HANDLE()
        self.require(self.open_archive(str(Path(path).resolve()), 0, 0 if writable else 0x100, C.byref(handle)), f"open {path}")
        return handle

    def create(self, path, capacity):
        handle = W.HANDLE()
        self.require(self.create_archive(str(Path(path).resolve()), 0, capacity, C.byref(handle)), f"create {path}")
        return handle

    def read(self, archive, name):
        file = W.HANDLE()
        self.require(self.open_file(archive, name.encode("utf-8"), 0, C.byref(file)), f"open member {name}")
        try:
            high = W.DWORD()
            size = self.get_file_size(file, C.byref(high))
            if high.value or size > 200_000_000:
                raise ValueError(f"Unexpected member size: {name}")
            buffer = C.create_string_buffer(size)
            got = W.DWORD()
            self.require(self.read_file(file, buffer, size, C.byref(got), None), f"read member {name}")
            if got.value != size:
                raise ValueError(f"Short member: {name}")
            return buffer.raw
        finally:
            self.close_file(file)

    def names(self, archive):
        names = self.read(archive, "(listfile)").decode("utf-8").splitlines()
        result = {}
        for name in names:
            key = name.lower()
            if key in {"(listfile)", "(attributes)", "(signature)"}:
                continue
            if key in result:
                raise ValueError(f"Case collision: {name}")
            result[key] = name
        return result

    def add(self, archive, source, name):
        self.require(self.add_file(archive, str(Path(source).resolve()), name.encode("utf-8"), 0x80000200, 2, 2), f"add {name}")


def member_hashes(mpq, path):
    archive = mpq.open(path)
    try:
        return {key: digest(mpq.read(archive, name)) for key, name in mpq.names(archive).items()}
    finally:
        mpq.close_archive(archive)


def assert_source(path, asset):
    if path.stat().st_size != asset["Bytes"] or digest_file(path) != asset["Sha256"]:
        raise ValueError(f"Source does not match published catalog: {path}")


def emit_asset(key, path, payload):
    parts = []
    with path.open("rb") as stream:
        while chunk := stream.read(PART_SIZE):
            hash_value = digest(chunk)
            part = payload / (hash_value + ".bin")
            if part.exists():
                if part.stat().st_size != len(chunk) or digest_file(part) != hash_value:
                    raise ValueError(f"Existing payload segment differs: {part}")
            else:
                part.write_bytes(chunk)
            parts.append({"Sha256": hash_value, "Bytes": len(chunk), "FileName": part.name, "Url": ""})
    return {"Id": key, "Bytes": path.stat().st_size, "Sha256": digest_file(path), "Parts": parts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root-m", type=Path, required=True, help="Read-only published Maps MPQ source")
    parser.add_argument("--localized-t", type=Path, required=True, help="Directory of published patch-<locale>-T.MPQ archives")
    parser.add_argument("--caves-table", type=Path, required=True)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--stormlib", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    payload = output / "payload"
    payload.mkdir(exist_ok=True)
    catalog = json.loads(args.catalog.read_text(encoding="utf-8-sig"))
    if catalog.get("MapPackVersion") != "WDM-2.4.5" or set(LOCALES) != set(catalog["Locales"]):
        raise ValueError("Unexpected map pack or localized asset set")
    mpq = Mpq(args.stormlib)
    source = args.root_m.resolve()
    assert_source(source, catalog["Assets"]["Maps"])
    caves = args.caves_table.read_bytes()
    if digest(caves) != "178b3832815d2881a543fbf440901226dad95b1fac1d85a065df7a813cc4571b":
        raise ValueError("Unexpected caves WorldMapArea DBC")
    before_root = member_hashes(mpq, source)
    if TABLE.lower() not in before_root:
        raise ValueError("Root archive lacks WorldMapArea DBC")
    source_archive = mpq.open(source)
    try:
        root_old = mpq.read(source_archive, TABLE)
    finally:
        mpq.close_archive(source_archive)
    old_rows, cave_rows = rows(root_old), rows(caves)
    added, removed = sorted(cave_rows.keys() - old_rows.keys()), sorted(old_rows.keys() - cave_rows.keys())
    changed = sorted(k for k in cave_rows.keys() & old_rows.keys() if cave_rows[k] != old_rows[k])
    if len(old_rows) != 159 or len(cave_rows) != 212 or len(added) != 53 or removed:
        raise ValueError("Unexpected WorldMapArea record delta")
    if not {1035, 1036}.issubset(cave_rows) or not all(cave_rows[k][10] == 161 for k in (1035, 1036)):
        raise ValueError("Caverns rows or Tanaris parent differ")
    merged_table = merge_tables(root_old, caves)
    merged_path = output / "merged-WorldMapArea.dbc"
    merged_path.write_bytes(merged_table)
    root_target = output / "patch-m.mpq"
    if root_target.exists():
        raise ValueError(f"Refusing to overwrite staged output: {root_target}")
    source_archive = mpq.open(source)
    try:
        source_names = mpq.names(source_archive)
        archive = mpq.create(root_target, 1 << math.ceil(math.log2(len(source_names) + 8)))
        try:
            temp = output / "member.tmp"
            for index, (lower, name) in enumerate(sorted(source_names.items())):
                if lower == TABLE.lower():
                    mpq.add(archive, merged_path, name)
                else:
                    temp.write_bytes(mpq.read(source_archive, name))
                    mpq.add(archive, temp, name)
                if (index + 1) % 2000 == 0:
                    print(f"ROOT {index + 1}/{len(source_names)}", flush=True)
        finally:
            mpq.close_archive(archive)
    finally:
        mpq.close_archive(source_archive)
    after_root = member_hashes(mpq, root_target)
    if before_root.keys() != after_root.keys() or {key for key in before_root if before_root[key] != after_root[key]} != {TABLE.lower()}:
        raise ValueError("Root archive changed unexpected members")
    if after_root[TABLE.lower()] != digest(merged_table):
        raise ValueError("Root DBC readback differs")
    assets = {"Maps": emit_asset("Maps", root_target, payload)}
    report = {**META, "status": "STATIC_MEMBER_PARITY_PASS", "runtime": "PENDING_IN_GAME", "root": {
        "source": str(source), "source_sha256": digest_file(source), "candidate_sha256": assets["Maps"]["Sha256"],
        "members": len(after_root), "changed_members": [TABLE], "old_dbc_sha256": digest(root_old),
        "caves_source_dbc_sha256": digest(caves), "new_dbc_sha256": digest(merged_table),
        "old_rows": len(old_rows), "new_rows": len(cave_rows),
        "added_record_ids": added, "removed_record_ids": removed, "changed_record_ids": [],
        "upstream_shared_rows_preserved_from_lau": changed,
        "added_records": {str(k): {"fields_raw_u32": list(rows(merged_table)[k]), "map_name": string_at(merged_table, rows(merged_table)[k][3]).decode("ascii")} for k in added},
        "caverns_rows": {str(k): list(rows(merged_table)[k]) for k in (1035, 1036)},
    }, "locales": []}
    for locale in LOCALES:
        source_t = (args.localized_t / f"patch-{locale}-T.MPQ").resolve()
        key = "MapDetails-" + locale
        assert_source(source_t, catalog["Assets"][key])
        archive = mpq.open(source_t)
        try:
            names = mpq.names(archive)
            if TABLE.lower() not in names or digest(mpq.read(archive, names[TABLE.lower()])) != digest(caves):
                raise ValueError(f"Localized DBC differs: {locale}")
            expected = {lower: digest(mpq.read(archive, name)) for lower, name in names.items() if lower != TABLE.lower()}
            target = output / f"patch-{locale}-T.MPQ"
            if not target.exists():
                capacity = 1 << math.ceil(math.log2(len(expected) + 8))
                result = mpq.create(target, capacity)
                try:
                    temp = output / "member.tmp"
                    for lower, name in sorted(names.items()):
                        if lower == TABLE.lower():
                            continue
                        temp.write_bytes(mpq.read(archive, name))
                        mpq.add(result, temp, name)
                finally:
                    mpq.close_archive(result)
        finally:
            mpq.close_archive(archive)
        actual = member_hashes(mpq, target)
        if actual != expected or TABLE.lower() in actual:
            raise ValueError(f"Localized member parity failed: {locale}")
        assets[key] = emit_asset(key, target, payload)
        report["locales"].append({"locale": locale, "source_sha256": digest_file(source_t),
                                  "candidate_sha256": assets[key]["Sha256"], "retained_members": len(expected),
                                  "removed_members": [TABLE], "retained_member_bytes_identical": True})
        print(f"MAP {locale}: {len(expected)} retained members", flush=True)
    (output / "member.tmp").unlink(missing_ok=True)
    sources = {key: str((output / ("patch-m.mpq" if key == "Maps" else f"patch-{key.removeprefix('MapDetails-')}-T.MPQ")).resolve()) for key in assets}
    for key, asset in catalog["Assets"].items():
        if not key.startswith("MapAddon-"):
            continue
        if len(asset["Parts"]) != 1:
            raise ValueError(f"Map addon asset has multiple parts: {key}")
        path = (args.localized_t / "payload" / asset["Parts"][0]["FileName"]).resolve()
        assert_source(path, asset)
        sources[key] = str(path)
    (output / "map-source-index.json").write_text(json.dumps({**META, "sources": sources}, indent=2) + "\n", encoding="utf-8")
    (output / "catalog-delta.json").write_text(json.dumps({**META, "MapPackVersion": "WDM-2.4.5", "PublicReady": False, "Assets": assets}, indent=2) + "\n", encoding="utf-8")
    (output / "map-assets.json").write_text(json.dumps({**META, "Assets": assets}, indent=2) + "\n", encoding="utf-8")
    (output / "caverns-build-proof.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("STATIC_MEMBER_PARITY_PASS", flush=True)


if __name__ == "__main__":
    main()

"""Small binary helpers for the ICC range-circle experiment.

Author/Creator/Modifier: Neil Mitchell.
"""

from __future__ import annotations

import struct
from pathlib import Path


def load_wdbc(path: Path):
    data = path.read_bytes()
    magic, count, fields, record_size, string_size = struct.unpack_from("<4s4I", data)
    if magic != b"WDBC":
        raise ValueError(f"Unexpected DBC magic in {path}: {magic!r}")
    if record_size != fields * 4:
        raise ValueError(
            f"Unsupported packed record size in {path}: {record_size} vs {fields * 4}"
        )
    records = [
        bytearray(data[20 + i * record_size : 20 + (i + 1) * record_size])
        for i in range(count)
    ]
    strings_at = 20 + count * record_size
    strings = bytearray(data[strings_at : strings_at + string_size])
    if len(strings) != string_size:
        raise ValueError(f"Truncated WDBC string block in {path}")
    return fields, records, strings


def save_wdbc(path: Path, fields: int, records, strings: bytearray):
    header = struct.pack("<4s4I", b"WDBC", len(records), fields, fields * 4, len(strings))
    path.write_bytes(header + b"".join(records) + strings)


def u32(record: bytes | bytearray, field: int) -> int:
    return struct.unpack_from("<I", record, field * 4)[0]


def set_u32(record: bytearray, field: int, value: int):
    struct.pack_into("<I", record, field * 4, value)


def set_f32(record: bytearray, field: int, value: float):
    struct.pack_into("<f", record, field * 4, value)


def add_string(strings: bytearray, value: str) -> int:
    encoded = value.encode("utf-8") + b"\0"
    offset = len(strings)
    strings.extend(encoded)
    return offset


def string_at(strings: bytes | bytearray, offset: int) -> str:
    end = strings.find(0, offset)
    if end < 0:
        raise ValueError(f"Unterminated WDBC string at offset {offset}")
    return bytes(strings[offset:end]).decode("utf-8", errors="strict")


def by_id(records):
    result = {}
    for record in records:
        ident = u32(record, 0)
        if ident in result:
            raise ValueError(f"Duplicate WDBC record ID {ident}")
        result[ident] = record
    return result


def append_aligned(data: bytearray, payload: bytes, alignment: int = 16) -> int:
    data.extend(b"\0" * (-len(data) % alignment))
    offset = len(data)
    data.extend(payload)
    return offset


def field_diffs(before: bytes | bytearray, after: bytes | bytearray):
    if len(before) != len(after) or len(before) % 4:
        raise ValueError("DBC records must have equal four-byte field layout")
    return [
        {"field": field, "old": u32(before, field), "new": u32(after, field)}
        for field in range(len(before) // 4)
        if before[field * 4 : field * 4 + 4] != after[field * 4 : field * 4 + 4]
    ]

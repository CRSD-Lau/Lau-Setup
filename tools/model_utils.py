# Author/Creator/Modifier: Neil Mitchell
import struct
import struct as S
from pathlib import Path
def load_wdbc(path: Path):
    data = path.read_bytes()
    magic, count, fields, record_size, string_size = struct.unpack_from("<4s4I", data)
    if magic != b"WDBC":
        raise ValueError(f"Unexpected DBC magic in {path}: {magic!r}")
    if record_size != fields * 4:
        raise ValueError(f"Unsupported packed record size in {path}: {record_size} vs {fields * 4}")
    records = [bytearray(data[20 + i * record_size : 20 + (i + 1) * record_size]) for i in range(count)]
    strings_at = 20 + count * record_size
    strings = bytearray(data[strings_at : strings_at + string_size])
    return fields, records, strings


def save_wdbc(path: Path, fields: int, records, strings: bytearray):
    header = struct.pack("<4s4I", b"WDBC", len(records), fields, fields * 4, len(strings))
    path.write_bytes(header + b"".join(records) + strings)


def u32(record: bytearray, field: int):
    return struct.unpack_from("<I", record, field * 4)[0]


def set_u32(record: bytearray, field: int, value: int):
    struct.pack_into("<I", record, field * 4, value)


def set_f32(record: bytearray, field: int, value: float):
    struct.pack_into("<f", record, field * 4, value)


def string_at(strings: bytearray, offset: int):
    end = strings.find(0, offset)
    if end < 0:
        end = len(strings)
    return bytes(strings[offset:end]).decode("utf-8", errors="replace")


def add_string(strings: bytearray, value: str):
    encoded = value.encode("utf-8") + b"\0"
    offset = len(strings)
    strings.extend(encoded)
    return offset


def by_id(records):
    return {u32(record, 0): record for record in records}


def append(data, payload):
    data.extend(b'\0' * (-len(data) % 16))
    offset = len(data)
    data.extend(payload)
    return offset


def array(data, header, payload, count):
    offset = append(data, payload)
    S.pack_into('<2I', data, header, count, offset)
    return offset


def constant_alpha(data, opacity):
    time = append(data, S.pack('<I', 0))
    key = append(data, S.pack('<h', round(32767 * opacity)))
    times = append(data, S.pack('<2I', 1, time))
    keys = append(data, S.pack('<2I', 1, key))
    return S.pack('<Hh4I', 0, -1, 1, times, 1, keys)

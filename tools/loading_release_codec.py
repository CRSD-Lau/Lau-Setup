"""Portable LoadingScreens DBC and BLP helpers for the loading release.

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell
"""
from __future__ import annotations

import hashlib
import io
import struct
from pathlib import Path

from PIL import Image

META = {"Author": "Neil Mitchell", "Creator": "Neil Mitchell", "LastModifiedBy": "Neil Mitchell"}
TABLE = r"DBFilesClient\LoadingScreens.dbc"
STORAGE_SIZE = (4096, 2048)


def file_sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def decoded_string(block: bytes, offset: int, label: str) -> str:
    if not isinstance(offset, int) or offset < 0 or offset >= len(block):
        raise ValueError(f"{label} string offset outside string block")
    end = block.find(b"\0", offset)
    if end < 0:
        raise ValueError(f"{label} string is not NUL terminated")
    return block[offset:end].decode("utf-8", "strict")


def parse_loading_dbc(data: bytes) -> list[dict]:
    if len(data) < 20:
        raise ValueError("LoadingScreens DBC is shorter than its header")
    signature, count, fields, record_size, string_size = struct.unpack_from("<4s4I", data)
    if signature != b"WDBC" or fields != 4 or record_size != 16:
        raise ValueError("Unexpected LoadingScreens DBC schema")
    records_end = 20 + count * record_size
    if records_end < 20 or records_end + string_size != len(data):
        raise ValueError("LoadingScreens DBC has invalid structural bounds")
    strings = data[records_end:]
    rows, ids = [], set()
    for index in range(count):
        offset = 20 + index * record_size
        row = list(struct.unpack_from("<4I", data, offset))
        if row[0] in ids:
            raise ValueError(f"Duplicate LoadingScreens ID {row[0]}")
        ids.add(row[0])
        rows.append({"index": index, "offset": offset, "id": row[0],
                     "name": decoded_string(strings, row[1], f"LoadingScreens ID {row[0]}"),
                     "path": decoded_string(strings, row[2], f"LoadingScreens ID {row[0]}"),
                     "flag": row[3]})
    return rows


def normalized_path(value: str, label: str) -> str:
    if (not isinstance(value, str) or not value or "/" in value or
        value.startswith("\\") or ".." in value.split("\\")):
        raise ValueError(f"Invalid {label} path")
    return value.lower()


def wide_member_path(base: str) -> str:
    prefix, separator, extension = base.rpartition(".")
    if not separator or not prefix or extension.lower() != "blp":
        raise ValueError(f"Loading-screen member must end in .blp: {base}")
    return prefix + "Wide." + extension


def encode_blp(png_path: Path, expected_sha256: str) -> bytes:
    if file_sha(png_path) != expected_sha256:
        raise ValueError(f"Approved PNG changed: {png_path.name}")
    with Image.open(png_path) as source:
        source.load()
        image = source.convert("RGB").resize(STORAGE_SIZE, Image.Resampling.LANCZOS)
    if file_sha(png_path) != expected_sha256:
        raise ValueError(f"Approved PNG changed during conversion: {png_path.name}")
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
    payload = (struct.pack("<4sI4B2I", b"BLP2", 1, 2, 0, 0, 1, *STORAGE_SIZE) +
               struct.pack("<16I", *offsets) + struct.pack("<16I", *sizes) + b"".join(blocks))
    if len(payload) != offset:
        raise ValueError("BLP packing length mismatch")
    return payload


def assert_blp(data: bytes) -> None:
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

"""Build the native 16:9 loading-screen executable from an exact known input.

Author / Creator / Last Modified By: Neil Mitchell
"""
from __future__ import annotations

import argparse
import hashlib
import struct
from pathlib import Path

import pefile

OLD_SHA256 = "6993049f1338b32a0423612093a8c7c6895b112504b83d6826d4c2174692cd37"
NATIVE_SHA256 = "a6767f7ed4d1f7c67c144eed7bf9707cd270d95af200f4accd0c6fc66ca14889"
OUTPUT_SHA256 = "4218fef354f875d1d27aae9cc6a93c75aaadaa1f0beea1204172793cd39e0505"
BASE = 0x400000
UV_SITE = 0x408615
DRAW_SITE = 0x40A602
WIDE_RATIO = 0xAB63B8
OLD_UV_DETOUR = bytes.fromhex("e8e64a9f00")
OLD_DRAW_DETOUR = bytes.fromhex("e8f9299f00")
NATIVE_UV = bytes.fromhex("680064ab00")
NATIVE_DRAW = bytes.fromhex("e899dfffff")
WIDE_16_9 = struct.pack("<f", 16 / 9)


def digest(data: bytes | bytearray) -> str:
    return hashlib.sha256(data).hexdigest()


def offset(pe: pefile.PE, va: int) -> int:
    return pe.get_offset_from_rva(va - BASE)


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def assert_safe_paths(source: Path, destination: Path,
                      protected_client_root: Path) -> tuple[Path, Path]:
    protected_client_root = protected_client_root.resolve(strict=True)
    if not protected_client_root.is_dir():
        raise ValueError("protected client root must be an existing directory")
    protected_client_exe = (protected_client_root / "WoW.exe").resolve(strict=False)
    source_resolved = source.resolve(strict=True)
    if is_within(source_resolved, protected_client_root) and source_resolved != protected_client_exe:
        raise ValueError("source inside the protected client must be its exact WoW.exe")
    if destination.exists():
        raise ValueError("destination must be a fresh staged output path")
    destination_resolved = destination.resolve(strict=False)
    if source_resolved == destination_resolved:
        raise ValueError("destination must not alias source")
    if is_within(destination_resolved, protected_client_root):
        raise ValueError("destination must not be inside the protected client tree")
    return source_resolved, destination_resolved


def assert_native_wide_geometry(pe: pefile.PE, data: bytes | bytearray) -> None:
    """Both native branches must retain the same `wide / base` arithmetic."""
    expected = bytes.fromhex("d905b863ab00d835b463ab00d9e8")
    for va in (0x409BB5, 0x40A372):
        start = offset(pe, va)
        if data[start : start + len(expected)] != expected:
            raise ValueError(f"native Wide geometry at 0x{va:X} is not the supported instruction sequence")


def build(source: Path, destination: Path, protected_client_root: Path) -> str:
    source, destination = assert_safe_paths(source, destination, protected_client_root)
    source_bytes = source.read_bytes()
    data = bytearray(source_bytes)
    source_hash = digest(data)
    if source_hash not in {OLD_SHA256, NATIVE_SHA256}:
        raise ValueError("Executable is not an exact supported Lau input")
    pe = pefile.PE(data=bytes(data), fast_load=True)
    assert_native_wide_geometry(pe, data)
    uv_off, draw_off, ratio_off = (offset(pe, va) for va in (UV_SITE, DRAW_SITE, WIDE_RATIO))
    if source_hash == OLD_SHA256:
        if data[uv_off : uv_off + 5] != OLD_UV_DETOUR or data[draw_off : draw_off + 5] != OLD_DRAW_DETOUR:
            raise ValueError("original input does not contain the supported loading detours")
        data[uv_off : uv_off + 5] = NATIVE_UV
        data[draw_off : draw_off + 5] = NATIVE_DRAW
    else:
        if data[uv_off : uv_off + 5] != NATIVE_UV or data[draw_off : draw_off + 5] != NATIVE_DRAW:
            raise ValueError("native input does not contain the supported restored instructions")
    if data[ratio_off : ratio_off + 4] != struct.pack("<f", 1.6):
        raise ValueError("native input does not contain the supported 16:10 Wide constant")
    data[ratio_off : ratio_off + 4] = WIDE_16_9
    if digest(data) != OUTPUT_SHA256:
        raise ValueError("built executable does not match the approved deterministic output")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    if digest(destination.read_bytes()) != OUTPUT_SHA256:
        raise ValueError("written executable did not read back as the approved output")
    if source.read_bytes() != source_bytes or digest(source_bytes) != source_hash:
        raise ValueError("source changed while building")
    return OUTPUT_SHA256


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--protected-client-root", required=True, type=Path,
                        help="Existing client root that staged output must never enter")
    args = parser.parse_args()
    print(build(args.source, args.destination, args.protected_client_root))


if __name__ == "__main__":
    main()

"""Minimal StormLib wrapper for scoped Patch-Y mutation and readback.

The DLL path is supplied through STORMLIB_DLL. The DLL is a build dependency
and is never copied into the payload. Author/Creator/Modifier: Neil Mitchell.
"""

from __future__ import annotations

import ctypes as C
import os
from ctypes import wintypes as W
from pathlib import Path


def _load():
    path = os.environ.get("STORMLIB_DLL")
    if not path:
        raise RuntimeError("Set STORMLIB_DLL to a trusted x64 Unicode StormLib.dll")
    dll_path = Path(path).resolve()
    if not dll_path.is_file():
        raise FileNotFoundError(f"STORMLIB_DLL does not exist: {dll_path}")
    lib = C.WinDLL(str(dll_path))
    signatures = [
        ("SFileOpenArchive", [C.c_void_p, W.DWORD, W.DWORD, C.POINTER(W.HANDLE)], C.c_bool),
        ("SFileCloseArchive", [W.HANDLE], C.c_bool),
        ("SFileOpenFileEx", [W.HANDLE, C.c_char_p, W.DWORD, C.POINTER(W.HANDLE)], C.c_bool),
        ("SFileGetFileSize", [W.HANDLE, C.POINTER(W.DWORD)], W.DWORD),
        ("SFileReadFile", [W.HANDLE, C.c_void_p, W.DWORD, C.POINTER(W.DWORD), C.c_void_p], C.c_bool),
        ("SFileCloseFile", [W.HANDLE], C.c_bool),
        ("SFileAddFileEx", [W.HANDLE, C.c_void_p, C.c_char_p, W.DWORD, W.DWORD, W.DWORD], C.c_bool),
    ]
    for name, args, result in signatures:
        fn = getattr(lib, name)
        fn.argtypes, fn.restype = args, result
    return lib


dll = _load()


def opened(path: Path, flags: int = 0x100):
    handle = W.HANDLE()
    path_buffer = C.create_unicode_buffer(str(path.resolve()))
    if not dll.SFileOpenArchive(C.cast(path_buffer, C.c_void_p), 0, flags, C.byref(handle)):
        raise OSError(f"Failed to open MPQ: {path}")
    return handle


def read_member(archive, name: str):
    handle = W.HANDLE()
    if not dll.SFileOpenFileEx(archive, name.encode("ascii"), 0, C.byref(handle)):
        return None
    try:
        high = W.DWORD()
        size = dll.SFileGetFileSize(handle, C.byref(high))
        if high.value or size == 0xFFFFFFFF or size >= 150_000_000:
            raise ValueError(f"Unsupported member size for {name}: high={high.value}, low={size}")
        output, read = C.create_string_buffer(size), W.DWORD()
        if not dll.SFileReadFile(handle, output, size, C.byref(read), None) or read.value != size:
            raise OSError(f"Failed to read MPQ member: {name}")
        return output.raw
    finally:
        dll.SFileCloseFile(handle)


def snapshot(path: Path):
    archive = opened(path)
    try:
        listed = read_member(archive, "(listfile)")
        if listed is None:
            raise ValueError(f"MPQ has no readable (listfile): {path}")
        names = set(listed.decode("utf-8-sig").splitlines()) - {"(listfile)", "(attributes)"}
        result = {}
        for name in names:
            data = read_member(archive, name)
            if data is None:
                raise ValueError(f"Listed MPQ member cannot be read: {name}")
            result[name] = data
        return result
    finally:
        dll.SFileCloseArchive(archive)


def add_or_replace(archive, local_path: Path, member_name: str):
    local_buffer = C.create_unicode_buffer(str(local_path.resolve()))
    flags = 0x80000200  # replace existing + zlib compression
    if not dll.SFileAddFileEx(
        archive,
        C.cast(local_buffer, C.c_void_p),
        member_name.encode("ascii"),
        flags,
        2,
        2,
    ):
        raise OSError(f"Failed to add MPQ member: {member_name}")

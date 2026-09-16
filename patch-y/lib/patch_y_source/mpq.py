"""Cross-platform, bounded StormLib adapter for Patch-Y archives.

Set STORMLIB_DLL on Windows or STORMLIB_LIBRARY on Linux. Linux also searches
for the system Storm library installed by libstorm9.

Author / Creator / Last Modified By: Neil Mitchell
"""

from __future__ import annotations

import ctypes as C
import ctypes.util
import os
import re
import sys
from pathlib import Path

from .core import OverlayError, normalize_member_path, sha256_bytes

DWORD = C.c_uint32
HANDLE = C.c_void_p
INVALID_HANDLE = C.c_void_p(-1).value
READ_ONLY = 0x100
REPLACE_COMPRESS = 0x80000200
ZLIB = 2


class FindData(C.Structure):
    _fields_ = [
        ("name", C.c_char * 260),
        ("plain_name", C.c_void_p),
        ("hash_index", DWORD),
        ("block_index", DWORD),
        ("size", DWORD),
        ("flags", DWORD),
        ("compressed_size", DWORD),
        ("time_low", DWORD),
        ("time_high", DWORD),
        ("locale", DWORD),
    ]


class Storm:
    def __init__(self, library: str | None = None):
        if sys.platform == "win32":
            selected = library or os.environ.get("STORMLIB_DLL")
            if not selected or not Path(selected).is_file():
                raise RuntimeError("Set STORMLIB_DLL to a trusted x64 Unicode StormLib.dll")
            self.lib = C.WinDLL(str(Path(selected).resolve()), use_last_error=True)
            self.path_type = C.c_wchar_p
            self._path = lambda path: str(Path(path).resolve())
        else:
            selected = library or os.environ.get("STORMLIB_LIBRARY") or ctypes.util.find_library("storm")
            if not selected:
                raise RuntimeError("Install libstorm9/libstorm-dev or set STORMLIB_LIBRARY")
            self.lib = C.CDLL(selected, use_errno=True)
            self.path_type = C.c_char_p
            self._path = lambda path: os.fsencode(Path(path).resolve())
        self.open_archive = self._bind("SFileOpenArchive", [self.path_type, DWORD, DWORD, C.POINTER(HANDLE)], C.c_bool)
        self.close_archive = self._bind("SFileCloseArchive", [HANDLE], C.c_bool)
        self.open_file = self._bind("SFileOpenFileEx", [HANDLE, C.c_char_p, DWORD, C.POINTER(HANDLE)], C.c_bool)
        self.get_file_size = self._bind("SFileGetFileSize", [HANDLE, C.POINTER(DWORD)], DWORD)
        self.read_file = self._bind("SFileReadFile", [HANDLE, C.c_void_p, DWORD, C.POINTER(DWORD), C.c_void_p], C.c_bool)
        self.close_file = self._bind("SFileCloseFile", [HANDLE], C.c_bool)
        self.find_first = self._bind("SFileFindFirstFile", [HANDLE, C.c_char_p, C.POINTER(FindData), self.path_type], HANDLE)
        self.find_next = self._bind("SFileFindNextFile", [HANDLE, C.POINTER(FindData)], C.c_bool)
        self.find_close = self._bind("SFileFindClose", [HANDLE], C.c_bool)
        self.add_file = self._bind("SFileAddFileEx", [HANDLE, self.path_type, C.c_char_p, DWORD, DWORD, DWORD], C.c_bool)
        self.remove_file = self._bind("SFileRemoveFile", [HANDLE, C.c_char_p, DWORD], C.c_bool)
        self.compact_archive = self._bind("SFileCompactArchive", [HANDLE, self.path_type, C.c_bool], C.c_bool)

    def _bind(self, name: str, arguments: list[object], result: object):
        function = getattr(self.lib, name)
        function.argtypes = arguments
        function.restype = result
        return function

    def _require(self, ok: object, label: str) -> None:
        if not ok:
            error = C.get_last_error() if sys.platform == "win32" else C.get_errno()
            raise RuntimeError(f"StormLib {label} failed (error {error})")

    def _open(self, path: Path, *, writable: bool = False) -> HANDLE:
        handle = HANDLE()
        self._require(self.open_archive(self._path(path), 0, 0 if writable else READ_ONLY, C.byref(handle)), f"open {path}")
        return handle

    def read_member(self, archive: HANDLE, member: str) -> bytes:
        file_handle = HANDLE()
        self._require(self.open_file(archive, member.encode("ascii"), 0, C.byref(file_handle)), f"open member {member}")
        try:
            high = DWORD()
            size = self.get_file_size(file_handle, C.byref(high))
            if high.value or size == 0xFFFFFFFF or size > 150_000_000:
                raise OverlayError(f"Unsupported MPQ member size: {member}")
            if size == 0:
                return b""
            output = C.create_string_buffer(size)
            read = DWORD()
            self._require(self.read_file(file_handle, output, size, C.byref(read), None), f"read member {member}")
            if read.value != size:
                raise OverlayError(f"Short MPQ member read: {member}")
            return output.raw
        finally:
            self.close_file(file_handle)

    def inventory(self, path: Path, *, include_bytes: bool = False) -> dict[str, dict[str, object]]:
        archive = self._open(path)
        result: dict[str, dict[str, object]] = {}
        try:
            data = FindData()
            search = self.find_first(archive, b"*", C.byref(data), None)
            if not search or search == INVALID_HANDLE:
                raise RuntimeError(f"StormLib could not enumerate {path}")
            try:
                while True:
                    name = bytes(data.name).split(b"\0", 1)[0].decode("utf-8")
                    if re.fullmatch(r"File[0-9A-Fa-f]+\..*", name):
                        raise OverlayError(f"Archive contains an unnamed member: {name}")
                    normalized = normalize_member_path(name, allow_internal=True)
                    key = normalized.casefold()
                    if key in result:
                        raise OverlayError(f"Archive contains a case-colliding member: {name}")
                    content = self.read_member(archive, name)
                    row: dict[str, object] = {"name": normalized, "bytes": len(content), "sha256": sha256_bytes(content)}
                    if include_bytes:
                        row["content"] = content
                    result[key] = row
                    if not self.find_next(search, C.byref(data)):
                        break
            finally:
                self.find_close(search)
        finally:
            self.close_archive(archive)
        return result

    def extract(self, archive_path: Path, destination: Path) -> None:
        inventory = self.inventory(archive_path, include_bytes=True)
        if destination.exists() and any(destination.iterdir()):
            raise OverlayError(f"Inspection destination is not empty: {destination}")
        destination.mkdir(parents=True, exist_ok=True)
        for row in inventory.values():
            name = str(row["name"])
            if name.startswith("("):
                continue
            target = destination.joinpath(*name.split("\\")).resolve()
            if not target.is_relative_to(destination.resolve()):
                raise OverlayError(f"Extraction escaped destination: {name}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(row["content"])

    def mutate(self, archive_path: Path, replacements: dict[str, Path], deletions: set[str]) -> None:
        archive = self._open(archive_path, writable=True)
        try:
            for member in sorted(deletions, key=str.casefold):
                self._require(self.remove_file(archive, member.encode("ascii"), 0), f"remove {member}")
            for member, source in sorted(replacements.items(), key=lambda item: item[0].casefold()):
                self._require(
                    self.add_file(archive, self._path(source), member.encode("ascii"), REPLACE_COMPRESS, ZLIB, ZLIB),
                    f"add/replace {member}",
                )
        finally:
            self.close_archive(archive)

    def compact(self, archive_path: Path) -> None:
        archive = self._open(archive_path, writable=True)
        try:
            self._require(self.compact_archive(archive, None, False), f"compact {archive_path}")
        finally:
            self.close_archive(archive)

"""Small, strict WDBC editor used by structured Patch-Y overlay operations.

Author / Creator / Last Modified By: Neil Mitchell
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from typing import Any

from .core import OverlayError


@dataclass
class Wdbc:
    field_count: int
    records: list[bytearray]
    strings: bytearray

    @classmethod
    def parse(cls, data: bytes) -> "Wdbc":
        if len(data) < 20 or data[:4] != b"WDBC":
            raise OverlayError("DBC member is not a WDBC table")
        record_count, field_count, record_size, string_size = struct.unpack_from("<4I", data, 4)
        if field_count == 0 or record_size != field_count * 4:
            raise OverlayError("Unsupported WDBC field/record layout")
        expected = 20 + record_count * record_size + string_size
        if expected != len(data):
            raise OverlayError("WDBC header sizes do not match the member bytes")
        records = [
            bytearray(data[20 + index * record_size : 20 + (index + 1) * record_size])
            for index in range(record_count)
        ]
        ids = [struct.unpack_from("<I", record, 0)[0] for record in records]
        if len(ids) != len(set(ids)):
            raise OverlayError("WDBC contains duplicate record IDs")
        return cls(field_count, records, bytearray(data[20 + record_count * record_size :]))

    def encode(self) -> bytes:
        record_size = self.field_count * 4
        header = b"WDBC" + struct.pack("<4I", len(self.records), self.field_count, record_size, len(self.strings))
        return header + b"".join(self.records) + bytes(self.strings)

    def _record(self, record_id: int) -> bytearray:
        matches = [record for record in self.records if struct.unpack_from("<I", record, 0)[0] == record_id]
        if len(matches) != 1:
            raise OverlayError(f"DBC record ID not found exactly once: {record_id}")
        return matches[0]

    def _string(self, offset: int) -> str:
        if offset < 0 or offset >= len(self.strings):
            raise OverlayError(f"DBC string offset is outside the string block: {offset}")
        end = self.strings.find(b"\0", offset)
        if end < 0:
            raise OverlayError(f"DBC string has no terminator: {offset}")
        return bytes(self.strings[offset:end]).decode("utf-8")

    def _append_string(self, value: str) -> int:
        encoded = value.encode("utf-8") + b"\0"
        offset = len(self.strings)
        self.strings.extend(encoded)
        return offset

    def apply(self, edit: dict[str, Any]) -> None:
        record = self._record(edit["recordId"])
        field = edit["fieldIndex"]
        if field < 0 or field >= self.field_count:
            raise OverlayError(f"DBC field index outside table: {field}")
        offset = field * 4
        value_type = edit["valueType"]
        old = edit["oldValue"]
        new = edit["newValue"]
        if value_type == "uint32":
            actual = struct.unpack_from("<I", record, offset)[0]
            if actual != old or not isinstance(new, int) or not 0 <= new <= 0xFFFFFFFF:
                raise OverlayError(f"DBC uint32 precondition/value failed for record {edit['recordId']} field {field}")
            struct.pack_into("<I", record, offset, new)
        elif value_type == "float32":
            actual = struct.unpack_from("<f", record, offset)[0]
            if not isinstance(old, (int, float)) or not isinstance(new, (int, float)) or actual != float(old):
                raise OverlayError(f"DBC float32 precondition/value failed for record {edit['recordId']} field {field}")
            struct.pack_into("<f", record, offset, float(new))
        elif value_type == "string":
            string_offset = struct.unpack_from("<I", record, offset)[0]
            if self._string(string_offset) != old or not isinstance(new, str):
                raise OverlayError(f"DBC string precondition/value failed for record {edit['recordId']} field {field}")
            struct.pack_into("<I", record, offset, self._append_string(new))
        else:
            raise OverlayError(f"Unsupported DBC value type: {value_type}")


def apply_edits(data: bytes, edits: list[dict[str, Any]]) -> bytes:
    table = Wdbc.parse(data)
    for edit in edits:
        table.apply(edit)
    return table.encode()

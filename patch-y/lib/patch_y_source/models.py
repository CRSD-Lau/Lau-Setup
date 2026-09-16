"""Reusable binary helpers for scoped M2/SKIN visual transforms.

These helpers do not guess offsets. A recipe must supply reviewed offsets and
strides for the exact model family being edited.

Author / Creator / Last Modified By: Neil Mitchell
"""

from __future__ import annotations

import math
import struct

from .core import OverlayError


def scale_xy_vertices(data: bytes, *, offset: int, count: int, stride: int, factor: float) -> bytes:
    if offset < 0 or count < 0 or stride < 8 or not math.isfinite(factor) or factor <= 0:
        raise OverlayError("Invalid vertex transform recipe")
    end = offset + count * stride
    if end > len(data):
        raise OverlayError("Vertex transform exceeds model bytes")
    output = bytearray(data)
    for index in range(count):
        position = offset + index * stride
        x, y = struct.unpack_from("<2f", output, position)
        struct.pack_into("<2f", output, position, x * factor, y * factor)
    return bytes(output)


def rewrite_bounds(data: bytes, *, offset: int, minimum: tuple[float, float, float], maximum: tuple[float, float, float], radius: float) -> bytes:
    values = (*minimum, *maximum, radius)
    if offset < 0 or offset + 28 > len(data) or not all(math.isfinite(value) for value in values) or radius < 0:
        raise OverlayError("Invalid model bounds recipe")
    output = bytearray(data)
    struct.pack_into("<7f", output, offset, *values)
    return bytes(output)


def replace_texture_reference(data: bytes, *, old: str, new: str, expected_occurrences: int = 1) -> bytes:
    """Replace an exact, fixed-width embedded texture reference.

    Fixed width keeps every following M2/MDX offset stable. Variable-length
    reference rewrites require a format-aware rebuild and are rejected here.
    """
    try:
        old_bytes = old.encode("ascii")
        new_bytes = new.encode("ascii")
    except UnicodeEncodeError as exc:
        raise OverlayError("Texture references must be ASCII") from exc
    if not old_bytes or len(old_bytes) != len(new_bytes) or expected_occurrences < 1:
        raise OverlayError("Texture reference replacements must be non-empty, fixed-width, and expected")
    actual = data.count(old_bytes)
    if actual != expected_occurrences:
        raise OverlayError(f"Texture reference occurrence precondition failed: expected {expected_occurrences}, found {actual}")
    return data.replace(old_bytes, new_bytes)

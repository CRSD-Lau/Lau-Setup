"""Minimal BLP2/DXT helpers for reviewable solid-color marker recipes.

Author / Creator / Last Modified By: Neil Mitchell
"""

from __future__ import annotations

import struct

from .core import OverlayError


def rgb888_to_rgb565(red: int, green: int, blue: int) -> int:
    if not all(isinstance(value, int) and 0 <= value <= 255 for value in (red, green, blue)):
        raise OverlayError("RGB components must be integers from 0 through 255")
    return ((red >> 3) << 11) | ((green >> 2) << 5) | (blue >> 3)


def recolor_dxt1_endpoints(data: bytes, *, red: int, green: int, blue: int) -> bytes:
    if len(data) < 148 or data[:4] != b"BLP2":
        raise OverlayError("Expected a BLP2 texture")
    compression = data[8]
    alpha_depth = data[9]
    alpha_encoding = data[10]
    if (compression, alpha_depth, alpha_encoding) != (2, 0, 0):
        raise OverlayError("Only opaque DXT1 BLP2 textures are supported by this helper")
    offsets = struct.unpack_from("<16I", data, 20)
    sizes = struct.unpack_from("<16I", data, 84)
    color = rgb888_to_rgb565(red, green, blue)
    output = bytearray(data)
    used = 0
    for offset, size in zip(offsets, sizes):
        if not offset and not size:
            continue
        if offset < 148 or size <= 0 or offset + size > len(output) or size % 8:
            raise OverlayError("Invalid DXT1 mip table")
        for block in range(offset, offset + size, 8):
            struct.pack_into("<HH", output, block, color, color)
        used += 1
    if not used:
        raise OverlayError("BLP2 texture has no mip levels")
    return bytes(output)

"""Build three private ICC diagnostic rings with a 12-unit visible radius.

The donor M2 quad half-width is 2.8592245579 model units. In the retained PNG,
the bright ring's outer axis is 249.5 pixels from centre across a 255.5-pixel
texture half-width (alpha and RGB >= 64). This build therefore uses a
12.2885771543-unit quad half-width so that the measured visible ring radius is
12.0 model units. Runtime yards and attachment still need in-game calibration.
Author/Creator/Modifier: Neil Mitchell.
"""

from __future__ import annotations

import hashlib
import math
import shutil
import struct
from pathlib import Path

from range_model_utils import append_aligned

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "editing" / "range-circles"
OUTPUT = ROOT / "dist" / "model" / "Spells" / "Lau_ICC_RangeTest"

EXPECTED = {
    "Range_Circle_White_Small_50.m2": "afc59a8401ec696ee84193ef6dac8990b21b56d669e5e6752fae5865e125c9f4",
    "Range_Circle_White_Small_5000.skin": "75dabfe9613e249a23931f950197dc6857b06f2cf4d41b52f5a1fb7a3eed307e",
    "Range_Circle_White_Small_50.blp": "a71b5efcb101918b6e478e1bbc0fb1535123b9f8205487112d7e434d2e9c1224",
}

CUES = {
    "ShadowPrison12": (0.15, 0.70, 1.00),
    "EmpoweredVortex12": (0.72, 0.25, 1.00),
    "BloodNova12": (1.00, 0.18, 0.12),
}
MODEL_FILES = tuple(CUES)

VISIBLE_RADIUS_FRACTION = 249.5 / 255.5
QUAD_HALF_WIDTH = 12.0 / VISIBLE_RADIUS_FRACTION


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def recolor_dxt5(source: bytes, rgb_multiplier) -> bytes:
    data = bytearray(source)
    if struct.unpack_from("<4sI4B", data) != (b"BLP2", 1, 2, 8, 7, 1):
        raise ValueError("Expected BLP2 DXT5 ring source with eight-bit alpha")
    offsets = struct.unpack_from("<16I", data, 20)
    sizes = struct.unpack_from("<16I", data, 84)
    for offset, size in zip(offsets, sizes):
        if not size:
            continue
        if size % 16:
            raise ValueError("DXT5 mip is not an even block count")
        for block in range(offset, offset + size, 16):
            # Alpha endpoints/indices and color indices remain byte-identical.
            for endpoint in (block + 8, block + 10):
                value = struct.unpack_from("<H", data, endpoint)[0]
                red, green, blue = (value >> 11) & 31, (value >> 5) & 63, value & 31
                red = min(31, round(red * rgb_multiplier[0]))
                green = min(63, round(green * rgb_multiplier[1]))
                blue = min(31, round(blue * rgb_multiplier[2]))
                struct.pack_into("<H", data, endpoint, (red << 11) | (green << 5) | blue)
    return bytes(data)


def build_model(source: bytes, stem: str) -> bytes:
    data = bytearray(source)
    if data[:4] != b"MD20":
        raise ValueError("Expected Wrath MD20 model")
    vertex_count, vertex_offset = struct.unpack_from("<II", data, 60)
    if vertex_count != 4:
        raise ValueError(f"Expected four-vertex ring donor, got {vertex_count}")
    positions = [struct.unpack_from("<3f", data, vertex_offset + i * 48) for i in range(vertex_count)]
    donor_radius = max(max(abs(x), abs(y)) for x, y, _ in positions)
    if not math.isclose(donor_radius, 2.859224557876587, abs_tol=1e-6):
        raise ValueError(f"Unexpected donor radius {donor_radius}")
    scale = QUAD_HALF_WIDTH / donor_radius
    updated = []
    for index, (x, y, z) in enumerate(positions):
        xyz = (x * scale, y * scale, z)
        updated.append(xyz)
        struct.pack_into("<3f", data, vertex_offset + index * 48, *xyz)
    minimum = tuple(min(v[axis] for v in updated) for axis in range(3))
    maximum = tuple(max(v[axis] for v in updated) for axis in range(3))
    radius = max(math.sqrt(sum(c * c for c in v)) for v in updated)
    bounds = minimum + maximum + (radius,)
    struct.pack_into("<7f", data, 160, *bounds)
    sequence_count, sequence_offset = struct.unpack_from("<II", data, 28)
    if sequence_count != 3:
        raise ValueError(f"Expected three native ring sequences, got {sequence_count}")
    for index in range(sequence_count):
        # Only each sequence's seven-float bounds block changes.
        struct.pack_into("<7f", data, sequence_offset + index * 64 + 32, *bounds)

    texture_count, texture_offset = struct.unpack_from("<II", data, 80)
    if texture_count != 1:
        raise ValueError(f"Expected one donor texture, got {texture_count}")
    texture_path = f"Spells\\Lau_ICC_RangeTest\\{stem}.blp".encode("ascii") + b"\0"
    path_offset = append_aligned(data, texture_path)
    texture_type, flags, _, _ = struct.unpack_from("<4I", data, texture_offset)
    struct.pack_into("<4I", data, texture_offset, texture_type, flags, len(texture_path), path_offset)
    return bytes(data)


def build_skin(source: bytes, model: bytes) -> bytes:
    data = bytearray(source)
    if data[:4] != b"SKIN":
        raise ValueError("Expected native SKIN input")
    vertex_count, vertex_offset = struct.unpack_from("<II", model, 60)
    vertices = [struct.unpack_from("<3f", model, vertex_offset + index * 48) for index in range(vertex_count)]
    minimum = tuple(min(v[axis] for v in vertices) for axis in range(3))
    maximum = tuple(max(v[axis] for v in vertices) for axis in range(3))
    center = tuple((minimum[axis] + maximum[axis]) / 2 for axis in range(3))
    # Use the conservative model/sequence radius from origin. It is 0.0022
    # units larger than the centre-relative XY corner radius because Z=0.2778.
    radius = max(math.sqrt(sum(c * c for c in v)) for v in vertices)
    submesh_count, submesh_offset = struct.unpack_from("<II", data, 28)
    if submesh_count != 1:
        raise ValueError(f"Expected one ring submesh, got {submesh_count}")
    struct.pack_into("<7f", data, submesh_offset + 20, *(center + center + (radius,)))
    return bytes(data)


def main():
    inputs = {}
    for name, expected_hash in EXPECTED.items():
        data = (SOURCE / name).read_bytes()
        if sha256(data) != expected_hash:
            raise ValueError(f"Native input hash mismatch: {name}")
        inputs[name] = data
    if OUTPUT.exists():
        resolved = OUTPUT.resolve()
        expected_parent = (ROOT / "dist" / "model" / "Spells").resolve()
        if resolved.parent != expected_parent or ROOT.resolve() not in resolved.parents:
            raise ValueError(f"Refusing to reset unexpected model directory: {resolved}")
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for stem, color in CUES.items():
        model = build_model(inputs["Range_Circle_White_Small_50.m2"], stem)
        (OUTPUT / f"{stem}.m2").write_bytes(model)
        (OUTPUT / f"{stem}00.skin").write_bytes(
            build_skin(inputs["Range_Circle_White_Small_5000.skin"], model)
        )
        (OUTPUT / f"{stem}.blp").write_bytes(recolor_dxt5(inputs["Range_Circle_White_Small_50.blp"], color))
        print(
            f"PASS visible-radius=12.0 quad-half-width={QUAD_HALF_WIDTH:.10f} cue={stem}",
            flush=True,
        )


if __name__ == "__main__":
    main()

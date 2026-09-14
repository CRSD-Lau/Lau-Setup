"""Build the static BPC floor-marker test payload.

The markers are a one-yard, low-contrast ring used as room-fixed doodads in
the Blood Prince Council WMO.  They are deliberately not spell visuals: this
test is for the supplied 25-player position plan and remains visible only in
that room.  Author/Creator/Modifier: Neil Mitchell.
"""

from __future__ import annotations

import hashlib
import math
import shutil
import struct
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from range_model_utils import append_aligned


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "editing" / "range-circles"
NATIVE = ROOT / "editing" / "native" / "World" / "WMO" / "Dungeon" / "IcecrownRaid" / "middle_section"
OUTPUT = ROOT / "dist" / "model" / "Spells" / "Lau_BPC_FloorMarkers"
WMO_OUTPUT = ROOT / "dist" / "wmo" / "World" / "WMO" / "Dungeon" / "IcecrownRaid"
PRIVATE_PREFIX = "Spells\\Lau_BPC_FloorMarkers"

EXPECTED = {
    "Range_Circle_White_Small_50.m2": "afc59a8401ec696ee84193ef6dac8990b21b56d669e5e6752fae5865e125c9f4",
    "Range_Circle_White_Small_5000.skin": "75dabfe9613e249a23931f950197dc6857b06f2cf4d41b52f5a1fb7a3eed307e",
    "Range_Circle_White_Small_50.blp": "a71b5efcb101918b6e478e1bbc0fb1535123b9f8205487112d7e434d2e9c1224",
}

# The supplied image is a tactical guide, not literal world coordinates. These
# inferred room points preserve its role zones while enforcing a 13-yard centre
# separation between every pair: a one-yard margin over Vortex's 12-yard range.
MARKER_POINTS = (
    ("M1", -25, 260), ("M2", -5, 260), ("M3", -45, 260), ("M4", 15, 260),
    ("M5", -65, 260), ("M6", 35, 260), ("M7", -55, 275), ("M8", 25, 275),
    ("M9", -80, 275), ("M10", 45, 275),
    ("H1", -25, 294), ("H2", 15, 294), ("H3", -55, 294), ("H4", -40, 310),
    ("H5", -5, 310),
    ("R1", -95, 294), ("R2", -80, 310), ("R3", -75, 330), ("R4", -70, 350),
    ("R5", -35, 365), ("R6", 0, 365), ("R7", 30, 345), ("R8", 45, 330),
    ("R9", 55, 310), ("R10", 65, 292),
)
MINIMUM_SEPARATION = 13.0


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_chunks(data: bytes):
    chunks, offset = [], 0
    while offset + 8 <= len(data):
        raw_tag = data[offset:offset + 4]
        size = struct.unpack_from("<I", data, offset + 4)[0]
        end = offset + 8 + size
        if end > len(data):
            raise ValueError("Truncated WMO chunk")
        chunks.append((raw_tag, data[offset + 8:end]))
        offset = end
    if offset != len(data):
        raise ValueError("Trailing incomplete WMO data")
    return chunks


def write_chunks(chunks):
    return b"".join(tag + struct.pack("<I", len(payload)) + payload for tag, payload in chunks)


def marker_path(label: str, suffix: str) -> str:
    return f"{PRIVATE_PREFIX}\\{label}.{suffix}"


def build_model(source: bytes, label: str) -> bytes:
    data = bytearray(source)
    count, offset = struct.unpack_from("<II", data, 60)
    if data[:4] != b"MD20" or count != 4:
        raise ValueError("Unexpected native ring donor")
    old = [struct.unpack_from("<3f", data, offset + index * 48) for index in range(count)]
    donor_radius = max(max(abs(x), abs(y)) for x, y, _ in old)
    if not math.isclose(donor_radius, 2.859224557876587, abs_tol=1e-6):
        raise ValueError("Unexpected native ring radius")
    scaled = []
    for index, (x, y, z) in enumerate(old):
        value = (x / donor_radius, y / donor_radius, z)
        scaled.append(value)
        struct.pack_into("<3f", data, offset + index * 48, *value)
    minimum = tuple(min(value[axis] for value in scaled) for axis in range(3))
    maximum = tuple(max(value[axis] for value in scaled) for axis in range(3))
    radius = max(math.sqrt(sum(value * value for value in row)) for row in scaled)
    bounds = minimum + maximum + (radius,)
    struct.pack_into("<7f", data, 160, *bounds)
    sequences, sequence_offset = struct.unpack_from("<II", data, 28)
    for index in range(sequences):
        struct.pack_into("<7f", data, sequence_offset + index * 64 + 32, *bounds)
    textures, texture_offset = struct.unpack_from("<II", data, 80)
    if textures != 1:
        raise ValueError("Unexpected native ring texture count")
    path = marker_path(label, "blp").encode("ascii") + b"\0"
    path_offset = append_aligned(data, path)
    kind, flags, _, _ = struct.unpack_from("<4I", data, texture_offset)
    struct.pack_into("<4I", data, texture_offset, kind, flags, len(path), path_offset)
    return bytes(data)


def build_skin(source: bytes, model: bytes) -> bytes:
    data = bytearray(source)
    count, offset = struct.unpack_from("<II", model, 60)
    vertices = [struct.unpack_from("<3f", model, offset + index * 48) for index in range(count)]
    minimum = tuple(min(row[axis] for row in vertices) for axis in range(3))
    maximum = tuple(max(row[axis] for row in vertices) for axis in range(3))
    centre = tuple((minimum[axis] + maximum[axis]) / 2 for axis in range(3))
    radius = max(math.sqrt(sum(value * value for value in row)) for row in vertices)
    _, submesh_offset = struct.unpack_from("<II", data, 28)
    struct.pack_into("<7f", data, submesh_offset + 20, *(centre + centre + (radius,)))
    return bytes(data)


def rgb565(rgb):
    return ((rgb[0] * 31 + 127) // 255 << 11) | ((rgb[1] * 63 + 127) // 255 << 5) | ((rgb[2] * 31 + 127) // 255)


def unpack565(value):
    return ((value >> 11) * 255 // 31, ((value >> 5) & 63) * 255 // 63, (value & 31) * 255 // 31)


def dxt5_block(pixels):
    alphas = [pixel[3] for pixel in pixels]
    a0, a1 = max(alphas), min(alphas)
    alpha_palette = [a0, a1] + [(a0 * (7 - index) + a1 * index) // 7 for index in range(1, 7)] if a0 > a1 else [a0] * 8
    alpha_bits = sum(min(range(8), key=lambda index: abs(alpha_palette[index] - alpha)) << (3 * index) for index, alpha in enumerate(alphas))
    colors = [pixel[:3] for pixel in pixels]
    low, high = min(colors, key=sum), max(colors, key=sum)
    c0, c1 = rgb565(high), rgb565(low)
    if c0 <= c1: c0, c1 = c1, c0
    first, second = unpack565(c0), unpack565(c1)
    color_palette = [first, second, tuple((2 * first[i] + second[i]) // 3 for i in range(3)), tuple((first[i] + 2 * second[i]) // 3 for i in range(3))]
    color_bits = sum(min(range(4), key=lambda index: sum((color_palette[index][channel] - color[channel]) ** 2 for channel in range(3))) << (2 * index) for index, color in enumerate(colors))
    return struct.pack("<BB", a0, a1) + alpha_bits.to_bytes(6, "little") + struct.pack("<HHI", c0, c1, color_bits)


def labelled_dxt5(source: bytes, label: str) -> bytes:
    if struct.unpack_from("<4sI4B", source) != (b"BLP2", 1, 2, 8, 7, 1):
        raise ValueError("Unexpected native ring texture")
    width, height = struct.unpack_from("<II", source, 12)
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    inset, edge = 34, 10
    # A dark stone-like plaque and fine cold-grey rim stay legible while fitting ICC's floor.
    draw.ellipse((inset, inset, width - inset, height - inset), fill=(64, 74, 79, 105), outline=(134, 148, 151, 160), width=edge)
    draw.ellipse((inset + 22, inset + 22, width - inset - 22, height - inset - 22), outline=(37, 45, 50, 125), width=5)
    font = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 136 if len(label) == 2 else 112)
    box = draw.textbbox((0, 0), label, font=font)
    position = ((width - (box[2] - box[0])) // 2, (height - (box[3] - box[1])) // 2 - box[1] - 6)
    draw.text(position, label, font=font, fill=(202, 215, 213, 225), stroke_width=2, stroke_fill=(24, 31, 35, 205))
    header, offset, mip_payloads = bytearray(source[:148]), 148, []
    while True:
        rgba = image.convert("RGBA")
        pixels = list(rgba.getdata())
        payload = b"".join(dxt5_block([pixels[min(y + dy, rgba.height - 1) * rgba.width + min(x + dx, rgba.width - 1)] for dy in range(4) for dx in range(4)]) for y in range(0, rgba.height, 4) for x in range(0, rgba.width, 4))
        mip_payloads.append(payload)
        if rgba.width == rgba.height == 1: break
        image = rgba.resize((max(1, rgba.width // 2), max(1, rgba.height // 2)), Image.Resampling.LANCZOS)
    for index, payload in enumerate(mip_payloads):
        struct.pack_into("<I", header, 20 + index * 4, offset)
        struct.pack_into("<I", header, 84 + index * 4, len(payload))
        offset += len(payload)
    return bytes(header) + b"".join(mip_payloads)


def group_chunks(data: bytes):
    chunks = read_chunks(data)
    if len(chunks) < 2 or chunks[0][0][::-1] != b"MVER" or chunks[1][0][::-1] != b"MOGP":
        raise ValueError("Expected an MVER/MOGP WMO group")
    header_and_children = chunks[1][1]
    if len(header_and_children) < 68:
        raise ValueError("Short MOGP header")
    return chunks, header_and_children[:68], read_chunks(header_and_children[68:])


def floor_height(group_data: bytes, x: float, y: float) -> float:
    _, _, children = group_chunks(group_data)
    data = {tag[::-1].decode("ascii"): payload for tag, payload in children}
    vertices = [struct.unpack_from("<3f", data["MOVT"], offset) for offset in range(0, len(data["MOVT"]), 12)]
    indices = struct.unpack("<" + str(len(data["MOVI"]) // 2) + "H", data["MOVI"])
    heights = []
    for offset in range(0, len(indices), 3):
        a, b, c = (vertices[indices[offset + index]] for index in range(3))
        determinant = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
        if abs(determinant) < 1e-7:
            continue
        u = ((b[1] - c[1]) * (x - c[0]) + (c[0] - b[0]) * (y - c[1])) / determinant
        v = ((c[1] - a[1]) * (x - c[0]) + (a[0] - c[0]) * (y - c[1])) / determinant
        w = 1.0 - u - v
        if min(u, v, w) >= -1e-5:
            heights.append(u * a[2] + v * b[2] + w * c[2])
    if not heights:
        raise ValueError(f"No floor triangle under BPC marker at {x:.2f}, {y:.2f}")
    # The topmost local surface is the walkable floor at this point.
    return max(heights)


def patch_wmo(root_data: bytes, group_data: bytes):
    root = read_chunks(root_data)
    by_tag = {tag[::-1].decode("ascii"): index for index, (tag, _) in enumerate(root)}
    for required in ("MOHD", "MODS", "MODN", "MODD"):
        if required not in by_tag:
            raise ValueError(f"Missing root WMO {required}")
    modn_index, modd_index = by_tag["MODN"], by_tag["MODD"]
    names = bytearray(root[modn_index][1])
    old_defs = root[modd_index][1]
    if len(old_defs) % 40:
        raise ValueError("Malformed MODD")
    start = len(old_defs) // 40
    records, marker_report = bytearray(), []
    for label, x, y in MARKER_POINTS:
        name_offset = len(names)
        names.extend(marker_path(label, "mdx").encode("ascii") + b"\0")
        z = floor_height(group_data, x, y)
        records.extend(struct.pack("<I3f4ffI", name_offset, x, y, z, 0.0, 0.0, 0.0, 1.0, 1.0, 0xFF6F7A80))
        marker_report.append({"label": label, "x": round(x, 3), "y": round(y, 3), "z": round(z, 3)})
    root[modn_index] = (root[modn_index][0], bytes(names))
    root[modd_index] = (root[modd_index][0], old_defs + bytes(records))
    mohd_index = by_tag["MOHD"]
    mohd = bytearray(root[mohd_index][1])
    # Preserve the source header's historic 15-entry delta while extending it.
    original_count = struct.unpack_from("<I", mohd, 20)[0]
    struct.pack_into("<I", mohd, 20, original_count + len(MARKER_POINTS))
    root[mohd_index] = (root[mohd_index][0], bytes(mohd))
    mods_index = by_tag["MODS"]
    mods = bytearray(root[mods_index][1])
    if len(mods) != 32:
        raise ValueError("Expected one BPC default doodad set")
    struct.pack_into("<I", mods, 24, struct.unpack_from("<I", mods, 24)[0] + len(MARKER_POINTS))
    root[mods_index] = (root[mods_index][0], bytes(mods))

    outer, header, children = group_chunks(group_data)
    for index, (tag, payload) in enumerate(children):
        if tag[::-1] == b"MODR":
            refs = list(struct.unpack("<" + str(len(payload) // 2) + "H", payload))
            refs.extend(range(start, start + len(MARKER_POINTS)))
            children[index] = (tag, struct.pack("<" + str(len(refs)) + "H", *refs))
            break
    else:
        # Some WMO groups have no original doodads.  A MODR table and matching
        # group flag keep the test markers scoped to the selected room group.
        children.append((b"RDOM", struct.pack("<" + str(len(MARKER_POINTS)) + "H", *range(start, start + len(MARKER_POINTS)))))
        header = bytearray(header)
        struct.pack_into("<I", header, 8, struct.unpack_from("<I", header, 8)[0] | 0x800)
        header = bytes(header)
    outer[1] = (outer[1][0], header + write_chunks(children))
    return write_chunks(root), write_chunks(outer), marker_report


def reset(path: Path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def main():
    inputs = {}
    for filename, expected in EXPECTED.items():
        value = (SOURCE / filename).read_bytes()
        if sha256(value) != expected:
            raise ValueError(f"Native input hash mismatch: {filename}")
        inputs[filename] = value
    reset(OUTPUT)
    for label, _, _ in MARKER_POINTS:
        model = build_model(inputs["Range_Circle_White_Small_50.m2"], label)
        (OUTPUT / f"{label}.m2").write_bytes(model)
        (OUTPUT / f"{label}00.skin").write_bytes(build_skin(inputs["Range_Circle_White_Small_5000.skin"], model))
        (OUTPUT / f"{label}.blp").write_bytes(labelled_dxt5(inputs["Range_Circle_White_Small_50.blp"], label))
    root, group, report = patch_wmo(
        (NATIVE / "IcecrownRaid_middle_section.wmo").read_bytes(),
        (NATIVE / "IcecrownRaid_middle_section_023.wmo").read_bytes(),
    )
    reset(WMO_OUTPUT)
    (WMO_OUTPUT / "IcecrownRaid_middle_section.wmo").write_bytes(root)
    (WMO_OUTPUT / "IcecrownRaid_middle_section_023.wmo").write_bytes(group)
    separations = [
        (math.hypot(left[1] - right[1], left[2] - right[2]), left[0], right[0])
        for index, left in enumerate(MARKER_POINTS)
        for right in MARKER_POINTS[index + 1:]
    ]
    closest, closest_left, closest_right = min(separations)
    if closest < MINIMUM_SEPARATION:
        raise ValueError(f"BPC marker separation {closest:.3f} is below {MINIMUM_SEPARATION:.1f} yards")
    report_path = ROOT / "dist" / "bpc-floor-marker-positions.json"
    report_path.write_text(__import__("json").dumps(report, indent=2) + "\n", encoding="utf-8")
    (ROOT / "dist" / "bpc-floor-marker-separation.json").write_text(
        __import__("json").dumps({
            "Author": "Neil Mitchell", "Creator": "Neil Mitchell", "LastModifiedBy": "Neil Mitchell",
            "minimum_required_planar_yards": MINIMUM_SEPARATION,
            "minimum_actual_planar_yards": round(closest, 3),
            "closest_pair": [closest_left, closest_right],
            "all_pairs_at_least_minimum": True,
        }, indent=2) + "\n", encoding="utf-8")
    print(f"PASS BPC static markers={len(report)} radius=1.0 model-units min-separation={closest:.3f}")
    for row in report:
        print(f"{row['label']}: ({row['x']}, {row['y']}, {row['z']})")


if __name__ == "__main__":
    main()

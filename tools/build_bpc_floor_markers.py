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

from range_model_utils import append_aligned


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "editing" / "range-circles"
NATIVE = ROOT / "editing" / "native" / "World" / "WMO" / "Dungeon" / "IcecrownRaid" / "middle_section"
OUTPUT = ROOT / "dist" / "model" / "Spells" / "Lau_BPC_FloorMarkers"
WMO_OUTPUT = ROOT / "dist" / "wmo" / "World" / "WMO" / "Dungeon" / "IcecrownRaid"
MARKER_PATH = "Spells\\Lau_BPC_FloorMarkers\\Bpc_Floor_Marker.mdx"

EXPECTED = {
    "Range_Circle_White_Small_50.m2": "afc59a8401ec696ee84193ef6dac8990b21b56d669e5e6752fae5865e125c9f4",
    "Range_Circle_White_Small_5000.skin": "75dabfe9613e249a23931f950197dc6857b06f2cf4d41b52f5a1fb7a3eed307e",
    "Range_Circle_White_Small_50.blp": "a71b5efcb101918b6e478e1bbc0fb1535123b9f8205487112d7e434d2e9c1224",
}

# These screenshot-space centres are the supplied plan.  The BPC room overlay
# is named upperbloodprince and spans X=-94.5..55.2, Y=246.5..322.7; its main
# walkable geometry is middle-section group 023 (icetop).  The planner image
# map area is X=575..1786, Y=102..784, so this projection preserves the exact
# relative layout while placing every point on that group's real floor.
SCREEN_POINTS = (
    ("M1", 1124, 278), ("M2", 1245, 278), ("M3", 1087, 233), ("M4", 1282, 234),
    ("M5", 965, 234), ("M6", 1406, 234), ("M7", 850, 278), ("M8", 1537, 278),
    ("M9", 749, 301), ("M10", 1622, 301),
    ("H1", 1186, 459), ("H2", 1380, 447), ("H3", 992, 447), ("H4", 1064, 536),
    ("H5", 1320, 536),
    ("R1", 625, 484), ("R2", 883, 396), ("R3", 820, 476), ("R4", 771, 662),
    ("R5", 1040, 728), ("R6", 1330, 728), ("R7", 1599, 653), ("R8", 1574, 475),
    ("R9", 1488, 396), ("R10", 1745, 475),
)


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


def build_model(source: bytes) -> bytes:
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
    path = MARKER_PATH.replace(".mdx", ".blp").encode("ascii") + b"\0"
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


def tint_dxt5(source: bytes) -> bytes:
    data = bytearray(source)
    if struct.unpack_from("<4sI4B", data) != (b"BLP2", 1, 2, 8, 7, 1):
        raise ValueError("Unexpected native ring texture")
    offsets = struct.unpack_from("<16I", data, 20)
    sizes = struct.unpack_from("<16I", data, 84)
    for offset, size in zip(offsets, sizes):
        for block in range(offset, offset + size, 16):
            for endpoint in (block + 8, block + 10):
                value = struct.unpack_from("<H", data, endpoint)[0]
                red, green, blue = (value >> 11) & 31, (value >> 5) & 63, value & 31
                # Muted cold-grey: readable on ICC stone but deliberately not a beacon.
                red, green, blue = round(red * .38), round(green * .43), round(blue * .48)
                struct.pack_into("<H", data, endpoint, (red << 11) | (green << 5) | blue)
    return bytes(data)


def group_chunks(data: bytes):
    chunks = read_chunks(data)
    if len(chunks) < 2 or chunks[0][0][::-1] != b"MVER" or chunks[1][0][::-1] != b"MOGP":
        raise ValueError("Expected an MVER/MOGP WMO group")
    header_and_children = chunks[1][1]
    if len(header_and_children) < 68:
        raise ValueError("Short MOGP header")
    return chunks, header_and_children[:68], read_chunks(header_and_children[68:])


def point_to_local(screen_x: int, screen_y: int):
    return (
        -94.5 + (screen_x - 575.0) * (149.7 / 1211.0),
        246.5 + (screen_y - 102.0) * (76.2 / 682.0),
    )


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
    name_offset = len(names)
    names.extend(MARKER_PATH.encode("ascii") + b"\0")
    records, marker_report = bytearray(), []
    for label, screen_x, screen_y in SCREEN_POINTS:
        x, y = point_to_local(screen_x, screen_y)
        z = floor_height(group_data, x, y)
        records.extend(struct.pack("<I3f4ffI", name_offset, x, y, z, 0.0, 0.0, 0.0, 1.0, 1.0, 0xFF6F7A80))
        marker_report.append({"label": label, "x": round(x, 3), "y": round(y, 3), "z": round(z, 3)})
    root[modn_index] = (root[modn_index][0], bytes(names))
    root[modd_index] = (root[modd_index][0], old_defs + bytes(records))
    mohd_index = by_tag["MOHD"]
    mohd = bytearray(root[mohd_index][1])
    # Preserve the source header's historic 15-entry delta while extending it.
    original_count = struct.unpack_from("<I", mohd, 20)[0]
    struct.pack_into("<I", mohd, 20, original_count + len(SCREEN_POINTS))
    root[mohd_index] = (root[mohd_index][0], bytes(mohd))
    mods_index = by_tag["MODS"]
    mods = bytearray(root[mods_index][1])
    if len(mods) != 32:
        raise ValueError("Expected one BPC default doodad set")
    struct.pack_into("<I", mods, 24, struct.unpack_from("<I", mods, 24)[0] + len(SCREEN_POINTS))
    root[mods_index] = (root[mods_index][0], bytes(mods))

    outer, header, children = group_chunks(group_data)
    for index, (tag, payload) in enumerate(children):
        if tag[::-1] == b"MODR":
            refs = list(struct.unpack("<" + str(len(payload) // 2) + "H", payload))
            refs.extend(range(start, start + len(SCREEN_POINTS)))
            children[index] = (tag, struct.pack("<" + str(len(refs)) + "H", *refs))
            break
    else:
        # Some WMO groups have no original doodads.  A MODR table and matching
        # group flag keep the test markers scoped to the selected room group.
        children.append((b"RDOM", struct.pack("<" + str(len(SCREEN_POINTS)) + "H", *range(start, start + len(SCREEN_POINTS)))))
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
    model = build_model(inputs["Range_Circle_White_Small_50.m2"])
    (OUTPUT / "Bpc_Floor_Marker.m2").write_bytes(model)
    (OUTPUT / "Bpc_Floor_Marker00.skin").write_bytes(build_skin(inputs["Range_Circle_White_Small_5000.skin"], model))
    (OUTPUT / "Bpc_Floor_Marker.blp").write_bytes(tint_dxt5(inputs["Range_Circle_White_Small_50.blp"]))
    root, group, report = patch_wmo(
        (NATIVE / "IcecrownRaid_middle_section.wmo").read_bytes(),
        (NATIVE / "IcecrownRaid_middle_section_023.wmo").read_bytes(),
    )
    reset(WMO_OUTPUT)
    (WMO_OUTPUT / "IcecrownRaid_middle_section.wmo").write_bytes(root)
    (WMO_OUTPUT / "IcecrownRaid_middle_section_023.wmo").write_bytes(group)
    report_path = ROOT / "dist" / "bpc-floor-marker-positions.json"
    report_path.write_text(__import__("json").dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"PASS BPC static markers={len(report)} radius=1.0 model-units")
    for row in report:
        print(f"{row['label']}: ({row['x']}, {row['y']}, {row['z']})")


if __name__ == "__main__":
    main()

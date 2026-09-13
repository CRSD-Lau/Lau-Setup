"""Static regression tests for generated ICC range-circle artifacts.

Author/Creator/Modifier: Neil Mitchell.
"""

from __future__ import annotations

import hashlib
import json
import math
import struct
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_range_model import EXPECTED, MODEL_FILES, QUAD_HALF_WIDTH, ROOT, SOURCE
from range_model_utils import by_id, load_wdbc, u32

DIST = ROOT / "dist"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class RangeModelTests(unittest.TestCase):
    def test_native_inputs_are_exact(self):
        for name, expected in EXPECTED.items():
            self.assertEqual(sha256(SOURCE / name), expected)

    def test_private_models_have_measured_visible_radius(self):
        source = (SOURCE / "Range_Circle_White_Small_50.m2").read_bytes()
        bone_count, bone_offset = struct.unpack_from("<II", source, 44)
        render_count, render_offset = struct.unpack_from("<II", source, 112)
        sequence_count, sequence_offset = struct.unpack_from("<II", source, 28)
        for stem in MODEL_FILES:
            path = DIST / "model" / "Spells" / "Lau_ICC_RangeTest" / f"{stem}.m2"
            data = path.read_bytes()
            vertex_count, vertex_offset = struct.unpack_from("<II", data, 60)
            positions = [struct.unpack_from("<3f", data, vertex_offset + i * 48) for i in range(vertex_count)]
            self.assertEqual(vertex_count, 4)
            self.assertAlmostEqual(max(max(abs(x), abs(y)) for x, y, _ in positions), QUAD_HALF_WIDTH, places=5)
            visible = QUAD_HALF_WIDTH * (249.5 / 255.5)
            self.assertAlmostEqual(visible, 12.0, places=7)
            bounds = struct.unpack_from("<7f", data, 160)
            expected_radius = max(math.sqrt(sum(c * c for c in vertex)) for vertex in positions)
            self.assertAlmostEqual(bounds[0], min(v[0] for v in positions), places=5)
            self.assertAlmostEqual(bounds[1], min(v[1] for v in positions), places=5)
            self.assertAlmostEqual(bounds[3], max(v[0] for v in positions), places=5)
            self.assertAlmostEqual(bounds[4], max(v[1] for v in positions), places=5)
            self.assertAlmostEqual(bounds[6], expected_radius, places=5)
            self.assertEqual(sequence_count, 3)
            for index in range(sequence_count):
                self.assertEqual(
                    struct.unpack_from("<7f", data, sequence_offset + index * 64 + 32),
                    bounds,
                )
            self.assertEqual(
                data[bone_offset : bone_offset + bone_count * 88],
                source[bone_offset : bone_offset + bone_count * 88],
            )
            self.assertEqual(
                data[render_offset : render_offset + render_count * 4],
                source[render_offset : render_offset + render_count * 4],
            )
            texture_count, texture_offset = struct.unpack_from("<II", data, 80)
            self.assertEqual(texture_count, 1)
            _, _, length, offset = struct.unpack_from("<4I", data, texture_offset)
            self.assertEqual(data[offset : offset + length], f"Spells\\Lau_ICC_RangeTest\\{stem}.blp\0".encode())

    def test_skin_changes_are_limited_to_submesh_bounds_and_cue_textures_are_distinct(self):
        donor_skin = (SOURCE / "Range_Circle_White_Small_5000.skin").read_bytes()
        textures = []
        for stem in MODEL_FILES:
            base = DIST / "model" / "Spells" / "Lau_ICC_RangeTest"
            skin = (base / f"{stem}00.skin").read_bytes()
            submesh_count, submesh_offset = struct.unpack_from("<II", skin, 28)
            self.assertEqual(submesh_count, 1)
            allowed = set(range(submesh_offset + 20, submesh_offset + 48))
            self.assertTrue(all(old == new or index in allowed for index, (old, new) in enumerate(zip(donor_skin, skin))))
            self.assertEqual(len(skin), len(donor_skin))
            center_a = struct.unpack_from("<3f", skin, submesh_offset + 20)
            center_b = struct.unpack_from("<3f", skin, submesh_offset + 32)
            radius = struct.unpack_from("<f", skin, submesh_offset + 44)[0]
            self.assertEqual(center_a, center_b)
            self.assertAlmostEqual(center_a[0], 0.0, places=5)
            self.assertAlmostEqual(center_a[1], 0.0, places=5)
            self.assertAlmostEqual(center_a[2], 0.277777791, places=5)
            self.assertAlmostEqual(radius, math.sqrt(2 * QUAD_HALF_WIDTH**2 + center_a[2] ** 2), places=4)
            texture = (base / f"{stem}.blp").read_bytes()
            self.assertEqual(struct.unpack_from("<4sI4B", texture), (b"BLP2", 1, 2, 8, 7, 1))
            textures.append(hashlib.sha256(texture).hexdigest())
        self.assertEqual(len(set(textures)), 3)


class RangePayloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((DIST / "catalog.json").read_text(encoding="utf-8"))
        cls.baseline = json.loads((DIST / "baseline.json").read_text(encoding="utf-8"))
        cls.scope = json.loads((DIST / "scope-validation.json").read_text(encoding="utf-8"))

    def test_metadata_and_runtime_limit(self):
        self.assertEqual(self.scope["Author"], "Neil Mitchell")
        self.assertEqual(self.scope["Creator"], "Neil Mitchell")
        self.assertEqual(self.scope["LastModifiedBy"], "Neil Mitchell")
        self.assertTrue(self.scope["geometry_basis"]["runtime_calibration_required"])
        self.assertFalse(self.catalog["PublicReady"])

    def test_six_archive_hashes_match_catalog(self):
        results = self.scope["results"]
        self.assertEqual(len(results), 6)
        for result in results:
            edition = result["edition"]
            archive = DIST / "payload" / f"{edition}.mpq"
            asset = self.catalog["Assets"][edition]
            self.assertEqual(archive.stat().st_size, asset["Bytes"])
            self.assertEqual(sha256(archive), asset["Sha256"])
            self.assertEqual(sha256(DIST / "payload" / f"{asset['Sha256']}.bin"), asset["Sha256"])
            self.assertTrue(result["unrelated_members_byte_identical"])
            self.assertTrue(result["archive_snapshot_readback_exact"])

    def test_exact_spell_visual_only_diffs(self):
        expected = {72038, 72815, 72816, 72817, 72378, 73058, 73001}
        excluded = {72379, 72380, 72438, 72439, 72440, 72998}
        for result in self.scope["results"]:
            dbc = result["dbc"]
            spell = dbc["Spell"]
            self.assertEqual(set(spell["changed_original_ids"]), expected)
            self.assertTrue(excluded.isdisjoint(spell["changed_original_ids"]))
            for record in spell["record_field_diffs"]:
                self.assertEqual({diff["field"] for diff in record["field_diffs"]}, {131})
            for table in ("SpellVisual", "SpellVisualKit", "SpellVisualEffectName", "SpellVisualKitModelAttach"):
                self.assertEqual(dbc[table]["changed_original_ids"], [])
                self.assertEqual(len(dbc[table]["added_ids"]), 3)

    def test_per_edition_spell_strings_are_preserved(self):
        for result in self.scope["results"]:
            self.assertTrue(result["dbc"]["Spell"]["original_string_block_prefix_preserved"])
            self.assertEqual(
                result["dbc"]["Spell"]["before_records"],
                result["dbc"]["Spell"]["after_records"],
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)

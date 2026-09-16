"""Patch-Y source unit and integration tests.

Author / Creator / Last Modified By: Neil Mitchell
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import struct
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "patch-y" / "lib"))

from patch_y_source.blp import recolor_dxt1_endpoints, rgb888_to_rgb565
from patch_y_source.core import OverlayError, load_baseline, load_operations, load_servers, normalize_member_path
from patch_y_source.dbc import Wdbc, apply_edits
from patch_y_source.models import replace_texture_reference, rewrite_bounds, scale_xy_vertices
from patch_y_source.workflow import build_candidates


class ManifestTests(unittest.TestCase):
    def test_public_baseline_describes_six_hash_pinned_editions(self):
        baseline = load_baseline(ROOT / "patch-y" / "baseline.json")

        self.assertEqual("3.0.9", baseline["gameVersion"])
        self.assertEqual(6, len(baseline["editions"]))
        self.assertGreater((ROOT / "patch-y" / "baseline.json").stat().st_size, 500_000)
        self.assertEqual({500, 507, 508}, {row["memberCount"] for row in baseline["editions"].values()})

    def test_rejects_traversal_absolute_internal_and_unsupported_paths(self):
        rejected = ["../secret.blp", "C:\\client\\x.blp", "(listfile)", "Spells\\x.exe", "Spells\\bad\0name.blp"]

        for value in rejected:
            with self.subTest(value=value), self.assertRaises(OverlayError):
                normalize_member_path(value)

    def test_empty_public_overlays_cover_all_six_editions(self):
        baseline = load_baseline(ROOT / "patch-y" / "baseline.json")

        operations = load_operations(ROOT / "patch-y", baseline["editions"])

        self.assertEqual(set(baseline["editions"]), set(operations))
        self.assertTrue(all(not rows for rows in operations.values()))

    def test_server_profiles_keep_warmane_and_wowcircle_requirements_separate(self):
        profiles = load_servers(ROOT / "patch-y" / "servers.json")

        self.assertEqual({"warmane", "wowcircle"}, set(profiles))
        self.assertIn("Icecrown", profiles["warmane"]["knownRealmNames"])
        self.assertIn("WoW-Circle-x100", profiles["wowcircle"]["knownRealmNames"])
        self.assertIn("cutters move faster", profiles["wowcircle"]["databaseNotes"])
        self.assertIn("fire radiuses are larger", profiles["wowcircle"]["databaseNotes"])

    def test_overlay_requires_exact_source_hash_and_before_hash(self):
        baseline = load_baseline(ROOT / "patch-y" / "baseline.json")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "servers.json").write_text((ROOT / "patch-y" / "servers.json").read_text(encoding="utf-8"), encoding="utf-8")
            (root / "overlays" / "common" / "files").mkdir(parents=True)
            source = root / "overlays" / "common" / "files" / "marker.blp"
            source.write_bytes(b"marker")
            operation = {
                "action": "replace",
                "servers": ["warmane"],
                "member": "Spells\\Marker.blp",
                "source": "files/marker.blp",
                "sourceSha256": hashlib.sha256(b"marker").hexdigest(),
                "expectedBeforeSha256": "0" * 64,
                "reason": "Fixture",
            }
            (root / "overlays" / "common" / "manifest.json").write_text(
                json.dumps({"schemaVersion": 1, "overlay": "common", "operations": [operation]}), encoding="utf-8"
            )
            for edition in baseline["editions"]:
                target = root / "overlays" / "editions" / edition
                target.mkdir(parents=True)
                (target / "manifest.json").write_text(
                    json.dumps({"schemaVersion": 1, "overlay": edition, "operations": []}), encoding="utf-8"
                )

            operations = load_operations(root, baseline["editions"])

            self.assertTrue(all(len(rows) == 1 for rows in operations.values()))
            self.assertTrue(all(rows[0].servers == ("warmane",) for rows in operations.values()))
            operation["sourceSha256"] = "f" * 64
            (root / "overlays" / "common" / "manifest.json").write_text(
                json.dumps({"schemaVersion": 1, "overlay": "common", "operations": [operation]}), encoding="utf-8"
            )
            with self.assertRaisesRegex(OverlayError, "source hash mismatch"):
                load_operations(root, baseline["editions"])

    def test_rejects_opaque_dbc_replacement(self):
        baseline = load_baseline(ROOT / "patch-y" / "baseline.json")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "servers.json").write_text((ROOT / "patch-y" / "servers.json").read_text(encoding="utf-8"), encoding="utf-8")
            common = root / "overlays" / "common"
            common.mkdir(parents=True)
            source = common / "opaque.dbc"
            source.write_bytes(b"WDBC")
            operation = {
                "action": "replace",
                "servers": ["warmane"],
                "member": "DBFilesClient\\SpellVisual.dbc",
                "source": "opaque.dbc",
                "sourceSha256": hashlib.sha256(b"WDBC").hexdigest(),
                "expectedBeforeSha256": "0" * 64,
                "reason": "Exercise whole-table rejection.",
            }
            (common / "manifest.json").write_text(
                json.dumps({"schemaVersion": 1, "overlay": "common", "operations": [operation]}), encoding="utf-8"
            )
            for edition in baseline["editions"]:
                target = root / "overlays" / "editions" / edition
                target.mkdir(parents=True)
                (target / "manifest.json").write_text(
                    json.dumps({"schemaVersion": 1, "overlay": edition, "operations": []}), encoding="utf-8"
                )

            with self.assertRaisesRegex(OverlayError, "Opaque DBC"):
                load_operations(root, baseline["editions"])


class WdbcTests(unittest.TestCase):
    @staticmethod
    def fixture() -> bytes:
        records = struct.pack("<III", 7, 11, 1) + struct.pack("<III", 8, 22, 5)
        strings = b"\0old\0other\0"
        return b"WDBC" + struct.pack("<4I", 2, 3, 12, len(strings)) + records + strings

    def test_applies_uint32_and_string_edits_with_old_value_guards(self):
        edits = [
            {"recordId": 7, "fieldName": "Visual", "fieldIndex": 1, "valueType": "uint32", "oldValue": 11, "newValue": 99, "reason": "Fixture"},
            {"recordId": 7, "fieldName": "Name", "fieldIndex": 2, "valueType": "string", "oldValue": "old", "newValue": "new", "reason": "Fixture"},
        ]

        result = Wdbc.parse(apply_edits(self.fixture(), edits))

        self.assertEqual(99, struct.unpack_from("<I", result.records[0], 4)[0])
        self.assertEqual("new", result._string(struct.unpack_from("<I", result.records[0], 8)[0]))
        self.assertEqual(self.fixture()[32:44], result.encode()[32:44])

    def test_rejects_wrong_old_value(self):
        edit = {"recordId": 7, "fieldName": "Visual", "fieldIndex": 1, "valueType": "uint32", "oldValue": 12, "newValue": 99, "reason": "Fixture"}

        with self.assertRaisesRegex(OverlayError, "precondition"):
            apply_edits(self.fixture(), [edit])


class BinaryTransformTests(unittest.TestCase):
    def test_scales_only_vertex_xy(self):
        data = struct.pack("<3f", 2.0, -3.0, 9.0) + b"tail"

        result = scale_xy_vertices(data, offset=0, count=1, stride=12, factor=1.5)

        self.assertEqual((3.0, -4.5, 9.0), struct.unpack_from("<3f", result, 0))
        self.assertEqual(b"tail", result[12:])

    def test_rewrites_reviewed_bounds_only(self):
        data = b"head" + bytes(28) + b"tail"

        result = rewrite_bounds(data, offset=4, minimum=(-1.0, -2.0, -3.0), maximum=(1.0, 2.0, 3.0), radius=4.0)

        self.assertEqual((-1.0, -2.0, -3.0, 1.0, 2.0, 3.0, 4.0), struct.unpack_from("<7f", result, 4))
        self.assertEqual(b"head", result[:4])
        self.assertEqual(b"tail", result[32:])

    def test_replaces_fixed_width_texture_reference_only(self):
        data = b"headSpells\\Old.blp\0tail"

        result = replace_texture_reference(
            data, old="Spells\\Old.blp", new="Spells\\New.blp", expected_occurrences=1
        )

        self.assertEqual(b"headSpells\\New.blp\0tail", result)
        with self.assertRaisesRegex(OverlayError, "fixed-width"):
            replace_texture_reference(data, old="Old.blp", new="Longer.blp")

    def test_recolors_every_opaque_dxt1_mip_block(self):
        data = bytearray(156)
        data[:4] = b"BLP2"
        data[8:12] = bytes((2, 0, 0, 1))
        struct.pack_into("<I", data, 12, 4)
        struct.pack_into("<I", data, 16, 4)
        struct.pack_into("<I", data, 20, 148)
        struct.pack_into("<I", data, 84, 8)

        result = recolor_dxt1_endpoints(bytes(data), red=248, green=68, blue=40)

        expected = rgb888_to_rgb565(248, 68, 40)
        self.assertEqual((expected, expected), struct.unpack_from("<HH", result, 148))
        self.assertEqual(data[4:148], result[4:148])


class SourcePackageTests(unittest.TestCase):
    def test_source_bundle_includes_contributor_workspace_without_generated_files(self):
        specification = importlib.util.spec_from_file_location("package_universal_source", ROOT / "tools" / "package_universal_source.py")
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "source.zip"

            module.build(ROOT, output)

            import zipfile
            with zipfile.ZipFile(output) as archive:
                names = set(archive.namelist())
            self.assertIn("LauSetup-source/patch-y/baseline.json", names)
            self.assertIn("LauSetup-source/tools/patch_y.py", names)
            self.assertIn("LauSetup-source/docs/PATCH-Y-DEVELOPMENT.md", names)
            self.assertFalse(any("/.cache/" in name or "/.work/" in name or "__pycache__" in name for name in names))
            self.assertFalse(any(name.lower().endswith(".mpq") for name in names))


class OutputSafetyTests(unittest.TestCase):
    def test_build_refuses_to_replace_unmarked_output(self):
        class UnusedStorm:
            pass

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "important"
            output.mkdir()
            (output / "keep.txt").write_text("keep", encoding="utf-8")

            with self.assertRaisesRegex(OverlayError, "unmarked candidate output"):
                build_candidates(
                    ROOT / "patch-y",
                    ROOT / "patch-y" / "baseline.json",
                    ROOT / "patch-y" / ".cache" / "baseline",
                    output,
                    UnusedStorm(),
                    "test",
                    "warmane",
                )

            self.assertEqual("keep", (output / "keep.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

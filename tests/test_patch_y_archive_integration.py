"""Real StormLib integration coverage for Patch-Y overlay actions.

Run only after the pinned baseline has been fetched. The test uses temporary
archives and never writes a game client.
Author / Creator / Last Modified By: Neil Mitchell
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import struct
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "patch-y"
sys.path.insert(0, str(SOURCE / "lib"))

from patch_y_source.core import load_baseline
from patch_y_source.dbc import Wdbc
from patch_y_source.mpq import Storm
from patch_y_source.workflow import build_candidates, verify_candidates


@unittest.skipUnless(os.environ.get("PATCH_Y_RUN_ARCHIVE_INTEGRATION") == "1", "requires fetched baseline and StormLib")
class ArchiveOverlayIntegrationTests(unittest.TestCase):
    def test_add_replace_delete_and_dbc_actions_change_only_declared_members(self):
        baseline_path = SOURCE / "baseline.json"
        baseline = load_baseline(baseline_path)
        baseline_dir = SOURCE / ".cache" / "baseline"
        storm = Storm()
        editions = list(baseline["editions"])
        inventories = {
            edition: storm.inventory(baseline_dir / baseline["editions"][edition]["archiveName"], include_bytes=True)
            for edition in editions
        }
        common_model = next(
            key for key, row in inventories[editions[0]].items()
            if str(row["name"]).lower().endswith(".m2")
            and all(key in inventories[edition] and inventories[edition][key]["sha256"] == row["sha256"] for edition in editions)
        )
        first = editions[0]
        texture = next(key for key, row in inventories[first].items() if str(row["name"]).lower().endswith(".blp"))
        dbc = next(key for key, row in inventories[first].items() if str(row["name"]).lower().endswith("spellvisual.dbc"))
        deleted = next(
            key for key, row in inventories[first].items()
            if str(row["name"]).lower().endswith(".txt") and key not in {common_model, texture, dbc}
        )
        table = Wdbc.parse(inventories[first][dbc]["content"])
        record_id = struct.unpack_from("<I", table.records[0], 0)[0]
        old_value = struct.unpack_from("<I", table.records[0], 4)[0]

        with tempfile.TemporaryDirectory(prefix="patch-y-overlay-integration-") as directory:
            source_root = Path(directory) / "source"
            source_root.mkdir()
            shutil.copy2(SOURCE / "servers.json", source_root / "servers.json")
            common = source_root / "overlays" / "common"
            common_files = common / "files"
            common_files.mkdir(parents=True)
            added_source = common_files / "fixture.txt"
            added_source.write_text("Patch-Y source integration fixture\n", encoding="ascii")
            common_operations = [
                {
                    "action": "transform",
                    "servers": ["warmane"],
                    "member": inventories[first][common_model]["name"],
                    "expectedBeforeSha256": inventories[first][common_model]["sha256"],
                    "recipe": {
                        "kind": "rewrite_bounds",
                        "offset": len(inventories[first][common_model]["content"]) - 28,
                        "minimum": [-1.0, -1.0, -1.0],
                        "maximum": [1.0, 1.0, 1.0],
                        "radius": 2.0,
                    },
                    "reason": "Exercise a shared parameterized model transform.",
                },
                {
                    "action": "add",
                    "servers": ["warmane"],
                    "member": "Interface\\AddOns\\!PYAndre\\SourceWorkflowFixture.txt",
                    "source": "files/fixture.txt",
                    "sourceSha256": hashlib.sha256(added_source.read_bytes()).hexdigest(),
                    "reason": "Exercise a declared added member.",
                },
            ]
            (common / "manifest.json").write_text(
                json.dumps({"schemaVersion": 1, "overlay": "common", "operations": common_operations}), encoding="utf-8"
            )
            for edition in editions:
                overlay = source_root / "overlays" / "editions" / edition
                files = overlay / "files"
                files.mkdir(parents=True)
                operations = []
                if edition == first:
                    texture_data = bytearray(inventories[first][texture]["content"])
                    texture_data[-1] ^= 1
                    texture_source = files / "fixture.blp"
                    texture_source.write_bytes(texture_data)
                    operations.extend(
                        [
                            {
                                "action": "replace",
                                "servers": ["warmane"],
                                "member": inventories[first][texture]["name"],
                                "source": "files/fixture.blp",
                                "sourceSha256": hashlib.sha256(texture_data).hexdigest(),
                                "expectedBeforeSha256": inventories[first][texture]["sha256"],
                                "reason": "Exercise an edition-only texture replacement.",
                            },
                            {
                                "action": "dbc",
                                "servers": ["warmane"],
                                "member": inventories[first][dbc]["name"],
                                "expectedBeforeSha256": inventories[first][dbc]["sha256"],
                                "reason": "Exercise a structured DBC operation.",
                                "edits": [
                                    {
                                        "recordId": record_id,
                                        "fieldName": "Integration fixture field",
                                        "fieldIndex": 1,
                                        "valueType": "uint32",
                                        "oldValue": old_value,
                                        "newValue": old_value ^ 1,
                                        "reason": "Exercise a guarded record-level DBC edit.",
                                    }
                                ],
                            },
                            {
                                "action": "delete",
                                "servers": ["warmane"],
                                "member": inventories[first][deleted]["name"],
                                "expectedBeforeSha256": inventories[first][deleted]["sha256"],
                                "reason": "Exercise a declared deletion.",
                            },
                        ]
                    )
                (overlay / "manifest.json").write_text(
                    json.dumps({"schemaVersion": 1, "overlay": edition, "operations": operations}), encoding="utf-8"
                )
            output = Path(directory) / "candidate"

            report = build_candidates(source_root, baseline_path, baseline_dir, output, storm, "integration", "warmane")
            verified = verify_candidates(baseline_path, baseline_dir, output, source_root, storm, "warmane")

            self.assertTrue(all(row["status"] == "PASS" for row in report["archives"]))
            self.assertTrue(all(row["status"] == "PASS" for row in verified["results"]))
            first_report = next(row for row in report["archives"] if row["edition"] == first)
            self.assertEqual(5, len(first_report["declaredChanges"]))


if __name__ == "__main__":
    unittest.main()

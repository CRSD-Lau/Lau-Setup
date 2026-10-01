"""Manual Patch-Y package tests. Author: Neil Mitchell."""

import copy
import hashlib
import importlib.util
import json
import pathlib
import tempfile
import unittest
import zipfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("package_patch_y_manual", ROOT / "tools/package_patch_y_manual.py")
package = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package)


def sha(data):
    return hashlib.sha256(data).hexdigest()


class ManualPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="patch-y-manual-test-")
        self.root = pathlib.Path(self.temp.name)
        self.payload = self.root / "payload"
        self.payload.mkdir()
        self.output = self.root / "output"
        self.catalog_path = self.root / "catalog.json"
        self.data = {
            "Y-HD-NewSpells-On-Consecration-On": b"MPQ\x1aHD new spelling",
            "Y-HD-NewSpells-Off-Consecration-On": b"MPQ\x1aHD original spells",
            "Y-Non-HD-Consecration-On": b"MPQ\x1aNon HD",
            "SpellAssets": b"MPQ\x1aSpell assets and models",
            "SpellTables": b"MPQ\x1aSpell tables",
        }
        assets = {}
        for asset_id, data in self.data.items():
            chunks = [data[:9], data[9:]] if asset_id == "SpellAssets" else [data]
            parts = []
            for chunk in chunks:
                digest = sha(chunk)
                name = digest + ".bin"
                (self.payload / name).write_bytes(chunk)
                parts.append({"Sha256": digest, "Bytes": len(chunk), "FileName": name,
                              "Url": "https://github.com/CRSD-Lau/Lau-Setup/releases/download/payload-3.1.0/" + name})
            assets[asset_id] = {"Id": asset_id, "Bytes": len(data), "Sha256": sha(data), "Parts": parts}
        locales = sorted(package.KNOWN_LOCALES)
        self.catalog = {**package.META, "Version": "3.1.0", "PublicReady": True,
                        "Locales": sorted(set(locales) - set(package.FALLBACKS)),
                        "ClientLocales": locales,
                        "VisualAssetLocales": {locale: package.FALLBACKS.get(locale, locale) for locale in locales},
                        "Assets": assets}
        self.save_catalog()

    def tearDown(self):
        self.temp.cleanup()

    def save_catalog(self):
        self.catalog_path.write_text(json.dumps(self.catalog), encoding="utf-8")

    def build(self):
        return package.build(self.catalog_path, self.output, payload_dir=self.payload, version="3.1.0")

    def test_packages_mapping_metadata_and_deterministic_rebuild(self):
        rows = self.build()
        self.assertEqual(len(rows), 3)
        self.assertTrue(package.verify_output(self.catalog_path, self.output, "3.1.0"))
        before = [sha((self.output / row[1]).read_bytes()) for row in rows]
        for edition, ids in package.EDITIONS:
            path = self.output / package.package_filename("3.1.0", edition)
            with zipfile.ZipFile(path) as archive:
                expected = ["patch-y.mpq"] + (["patch-s.mpq", "patch-LOCALE-S.MPQ"] if edition == "HD-New-Spells" else [])
                self.assertEqual(archive.namelist(), expected + ["README.txt", "package-manifest.json"])
                self.assertEqual(archive.comment, package.COMMENT)
                for info in archive.infolist():
                    self.assertEqual(info.comment, package.COMMENT)
                manifest = json.loads(archive.read("package-manifest.json"))
                self.assertEqual({key: manifest[key] for key in package.META}, package.META)
                self.assertEqual([f["AssetId"] for f in manifest["Files"]], list(ids))
                self.assertEqual(archive.read("patch-y.mpq"), self.data[ids[0]])
                y = manifest["Files"][0]
                self.assertEqual(len(y["Destinations"]), 24)
                self.assertIn({"Locale": "itIT", "Path": "Data/itIT/patch-itIT-Y.MPQ"}, y["Destinations"])
                self.assertEqual(manifest["VisualAssetLocales"]["itIT"], "enUS")
                readme = archive.read("README.txt").decode()
                self.assertIn("OUTSIDE Data", readme)
                self.assertIn("/pyversion", readme)
                self.assertIn("WTF/Config.wtf", readme)
                self.assertIn("To undo", readme)
                self.assertIn("Andre", readme)
                self.assertIn("Suppository", readme)
                if edition != "HD-New-Spells":
                    self.assertIn("move any existing Data/patch-s.mpq", readme)
        self.assertEqual(before, [sha((self.output / row[1]).read_bytes()) for row in self.build()])
        index = json.loads((self.output / "manual-downloads.json").read_text())
        self.assertTrue(all("/payload-3.1.0/" in item["Url"] for item in index["Packages"]))
        self.assertIn("Neil Mitchell", (self.output / "SHA256SUMS-Patch-Y.txt").read_text())

    def test_corrupt_part_and_missing_companion_fail_closed(self):
        spell_part = self.catalog["Assets"]["SpellAssets"]["Parts"][1]["FileName"]
        (self.payload / spell_part).write_bytes(b"wrong")
        with self.assertRaisesRegex(ValueError, "corrupt local part"):
            self.build()
        self.assertFalse((self.output / "manual-downloads.json").exists())
        (self.payload / spell_part).unlink()
        with self.assertRaisesRegex(FileNotFoundError, "missing local part"):
            self.build()

    def test_wrong_version_unsafe_url_and_missing_asset(self):
        with self.assertRaisesRegex(ValueError, "version"):
            package.build(self.catalog_path, self.output, payload_dir=self.payload, version="3.0.9")
        copy_catalog = copy.deepcopy(self.catalog)
        del self.catalog["Assets"]["SpellTables"]
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, "SpellTables"):
            self.build()
        self.catalog = copy_catalog
        self.catalog["Assets"]["SpellTables"]["Parts"][0]["Url"] = "https://example.com/evil.bin"
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, "untrusted"):
            self.build()

    def test_public_ready_catalog_metadata_and_output_guard(self):
        original = copy.deepcopy(self.catalog)
        self.catalog["PublicReady"] = False
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, "PublicReady"):
            self.build()
        self.catalog = copy.deepcopy(original)
        self.catalog["Creator"] = "Someone Else"
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, "author metadata"):
            self.build()
        self.catalog = original
        self.save_catalog()
        self.output.mkdir()
        (self.output / "old-release.zip").write_bytes(b"old")
        with self.assertRaisesRegex(ValueError, "unrelated files"):
            self.build()

    def test_archive_extras_are_rejected(self):
        self.build()
        path = self.output / "Patch-Y-3.1.0-Non-HD.zip"
        with zipfile.ZipFile(path, "a") as archive:
            archive.writestr("extra.exe", b"MZ")
        with self.assertRaisesRegex(ValueError, "extra entries"):
            package.verify_output(self.catalog_path, self.output)
        with self.assertRaisesRegex(ValueError, "extra entries"):
            self.build()

    def test_archive_metadata_and_index_tampering_are_rejected(self):
        self.build()
        path = self.output / "Patch-Y-3.1.0-Non-HD.zip"
        with zipfile.ZipFile(path, "a") as archive:
            archive.comment = b"wrong author"
        with self.assertRaisesRegex(ValueError, "author metadata"):
            package.verify_output(self.catalog_path, self.output)
        # A fresh fixture isolates the index check from the damaged archive.
        path.unlink()
        for name in ("Patch-Y-3.1.0-HD-New-Spells.zip", "Patch-Y-3.1.0-HD-Original-Spells.zip",
                     "manual-downloads.json", "SHA256SUMS-Patch-Y.txt"):
            (self.output / name).unlink()
        self.build()
        index = self.output / "manual-downloads.json"
        value = json.loads(index.read_text())
        value["Packages"][0]["Sha256"] = "0" * 64
        index.write_text(json.dumps(value), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "manual-downloads"):
            package.verify_output(self.catalog_path, self.output)

    def test_checksum_file_tampering_is_rejected(self):
        self.build()
        sums = self.output / "SHA256SUMS-Patch-Y.txt"
        sums.write_text(sums.read_text().replace("Neil Mitchell", "Other Author", 1))
        with self.assertRaisesRegex(ValueError, "SHA256SUMS"):
            package.verify_output(self.catalog_path, self.output)

    def test_catalog_path_traversal_and_tampered_manifest_rejected(self):
        self.catalog["Assets"]["SpellTables"]["Parts"][0]["FileName"] = "../evil.bin"
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, "unsafe part filename"):
            self.build()


if __name__ == "__main__":
    unittest.main()

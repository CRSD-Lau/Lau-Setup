"""Released-catalog resolver tests. Author: Neil Mitchell."""

import base64
import hashlib
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
SPEC = importlib.util.spec_from_file_location("resolve_manual_catalog", ROOT / "tools/resolve_manual_catalog.py")
resolver = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(resolver)


def catalog(public_ready):
    locales = sorted(resolver.load_catalog.__globals__["KNOWN_LOCALES"])
    assets = {}
    for asset_id in resolver.ASSET_IDS:
        data = ("MPQ!" + asset_id).encode()
        digest = hashlib.sha256(data).hexdigest()
        name = digest + ".bin"
        assets[asset_id] = {"Id": asset_id, "Bytes": len(data), "Sha256": digest,
                            "Parts": [{"Bytes": len(data), "Sha256": digest, "FileName": name,
                                       "Url": ("https://github.com/CRSD-Lau/Lau-Setup/releases/download/"
                                               "payload-3.1.0/" + name) if public_ready else ""}]}
    return {"Author": "Neil Mitchell", "Creator": "Neil Mitchell", "LastModifiedBy": "Neil Mitchell",
            "Version": "3.1.0", "InstallerVersion": "1.5.0", "PublicReady": public_ready,
            "Locales": sorted(set(locales) - {"enGB", "itIT", "ptBR"}), "ClientLocales": locales,
            "VisualAssetLocales": {locale: "enUS" if locale in {"enGB", "itIT", "ptBR"} else locale
                                   for locale in locales}, "Assets": assets}


class ResolverTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="manual-catalog-resolver-")
        self.root = pathlib.Path(self.temp.name)
        self.output = self.root / "catalog.json"
        self.payload = catalog(False)
        self.installer = catalog(True)
        self.calls = []

    def tearDown(self):
        self.temp.cleanup()

    def fake_run(self, cmd, **kwargs):
        self.calls.append(cmd)
        self.assertEqual(cmd[0], "gh")
        self.assertEqual(kwargs["check"], True)
        if cmd[1:3] == ["release", "view"]:
            tag = cmd[3]
            if tag not in ("payload-3.1.0", "v1.5.0"):
                raise subprocess.CalledProcessError(1, cmd)
            return SimpleNamespace(stdout=json.dumps({"tagName": tag, "isDraft": False}))
        if cmd[1] == "api":
            tag = cmd[2].split("ref=")[-1]
            value = self.payload if tag == "payload-3.1.0" else self.installer if tag == "v1.5.0" else None
            if value is None:
                raise subprocess.CalledProcessError(1, cmd)
            data = json.dumps(value, sort_keys=True).encode()
            return SimpleNamespace(stdout=json.dumps({"encoding": "base64", "content": base64.b64encode(data).decode()}))
        self.fail("unexpected gh command: " + repr(cmd))

    def run_resolver(self, tag, **kwargs):
        with mock.patch.object(resolver.subprocess, "run", side_effect=self.fake_run):
            return resolver.resolve("CRSD-Lau/Lau-Setup", tag, self.output, **kwargs)

    def test_payload_falls_back_only_to_matching_public_installer_catalog(self):
        env = self.root / "github-env"
        result = self.run_resolver("payload-3.1.0", github_env=env)
        self.assertEqual(result, {"game_tag": "payload-3.1.0", "version": "3.1.0", "catalog_ref": "v1.5.0"})
        self.assertEqual(json.loads(self.output.read_text()), self.installer)
        self.assertEqual(env.read_text(), "RELEASE_GAME_TAG=payload-3.1.0\nRELEASE_GAME_VERSION=3.1.0\n")
        self.assertEqual(len(self.calls), 4)
        self.assertEqual(self.run_resolver("payload-3.1.0"), result)

    def test_installer_event_checks_published_game_tag_and_payload_parity(self):
        result = self.run_resolver("v1.5.0")
        self.assertEqual(result["catalog_ref"], "v1.5.0")
        self.assertIn(["gh", "release", "view", "payload-3.1.0", "--repo", "CRSD-Lau/Lau-Setup",
                       "--json", "tagName,isDraft"], self.calls)

    def test_public_ready_payload_uses_exact_payload_tag(self):
        self.payload = catalog(True)
        result = self.run_resolver("payload-3.1.0")
        self.assertEqual(result["catalog_ref"], "payload-3.1.0")
        self.assertEqual(len(self.calls), 2)

    def test_asset_and_locale_drift_fail_without_output(self):
        for field in ("Sha256", "Bytes"):
            with self.subTest(field=field):
                self.payload = catalog(False)
                asset = self.payload["Assets"][resolver.ASSET_IDS[0]]
                asset[field] = "f" * 64 if field == "Sha256" else asset[field] + 1
                with self.assertRaisesRegex(ValueError, "catalogs differ"):
                    self.run_resolver("payload-3.1.0")
                self.assertFalse(self.output.exists())
        self.payload = catalog(False)
        self.payload["Assets"][resolver.ASSET_IDS[0]]["Parts"][0]["FileName"] = "different.bin"
        with self.assertRaisesRegex(ValueError, "catalogs differ"):
            self.run_resolver("payload-3.1.0")
        self.payload = catalog(False)
        self.payload["VisualAssetLocales"]["itIT"] = "frFR"
        with self.assertRaisesRegex(ValueError, "VisualAssetLocales"):
            self.run_resolver("payload-3.1.0")

    def test_unready_candidate_wrong_version_and_existing_output_rejected(self):
        self.installer["PublicReady"] = False
        with self.assertRaisesRegex(ValueError, "PublicReady"):
            self.run_resolver("payload-3.1.0")
        self.installer = catalog(True)
        self.installer["Version"] = "3.2.0"
        with self.assertRaisesRegex(ValueError, "Version"):
            self.run_resolver("payload-3.1.0")
        self.installer = catalog(True)
        self.output.write_text("old", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "existing output differs"):
            self.run_resolver("payload-3.1.0")

    def test_tag_and_release_guards(self):
        with self.assertRaisesRegex(ValueError, "release-tag"):
            resolver.resolve("CRSD-Lau/Lau-Setup", "payload-3.1.0;evil", self.output)
        self.payload["Version"] = "3.2.0"
        with self.assertRaisesRegex(ValueError, "payload tag"):
            self.run_resolver("payload-3.1.0")
        self.payload = catalog(False)
        self.installer["InstallerVersion"] = "1.4.0"
        with self.assertRaisesRegex(ValueError, "InstallerVersion"):
            self.run_resolver("payload-3.1.0")


if __name__ == "__main__":
    unittest.main()

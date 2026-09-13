"""Tests for the bounded Lau Setup installer translation catalog.

Author, Creator, Last Modified By: Neil Mitchell
"""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("translate_installer", ROOT / "tools" / "translate_installer.py")
translation = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(translation)


class TranslationCatalogTests(unittest.TestCase):
    def test_extracts_ui_helpers_exceptions_progress_and_linux_errors(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "app").mkdir(); (root / "wine").mkdir()
            (root / "app" / "Core.cs").write_text(
                'throw new IOException("Missing file: "+path+". Retry."); report("Installing "+name+"…");', encoding="utf-8")
            (root / "app" / "Main.cs").write_text(
                'Label("Choose folder",10,x,y); SetText(status,"Downloaded {0}",size); Ui.T("Ready");', encoding="utf-8")
            for name in ("Downloader.cs", "MpqScan.cs"): (root / "app" / name).write_text("", encoding="utf-8")
            (root / "wine" / "lau_wine.py").write_text("raise ValueError('Close WoW: '+path)\n", encoding="utf-8")
            keys = translation.extract_keys(root)
            self.assertIn("Missing file: {0}. Retry.", keys)
            self.assertIn("Installing {0}…", keys)
            self.assertIn("Downloaded {0}", keys)
            self.assertIn("Close WoW: {0}", keys)

    def test_mask_round_trip_preserves_placeholders_files_versions_and_url(self):
        source = "Lau Setup keeps WoW.exe at 3.3.5a; see {0} and https://example.invalid/a."
        masked, saved = translation.mask(source)
        self.assertEqual(source, translation.unmask(masked, masked, saved))
        self.assertNotIn("WoW.exe", masked)

    def test_damaged_placeholder_is_rejected(self):
        keys = ["Downloaded {0} / {1}"]
        data = dict(translation.META, languages={})
        for locale in translation.LOCALES:
            data["languages"][locale] = {keys[0]: keys[0]}
        data["languages"]["fr-FR"][keys[0]] = "Téléchargé {0}"
        with self.assertRaisesRegex(ValueError, "changed placeholders"):
            translation.validate(data, keys)

    def test_damaged_protected_name_is_rejected(self):
        keys = ["Run Lau Setup with WoW.exe {0}"]
        data = dict(translation.META, languages={})
        for locale in translation.LOCALES:
            data["languages"][locale] = {keys[0]: keys[0]}
        data["languages"]["de-DE"][keys[0]] = "Lau-Setup mit WoW.exe {0} ausführen"
        with self.assertRaisesRegex(ValueError, "changed protected token"):
            translation.validate(data, keys)

    def test_missing_key_and_silent_english_are_rejected(self):
        keys = ["Choose the existing game folder"]
        data = dict(translation.META, languages={})
        for locale in translation.LOCALES:
            data["languages"][locale] = {keys[0]: keys[0] if locale == "en-US" else "Choisir le dossier de jeu existant"}
        data["languages"]["de-DE"] = {}
        with self.assertRaisesRegex(ValueError, "catalog keys differ"):
            translation.validate(data, keys)
        data["languages"]["de-DE"] = {keys[0]: keys[0]}
        with self.assertRaisesRegex(ValueError, "silently falls back"):
            translation.validate(data, keys)

    def test_checked_in_catalog_is_complete(self):
        self.assertTrue((ROOT / "app" / "translations.json").is_file(), "checked-in translation catalog is missing")
        translation.validate(root=ROOT)


if __name__ == "__main__": unittest.main()

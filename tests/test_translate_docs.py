"""Translation integrity tests. Author/creator/modifier: Neil Mitchell."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import translate_docs as t


class TranslationTests(unittest.TestCase):
    def test_catalog_coverage_and_brazilian_portuguese(self):
        values = t.locales()
        self.assertEqual(len(values), 10)
        self.assertEqual(values["ptBR"]["tag"], "pt-BR")
        self.assertIn("Brazilian", values["ptBR"]["instruction"])
        self.assertNotEqual(values["esES"], values["esMX"])
        self.assertNotEqual(values["zhCN"], values["zhTW"])

    def test_catalog_drift_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            t.write(root / "tools/translation-locales.json", t.read(t.ROOT / "tools/translation-locales.json"))
            t.write(root / "build/catalog.json", json.dumps({"Locales": list(t.locales()) + ["jaJP"]}))
            with self.assertRaisesRegex(ValueError, "cover exactly"):
                t.locales(root)

    def test_command_links_numbers_and_metadata_survive(self):
        original = (t.META + '\nInstall **3.0.8** using `/pyversion` and [Download](https://example.com/a.zip).\n'
                    '```sh\nWINEPREFIX="/absolute/path" sh LauSetup.sh\n```\n'
                    '<img src="docs/a.png" />\nAuthor / Creator / Last Modified By: Neil Mitchell\n')
        masked, saved = t.mask(original)
        translated = masked.replace("Install", "Instale").replace("using", "usando").replace("Download", "Baixar")
        result = t.unmask(translated, masked, saved)
        self.assertIn('WINEPREFIX="/absolute/path" sh LauSetup.sh', result)
        self.assertIn("https://example.com/a.zip", result)
        self.assertIn(t.META, result)
        self.assertIn("**3.0.8**", result)

    def test_rejects_lost_and_duplicate_placeholders(self):
        masked, saved = t.mask("Install `WoW.exe` version 3.0.8.")
        token = t.TOKEN.search(masked)[0]
        for bad in (masked.replace(token, ""), masked + token):
            with self.assertRaisesRegex(ValueError, "protected"):
                t.unmask(bad, masked, saved)

    def test_rejects_invented_links_html_and_code(self):
        masked, saved = t.mask("Read [guide](README.md).")
        for suffix in (" https://evil.example", " <script>alert(1)</script>", " `rm -rf /`", " [extra](evil.md)"):
            with self.assertRaisesRegex(ValueError, "markup"):
                t.unmask(masked + suffix, masked, saved)

    def test_rejects_english_fallback_and_truncation(self):
        masked, saved = t.mask("Please install the latest version of the upgrade and read the documentation before changing any files on your computer today or tomorrow.")
        with self.assertRaisesRegex(ValueError, "unchanged"):
            t.unmask(masked, masked, saved)
        with self.assertRaisesRegex(ValueError, "truncated"):
            t.unmask("Fim.", masked, saved)

    def test_plain_text_wine_command_is_protected(self):
        original = 'Run:\n\n   WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh\n\nNext step.'
        masked, saved = t.mask(original)
        self.assertNotIn("WINEPREFIX", masked)
        self.assertIn('WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh', t.unmask(masked, masked, saved))

    def test_links_point_to_locale_documents_and_original_assets(self):
        original = '[Home](../README.md#download) [Wine](../wine/README.txt) ![Image](assets/a.png) [Code](../app/Core.cs)'
        result = t.rewrite_links(original, "docs/TECHNICAL.md", "pt-BR", ["README.md", "wine/README.txt", "docs/TECHNICAL.md"])
        self.assertIn("(../README.md#download)", result)
        self.assertIn("(../wine/README.md)", result)
        self.assertIn("(../../../assets/a.png)", result)
        self.assertIn("(../../../../app/Core.cs)", result)

    def test_stable_anchors_and_code_fences(self):
        result = t.stable_headings("## Download\n\n## Download\n\n```sh\n# not a heading\n```\n")
        self.assertIn('id="download"', result)
        self.assertIn('id="download-1"', result)
        self.assertNotIn('id="not-a-heading"', result)

    def test_chunks_preserve_complete_input(self):
        original = "A paragraph.\n\n" * 200
        self.assertEqual("".join(t.chunks(original, 80)), original)

    def test_local_model_only(self):
        with self.assertRaisesRegex(ValueError, "pinned local"):
            t.request_translation("hello", t.locales()["ptBR"], "paid-cloud-model")

    def test_generation_cache_and_failure_preserves_previous_page(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            t.write(root / "README.md", "# Install\n\nInstall `WoW.exe` version 3.0.8.\n")
            locale = t.locales()["ptBR"]
            calls = []

            def translator(text, language, model):
                calls.append(text)
                return text.replace("Install", "Instalar").replace("Automatic translation", "Tradução automática")

            self.assertTrue(t.translate_one("README.md", locale, ["README.md"], t.MODEL, root, translator))
            output = root / t.destination("README.md", "pt-BR")
            before = t.read(output)
            self.assertIn("Instalar", before)
            self.assertIn(t.META, before)
            self.assertFalse(t.translate_one("README.md", locale, ["README.md"], t.MODEL, root, translator))
            self.assertEqual(len(calls), 1)
            t.write(root / "README.md", "# Install\n\nInstall `Changed.exe` version 3.0.9.\n")
            with self.assertRaises(ValueError):
                t.translate_one("README.md", locale, ["README.md"], t.MODEL, root, lambda *args: "broken")
            self.assertEqual(t.read(output), before)

    def test_discovery_excludes_generated_and_agent_instructions(self):
        tracked = b"README.md\0README.txt\0AGENTS.md\0docs/TECHNICAL.md\0docs/i18n/fr/README.md\0wine/README.txt\0app/README.md\0"
        with patch.object(subprocess, "check_output", return_value=tracked):
            self.assertEqual(t.sources(), ["README.md", "README.txt", "docs/TECHNICAL.md", "wine/README.txt"])

    def test_navigation_has_no_missing_links_and_does_not_dirty_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            t.write(root / "README.md", "# Install\n")
            t.write(root / "tools/translation-locales.json", t.read(t.ROOT / "tools/translation-locales.json"))
            t.write(root / "build/catalog.json", json.dumps({"Locales": list(t.locales())[:-1]}))
            t.write(root / "docs/i18n/pt-BR/README.md", t.META + "\n# Instalar\n")
            with patch.object(t, "sources", return_value=["README.md"]):
                t.navigation(root)
                first = t.read(root / "README.md")
                self.assertIn("[Português (Brasil)](docs/i18n/pt-BR/README.md)", first)
                self.assertNotIn("[Français]", first)
                self.assertEqual(t.clean_source(first), "# Install\n")
                t.navigation(root)
                self.assertEqual(first, t.read(root / "README.md"))


if __name__ == "__main__":
    unittest.main()

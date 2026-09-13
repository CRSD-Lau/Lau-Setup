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
        self.assertEqual(values["ptBR"]["google"], "pt")
        self.assertEqual(values["esES"]["google"], values["esMX"]["google"])
        self.assertNotEqual(values["esES"], values["esMX"])
        self.assertNotEqual(values["zhCN"], values["zhTW"])

    def test_catalog_drift_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            t.write(root / "tools/translation-locales.json", t.read(t.ROOT / "tools/translation-locales.json"))
            t.write(root / "build/catalog.json", json.dumps({"Locales": list(t.locales()) + ["jaJP"]}))
            with self.assertRaisesRegex(ValueError, "cover exactly"):
                t.locales(root)

    def test_reviewed_platform_scope_cannot_be_inverted(self):
        source = 'Lutris, Proton and macOS integrations are outside this release'
        locale = t.locales()['zhTW']
        masked, saved = t.mask(source, locale)
        self.assertTrue(t.TOKEN.fullmatch(masked))
        self.assertEqual(t.unmask(masked, masked, saved), '此版本不包含 Lutris、Proton 和 macOS 整合')
        self.assertNotIn('glossary', t.scoped_locale('An unrelated document.', locale))
        self.assertIn('glossary', t.scoped_locale(source, locale))

    def test_glossary_invalidates_only_affected_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            locale = t.locales()['zhTW']
            previous = {k:v for k,v in locale.items() if k != 'glossary'}
            t.write(root / 'README.md', 'An unrelated document.')
            self.assertEqual(t.fingerprint('README.md',locale,['README.md'],t.PROVIDER,root),
                             t.fingerprint('README.md',previous,['README.md'],t.PROVIDER,root))
            t.write(root / 'README.md', next(iter(locale['glossary'])))
            self.assertNotEqual(t.fingerprint('README.md',locale,['README.md'],t.PROVIDER,root),
                                t.fingerprint('README.md',previous,['README.md'],t.PROVIDER,root))

    def test_unsigned_claim_is_locked_for_every_locale(self):
        for locale in t.locales().values():
            for source, key in [('The executable is unsigned', 'executable'),
                                ('The executable remains unsigned', 'executable'),
                                ('This installer is unsigned', 'installer'),
                                ('Windows packages are unsigned', 'windows')]:
                masked, saved = t.mask(source, locale)
                self.assertTrue(t.TOKEN.fullmatch(masked))
                self.assertEqual(t.unmask(masked, masked, saved), locale['unsigned'][key])
        # Numeric signedness is a different concept and must not become a signature claim.
        masked, saved = t.mask('raw unsigned 32-bit words', t.locales()['ptBR'])
        self.assertIn('unsigned', masked)

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

    def test_text_guide_literals_render_as_code(self):
        original = 'Run:\n\n   WINEPREFIX="/existing/prefix" sh LauSetup.sh\n\nKeep .mpq.disabled.<12-character hash>.\n'
        result = t.source_markdown('wine/README.txt', original)
        self.assertIn('```sh\nWINEPREFIX="/existing/prefix" sh LauSetup.sh\n```', result)
        self.assertIn('`.mpq.disabled.<12-character hash>`', result)
        self.assertEqual(t.source_markdown('README.md', original), original)

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

    def test_short_cjk_labels_are_not_treated_as_truncation(self):
        self.assertEqual(t.unmask('要求', 'Requirements', []), '要求')

    def test_prose_fallback_uses_plain_translation_mode(self):
        original = 'Raw six-edition `WoW.exe`'
        masked, saved = t.mask(original)
        modes = []
        def translator(text, locale, model, plain=False):
            modes.append(plain)
            return 'Seis ediciones originales' if plain else '# Explanations instead of translation'
        result = t.translate_context(masked, t.locales()['esES'], t.PROVIDER, translator, {}, saved)
        self.assertEqual(t.unmask(result, masked, saved), 'Seis ediciones originales `WoW.exe`')
        self.assertEqual(modes, [False, True])

    def test_free_google_provider_only(self):
        with self.assertRaisesRegex(ValueError, "free Google"):
            t.request_translation("hello", t.locales()["ptBR"], "paid-cloud-model")

    def test_google_result_parser_and_target(self):
        parsed = t.GoogleResult()
        parsed.feed('<input name="tl" value="pt"><div class="result-container">Olá &amp; <b>mundo</b><br>Fim</div><p>ignored</p>')
        self.assertEqual(parsed.target, 'pt')
        self.assertEqual(''.join(parsed.parts), 'Olá & mundo\nFim')

    def test_google_rejects_language_fallback(self):
        from io import BytesIO
        with patch.object(t.time, 'sleep'), patch.object(t.urllib.request, 'urlopen',
                return_value=BytesIO(b'<input name="tl" value="en"><div class="result-container">English</div>')):
            with self.assertRaisesRegex(ValueError, 'target rejected'):
                t.request_translation('Hello', t.locales()['ptBR'], t.PROVIDER)

    def test_google_retries_temporary_empty_pages(self):
        from io import BytesIO
        responses = [BytesIO(b'<html>Temporarily unavailable</html>'),
                     BytesIO('<input name="tl" value="pt"><div class="result-container">Site e galeria</div>'.encode())]
        with patch.object(t.time, 'sleep'), patch.object(t.urllib.request, 'urlopen', side_effect=responses) as call:
            self.assertEqual(t.request_translation('Website &amp; gallery', t.locales()['ptBR'], t.PROVIDER), 'Site e galeria')
            self.assertEqual(call.call_count, 2)
            self.assertIn('q=Website+%26+gallery', call.call_args.args[0])

    def test_google_rate_limit_stops_without_retry(self):
        error = t.urllib.error.HTTPError('https://translate.google.com/m', 429, 'limited', {}, None)
        with patch.object(t.time, 'sleep'), patch.object(t.urllib.request, 'urlopen', side_effect=error) as call:
            with self.assertRaisesRegex(ValueError, 'rate-limited'):
                t.request_translation('Hello', t.locales()['ptBR'], t.PROVIDER)
            self.assertEqual(call.call_count, 1)

    def test_html_elements_keep_their_own_text(self):
        masked, saved = t.mask('<strong>Your Wrath.</strong><br />The Windows installer.')
        calls = []
        def translator(text, *_):
            calls.append(text)
            return text.replace('Your', 'Seu').replace('The', 'O').replace('installer', 'instalador')
        result = t.translate_context(masked, t.locales()['ptBR'], t.PROVIDER, translator, {}, saved)
        self.assertEqual(t.unmask(result, masked, saved), '<strong>Seu Wrath.</strong><br />O Windows instalador.')
        self.assertFalse(any('Your' in call and 'installer' in call for call in calls))

    def test_russian_omits_standalone_articles_in_prose_fallback(self):
        original = 'The [technical reference](docs/TECHNICAL.md) describes a `WoW.exe` installation.'
        masked, saved = t.mask(original)
        calls = []
        def translator(text, *_):
            calls.append(text)
            return text.replace('technical reference', 'техническое руководство').replace('describes a', 'описывает').replace('installation', 'установку')
        result = t.translate_prose(masked, t.locales()['ruRU'], t.PROVIDER, translator, {})
        restored = t.unmask(result, masked, saved)
        self.assertNotIn('The', calls)
        self.assertNotIn('The', restored)
        self.assertIn('[техническое руководство](docs/TECHNICAL.md)', restored)
        # Unexpected empty translations remain an error.
        with self.assertRaises(ValueError):
            t.translate_prose('installation', t.locales()['ruRU'], t.PROVIDER, lambda *_: '', {})

    def test_long_prose_respects_google_input_limit(self):
        text = 'A lengthy sentence about software. ' * 100
        calls = []
        def translator(value, *_):
            calls.append(len(value))
            return value.replace('lengthy', 'larga')
        result = t.translate_context(text, t.locales()['esES'], t.PROVIDER, translator, {}, [])
        self.assertLessEqual(max(calls), 2000)
        self.assertEqual(result, text.replace('lengthy', 'larga'))

    def test_generation_cache_and_failure_preserves_previous_page(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            t.write(root / "README.md", "# Install\n\nInstall `WoW.exe` version 3.0.8.\n")
            locale = t.locales()["ptBR"]
            calls = []

            def translator(text, language, model, plain=False):
                calls.append(text)
                return text.replace("Install", "Instalar").replace("Automatic translation", "Tradução automática")

            self.assertTrue(t.translate_one("README.md", locale, ["README.md"], t.PROVIDER, root, translator))
            output = root / t.destination("README.md", "pt-BR")
            before = t.read(output)
            self.assertIn("Instalar", before)
            self.assertIn(t.META, before)
            self.assertFalse(t.translate_one("README.md", locale, ["README.md"], t.PROVIDER, root, translator))
            count = len(calls)
            self.assertFalse(t.translate_one("README.md", locale, ["README.md"], t.PROVIDER, root, translator))
            self.assertEqual(len(calls), count)
            t.write(root / "README.md", "# Download\n\nDownload `Changed.exe` version 3.0.9.\n")
            with self.assertRaises(ValueError):
                t.translate_one("README.md", locale, ["README.md"], t.PROVIDER, root, lambda *args: "<script>broken</script>")
            self.assertEqual(t.read(output), before)

    def test_model_never_receives_protected_spans_or_markdown(self):
        original = '# Install [guide](https://example.com) with `WoW.exe` version 3.0.8.\n'
        masked, saved = t.mask(original)
        calls = []
        def translator(prose, *_):
            calls.append(prose)
            return prose.replace('Install', 'Instalar').replace('guide', 'guia').replace('with', 'com').replace('version', 'versão')
        translated = t.translate_prose(masked, t.locales()['ptBR'], t.PROVIDER, translator, {})
        for prose in calls:
            self.assertNotRegex(prose, r'ZXQKEEP|https://|WoW.exe|3.0.8|[\[\]#`]')
        result = t.unmask(translated, masked, saved)
        self.assertEqual(result, '# Instalar [guia](https://example.com) com `WoW.exe` versão 3.0.8.\n')

    def test_discovery_excludes_generated_and_agent_instructions(self):
        tracked = b"README.md\0START-HERE.txt\0AGENTS.md\0docs/TECHNICAL.md\0docs/i18n/fr/README.md\0wine/README.txt\0app/README.md\0"
        with patch.object(subprocess, "check_output", return_value=tracked):
            self.assertEqual(t.sources(), ["README.md", "START-HERE.txt", "docs/TECHNICAL.md", "wine/README.txt"])

    def test_colliding_markdown_and_text_names_fail(self):
        with patch.object(subprocess, "check_output", return_value=b"README.md\0README.txt\0"):
            with self.assertRaisesRegex(ValueError, "collide"):
                t.sources()

    def test_new_source_invalidates_links_in_cached_documents(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            t.write(root / "README.md", "# Install\n")
            locale = t.locales()["ptBR"]
            self.assertNotEqual(t.fingerprint("README.md", locale, ["README.md"], t.PROVIDER, root),
                                t.fingerprint("README.md", locale, ["README.md", "NEW.md"], t.PROVIDER, root))

    def test_publication_rejects_missing_translations(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            t.write(root / "tools/translation-locales.json", t.read(t.ROOT / "tools/translation-locales.json"))
            t.write(root / "build/catalog.json", json.dumps({"Locales": list(t.locales())[:-1]}))
            with patch.object(t, "sources", return_value=["README.md"]), self.assertRaises(FileNotFoundError):
                t.verify_complete(root)

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

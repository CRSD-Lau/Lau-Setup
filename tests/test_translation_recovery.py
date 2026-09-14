"""Recovery behavior tests. Author/creator/modifier: Neil Mitchell."""

from email.utils import formatdate
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import recover_doc_translations as r
import translate_docs as t


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.cache = self.root / "cache"
        self.env = patch.dict(os.environ, {"TRANSLATION_CACHE_DIR": str(self.cache),
                                          "GITHUB_OUTPUT": str(self.root / "output"),
                                          "GITHUB_STEP_SUMMARY": str(self.root / "summary")})
        self.env.start()
        self.addCleanup(self.env.stop)
        t.write(self.root / "README.md", "# Install\n\nInstall the application.\n")
        self.locale = t.locales()["ptBR"]
        for target, value in (("sources", ["README.md"]), ("locales", {"enUS": {"tag": "en"}, "ptBR": self.locale})):
            mock = patch.object(t, target, return_value=value)
            mock.start()
            self.addCleanup(mock.stop)

    def test_retry_header_seconds_date_invalid(self):
        self.assertEqual(t.retry_after_seconds(" 120 "), 120)
        self.assertEqual(t.retry_after_seconds(formatdate(1500, usegmt=True), now=1000), 500)
        self.assertEqual(t.retry_after_seconds(formatdate(500, usegmt=True), now=1000), 0)
        self.assertIsNone(t.retry_after_seconds("unknown"))
        self.assertIsNone(t.retry_after_seconds(None))

    def test_429_preserves_retry_header_and_does_not_retry(self):
        error = t.urllib.error.HTTPError("https://translate.google.com/m", 429, "limited", {"Retry-After": "7200"}, None)
        with patch.object(t.time, "sleep"), patch.object(t.urllib.request, "urlopen", side_effect=error) as request:
            with self.assertRaises(t.TranslationDeferred) as caught:
                t.request_translation("Hello", self.locale, t.PROVIDER)
        self.assertEqual(caught.exception.retry_after, 7200)
        self.assertEqual(request.call_count, 1)

    def test_cooldown_blocks_requests_and_survives_new_run(self):
        translator = Mock(side_effect=t.TranslationDeferred("limited", 7200))
        r.recover(self.root, translator, now=lambda: 1000)
        state = json.loads(t.read(self.cache / "cooldown.json"))
        self.assertEqual(state["until"], 8200)
        self.assertEqual(state["Creator"], "Neil Mitchell")
        translator.reset_mock()
        r.recover(self.root, translator, now=lambda: 2000)
        translator.assert_not_called()
        self.assertNotIn("ready=true", t.read(self.root / "output"))

    def test_server_retry_header_defers_immediately(self):
        error = t.urllib.error.HTTPError("https://translate.google.com/m", 503, "unavailable", {"Retry-After": "9000"}, None)
        with patch.object(t.time, "sleep"), patch.object(t.urllib.request, "urlopen", side_effect=error) as request:
            with self.assertRaises(t.TranslationDeferred) as caught:
                t.request_translation("Hello", self.locale, t.PROVIDER)
        self.assertEqual(caught.exception.retry_after, 9000)
        self.assertEqual(request.call_count, 1)

    def test_repeated_limits_increase_fallback_delay(self):
        translator = Mock(side_effect=t.TranslationDeferred("limited"))
        r.recover(self.root, translator, now=lambda: 1000)
        r.recover(self.root, translator, now=lambda: 5000)
        state = json.loads(t.read(self.cache / "cooldown.json"))
        self.assertEqual(state["until"], 12200)
        self.assertIn("not a guaranteed Google reset", t.read(self.root / "summary"))

    def test_complete_then_noop_without_provider(self):
        r.recover(self.root, lambda text, *_: text.replace("Install", "Instalar"))
        self.assertIn("ready=true", t.read(self.root / "output"))
        translator = Mock(side_effect=AssertionError("No network for current pages"))
        r.recover(self.root, translator)
        translator.assert_not_called()
        self.assertEqual(r.pending(self.root), [])
        t.write(self.root / "README.md", "New documentation.")
        self.assertEqual(r.pending(self.root), [("ptBR", "README.md")])

    def test_integrity_failure_cannot_be_published(self):
        with self.assertRaises(ValueError):
            r.recover(self.root, lambda *_: "<script>unsafe</script>")
        self.assertFalse((self.root / "output").exists())
        self.assertFalse((self.cache / "cooldown.json").exists())

    def test_budget_defers_before_network(self):
        translator = Mock()
        timer = iter([0, r.WORK_BUDGET + 1])
        r.recover(self.root, translator, monotonic=lambda: next(timer))
        translator.assert_not_called()
        self.assertIn("45-minute", t.read(self.root / "summary"))
        self.assertNotIn("ready=true", t.read(self.root / "output"))

    def test_interrupted_document_reuses_accepted_segments(self):
        checkpoint = self.cache / "pt-BR.json"
        first = t.SegmentCache({}, checkpoint)
        calls = []
        def translate(text, *_):
            calls.append(text)
            if text == "Later paragraph":
                raise t.TranslationDeferred("limited")
            return text.replace("First", "Primeiro")
        self.assertEqual(t.translate_context("First paragraph", self.locale, t.PROVIDER, translate, first, []), "Primeiro paragraph")
        with self.assertRaises(t.TranslationDeferred):
            t.translate_context("Later paragraph", self.locale, t.PROVIDER, translate, first, [])
        resumed = t.SegmentCache(json.loads(t.read(checkpoint)), checkpoint)
        no_network = Mock(side_effect=AssertionError("Should reuse accepted segment"))
        self.assertEqual(t.translate_context("First paragraph", self.locale, t.PROVIDER, no_network, resumed, []), "Primeiro paragraph")
        no_network.assert_not_called()
        self.assertEqual(len(resumed), 1)

    def test_partial_document_restart_and_atomic_publication(self):
        output = self.root / t.destination("README.md", "pt-BR")
        t.write(output, "Previously published page\n")
        chunks = ["First paragraph", "Later paragraph"]
        translator = Mock(side_effect=["Primeiro paragraph", t.TranslationDeferred("limited")])
        with patch.object(t, "chunks", return_value=chunks):
            with self.assertRaises(t.TranslationDeferred):
                t.translate_one("README.md", self.locale, ["README.md"], t.PROVIDER, self.root, translator)
        self.assertEqual(t.read(output), "Previously published page\n")
        self.assertTrue((self.cache / "pt-BR.json").is_file())
        # The full document's integrity check is intentionally not mocked. Resume
        # reuses the accepted first segment, then rejects this incomplete fixture.
        resumed = Mock(return_value="Segundo paragraph")
        with patch.object(t, "chunks", return_value=chunks), self.assertRaises(ValueError):
            t.translate_one("README.md", self.locale, ["README.md"], t.PROVIDER, self.root, resumed)
        resumed.assert_called_once()
        self.assertEqual(resumed.call_args.args[0], "Later paragraph")
        self.assertEqual(t.read(output), "Previously published page\n")


if __name__ == "__main__":
    unittest.main()

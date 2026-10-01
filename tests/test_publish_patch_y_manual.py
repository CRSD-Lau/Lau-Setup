"""Manual release publication safety. Author/Creator/Modifier: Neil Mitchell."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('publish_manual', Path(__file__).resolve().parents[1] / 'tools/publish_patch_y_manual.py')
publish = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publish)


class PublishTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.names = [f'Patch-Y-3.1.0-{edition}.zip' for edition in ('HD-New-Spells', 'HD-Original-Spells', 'Non-HD')]
        self.names += ['SHA256SUMS-Patch-Y.txt', 'manual-downloads.json']
        for name in self.names:
            (self.root / name).write_bytes(name.encode())
        self.remote = {}
        self.body = '# Existing release\n\nOriginal credit and DBC history.'
        self.mutations = []
        self.normalize_remote_crlf = False

    def tearDown(self):
        self.temporary.cleanup()

    def fake_gh(self, *args):
        action = args[1]
        if action == 'view':
            return json.dumps({'assets': [{'name': name} for name in self.remote], 'body': self.body,
                               'isDraft': False, 'url': 'https://github.com/CRSD-Lau/Lau-Setup/releases/tag/payload-3.1.0'})
        if action == 'download':
            name = args[args.index('--pattern') + 1]
            directory = Path(args[args.index('--dir') + 1])
            (directory / name).write_bytes(self.remote[name])
        elif action == 'upload':
            self.mutations.append(('upload', args))
            for filename in args[3:args.index('--repo')]:
                path = Path(filename)
                self.assertNotIn(path.name, self.remote)
                self.remote[path.name] = path.read_bytes()
        elif action == 'edit':
            self.mutations.append(('edit', args))
            self.body = Path(args[args.index('--notes-file') + 1]).read_text(encoding='utf-8')
            if self.normalize_remote_crlf:
                self.body = self.body.replace('\n', '\r\n')
        else:
            raise AssertionError(args)
        return ''

    def run_publish(self):
        with patch.object(publish, 'gh', side_effect=self.fake_gh), patch.object(publish.subprocess, 'run'):
            publish.publish(self.root / 'catalog.json', self.root, 'CRSD-Lau/Lau-Setup', 'payload-3.1.0')

    def test_different_existing_asset_blocks_all_mutations(self):
        self.remote[self.names[-1]] = b'published different bytes'
        with self.assertRaisesRegex(ValueError, 'refusing replacement'):
            self.run_publish()
        self.assertEqual(self.mutations, [])

    def test_missing_only_upload_preserves_notes_and_readback(self):
        self.remote[self.names[0]] = (self.root / self.names[0]).read_bytes()
        self.run_publish()
        upload = self.mutations[0][1]
        self.assertNotIn(str(self.root / self.names[0]), upload)
        self.assertEqual(set(self.remote), set(self.names))
        self.assertIn('Original credit and DBC history.', self.body)
        self.assertIn('No DBC edits from manual packaging.', self.body)
        self.mutations.clear()
        self.run_publish()
        self.assertTrue(all(action == 'edit' for action, _ in self.mutations))
        self.assertEqual(self.body.count('<!-- patch-y-manual:start -->'), 1)

    def test_wrong_tag_fails_before_external_commands(self):
        with patch.object(publish, 'gh') as gh:
            with self.assertRaisesRegex(ValueError, 'tag'):
                publish.publish(self.root / 'catalog.json', self.root, 'CRSD-Lau/Lau-Setup', '../bad')
            gh.assert_not_called()

    def test_release_notes_readback_accepts_windows_newlines(self):
        self.normalize_remote_crlf = True
        self.run_publish()
        self.assertIn('\r\n', self.body)
        self.assertEqual(set(self.remote), set(self.names))


if __name__ == '__main__':
    unittest.main()

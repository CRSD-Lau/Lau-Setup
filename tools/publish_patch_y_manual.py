#!/usr/bin/env python3
"""Publish verified manual packages without replacing existing release assets.
Author, Creator, Last Modified By: Neil Mitchell
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def gh(*args):
    result = subprocess.run(['gh', *args], check=True, capture_output=True, text=True)
    return result.stdout


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def publish(catalog, output, repo, tag):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise ValueError('Invalid repository.')
    if not re.fullmatch(r'payload-[0-9]+\.[0-9]+\.[0-9]+', tag):
        raise ValueError('Invalid game release tag.')
    version = tag.removeprefix('payload-')
    # Verify against the catalog before making any external changes.
    subprocess.run([sys.executable, str(Path(__file__).with_name('package_patch_y_manual.py')),
                    'verify', '--catalog', str(catalog), '--output', str(output), '--version', version], check=True)
    labels = [('HD-New-Spells', 'HD — New spell visuals'),
              ('HD-Original-Spells', 'HD — Original spell visuals'), ('Non-HD', 'Non-HD / SD')]
    names = [f'Patch-Y-{version}-{slug}.zip' for slug, _label in labels]
    names += ['SHA256SUMS-Patch-Y.txt', 'manual-downloads.json']
    paths = [output / name for name in names]
    expected = {path.name: digest(path) for path in paths}
    release = json.loads(gh('release', 'view', tag, '--repo', repo, '--json', 'assets,body,isDraft,url'))
    if release['isDraft']:
        raise ValueError('Publish the game release before adding manual downloads.')
    existing = {asset['name'] for asset in release['assets']}
    with tempfile.TemporaryDirectory(prefix='patch-y-public-') as temporary:
        downloads = Path(temporary)
        # Preflight every collision before uploading anything. Never use --clobber.
        for name in names:
            if name in existing:
                gh('release', 'download', tag, '--repo', repo, '--pattern', name, '--dir', str(downloads))
                if digest(downloads / name) != expected[name]:
                    raise ValueError('Published asset differs; refusing replacement: ' + name)
        missing = [str(path) for path in paths if path.name not in existing]
        if missing:
            gh('release', 'upload', tag, *missing, '--repo', repo)
        for name in names:
            if name not in existing:
                gh('release', 'download', tag, '--repo', repo, '--pattern', name, '--dir', str(downloads))
            if digest(downloads / name) != expected[name]:
                raise ValueError('Public download SHA-256 mismatch: ' + name)
        base = f'https://github.com/{repo}/releases/download/{tag}'
        marker_start = '<!-- patch-y-manual:start -->'
        marker_end = '<!-- patch-y-manual:end -->'
        section = [marker_start, '## Manual Patch-Y downloads — no installer required', '',
                   'Choose one edition for your existing client:']
        section += [f'- [{label}]({base}/Patch-Y-{version}-{slug}.zip)' for slug, label in labels]
        section += ['', f'[Manual installation guide](https://github.com/{repo}/blob/main/docs/PATCH-Y-MANUAL-INSTALL.md) · '
                    f'[ZIP checksums]({base}/SHA256SUMS-Patch-Y.txt) · [Package manifest]({base}/manual-downloads.json)', '',
                    'The HD new-spells ZIP includes both required Patch-S companions. HD editions require an existing HD model pack. '
                    'Follow the included README to copy Patch-Y to Data and the active locale folder. '
                    'No installer, executable, loading-screen pack, map pack or addons are included.', '',
                    '**No DBC edits from manual packaging.** These MPQs match the installer catalog byte for byte; '
                    'existing gameplay validation and limits are unchanged.', marker_end]
        body = release['body'] or ''
        body = body.replace('These hash-named parts are downloaded and verified by Setup; they are not manual-install ZIPs.',
                            'The hash-named parts are used by Setup. Ready-to-copy manual Patch-Y ZIPs are linked below.')
        block = '\n'.join(section)
        if marker_start in body or marker_end in body:
            if body.count(marker_start) != 1 or body.count(marker_end) != 1 or body.index(marker_start) > body.index(marker_end):
                raise ValueError('Malformed manual-download section in release notes.')
            body = body[:body.index(marker_start)] + block + body[body.index(marker_end) + len(marker_end):]
        else:
            body = body.rstrip() + '\n\n' + block + '\n'
        notes = downloads / 'release-notes.md'
        notes.write_text(body, encoding='utf-8', newline='\n')
        gh('release', 'edit', tag, '--repo', repo, '--notes-file', str(notes))
        readback = json.loads(gh('release', 'view', tag, '--repo', repo, '--json', 'assets,body'))
        if not set(names).issubset({a['name'] for a in readback['assets']}) or block not in readback['body'].replace('\r\n', '\n'):
            raise ValueError('Release readback did not contain all manual artifacts and links.')
    print(json.dumps({'release': release['url'], 'sha256': expected, 'public_downloads_verified': True}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--repo', default='CRSD-Lau/Lau-Setup')
    parser.add_argument('--tag', required=True)
    args = parser.parse_args()
    publish(args.catalog.resolve(), args.output.resolve(), args.repo, args.tag)

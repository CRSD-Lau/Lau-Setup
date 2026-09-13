"""Package only the validated Windows ICC experiment. Author/Creator/Modifier: Neil Mitchell."""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile
ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
VERSION = 'icc-player-range-circles-test1'
FOLDER = 'Lau-ICC-Range-Circles-Test1'
ARCHIVE = FOLDER + '-Windows.zip'

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--installer-results', type=Path, required=True)
    parser.add_argument('--core-results', type=Path, required=True)
    parser.add_argument('--core-provenance', type=Path, required=True)
    args = parser.parse_args()
    scope = read(DIST / 'scope-validation.json')
    installer = read(args.installer_results)
    core = read(args.core_results)
    catalog = read(DIST / 'catalog.json')
    baseline = read(DIST / 'baseline.json')
    build = read(DIST / 'icc-range-build-provenance.json')
    core_binding = read(args.core_provenance)
    editions = sorted((key for key in catalog['Assets'] if key.startswith('Y-')))
    if not len(editions) == 6:
        raise ValueError('Release validation failed')
    if not installer['passed'] == 6:
        raise ValueError('All six installer editions must pass')
    if not (core['passed'] == 76 and len(core['results']) == 76 and (not core['StartAt'])):
        raise ValueError('Release validation failed')
    if not len({row['name'] for row in core['results']}) == 76:
        raise ValueError('Release validation failed')
    if not all((row['status'] == 'PASS' for row in core['results'])):
        raise ValueError('Release validation failed')
    if not core_binding['ResultsSha256'] == digest(args.core_results):
        raise ValueError('Release validation failed')
    if not core_binding['CoreTestsSha256'] == digest(DIST / 'CoreTests.exe') == build['CoreTestsSha256']:
        raise ValueError('Release validation failed')
    if not core_binding['Build'] == build:
        raise ValueError('Core results must bind the current build provenance')
    for name, expected in build['InputSha256'].items():
        if not digest(ROOT / name) == expected:
            raise ValueError('Changed build input: ' + name)
    if not digest(DIST / 'LauIccRangeTest.exe') == build['RangeInstallerSha256'] == installer['rangeInstallerSha256']:
        raise ValueError('Release validation failed')
    if not digest(DIST / 'RangeTestTests.exe') == build['RangeTestTestsSha256'] == installer['testRunnerSha256']:
        raise ValueError('Release validation failed')
    if not digest(DIST / 'catalog.json') == installer['embeddedRangeCatalogSha256']:
        raise ValueError('Release validation failed')
    if not digest(DIST / 'baseline.json') == installer['embeddedBaselineCatalogSha256']:
        raise ValueError('Release validation failed')
    if not digest(ROOT / 'app/RangeTest.cs') == installer['rangeTestSourceSha256']:
        raise ValueError('Release validation failed')
    if not installer['payloadYHashes'] == {name: catalog['Assets'][name]['Sha256'] for name in editions}:
        raise ValueError('Release validation failed')
    for check in ('six_editions', 'mixed_and_single_byte_rejected', 'corrupt_payload_before_write', 'partial_placement_installed_committing_and_recovery_required_rollback', 'repeat_no_op_and_exact_rollback', 'unrelated_sentinel_and_pending_journal_preserved'):
        if not installer[check] is True:
            raise ValueError('Required installer check missing: ' + check)
    for name, expected in scope['build_sources'].items():
        if not digest(ROOT / name) == expected:
            raise ValueError('Changed payload build input: ' + name)
    if not digest(ROOT / 'build/catalog.json') == scope['baseline_catalog_source_sha256']:
        raise ValueError('Release validation failed')
    if not sorted((row['edition'] for row in scope['results'])) == editions:
        raise ValueError('Release validation failed')
    if not all((row['unrelated_members_byte_identical'] for row in scope['results'])):
        raise ValueError('Release validation failed')
    for row in scope['results']:
        name = row['edition']
        if not row['output_archive_sha256'] == catalog['Assets'][name]['Sha256']:
            raise ValueError('Release validation failed')
        if not row['output_archive_bytes'] == catalog['Assets'][name]['Bytes']:
            raise ValueError('Release validation failed')
        if not row['baseline_archive_sha256'] == baseline['Assets'][name]['Sha256']:
            raise ValueError('Release validation failed')
        if not (row['archive_snapshot_readback_exact'] and len(row['changed']) == 5 and (len(row['added']) == 9)):
            raise ValueError('Release validation failed')
    if not read(ROOT / 'docs/dbc/icc-range-test1.json') == scope:
        raise ValueError('Regenerate the public DBC report')
    metadata = dict(Author='Neil Mitchell', Creator='Neil Mitchell', LastModifiedBy='Neil Mitchell')
    files = {'LauIccRangeTest.exe': DIST / 'LauIccRangeTest.exe', 'LauIccRangeTest.exe.config': DIST / 'LauIccRangeTest.exe.config', 'START-HERE.md': ROOT / 'ICC-RANGE-TEST.md', 'EDITING-ICC-RANGES.md': ROOT / 'EDITING-ICC-RANGES.md', 'DBC-CHANGES.md': ROOT / 'docs' / 'dbc' / 'icc-range-test1.md', 'DBC-CHANGES.json': ROOT / 'docs' / 'dbc' / 'icc-range-test1.json'}
    document_dir = DIST / 'packaged-docs'
    document_dir.mkdir(exist_ok=True)
    link_targets = {'ICC-RANGE-TEST.md': 'START-HERE.md',
                    'docs/dbc/icc-range-test1.md': 'DBC-CHANGES.md',
                    'docs/dbc/icc-range-test1.json': 'DBC-CHANGES.json',
                    'icc-range-test1.json': 'DBC-CHANGES.json'}
    for name, source in list(files.items()):
        if name.endswith('.md'):
            contents = source.read_text(encoding='utf-8')
            for old, new in link_targets.items():
                contents = contents.replace('](' + old + ')', '](' + new + ')')
            packaged = document_dir / name
            packaged.write_text(contents, encoding='utf-8')
            files[name] = packaged
    for edition in editions:
        path = DIST / 'payload' / (edition + '.mpq')
        asset = catalog['Assets'][edition]
        if not (path.stat().st_size == asset['Bytes'] and digest(path) == asset['Sha256']):
            raise ValueError('Release validation failed')
        if not asset['Sha256'] != baseline['Assets'][edition]['Sha256']:
            raise ValueError('Release validation failed')
        files['payload/' + path.name] = path
    validation = dict(**metadata, version=VERSION, baseline='Lau game 3.0.8, all six matching editions', issue='https://github.com/CRSD-Lau/Lau-Setup/issues/27', archive_scope=scope['results'], payload_build_inputs=scope['build_sources'], payload_build_dependency=scope['build_dependency'], installer_build=build, installer=installer, core_regression=core, core_provenance=core_binding, limits=['Experimental Windows-only build; unsigned .NET Framework 4.8 installer', "Warmane player attachment, timing, 12-yard scale and full-raid visibility require Andre's test", 'Direct Vortex/Blood Nova markers may appear only at impact; not certified advance warnings', 'Heroic Shadow Prison circles are an experimental aura carrier, not a normal-mode or DBS warning aura', 'No gameplay, spell duration, executable, addon, Q/M/S or account-setting changes'])
    (DIST / 'VALIDATION.json').write_text(json.dumps(validation, indent=2) + '\n', encoding='utf-8')
    files['VALIDATION.json'] = DIST / 'VALIDATION.json'
    for name, path in files.items():
        if not path.is_file():
            raise ValueError(name)
        if path.is_symlink():
            raise ValueError(name)
    manifest = ''.join((digest(path) + '  ' + name + '\n' for name, path in sorted(files.items())))
    (DIST / 'CONTENTS-SHA256.txt').write_text(manifest, encoding='utf-8')
    files['CONTENTS-SHA256.txt'] = DIST / 'CONTENTS-SHA256.txt'
    archive = DIST / ARCHIVE
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as package:
        package.comment = b'Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell'
        for name, path in sorted(files.items()):
            package.write(path, FOLDER + '/' + name)
    with zipfile.ZipFile(archive) as package:
        if not package.testzip() is None:
            raise ValueError('Release validation failed')
        if not sorted(package.namelist()) == sorted((FOLDER + '/' + name for name in files)):
            raise ValueError('Release validation failed')
        for name, path in files.items():
            if not hashlib.sha256(package.read(FOLDER + '/' + name)).hexdigest() == digest(path):
                raise ValueError(name)
        if not b'Creator: Neil Mitchell' in package.comment:
            raise ValueError('Release validation failed')
    checksums = ''.join((digest(path) + '  ' + path.name + '\n' for path in [archive, DIST / 'VALIDATION.json']))
    (DIST / 'SHA256SUMS.txt').write_text(checksums, encoding='utf-8')
    print(json.dumps(dict(**metadata, archive=str(archive), bytes=archive.stat().st_size, sha256=digest(archive), verified_packaged_files=len(files)), indent=2))
if __name__ == '__main__':
    main()

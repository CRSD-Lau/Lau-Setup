"""Package the reviewed source allowlist. Author, Creator, Last Modified By: Neil Mitchell."""
from pathlib import Path
import argparse
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
META = b'Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell'
ADDITIONS = [
    'tools/verify_wizard_polish.py',
    'tools/compact_mpqs.py', 'docs/COMPACTION.md', 'docs/compaction-3.0.9.json',
    'app/Localization.cs', 'app/translations.json', 'app/MpqScan.cs', 'app/MapAddons.cs', 'tools/build_wdm_catalog.py',
    'tools/test.ps1', 'tools/package_universal.py', 'tools/package_universal_source.py',
    'tools/translate_installer.py', 'tools/test_universal_windows.py', 'tools/test_universal_wine.py', 'tests/Tests.cs', 'tests/LocalizationTests.cs',
    'tests/test_universal_package.py', 'tests/test_translate_installer.py',
    'tests/LocalizationProbe.cs', 'tools/test_localization.ps1',
    'docs/dbc/map-pack-1.4.0.json', 'docs/MAP-PACK.md', 'docs/UNIVERSAL-INSTALLER.md', 'docs/RELEASE-1.2.0.md', 'docs/RELEASE-1.2.1.md', 'docs/RELEASE-1.3.0.md', 'docs/RELEASE-1.4.0.md', 'CHANGELOG.md',
    'MPQ-EDIT-BREAKDOWN.md', 'docs/PATCH-Y-DEVELOPMENT.md', 'docs/PATCH-Y-QUICKSTART-WINDOWS.md',
    'tools/patch_y.py', 'tools/patch-y.ps1', 'tools/Patch-Y-Start.cmd', 'tools/generate_patch_y_baseline.py', 'tests/test_patch_y_source.py', 'tests/test_patch_y_archive_integration.py',
    '.github/PULL_REQUEST_TEMPLATE.md', '.github/workflows/patch-y-source.yml',
]

PATCH_Y_EXCLUDED_PARTS = {'.cache', '.work', '__pycache__'}

def build(root=ROOT,output=None):
    root=Path(root).resolve()
    patch_y_names = [
        str(path.relative_to(root)).replace('\\', '/')
        for path in (root / 'patch-y').rglob('*')
        if path.is_file() and not PATCH_Y_EXCLUDED_PARTS.intersection(path.relative_to(root / 'patch-y').parts)
    ]
    names=sorted(set(json.loads((root/'build/wine-public-allowlist.json').read_text(encoding='utf-8-sig'))+ADDITIONS+patch_y_names))
    # Keep this manifest in the source bundle so it can reproduce its own archive.
    names.append('build/wine-public-allowlist.json')
    output=Path(output).resolve() if output else root/'dist/release-1.4.0/LauSetup-source-1.4.0.zip'
    output.parent.mkdir(parents=True,exist_ok=True)
    expected={}
    for name in names:
        path=(root/name).resolve()
        if not path.is_relative_to(root) or not path.is_file():raise ValueError('Invalid source allowlist entry: '+name)
        expected['LauSetup-source/'+name]=path.read_bytes()
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        archive.comment=META
        for name,data in expected.items():
            info=zipfile.ZipInfo(name);info.create_system=3;info.external_attr=(0o100755 if name.endswith('.sh') else 0o100644)<<16
            info.comment=META;info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,data)
    with zipfile.ZipFile(output) as archive:
        if archive.comment!=META or set(archive.namelist())!=set(expected):raise ValueError('Source package manifest or metadata mismatch.')
        for name,data in expected.items():
            if archive.read(name)!=data:raise ValueError('Source package byte mismatch: '+name)
    print(output)
    return output

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=ROOT);parser.add_argument('--output',type=Path)
    args=parser.parse_args();build(args.root,args.output)

"""Stage verified loading-release files as immutable installer parts.
Author / Creator / Last Modified By: Neil Mitchell
"""
import argparse
import hashlib
import json
from pathlib import Path

META = dict(Author='Neil Mitchell', Creator='Neil Mitchell', LastModifiedBy='Neil Mitchell')
CHUNK_BYTES = 96 * 1024 * 1024
APPROVED_PROOF_SHA256 = 'a1681b12133aa583852e2ab7de029279377b970ad58b663d2102686a3d6486e3'

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def stage(root):
    root = root.resolve()
    catalog_path = root / 'build/catalog.json'
    catalog = json.loads(catalog_path.read_text(encoding='utf-8-sig'))
    sources = json.loads((root/'build/source-index.json').read_text(encoding='utf-8-sig'))['sources']
    if catalog['Version'] != '3.1.0' or catalog['InstallerVersion'] != '1.5.0':
        raise ValueError('Unexpected release version')
    proof_path = root/'docs/dbc/loading-3.1.0.json'
    if digest(proof_path) != APPROVED_PROOF_SHA256:
        raise ValueError('Loading release proof is not the reviewed proof')
    proof = json.loads(proof_path.read_text(encoding='utf-8'))
    if proof['status'] != 'MPQ_MEMBER_AND_DBC_READBACK_PASS' or proof['gameVersion'] != catalog['Version']:
        raise ValueError('Loading release proof has not passed verification')
    approved = {'Executable': proof['outputs']['executable']}
    approved.update({'LoadingQ-'+locale: value for locale,value in proof['outputs']['locales'].items()})
    identities = {}
    replacements = {}
    for key in ['Executable', *('LoadingQ-'+locale for locale in catalog['Locales'])]:
        source = Path(sources[key]).resolve()
        if not source.is_relative_to(root/'build/loading-release'):
            raise ValueError('Loading source must be a staged release file: '+key)
        sha = digest(source)
        size = source.stat().st_size
        if sha != approved[key]['sha256'] or size != approved[key]['bytes']:
            raise ValueError('Staged file differs from approved loading proof: '+key)
        if sha not in identities:
            parts = []
            with source.open('rb') as stream:
                while data := stream.read(CHUNK_BYTES):
                    part_sha = hashlib.sha256(data).hexdigest()
                    name = part_sha + '.bin'
                    output = root/'payload'/name
                    if output.exists():
                        if output.stat().st_size != len(data) or digest(output) != part_sha:
                            raise ValueError('Existing payload identity mismatch: '+name)
                    else:
                        with output.open('xb') as target:
                            target.write(data)
                    parts.append(dict(Sha256=part_sha, Bytes=len(data), FileName=name, Url=''))
            if digest(source) != sha or sum(p['Bytes'] for p in parts) != size:
                raise ValueError('Source changed while staging: '+key)
            identities[sha] = dict(Sha256=sha, Bytes=size, Parts=parts)
        replacements[key] = dict(identities[sha], Id=key)
    catalog['Assets'].update(replacements)
    catalog.update(META, PublicReady=False)
    catalog_path.write_text(json.dumps(catalog, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(META, status='STAGED_LOADING_PARTS_VERIFIED', assets={k:dict(Sha256=v['Sha256'], Bytes=v['Bytes']) for k,v in replacements.items()}, unique_sources=len(identities)), indent=2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path(__file__).resolve().parents[1])
    stage(parser.parse_args().project)

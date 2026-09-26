"""Restore native loading-screen framing on the exact Lau executable.

Author / Creator / Last Modified By: Neil Mitchell

Only two five-byte instruction sites are replaced. The second site restores a
PUSH of a coordinate-table pointer, not a CALL into that data table. The added
section and its unrelated archive-list reserve-floor feature remain untouched.
"""
import argparse
import hashlib
import json
from pathlib import Path

SOURCE_SHA256 = '6993049f1338b32a0423612093a8c7c6895b112504b83d6826d4c2174692cd37'
SOURCE_BYTES = 7705600
PATCHES = (
    (0x9A02, bytes.fromhex('e8f9299f00'), bytes.fromhex('e899dfffff')),
    (0x7A15, bytes.fromhex('e8e64a9f00'), bytes.fromhex('680064ab00')),
)
META = dict(Author='Neil Mitchell', Creator='Neil Mitchell', LastModifiedBy='Neil Mitchell')

def digest(data):
    return hashlib.sha256(data).hexdigest()

def repair(data):
    if len(data) != SOURCE_BYTES or digest(data) != SOURCE_SHA256:
        raise ValueError('Executable is not the exact supported Lau input; no changes made.')
    result = bytearray(data)
    for offset, old, new in PATCHES:
        if data[offset:offset + len(old)] != old:
            raise ValueError('Loading hook signature mismatch; no changes made.')
        result[offset:offset + len(old)] = new
    return bytes(result)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--proof', type=Path, required=True)
    args = parser.parse_args()
    source, output = args.source.resolve(), args.output.resolve()
    if source == output or output.exists() or args.proof.exists():
        raise ValueError('Use new staged output and proof paths; never patch a live input in place.')
    before = source.read_bytes()
    after = repair(before)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(after)
    if output.read_bytes() != after or source.read_bytes() != before:
        raise ValueError('Output or source readback mismatch.')
    proof = dict(META, status='STAGED_BYTE_VERIFIED_IN_GAME_ACCEPTANCE_PENDING',
        source_sha256=digest(before), target_sha256=digest(after), bytes=len(after),
        patches=[dict(file_offset=hex(o), before=b.hex(), after=a.hex()) for o,b,a in PATCHES],
        changed_byte_offsets=[hex(i) for i,(a,b) in enumerate(zip(before,after)) if a != b],
        all_other_bytes_identical=True, dbc_changes=False,
        scope='Restore native loading draw call and native UV table push; preserve artwork and archive reserve fix.')
    args.proof.parent.mkdir(parents=True, exist_ok=True)
    args.proof.write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(proof, indent=2))

if __name__ == '__main__':
    main()

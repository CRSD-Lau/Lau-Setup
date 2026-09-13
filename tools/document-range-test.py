"""Write public exact DBC evidence from the verified scope report. Author/Creator/Modifier: Neil Mitchell."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
scope = json.loads((ROOT / 'dist/scope-validation.json').read_text(encoding='utf-8'))
target = ROOT / 'docs/dbc'
target.mkdir(parents=True, exist_ok=True)
(target / 'icc-range-test1.json').write_text(json.dumps(scope, indent=2) + '\n', encoding='utf-8')
lines = [
    '# ICC range circles — Test 1 DBC changes', '',
    '<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->', '',
    'Baseline: exact Lau game 3.0.8, compared separately for all six editions. This experimental branch does not change the stable release or `/pyversion`.', '',
    'All field numbers below are zero-based. Seven existing Spell records change only field 131 (first SpellVisual link); spell strings and every gameplay field are preserved. Four visual tables receive three new rows each. Every original row in those tables remains byte-identical. The full [JSON evidence](icc-range-test1.json) contains complete added-row values, decoded model paths, build input hashes and member hashes.', '',
    'Three private model/skin/texture sets are added under `Spells\\Lau_ICC_RangeTest`. Exactly five DBC members change per archive; all unrelated members pass exact StormLib readback comparison. Runtime player attachment, timing and intended 12-yard radius remain unverified.', '',
]
for result in scope['results']:
    lines += ['## ' + result['edition'], '',
              '- Baseline archive SHA-256: `' + result['baseline_archive_sha256'] + '`',
              '- Test archive SHA-256: `' + result['output_archive_sha256'] + '`',
              '- Test archive bytes: ' + str(result['output_archive_bytes']), '',
              '| Spell ID | Field | Before | After |', '| --- | --- | --- | --- |']
    for row in result['dbc']['Spell']['record_field_diffs']:
        for diff in row['field_diffs']:
            lines.append(f"| {row['id']} | {diff['field']} | {diff['old']} | {diff['new']} |")
    lines += ['', '| Cue | Visual donor → new | Kit donor → new | Effect donor → new | Attachment donor → new |', '| --- | --- | --- | --- | --- |']
    for name, cue in result['dbc']['allocation'].items():
        lines.append(f"| {name.replace('_', ' ')} | {cue['visual_donor']} → {cue['visual_id']} | {cue['kit_donor']} → {cue['kit_id']} | {cue['effect_donor']} → {cue['effect_id']} | {cue['attach_donor']} → {cue['attach_id']} |")
    lines += ['', '| Table | Before SHA-256 | After SHA-256 |', '| --- | --- | --- |']
    for table, evidence in result['dbc'].items():
        if table != 'allocation':
            lines.append(f"| {table} | `{evidence['before_sha256']}` | `{evidence['after_sha256']}` |")
    lines.append('')
(target / 'icc-range-test1.md').write_text('\n'.join(lines), encoding='utf-8')
print('Wrote exact six-edition DBC report and full JSON evidence')

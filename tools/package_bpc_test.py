"""Package the validated BPC floor-marker Windows test. Author/Creator/Modifier: Neil Mitchell."""
from pathlib import Path
import hashlib, json, zipfile

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
FOLDER='Lau-BPC-Floor-Markers-Test3'
ARCHIVE=DIST/(FOLDER+'-Windows.zip')

def digest(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()

def main():
    scope=json.loads((DIST/'scope-validation.json').read_text())
    separation=scope['position_separation']
    if not (scope['marker_count']==25 and scope['no_dbc_edits'] and scope['no_spell_or_gameplay_edits'] and separation['all_pairs_at_least_minimum'] and separation['minimum_actual_planar_yards']>=separation['minimum_required_planar_yards']>=13.0):raise ValueError('Invalid BPC scope')
    editions=sorted(k for k in json.loads((DIST/'catalog.json').read_text())['Assets'] if k.startswith('Y-'))
    if len(editions)!=6 or not all(row['archive_snapshot_readback_exact'] and len(row['added'])==77 and not row['changed_existing_members'] for row in scope['results']):raise ValueError('Payload validation failed')
    files={
      'LauBpcFloorMarkersTest.exe':DIST/'LauBpcFloorMarkersTest.exe',
      'LauBpcFloorMarkersTest.exe.config':DIST/'LauBpcFloorMarkersTest.exe.config',
      'START-HERE.md':ROOT/'BPC-FLOOR-MARKERS-TEST.md',
      'SCOPE-VALIDATION.json':DIST/'scope-validation.json',
      'POSITION-COORDINATES.json':DIST/'bpc-floor-marker-positions.json',
      'POSITION-SEPARATION.json':DIST/'bpc-floor-marker-separation.json',
    }
    for edition in editions:files['payload/'+edition+'.mpq']=DIST/'payload'/(edition+'.mpq')
    if not all(path.is_file() for path in files.values()):raise ValueError('Missing package input')
    manifest=''.join(digest(path)+'  '+name+'\n' for name,path in sorted(files.items()))
    (DIST/'CONTENTS-SHA256.txt').write_text(manifest,encoding='utf-8');files['CONTENTS-SHA256.txt']=DIST/'CONTENTS-SHA256.txt'
    with zipfile.ZipFile(ARCHIVE,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as package:
      package.comment=b'Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell'
      for name,path in sorted(files.items()):package.write(path,FOLDER+'/'+name)
    with zipfile.ZipFile(ARCHIVE) as package:
      if package.testzip() is not None:raise ValueError('Corrupt ZIP')
      if sorted(package.namelist())!=sorted(FOLDER+'/'+name for name in files):raise ValueError('ZIP content mismatch')
      if b'Creator: Neil Mitchell' not in package.comment:raise ValueError('ZIP metadata missing')
      for name,path in files.items():
        if hashlib.sha256(package.read(FOLDER+'/'+name)).hexdigest()!=digest(path):raise ValueError(name)
    result={'Author':'Neil Mitchell','Creator':'Neil Mitchell','LastModifiedBy':'Neil Mitchell','archive':str(ARCHIVE),'bytes':ARCHIVE.stat().st_size,'sha256':digest(ARCHIVE),'files':len(files),'markers':25,'no_dbc_edits':True}
    (DIST/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()

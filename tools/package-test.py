"""Create the allowlisted Windows test ZIP. Author/Creator/Modifier: Neil Mitchell."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
scope=json.loads((D/'scope-validation.json').read_text())
tests=json.loads((ROOT/'reports/lady-final/validation.json').read_text())
core=json.loads((ROOT/'reports/core-final-with-junction/results.json').read_text())
assert tests['passed']==6 and all(r['status']=='PASS' for r in core['results'])
assert len(scope['results'])==6 and all(r['unrelated_members_byte_identical'] for r in scope['results'])
catalog=json.loads((D/'catalog.json').read_text())
files={'LauSetup.exe':D/'LauSetup.exe','LauSetup.exe.config':D/'LauSetup.exe.config',
       'START-HERE.md':ROOT/'LADY-TEST.md','EDITING-LADY.md':ROOT/'EDITING-LADY.md'}
for key,a in catalog['Assets'].items():
    if key.startswith('Y-'):
        p=D/'payload'/(key+'.mpq');assert digest(p)==a['Sha256'] and p.stat().st_size==a['Bytes']
        files['payload/'+p.name]=p
validation=dict(Author='Neil Mitchell',Creator='Neil Mitchell',LastModifiedBy='Neil Mitchell',
    version='lady-deathwhisper-banshee-test1',baseline='3.0.8',scope=scope['results'],
    installer_six_editions=tests,core_regression=core,
    limits=['Windows only; unsigned','Warmane target correspondence and 25-player visibility unverified',
           'Beacon aura duration unchanged; no DBM changes','Original visual accepted locally; edition-specific game tests pending'])
(D/'VALIDATION.json').write_text(json.dumps(validation,indent=2));files['VALIDATION.json']=D/'VALIDATION.json'
manifest=''.join(digest(p)+'  '+n+'\n' for n,p in sorted(files.items()))
(D/'CONTENTS-SHA256.txt').write_text(manifest);files['CONTENTS-SHA256.txt']=D/'CONTENTS-SHA256.txt'
archive=D/'Lau-Lady-Deathwhisper-Test1-Windows.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name,p in sorted(files.items()):z.write(p,'Lau-Lady-Deathwhisper-Test1/'+name)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(files)
    for name,p in files.items():assert hashlib.sha256(z.read('Lau-Lady-Deathwhisper-Test1/'+name)).hexdigest()==digest(p)
(D/'SHA256SUMS.txt').write_text(digest(archive)+'  '+archive.name+'\n'+digest(D/'VALIDATION.json')+'  VALIDATION.json\n')
print('Allowlisted ZIP and every packaged file verified:',archive,archive.stat().st_size)

# Author, Creator, Last Modified By: Neil Mitchell
from pathlib import Path
import json,subprocess,os
r=Path(__file__).resolve().parents[1];out=r/'reports/previews';out.mkdir(parents=True,exist_ok=True)
pref=Path(os.environ['LOCALAPPDATA'])/'LauSetup/interface-language.txt';before=pref.read_bytes() if pref.exists() else None
result=[]
for locale in json.loads((r/'app/translations.json').read_text())['languages']:
 for state in ('initial','small-initial','options','small-options','ready','small-ready','busy','recovery','error','finished'):
  dest=out/(locale+'-'+state+'.png');subprocess.run([str(r/'dist/LauSetup.exe'),'--language',locale,'--render-preview',str(dest),state],check=True,timeout=30)
  snap=json.loads(Path(str(dest)+'.json').read_text(encoding='utf-8-sig'))
  overflow=[c for c in snap['Controls'] if c['Type']!='ComboBox' and not c['Scrollable'] and (c['TextHeight']>c['Height'] or ('Button' in c['Type'] and (c['Left']<0 or c['Top']<0 or c['Top']+c['Height']>c['ParentHeight'] or c['Left']+c['Width']>c['ParentWidth'])))]
  result.append(dict(Locale=locale,State=state,Overflow=overflow))
assert before==(pref.read_bytes() if pref.exists() else None)
(out/'validation.json').write_text(json.dumps(dict(Author='Neil Mitchell',Creator='Neil Mitchell',LastModifiedBy='Neil Mitchell',PreferenceUnchanged=True,Previews=result),ensure_ascii=False,indent=2))
print(json.dumps([x for x in result if x['Overflow']],ensure_ascii=False));print('Previews',len(result))

assert not any(item['Overflow'] for item in result), 'Clipped controls; see validation.json'

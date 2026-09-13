"""Render the exact Windows candidate without touching a game. Author, Creator, Last Modified By: Neil Mitchell."""
from pathlib import Path
import json
import os
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]
EXE=ROOT/'dist/universal-1.2.0/LauSetup.exe'
OUT=ROOT/'reports/universal-1.2.0/windows'

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(ROOT/'dist/universal-1.2.0/LauSetup.zip') as archive:
        expected={'LauSetup/'+name for name in ('LauSetup.exe','LauSetup.sh','lau_wine.py','lau-languages.json','README.txt')}
        if set(archive.namelist())!=expected:raise AssertionError('Unexpected package content')
        archive.extractall(OUT/'package')
    packaged_exe=OUT/'package/LauSetup/LauSetup.exe'
    if packaged_exe.read_bytes()!=EXE.read_bytes():raise AssertionError('Packaged executable bytes differ')
    if packaged_exe.with_suffix('.exe.config').exists():raise AssertionError('Standalone package unexpectedly has a config dependency')
    data=json.loads((ROOT/'app/translations.json').read_text(encoding='utf-8'))
    preference=Path(os.environ['LOCALAPPDATA'])/'LauSetup/interface-language.txt'
    before=preference.read_bytes() if preference.exists() else None
    result=[]
    startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
    for locale,strings in data['languages'].items():
        for state in ('initial','ready','busy','recovery','error'):
            output=OUT/(locale+'-'+state+'.png')
            subprocess.run([str(packaged_exe),'--language',locale,'--render-preview',str(output),state],check=True,timeout=40,startupinfo=startup)
            snapshot=json.loads(Path(str(output)+'.json').read_text(encoding='utf-8-sig'))
            if snapshot['Locale']!=locale:raise AssertionError('Wrong interface language: '+locale)
            texts=[c['Text'] for c in snapshot['Controls']]
            if strings['Interface language'] not in texts:raise AssertionError('Language selector did not translate: '+locale)
            if state=='error' and not any('Data\\patch-test.mpq' in text for text in texts):raise AssertionError('Localized error changed its filename')
            if not output.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'):raise AssertionError('Invalid preview PNG')
            overflow=[c for c in snapshot['Controls'] if c['Type']!='ComboBox' and not c['Scrollable'] and c['TextHeight']>c['Height']]
            result.append(dict(Locale=locale,State=state,Image=output.name,TextOverflow=overflow))
    after=preference.read_bytes() if preference.exists() else None
    if before!=after:raise AssertionError('Rendering previews changed the user preference')
    report=dict(Author='Neil Mitchell',Creator='Neil Mitchell',LastModifiedBy='Neil Mitchell',Previews=result,PreferenceUnchanged=True)
    (OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    overflow=[(r['Locale'],r['State'],c['Text']) for r in result for c in r['TextOverflow']]
    print(json.dumps(dict(Previews=len(result),TextOverflow=overflow,Report=str(OUT/'validation.json')),ensure_ascii=False))
    if overflow:raise SystemExit('Review and fix clipped text before delivery')

if __name__=='__main__':main()

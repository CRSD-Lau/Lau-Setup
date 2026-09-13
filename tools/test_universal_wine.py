#!/usr/bin/env python3
"""Normal-user Wine preview checks for the final shared package.
Author, Creator, Last Modified By: Neil Mitchell

Run only in the supplied Wine container after the final EXE and ZIP exist.
It retains the launcher's runtime/path/process checks and replaces only the
interactive application call with Lau Setup's built-in render-preview mode.
"""
from pathlib import Path
import importlib.util, json, os, subprocess, tempfile, zipfile

PROJECT=Path(os.environ.get('LAU_PROJECT','/project'))
ZIP=PROJECT/'dist/universal-1.2.0/LauSetup.zip'
EXE=PROJECT/'dist/universal-1.2.0/LauSetup.exe'
TRANSLATIONS=PROJECT/'app/translations.json'
PREFIX=Path(os.environ.get('WINEPREFIX','/tmp/lau-user'))
CASES=(
    ('en-US',{'LANG':'en_US.UTF-8'},()),('de-DE',{'LANG':'de_DE.UTF-8'},()),
    ('pt-BR',{'LANG':'pt_BR.UTF-8'},()),('zh-TW',{'LANG':'zh_TW.UTF-8'},()),
    ('ko-KR',{'LANG':'ko_KR.UTF-8'},()),('override-fr-FR',{'LANG':'en_US.UTF-8'},('--language','fr-FR')),
    ('auto-pt-BR',{'LANG':'pt_BR.UTF-8'},('--language','auto')),
)
STATES=('initial','ready','busy')

def preference_snapshot():
    """Preview must not create or change a real user preference in this prefix."""
    return {path: path.read_bytes() for path in PREFIX.rglob('interface-language.txt')}

def load_launcher(folder):
    spec=importlib.util.spec_from_file_location('universal_packaged_launcher',folder/'lau_wine.py')
    launcher=importlib.util.module_from_spec(spec);spec.loader.exec_module(launcher)
    return launcher

def wine_path(path):return 'Z:'+str(path).replace('/','\\')

def main():
    if os.geteuid()==0:raise SystemExit('Run this preview check as the normal lautest user.')
    if os.environ.get('DISPLAY')!=':99':raise SystemExit('Run with DISPLAY=:99.')
    if not ZIP.is_file() or not EXE.is_file() or not TRANSLATIONS.is_file():raise SystemExit('Final universal ZIP, EXE and translations are required.')
    if not (PREFIX/'system.reg').is_file():raise SystemExit('Expected supplied normal-user Wine prefix at '+str(PREFIX))
    spec=importlib.util.spec_from_file_location('universal_package_tool',PROJECT/'tools/package_universal.py')
    package=importlib.util.module_from_spec(spec);spec.loader.exec_module(package);package.verify_package(ZIP)
    evidence=Path(tempfile.mkdtemp(prefix='lau-universal-wine-',dir='/tmp'))
    print('EVIDENCE='+str(evidence),flush=True)
    try:
        with zipfile.ZipFile(ZIP) as archive:archive.extractall(evidence)
        folder=evidence/'LauSetup'
        if (folder/'LauSetup.exe').read_bytes()!=EXE.read_bytes():raise AssertionError('Packaged EXE does not match its release input.')
        if (folder/'lau-languages.json').read_bytes()!=TRANSLATIONS.read_bytes():raise AssertionError('Packaged translations do not match their source.')
        launcher=load_launcher(folder);before=preference_snapshot();original_call=subprocess.call;results=[]
        try:
            for name,locale,args in CASES:
                for key in ('LC_ALL','LC_MESSAGES','LANGUAGE','LANG'):os.environ.pop(key,None)
                os.environ.update(locale,WINEPREFIX=str(PREFIX),WINEARCH='win64',WINEDLLOVERRIDES='mshtml=',WINEDEBUG='-all',DISPLAY=':99')
                expected=launcher.ui_language()
                for state in STATES:
                    image=evidence/(name+'-'+state+'.png')
                    def render_only(command,**kwargs):
                        if command!=['wine',str(folder/'LauSetup.exe')]+list(args):raise AssertionError('Launcher command was not plain validated argv.')
                        if kwargs['env'].get('LAU_UI_LANGUAGE')!=expected:raise AssertionError('Host locale was not passed to Wine.')
                        return original_call(command+['--render-preview',wine_path(image),state],**kwargs)
                    launcher.subprocess.call=render_only
                    if launcher.main(list(args))!=0:raise AssertionError('Preview failed for '+name+' / '+state)
                    if not image.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'):raise AssertionError('Preview did not produce PNG for '+name+' / '+state)
                    observed=json.loads(Path(str(image)+'.json').read_text())
                    wanted='fr-FR' if name=='override-fr-FR' else expected
                    if observed['Locale']!=wanted:raise AssertionError('Rendered interface used '+observed['Locale']+' instead of '+wanted)
                    if observed.get('Capture')!='screen':raise AssertionError('Wine evidence must capture the real window, not Mono DrawToBitmap.')
                    if wanted in ('zh-CN','zh-TW','ko-KR') and not observed.get('Font','').startswith('Noto Sans CJK'):raise AssertionError('Test prefix is missing the documented Wine-visible CJK font.')
                    overflow=[c for c in observed['Controls'] if c['Type']!='ComboBox' and not c['Scrollable'] and c['TextHeight']>c['Height']]
                    if overflow:raise AssertionError('Clipped Wine interface text: '+repr(overflow))
                    results.append(dict(Locale=wanted,Case=name,State=state,Font=observed['Font'],Image=image.name,TextOverflow=overflow))
        finally:launcher.subprocess.call=original_call
        probe=PROJECT/'build/LocalizationTests.exe'
        if not probe.is_file():raise AssertionError('Compile tools/test_localization.ps1 before the Wine verification.')
        if launcher.run(['wine',str(probe),wine_path(evidence/'localization-fixture')],launcher.ui_language())!=0:raise AssertionError('Wine language persistence/live-switch fixture failed.')
        if preference_snapshot()!=before:raise AssertionError('Preview changed a Wine user interface-language preference.')
        (evidence/'validation.json').write_text(json.dumps(dict(Author='Neil Mitchell',Creator='Neil Mitchell',LastModifiedBy='Neil Mitchell',Previews=results,PreferenceUnchanged=True,LocalizationFixture='PASS'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print('EVIDENCE='+str(evidence));print('NORMAL_USER_UNIVERSAL_WINE_PREVIEW_PASS')
        return 0
    except BaseException:
        print('FAILED_EVIDENCE='+str(evidence),flush=True);raise

if __name__=='__main__':raise SystemExit(main())

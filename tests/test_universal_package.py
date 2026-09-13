"""Shared package and Linux language tests. Author: Neil Mitchell."""
import importlib.util,json,os,pathlib,stat,tempfile,unittest,zipfile
from unittest import mock

ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
package=load('package_universal',ROOT/'tools/package_universal.py')
wine=load('lau_wine_universal',ROOT/'wine/lau_wine.py')

LANGUAGES={'en-US','de-DE','fr-FR','es-ES','es-MX','pt-BR','ko-KR','ru-RU','zh-CN','zh-TW'}
def catalog():return {'Author':'Neil Mitchell','Creator':'Neil Mitchell','LastModifiedBy':'Neil Mitchell','languages':{tag:{'Example':'Example'} for tag in LANGUAGES}}

class UniversalPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='lau-universal-');self.root=pathlib.Path(self.temp.name)
        (self.root/'wine').mkdir();(self.root/'app').mkdir();(self.root/'dist/universal-1.2.0').mkdir(parents=True)
        (self.root/'wine/LauSetup.sh').write_bytes(b'#!/bin/sh\n');(self.root/'wine/lau_wine.py').write_bytes(b'print(1)\n');(self.root/'wine/README.txt').write_bytes(b'readme\n')
        self.exe=self.root/'dist/universal-1.2.0/LauSetup.exe';self.exe.write_bytes(b'MZ test executable')
        self.translations=self.root/'app/translations.json';self.translations.write_text(json.dumps(catalog()),encoding='utf-8')
    def tearDown(self):self.temp.cleanup()
    def test_contents_metadata_modes_and_exact_copy(self):
        output=package.build_package(self.root)
        self.assertEqual(output,self.root/'dist/universal-1.2.0/LauSetup.zip');self.assertTrue(package.verify_package(output))
        with zipfile.ZipFile(output) as archive:
            self.assertEqual(archive.namelist(),['LauSetup/'+name for name in package.PACKAGE_FILES])
            self.assertEqual(archive.read('LauSetup/LauSetup.exe'),self.exe.read_bytes())
            self.assertEqual(archive.read('LauSetup/lau-languages.json'),self.translations.read_bytes())
            self.assertEqual((archive.getinfo('LauSetup/LauSetup.sh').external_attr>>16)&0o777,0o755)
            self.assertIn(b'Neil Mitchell',archive.comment)
    def test_explicit_input_and_output_paths(self):
        alternate=self.root/'input.exe';alternate.write_bytes(b'MZ alternate')
        output=self.root/'candidate.zip';self.assertEqual(package.build_package(self.root,output,alternate,self.translations),output)
        with zipfile.ZipFile(output) as archive:self.assertEqual(archive.read('LauSetup/LauSetup.exe'),b'MZ alternate')
    def test_tamper_and_extra_payload_are_rejected(self):
        output=package.build_package(self.root);expected={name:(self.exe.read_bytes() if name=='LauSetup.exe' else self.translations.read_bytes() if name=='lau-languages.json' else (self.root/'wine'/({'LauSetup.sh':'LauSetup.sh','lau_wine.py':'lau_wine.py','README.txt':'README.txt'}[name])).read_bytes()) for name in package.PACKAGE_FILES}
        with zipfile.ZipFile(output,'a') as archive:archive.writestr('LauSetup/extra.dll',b'no')
        with self.assertRaisesRegex(ValueError,'allowlist'):package.verify_package(output,expected)
    def test_missing_source_fails_before_creating_package(self):
        self.exe.unlink()
        with self.assertRaises(FileNotFoundError):package.build_package(self.root)
    def test_catalog_rejects_malformed_keys_values_and_placeholders(self):
        value=catalog()
        for messages in value['languages'].values():messages['Welcome {0}']='Welcome {0}'
        value['languages']['de-DE']['Welcome {0}']='Willkommen {1}'
        with self.assertRaisesRegex(ValueError,'placeholders'):package._validate_catalog(json.dumps(value).encode())
        value=catalog();value['languages']['fr-FR']['Extra']='Extra'
        with self.assertRaisesRegex(ValueError,'key parity'):package._validate_catalog(json.dumps(value).encode())
        value=catalog();value['languages']['ko-KR']['Example']=''
        with self.assertRaisesRegex(ValueError,'empty'):package._validate_catalog(json.dumps(value).encode())
        value=catalog();value['languages']['en-US']['Example']='Changed'
        with self.assertRaisesRegex(ValueError,'identity'):package._validate_catalog(json.dumps(value).encode())

class WineLanguageTests(unittest.TestCase):
    def test_gnu_category_and_language_precedence(self):
        self.assertEqual(wine.ui_language({'LANG':'de_DE.UTF-8','LANGUAGE':'fr:de'}),'fr-FR')
        self.assertEqual(wine.ui_language({'LC_MESSAGES':'es_MX.UTF-8','LANG':'de_DE.UTF-8'}),'es-MX')
        self.assertEqual(wine.ui_language({'LC_ALL':'C','LANGUAGE':'fr:de','LANG':'de_DE.UTF-8'}),'en-US')
        self.assertEqual(wine.ui_language({'LC_ALL':'POSIX','LANGUAGE':'zh_TW:fr'}),'en-US')
        self.assertEqual(wine.ui_language({'LANG':'zh_HK.UTF-8'}),'zh-TW')
        self.assertEqual(wine.ui_language({'LANG':'es_AR.UTF-8'}),'es-MX')
        self.assertEqual(wine.ui_language({'LANG':'es_419.UTF-8'}),'es-MX')
        self.assertEqual(wine.ui_language({'LANG':'zh_Hant_CN.UTF-8'}),'zh-TW')
        self.assertEqual(wine.ui_language({'LANG':'zh_Hans_TW.UTF-8'}),'zh-CN')
        self.assertEqual(wine.ui_language({'LANG':'zh','LANGUAGE':'zh:de'}),'de-DE')
        self.assertEqual(wine.ui_language({'LANGUAGE':'fr:de'}),'en-US')
    def test_validated_cli_override(self):
        self.assertEqual(wine.parse_language(['--language','ru-RU'],{'LANG':'fr_FR'}),'ru-RU')
        self.assertEqual(wine.parse_language(['--language','auto'],{'LANG':'fr_FR'}),'auto')
        with self.assertRaisesRegex(ValueError,'--language'):wine.parse_language(['--language','ru;evil'])
        with self.assertRaisesRegex(ValueError,'--language'):wine.parse_language(['anything'])
        with self.assertRaisesRegex(ValueError,'--language'):wine.parse_language(['--language','auto','extra'])
    def test_launcher_error_uses_sibling_catalog_but_guard_protocol_does_not(self):
        with tempfile.TemporaryDirectory(prefix='lau-language-') as path:
            folder=pathlib.Path(path);data=catalog();data['languages']['fr-FR']['Example']='Exemple'
            (folder/'lau-languages.json').write_text(json.dumps(data),encoding='utf-8')
            self.assertEqual(wine.translate('Example','fr-FR',folder),'Exemple')
            self.assertEqual(wine.translate('Example','fr-FR',folder/'missing'),'Example')
    def test_run_preserves_environment_and_passes_language_without_launching_shell(self):
        class Service:
            server_port=40123
            def serve_forever(self):pass
            def shutdown(self):pass
            def server_close(self):pass
        with mock.patch.object(wine,'server',return_value=Service()),mock.patch.object(wine.threading,'Thread') as thread,mock.patch.object(wine.subprocess,'call',return_value=7) as call:
            with mock.patch.dict(os.environ,{'WINEPREFIX':'/safe/prefix','UNCHANGED':'yes'},clear=True):
                self.assertEqual(wine.run(['wine','/tmp/LauSetup.exe','--language','auto'],'fr'),7)
            command=call.call_args.args[0];environment=call.call_args.kwargs['env']
        self.assertEqual(command,['wine','/tmp/LauSetup.exe','--language','auto']);self.assertEqual(environment['LAU_UI_LANGUAGE'],'fr');self.assertEqual(environment['WINEPREFIX'],'/safe/prefix');self.assertEqual(environment['UNCHANGED'],'yes');thread.assert_called_once()
    def test_existing_guard_runner_callers_detect_host_language(self):
        service=mock.Mock();service.server_port=40124
        with mock.patch.object(wine,'server',return_value=service),mock.patch.object(wine.threading,'Thread'),mock.patch.object(wine.subprocess,'call',return_value=0) as call:
            with mock.patch.dict(os.environ,{'LANG':'de_DE.UTF-8'},clear=True):
                self.assertEqual(wine.run(['wine','fixture-tests.exe']),0)
            self.assertEqual(call.call_args.kwargs['env']['LAU_UI_LANGUAGE'],'de-DE')

if __name__=='__main__':unittest.main(verbosity=2)

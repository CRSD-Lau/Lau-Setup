"""Native safety acceptance tests. Author, Creator, Last Modified By: Neil Mitchell."""
import importlib.util,os,pathlib,subprocess,sys,tempfile,unittest
from unittest import mock
spec=importlib.util.spec_from_file_location('lau_wine',pathlib.Path(__file__).resolve().parents[1]/'wine/lau_wine.py')
host=importlib.util.module_from_spec(spec);spec.loader.exec_module(host)

class HostTests(unittest.TestCase):
    def setUp(self):self.temp=tempfile.TemporaryDirectory(prefix='lau-native-');self.root=pathlib.Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()
    def test_plain_and_missing_staging(self):
        path=self.root/'Data'/'enUS'/'new.mpq';self.assertEqual(host.plain(str(path)),str(path))
    def test_unicode_path(self):
        path=self.root/'Jeu français 中文';path.mkdir();self.assertEqual(host.plain(str(path)),str(path))
    def test_case_collision(self):
        (self.root/'Data').mkdir();(self.root/'data').mkdir()
        with self.assertRaisesRegex(ValueError,'case'):host.plain(str(self.root/'Data'))
    def test_case_mismatch(self):
        (self.root/'Data').mkdir()
        with self.assertRaisesRegex(ValueError,'casing'):host.plain(str(self.root/'data'))
    def test_symlink_and_dangling_link(self):
        (self.root/'target').mkdir();(self.root/'link').symlink_to(self.root/'target');(self.root/'dangling').symlink_to(self.root/'missing')
        for name in ('link','dangling'):
            with self.assertRaisesRegex(ValueError,'Linked'):host.plain(str(self.root/name/'new.mpq'))
    def test_hardlink(self):
        victim=self.root/'original';victim.write_text('KEEP');os.link(victim,self.root/'linked')
        with self.assertRaisesRegex(ValueError,'linked to another'):host.plain(str(self.root/'linked'))
        self.assertEqual(victim.read_text(),'KEEP')
    def test_fifo(self):
        os.mkfifo(self.root/'pipe')
        with self.assertRaisesRegex(ValueError,'ordinary'):host.plain(str(self.root/'pipe'))
    def test_shared_host_lock(self):
        one=host.Guard();two=host.Guard()
        try:
            lease=one.request(dict(operation='acquire',path=str(self.root)))['lease']
            with self.assertRaisesRegex(ValueError,'Another installer'):two.request(dict(operation='acquire',path=str(self.root)))
            one.request(dict(operation='check',path=str(self.root),lease=lease))
            one.request(dict(operation='release',path=str(self.root),lease=lease))
            two.request(dict(operation='acquire',path=str(self.root)))
        finally:one.close();two.close()
    def test_invalid_lease(self):
        guard=host.Guard()
        with self.assertRaisesRegex(ValueError,'no longer valid'):guard.request(dict(operation='check',path=str(self.root),lease='fake'))
    def test_space_uses_client_filesystem(self):
        guard=host.Guard()
        with mock.patch.object(host.os,'statvfs',return_value=type('Space',(),{'f_bavail':7,'f_frsize':4096})()) as query:
            self.assertEqual(guard.request(dict(operation='space',path=str(self.root)))['availableBytes'],28672)
            query.assert_called_once_with(str(self.root))
    def test_release_after_root_rename(self):
        root=self.root/'game';root.mkdir();guard=host.Guard()
        try:
            lease=guard.request(dict(operation='acquire',path=str(root)))['lease']
            moved=self.root/'moved';root.rename(moved)
            guard.request(dict(operation='release',path=str(root),lease=lease))
            moved.rename(root);guard.request(dict(operation='acquire',path=str(root)))
        finally:guard.close()
    def test_nested_mount_device_is_rejected(self):
        guard=host.Guard();guard.request(dict(operation='check',path=str(self.root)))
        nested=self.root/'Data';nested.mkdir()
        actual=os.stat
        def changed(path,*args,**kwargs):
            value=actual(path,*args,**kwargs)
            if str(path)==str(nested):
                values=list(value);values[2]=value.st_dev+1;return os.stat_result(values)
            return value
        # Mock only the device identity because this unprivileged container cannot
        # create bind mounts. The path traversal and guard request remain real.
        with mock.patch.object(host.os,'stat',side_effect=changed):
            with self.assertRaisesRegex(ValueError,'one local filesystem'):guard.request(dict(operation='path',path=str(nested/'new.mpq')))
    def test_native_process_argument_detection(self):
        # A real host process outside Wine's process list, with the PE argument
        # shape used by another prefix. Separate actual Wine tests follow this.
        process=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)',r'C:\Games\WoW.exe'])
        try:
            with self.assertRaisesRegex(ValueError,'Close all WoW'):host.processes()
        finally:process.terminate();process.wait()
    def test_game_name_boundaries(self):
        for value in ('WoW.exe',r'C:\Games\WOW.EXE','/a/WoW.exe (deleted)'):self.assertTrue(host.is_game(value))
        for value in ('not-wow.exe','WoW.exe.backup','LauSetup.exe'):self.assertFalse(host.is_game(value))
    def test_request_authentication(self):
        import urllib.request,urllib.error,threading
        guard=host.Guard();service=host.server(guard,'secret')
        threading.Thread(target=service.serve_forever,daemon=True).start()
        try:
            req=urllib.request.Request('http://127.0.0.1:%d/guard'%service.server_port,data=b'{}',method='POST')
            with self.assertRaises(urllib.error.HTTPError) as error:urllib.request.urlopen(req)
            self.assertEqual(error.exception.code,403)
        finally:service.shutdown();service.server_close();guard.close()
    def test_runtime_baseline_is_accepted_without_warning(self):
        registry='[Mono]\n"DisplayName"="Wine Mono Runtime"\n"DisplayVersion"="10.4.1"\n'
        detected,warnings=host.runtime_compatibility(registry,'wine-11.0')
        self.assertEqual(detected,'Detected Wine wine-11.0; Wine Mono 10.4.1.')
        self.assertEqual(warnings,[])
    def test_runtime_nonbaseline_versions_are_accepted_with_warnings(self):
        registry='[Mono]\n"DisplayName"="Wine Mono Runtime"\n"DisplayVersion"="10.5.0"\n'
        detected,warnings=host.runtime_compatibility(registry,'wine-11.7-staging')
        self.assertIn('wine-11.7-staging',detected)
        self.assertEqual(len(warnings),2)
        detected,warnings=host.runtime_compatibility(registry,'wine-12.0 (Staging)')
        self.assertIn('wine-12.0 (Staging)',detected)
        self.assertEqual(len(warnings),2)
        older='[Mono]\n"DisplayName"="Wine Mono Runtime"\n"DisplayVersion"="9.2.0"\n'
        detected,warnings=host.runtime_compatibility(older,'wine-8.21')
        self.assertIn('wine-8.21',detected)
        self.assertEqual(len(warnings),2)
    def test_runtime_rejects_missing_and_unparsable_versions(self):
        baseline='[Mono]\n"DisplayName"="Wine Mono Runtime"\n"DisplayVersion"="10.4.1"\n'
        with self.assertRaisesRegex(ValueError,'Detected Wine wine-11.0; Wine Mono Runtime is missing'):host.runtime_compatibility('', 'wine-11.0')
        with self.assertRaisesRegex(ValueError,'Could not read Wine version'):host.runtime_compatibility(baseline,'wine-staging')
    def test_runtime_accepts_installed_mono_without_registry_version(self):
        runtime=self.root/'drive_c'/'windows'/'mono'/'mono-2.0';runtime.mkdir(parents=True)
        detected,warnings=host.runtime_compatibility('', 'wine-9.0', self.root)
        self.assertIn('version not exposed',detected)
        self.assertEqual(len(warnings),2)

if __name__=='__main__':unittest.main(verbosity=2)

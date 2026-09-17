#!/usr/bin/env python3
"""Lau Setup Wine launcher and live host guard.
Author, Creator, Last Modified By: Neil Mitchell
"""
try:import fcntl
except ModuleNotFoundError:fcntl=None # Importable for cross-platform packaging tests; main rejects non-Linux hosts.
import hashlib, hmac, http.server, json, os, pathlib, re, secrets
import stat, subprocess, sys, threading

GAME = re.compile(r'^(wow|wow-64|wowclassic)\.exe$', re.I)
UI_LANGUAGES=('en-US','de-DE','fr-FR','es-ES','es-MX','pt-BR','ko-KR','ru-RU','zh-CN','zh-TW')
UI_LANGUAGE_OPTIONS=UI_LANGUAGES+('auto',)
WINE_BASELINE=(11,0,0)
MONO_BASELINE=(10,4,1)
WINE_VERSION=re.compile(r'^wine-(\d+)\.(\d+)(?:\.(\d+))?((?:[-+ ].*)?)$',re.I)
SEMVER=re.compile(r'^(\d+)\.(\d+)(?:\.(\d+))?((?:[-+].*)?)$')

def _locale_tag(value):
    """Map a GNU locale spelling to one of Lau Setup's BCP47 UI languages."""
    if not value:return None
    value=value.strip().split('.',1)[0].split('@',1)[0].replace('_','-')
    if value.upper() in ('C','POSIX'):return None
    bits=value.split('-');language=bits[0].lower();lower={item.lower() for item in bits[1:]}
    direct={'en':'en-US','de':'de-DE','fr':'fr-FR','ko':'ko-KR','ru':'ru-RU','pt':'pt-BR'}
    if language=='es':return 'es-MX' if lower & {'mx','419','ar','bo','br','bz','cl','co','cr','cu','do','ec','sv','gt','hn','ni','pa','py','pe','pr','uy','ve'} else 'es-ES'
    if language=='zh':
        if 'hans' in lower:return 'zh-CN'
        if 'hant' in lower:return 'zh-TW'
        if lower & {'cn','sg'}:return 'zh-CN'
        if lower & {'tw','hk','mo'}:return 'zh-TW'
        return None
    return direct.get(language)

def ui_language(environment=None):
    """Honor GNU LC_* precedence and LANGUAGE only outside the C/POSIX locale."""
    environment=os.environ if environment is None else environment
    category=next((environment.get(key) for key in ('LC_ALL','LC_MESSAGES','LANG') if environment.get(key)), 'C')
    category_is_c=category.strip().split('.',1)[0].split('@',1)[0].upper() in ('C','POSIX')
    if not category_is_c:
        for preferred in environment.get('LANGUAGE','').split(':'):
            tag=_locale_tag(preferred)
            if tag:return tag
    return _locale_tag(category) or 'en-US'

def parse_language(args, environment=None):
    """Return the selected UI language; only a plain, allowlisted argv is accepted."""
    if not args:return ui_language(environment)
    if len(args)==2 and args[0]=='--language' and args[1] in UI_LANGUAGE_OPTIONS:return args[1]
    raise ValueError('The --language option needs one of: '+', '.join(UI_LANGUAGE_OPTIONS)+'.')

def translate(message, language, folder=None):
    """Translate launcher-only messages from the sibling catalog when available.

    Guard HTTP responses intentionally remain raw protocol values for the C# UI.
    """
    try:
        catalog=pathlib.Path(folder or pathlib.Path(__file__).resolve().parent)/'lau-languages.json'
        value=json.loads(catalog.read_text(encoding='utf-8'))
        languages=value.get('languages',value)
        return languages.get(language,{}).get(message,message)
    except (OSError,ValueError,AttributeError):return message

def translate_error(message, language):
    prefix='The --language option needs one of: '
    if message.startswith(prefix):return translate(prefix,language)+message[len(prefix):]
    return translate(message,language)

def _version(value, pattern, name):
    """Return a comparable runtime version and suffix, rejecting ambiguous values."""
    match=pattern.fullmatch((value or '').strip())
    if not match:raise ValueError('Could not read '+name+' version: '+repr(value)+'.')
    return tuple(int(part or 0) for part in match.group(1,2,3)),match.group(4) or ''

def wine_version(value):
    return _version(value,WINE_VERSION,'Wine')

def mono_version(installed, prefix=None, wine_output=None):
    """Find Wine Mono from package metadata or its standard installed runtime path."""
    candidates=[]
    for block in installed.split('\n['):
        if '"DisplayName"="Wine Mono Runtime"' not in block:continue
        match=re.search(r'"DisplayVersion"="([^"]+)"',block)
        if match:candidates.append(match.group(1))
    if not candidates:
        runtime=prefix/'drive_c'/'windows'/'mono'/'mono-2.0' if prefix else None
        if runtime and runtime.is_dir():return None,'installed (version not exposed by this prefix)',''
        prefix='Detected Wine '+wine_output.strip()+'; ' if wine_output else ''
        raise ValueError(prefix+'Wine Mono Runtime is missing from this prefix.')
    parsed=[]
    for candidate in candidates:
        try:parsed.append((_version(candidate,SEMVER,'Wine Mono')[0],candidate))
        except ValueError:continue
    if not parsed:raise ValueError('Could not read Wine Mono version: '+repr(candidates[-1])+'.')
    version,display=max(parsed)
    return version,display,_version(display,SEMVER,'Wine Mono')[1]

def runtime_compatibility(installed, wine_output, prefix=None):
    """Allow parseable runtimes while retaining every real pre-write safety gate."""
    wine,wine_suffix=wine_version(wine_output)
    mono,mono_display,mono_suffix=mono_version(installed,prefix,wine_output)
    detected='Detected Wine '+wine_output.strip()+'; Wine Mono '+mono_display+'.'
    warnings=[]
    if wine!=WINE_BASELINE or wine_suffix:
        warnings.append('Wine '+wine_output.strip()+' differs from the validated Wine 11.0 baseline.')
    if mono is None:
        warnings.append('Wine Mono is installed but its version is not exposed by this prefix.')
    elif mono!=MONO_BASELINE or mono_suffix:
        warnings.append('Wine Mono '+mono_display+' differs from the validated Wine Mono 10.4.1 baseline.')
    return detected,warnings

def local_filesystem(path):
    mounts=[]
    for line in pathlib.Path('/proc/self/mountinfo').read_text().splitlines():
        left,right=line.split(' - ',1);parts=left.split();kind=right.split()[0]
        mount=re.sub(r'\\([0-7]{3})',lambda m:chr(int(m.group(1),8)),parts[4])
        if path==mount or path.startswith(mount.rstrip('/')+'/'):mounts.append((len(mount),kind))
    if not mounts or max(mounts)[1] not in ('ext4','xfs','btrfs','overlay','tmpfs'):
        raise ValueError('Use an ordinary local Linux filesystem (ext4, XFS or Btrfs), not a network or Windows-mounted drive.')

def is_game(value):
    return bool(GAME.fullmatch(value.removesuffix(' (deleted)').replace('\\','/').rsplit('/',1)[-1]))

def plain(path):
    """Inspect native names without resolving away symlinks or case collisions."""
    if not isinstance(path,str) or not path.startswith('/') or '\0' in path:
        raise ValueError('The Wine path could not be mapped to an absolute Linux path.')
    pieces=path.split('/')[1:]
    if any(p in ('.','..') for p in pieces):raise ValueError('Ambiguous Linux path.')
    current='/'
    for part in pieces:
        if not part:continue
        if os.path.isdir(current):
            matches=[p for p in os.listdir(current) if p.casefold()==part.casefold()]
            if len(matches)>1:raise ValueError('Names differing only by case are not supported: '+current)
            if matches and matches[0]!=part:raise ValueError('Wine path casing does not match the Linux filename: '+path)
        current=os.path.join(current,part)
        try:info=os.lstat(current)
        except FileNotFoundError:continue
        if stat.S_ISLNK(info.st_mode):raise ValueError('Linked folders or files are not supported: '+current)
        if not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode)):
            raise ValueError('Only ordinary local files and directories are supported: '+current)
        if stat.S_ISREG(info.st_mode) and info.st_nlink!=1:
            raise ValueError('This file is linked to another file: '+current)
    return os.path.normpath(path)

def processes():
    """Conservative host-wide check, including separate Wine servers/prefixes."""
    proc=pathlib.Path('/proc')
    if not (proc/'self/cmdline').exists():raise ValueError('Linux process inspection is unavailable.')
    for row in (proc/'mounts').read_text().splitlines():
        fields=row.split()
        if len(fields)>3 and fields[1]=='/proc' and any(o.startswith('hidepid=') and o!='hidepid=0' for o in fields[3].split(',')):
            raise ValueError('Restricted Linux process visibility is not supported.')
    for entry in proc.iterdir():
        if not entry.name.isdigit():continue
        try:
            status=(entry/'status').read_text()
            if re.search(r'^State:\s+[ZX]',status,re.M):continue
            comm=(entry/'comm').read_text().strip()
            argv=(entry/'cmdline').read_bytes().decode('utf-8','surrogateescape').split('\0')
            if is_game(comm) or any(is_game(arg) for arg in argv):
                raise ValueError('Close all WoW instances in every Wine prefix before installing or restoring.')
            if 'wine' in comm.lower():
                for line in (entry/'maps').read_text().splitlines():
                    fields=line.split(None,5)
                    if len(fields)==6 and is_game(fields[5]):
                        raise ValueError('Close all WoW instances in every Wine prefix before installing or restoring.')
        except (FileNotFoundError,ProcessLookupError):continue
        except PermissionError:
            raise ValueError('A live Linux process could not be inspected. Close other sessions and retry.')

class Guard:
    def __init__(self):
        self.leases={}
        self.roots={}
        self.mutex=threading.RLock()
    def root(self,path):
        path=plain(path)
        if path=='/' or not os.path.isdir(path):raise ValueError('Choose an existing game directory.')
        local_filesystem(path)
        info=os.stat(path)
        # Backups must share the client's device; reject mounted state directories.
        backup=os.path.join(path,'LauSetupBackups')
        plain(backup)
        if os.path.exists(backup) and os.stat(backup).st_dev!=info.st_dev:
            raise ValueError('Backups must be on the same filesystem as the client.')
        return path,(info.st_dev,info.st_ino)
    def request(self,data):
        with self.mutex:
            op=data.get('operation');path=data.get('path')
            if op=='release':
                lease=self.leases.get(data.get('lease'))
                if lease:
                    if lease[2]!=path:raise ValueError('The Linux client lock belongs to another folder.')
                    self.leases.pop(data.get('lease'));os.close(lease[0])
                return {}
            if op=='path':
                path=plain(path)
                for root,identity in self.roots.items():
                    if path==root or path.startswith(root+'/'):
                        ancestor=path
                        while not os.path.exists(ancestor):ancestor=os.path.dirname(ancestor)
                        local_filesystem(ancestor)
                        if os.stat(ancestor).st_dev!=identity[0]:raise ValueError('Client, Data and backup paths must remain on one local filesystem.')
                return {'path':path}
            path,identity=self.root(path)
            self.roots[path]=identity
            processes()
            if op=='acquire':
                if fcntl is None:raise ValueError('Linux file locking is unavailable.')
                lockdir='/tmp/lau-setup-locks-'+str(os.getuid())
                try:os.mkdir(lockdir,0o700)
                except FileExistsError:pass
                plain(lockdir)
                info=os.stat(lockdir)
                if info.st_uid!=os.getuid() or stat.S_IMODE(info.st_mode)!=0o700:
                    raise ValueError('The private installer lock directory is unsafe.')
                key=hashlib.sha256(repr(identity).encode()).hexdigest()
                fd=os.open(os.path.join(lockdir,key),os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
                try:
                    info=os.fstat(fd)
                    if not stat.S_ISREG(info.st_mode) or info.st_nlink!=1 or info.st_uid!=os.getuid():raise ValueError('Unsafe installer lock.')
                    fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
                except BaseException:
                    os.close(fd);raise ValueError('Another installer may be using this client.')
                token=secrets.token_hex(24);self.leases[token]=(fd,identity,path)
                return {'lease':token,'path':path}
            if op in ('check','space'):
                token=data.get('lease')
                if token:
                    lease=self.leases.get(token)
                    if lease is None or lease[1]!=identity or lease[2]!=path:raise ValueError('The Linux client lock is no longer valid.')
                if op=='space':
                    available=os.statvfs(path)
                    return {'availableBytes':available.f_bavail*available.f_frsize}
                return {}
            raise ValueError('Unknown host guard request.')
    def close(self):
        with self.mutex:
            for fd,_,_ in self.leases.values():os.close(fd)
            self.leases.clear()

def server(guard,secret):
    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_POST(self):
            if self.path!='/guard' or not hmac.compare_digest(self.headers.get('X-Lau-Token',''),secret):
                self.send_error(403);return
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=32768:raise ValueError('Invalid guard request size.')
                value=guard.request(json.loads(self.rfile.read(length)))
                body=json.dumps(dict(ok=True,**value)).encode()
            except Exception as error:body=json.dumps(dict(ok=False,error=str(error))).encode()
            self.send_response(200);self.send_header('Content-Type','application/json')
            self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    service=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
    service.daemon_threads=True
    return service

def run(command,language=None):
    guard=Guard();secret=secrets.token_hex(32);service=server(guard,secret)
    threading.Thread(target=service.serve_forever,daemon=True).start()
    # Preserve the caller's prefix and other Wine settings. This is only a
    # child-process UI preference; no prefix registry value is touched.
    env=os.environ.copy();env['LAU_WINE_GUARD_PORT']=str(service.server_port);env['LAU_WINE_GUARD_TOKEN']=secret;env['LAU_UI_LANGUAGE']=language or ui_language()
    try:return subprocess.call(command,env=env)
    finally:service.shutdown();service.server_close();guard.close()

def main(args=None):
    args=sys.argv[1:] if args is None else args;language=parse_language(args)
    if sys.platform!='linux':raise ValueError('This launcher is for Linux with Wine.')
    if sys.version_info<(3,9):raise ValueError('Lau Setup requires Python 3.9 or newer for its Linux safety checks.')
    if os.geteuid()==0:raise ValueError('Run Lau Setup as your normal user, not root.')
    prefix=pathlib.Path(os.environ.get('WINEPREFIX',str(pathlib.Path.home()/'.wine'))).expanduser()
    if not prefix.is_absolute() or not (prefix/'system.reg').is_file():
        raise ValueError('Select an existing Wine prefix with WINEPREFIX. Set up Wine 11 and Wine Mono 10.4.1 first; Lau Setup does not alter your runtime.')
    with (prefix/'system.reg').open(encoding='utf-8',errors='replace') as registry:
        installed=registry.read(32*1024*1024+1)
    if len(installed)>32*1024*1024:raise ValueError('The Wine runtime registry is too large to inspect safely.')
    if '#arch=win64' not in installed[:512]:raise ValueError('This release requires an existing 64-bit Wine prefix. It does not convert or replace older 32-bit prefixes.')
    version=subprocess.check_output(['wine','--version'],text=True).strip()
    detected,warnings=runtime_compatibility(installed,version,prefix)
    for warning in warnings:print('Lau Setup warning: '+warning+' '+detected,file=sys.stderr)
    folder=pathlib.Path(__file__).resolve().parent
    exe=folder/'LauSetup.exe'
    if not exe.is_file() or not (folder/'lau-languages.json').is_file():raise ValueError('LauSetup.exe, lau_wine.py and lau-languages.json must stay together.')
    # Select WINEPREFIX before launch; never modify runtime packages or game launchers.
    # Forward the same validated plain argv to Ui.Initialize. `auto` resets
    # its saved choice there while this host-derived value remains available.
    return run(['wine',str(exe)]+args,ui_language())

if __name__=='__main__':
    language=ui_language()
    try:
        language=parse_language(sys.argv[1:]);sys.exit(main(sys.argv[1:]))
    except Exception as error:print('Lau Setup: '+translate_error(str(error),language),file=sys.stderr);sys.exit(1)

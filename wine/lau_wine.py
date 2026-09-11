#!/usr/bin/env python3
"""Lau Setup Wine launcher and live host guard.
Author, Creator, Last Modified By: Neil Mitchell
"""
import fcntl, hashlib, hmac, http.server, json, os, pathlib, re, secrets
import stat, subprocess, sys, threading

GAME = re.compile(r'^(wow|wow-64|wowclassic)\.exe$', re.I)

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

def run(command):
    guard=Guard();secret=secrets.token_hex(32);service=server(guard,secret)
    threading.Thread(target=service.serve_forever,daemon=True).start()
    env=os.environ.copy();env['LAU_WINE_GUARD_PORT']=str(service.server_port);env['LAU_WINE_GUARD_TOKEN']=secret
    try:return subprocess.call(command,env=env)
    finally:service.shutdown();service.server_close();guard.close()

def main():
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
    if not any('"DisplayName"="Wine Mono Runtime"' in block and '"DisplayVersion"="10.4.1"' in block for block in installed.split('\n[')):
        raise ValueError('Install Wine Mono 10.4.1 in this prefix first: https://github.com/wine-mono/wine-mono/releases/tag/wine-mono-10.4.1')
    version=subprocess.check_output(['wine','--version'],text=True).strip()
    if version.split()[0]!='wine-11.0':raise ValueError('This release is validated with Wine 11.0. Other Wine versions are not supported yet.')
    folder=pathlib.Path(__file__).resolve().parent
    exe=folder/'LauSetup.exe'
    if not exe.is_file():raise ValueError('Keep LauSetup.exe beside this launcher.')
    # Select WINEPREFIX before launch; never modify runtime packages or game launchers.
    return run(['wine',str(exe)])

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as error:print('Lau Setup: '+str(error),file=sys.stderr);sys.exit(1)

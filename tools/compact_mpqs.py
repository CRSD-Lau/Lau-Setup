"""Compact staged Patch-Y copies and prove decompressed member parity.
Author, Creator, Last Modified By: Neil Mitchell.
"""
from pathlib import Path
import argparse,ctypes as C,ctypes.wintypes as W,hashlib,json,re,shutil,zipfile

def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  while b:=f.read(1024*1024):h.update(b)
 return h.hexdigest()
class Found(C.Structure):
 _fields_=[('name',C.c_char*260),('plain',C.c_void_p)]+[(n,W.DWORD) for n in ['hash_index','block_index','size','flags','compressed','time_lo','time_hi','locale']]
def main():
 p=argparse.ArgumentParser();p.add_argument('--catalog',required=True);p.add_argument('--sources',required=True);p.add_argument('--stormlib',required=True);p.add_argument('--output',required=True);p.add_argument('--game-version',required=True);a=p.parse_args()
 if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+',a.game_version):raise ValueError('Invalid game version')
 out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True);catalog=json.loads(Path(a.catalog).read_text(encoding='utf-8-sig'));sources=json.loads(Path(a.sources).read_text(encoding='utf-8-sig'))['sources'];lib=C.WinDLL(str(Path(a.stormlib).resolve()),use_last_error=True)
 def bind(name,args,result):f=getattr(lib,name);f.argtypes=args;f.restype=result;return f
 open_arc=bind('SFileOpenArchive',[C.c_wchar_p,W.DWORD,W.DWORD,C.POINTER(W.HANDLE)],C.c_bool);close_arc=bind('SFileCloseArchive',[W.HANDLE],C.c_bool)
 first=bind('SFileFindFirstFile',[W.HANDLE,C.c_char_p,C.POINTER(Found),C.c_wchar_p],W.HANDLE);nxt=bind('SFileFindNextFile',[W.HANDLE,C.POINTER(Found)],C.c_bool);end=bind('SFileFindClose',[W.HANDLE],C.c_bool)
 open_file=bind('SFileOpenFileEx',[W.HANDLE,C.c_char_p,W.DWORD,C.POINTER(W.HANDLE)],C.c_bool);read_file=bind('SFileReadFile',[W.HANDLE,C.c_void_p,W.DWORD,C.POINTER(W.DWORD),C.c_void_p],C.c_bool);close_file=bind('SFileCloseFile',[W.HANDLE],C.c_bool);locale=bind('SFileSetLocale',[W.DWORD],W.DWORD)
 info=bind('SFileGetFileInfo',[W.HANDLE,C.c_int,C.c_void_p,W.DWORD,C.POINTER(W.DWORD)],C.c_bool)
 add_file=bind('SFileAddFileEx',[W.HANDLE,C.c_wchar_p,C.c_char_p,W.DWORD,W.DWORD,W.DWORD],C.c_bool)
 compact=bind('SFileCompactArchive',[W.HANDLE,C.c_wchar_p,C.c_bool],C.c_bool)
 def require(ok,what):
  if not ok:raise RuntimeError(what+' failed: '+str(C.get_last_error()))
 def inventory(path):
  arc=W.HANDLE();require(open_arc(str(path),0,0x100,C.byref(arc)),'open readonly');result={}
  try:
   data=Found();search=first(arc,b'*',C.byref(data),None);require(search and search!=C.c_void_p(-1).value,'enumerate')
   try:
    while True:
     name=bytes(data.name).decode('utf-8');key=name.lower()+'|'+str(data.locale)
     if re.fullmatch(r'File[0-9A-Fa-f]+\..*',name):raise ValueError('Unknown member name: '+name)
     if key in result:raise ValueError('Duplicate name/locale: '+key)
     locale(data.locale);f=W.HANDLE();require(open_file(arc,name.encode(),0,C.byref(f)),'open member '+name)
     h=hashlib.sha256();remaining=data.size
     try:
      while remaining:
       take=min(1024*1024,remaining);buf=C.create_string_buffer(take);got=W.DWORD();require(read_file(f,buf,take,C.byref(got),None),'read member '+name)
       if got.value!=take:raise ValueError('Short member read '+name)
       h.update(buf.raw);remaining-=take
     finally:close_file(f)
     result[key]=dict(name=name,locale=data.locale,bytes=data.size,sha256=h.hexdigest(),flags=data.flags,time_lo=data.time_lo,time_hi=data.time_hi)
     if not nxt(search,C.byref(data)):break
   finally:end(search)
   count=W.DWORD();require(info(arc,36,C.byref(count),4,None),'archive member count')
   if count.value!=len(result):raise ValueError('Incomplete member enumeration')
  finally:close_arc(arc)
  return result
 old_version=catalog['Version'];catalog['Version']=a.game_version;catalog['PublicReady']=False
 payload=out/'payload';payload.mkdir(exist_ok=True)
 report=dict(Author='Neil Mitchell',Creator='Neil Mitchell',LastModifiedBy='Neil Mitchell',archives=[])
 for key in sorted(k for k in catalog['Assets'] if k.startswith('Y-')):
  src=Path(sources[key]).resolve();target=out/(key+'.mpq');asset=catalog['Assets'][key]
  if src==target or target.exists():raise ValueError('Output must be a new staged copy: '+str(target))
  if src.stat().st_size!=asset['Bytes'] or sha(src)!=asset['Sha256']:raise ValueError('Source/catalog mismatch: '+key)
  before=inventory(src);shutil.copy2(src,target);arc=W.HANDLE();require(open_arc(str(target),0,0,C.byref(arc)),'open staged copy')
  try:
   version_changes=[]
   if old_version!=a.game_version:
    toc='Interface\\AddOns\\!PYAndre\\!PYAndre.toc';locale(0);f=W.HANDLE();require(open_file(arc,toc.encode(),0,C.byref(f)),'open version TOC')
    try:
     size=before[toc.lower()+'|0']['bytes'];buf=C.create_string_buffer(size);got=W.DWORD();require(read_file(f,buf,size,C.byref(got),None),'read version TOC');raw=buf.raw
     if got.value!=size or raw.count(old_version.encode())!=2:raise ValueError('Unexpected version TOC')
    finally:close_file(f)
    updated=raw.replace(old_version.encode(),a.game_version.encode());tmp=out/(key+'.toc');tmp.write_bytes(updated)
    require(add_file(arc,str(tmp),toc.encode(),0x80000200,2,2),'update staged version TOC')
    version_changes=[toc]
  finally:close_arc(arc)
  versioned=inventory(target)
  for name,old in before.items():
   if old!=versioned[name] and name.split('|')[0] not in [x.lower() for x in version_changes]+['(attributes)','(listfile)']:raise ValueError('Unexpected version edit: '+name)
  if set(before)!=set(versioned):raise ValueError('Version edit changed inventory')
  if version_changes and versioned[toc.lower()+'|0']['sha256']!=hashlib.sha256(updated).hexdigest():raise ValueError('Version readback mismatch')
  before_compaction_bytes=target.stat().st_size
  require(open_arc(str(target),0,0,C.byref(arc)),'reopen versioned stage')
  try:require(compact(arc,None,False),'compact staged copy')
  finally:close_arc(arc)
  after=inventory(target)
  if set(before)!=set(after):raise ValueError('Member inventory changed: '+key)
  changes=[]
  for name,old in versioned.items():
   if old!=after[name]:
    raise ValueError('Content, metadata member or flags changed: '+name)
  if sha(src)!=asset['Sha256']:raise ValueError('Original changed: '+key)
  if target.stat().st_size>src.stat().st_size:raise ValueError('Compaction grew archive: '+key)
  row=dict(id=key,before_bytes=src.stat().st_size,after_bytes=target.stat().st_size,before_sha256=asset['Sha256'],after_sha256=sha(target),saved_bytes=src.stat().st_size-target.stat().st_size,member_count=len(before),members=after,metadata_changes=changes,version_changes=version_changes,pre_compaction_bytes=before_compaction_bytes)
  data=target.read_bytes();digest=row['after_sha256'];(payload/(digest+'.bin')).write_bytes(data)
  catalog['Assets'][key]=dict(Id=key,Bytes=len(data),Sha256=digest,Parts=[dict(Sha256=digest,Bytes=len(data),FileName=digest+'.bin',Url='https://github.com/CRSD-Lau/Lau-Setup/releases/download/payload-'+a.game_version+'/'+digest+'.bin')])
  row['header_before_hex']=src.read_bytes()[:32].hex();row['header_after_hex']=data[:32].hex()
  report['archives'].append(row);print('COMPACT_PASS',key,row['saved_bytes'],flush=True)
 (out/'catalog.json').write_text(json.dumps(catalog,indent=2)+'\n')
 with zipfile.ZipFile(out/('Lau-Patch-Y-'+a.game_version+'-All-Editions.zip'),'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  z.comment=b'Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell'
  for row in report['archives']:z.write(out/(row['id']+'.mpq'),row['id']+'.mpq')
 with zipfile.ZipFile(out/('Lau-Patch-Y-'+a.game_version+'-All-Editions.zip')) as z:
  for row in report['archives']:
   if hashlib.sha256(z.read(row['id']+'.mpq')).hexdigest()!=row['after_sha256']:raise ValueError('ZIP readback failed')
 report['saved_bytes']=sum(x['saved_bytes'] for x in report['archives']);(out/'compaction-proof.json').write_text(json.dumps(report,indent=2)+'\n');print('ALL_COMPACTION_PASS',report['saved_bytes'])
if __name__=='__main__':main()

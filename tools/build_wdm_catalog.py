"""Build map-only WDM archives and pinned per-file addon assets.
Author, Creator, Last Modified By: Neil Mitchell.
Requires an explicitly supplied StormLib DLL. Never writes a game client.
"""
from pathlib import Path
import argparse,ctypes as C,ctypes.wintypes as W,hashlib,json,math,re,subprocess
META=dict(Author='Neil Mitchell',Creator='Neil Mitchell',LastModifiedBy='Neil Mitchell')
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--upstream',required=True);p.add_argument('--stormlib',required=True);p.add_argument('--catalog',required=True);p.add_argument('--output',required=True);p.add_argument('--addon-tree',required=True);args=p.parse_args()
 src=Path(args.upstream);out=Path(args.output);out.mkdir(parents=True,exist_ok=True);payload=out/'payload';payload.mkdir(exist_ok=True)
 dll=C.WinDLL(str(Path(args.stormlib).resolve()))
 for name,types,result in [
 ('SFileOpenArchive',[C.c_void_p,W.DWORD,W.DWORD,C.POINTER(W.HANDLE)],C.c_bool),('SFileCloseArchive',[W.HANDLE],C.c_bool),('SFileOpenFileEx',[W.HANDLE,C.c_char_p,W.DWORD,C.POINTER(W.HANDLE)],C.c_bool),('SFileGetFileSize',[W.HANDLE,C.POINTER(W.DWORD)],W.DWORD),('SFileReadFile',[W.HANDLE,C.c_void_p,W.DWORD,C.POINTER(W.DWORD),C.c_void_p],C.c_bool),('SFileCloseFile',[W.HANDLE],C.c_bool),('SFileCreateArchive',[C.c_void_p,W.DWORD,W.DWORD,C.POINTER(W.HANDLE)],C.c_bool),('SFileAddFileEx',[W.HANDLE,C.c_void_p,C.c_char_p,W.DWORD,W.DWORD,W.DWORD],C.c_bool)]:
  fn=getattr(dll,name);fn.argtypes=types;fn.restype=result
 def opened(path):
  a=W.HANDLE();s=C.create_unicode_buffer(str(path.resolve()));assert dll.SFileOpenArchive(C.cast(s,C.c_void_p),0,0x100,C.byref(a));return a
 def read(a,name):
  f=W.HANDLE();assert dll.SFileOpenFileEx(a,name.encode(),0,C.byref(f)),name
  try:
   hi=W.DWORD();size=dll.SFileGetFileSize(f,C.byref(hi));assert hi.value==0 and size<150_000_000;b=C.create_string_buffer(size);got=W.DWORD();assert dll.SFileReadFile(f,b,size,C.byref(got),None) and got.value==size;return b.raw
  finally:dll.SFileCloseFile(f)
 def inventory(a):
  names=read(a,'(listfile)').decode().splitlines();result={}
  for n in names:
   if n.lower() in {'(listfile)','(attributes)','(signature)'}:continue
   assert n.lower() not in result,('case collision',n)
   result[n.lower()]=n
  return result
 catalog=json.loads(Path(args.catalog).read_text(encoding='utf-8-sig'));catalog['MapPackVersion']='WDM-2.4.5';catalog['PublicReady']=False
 records=[];addons=[]
 def asset(key,path):
  data=path.read_bytes();digest=sha(data);assert data
  part=payload/(digest+'.bin')
  if part.exists():assert part.read_bytes()==data
  else:part.write_bytes(data)
  catalog['Assets'][key]=dict(Id=key,Bytes=len(data),Sha256=digest,Parts=[dict(Sha256=digest,Bytes=len(data),FileName=digest+'.bin',Url='https://github.com/CRSD-Lau/Lau-Setup/releases/download/payload-maps-1.4.0/'+digest+'.bin')])
 for loc in catalog['Locales']:
  paths=[src/f'patch-{loc}-M.MPQ',src/f'patch-{loc}-N.MPQ'];arcs=[opened(path) for path in paths]
  try:
   inventories=[inventory(a) for a in arcs];chosen={};collisions=[]
   for i,names in enumerate(inventories):
    for lower,name in names.items():
     if lower in chosen:collisions.append(dict(member=name,winner='caves',stable_sha256=sha(read(arcs[0],inventories[0][lower])),caves_sha256=sha(read(arcs[1],name))))
     chosen[lower]=(i,name)
   assert {c['member'].lower() for c in collisions}=={'dbfilesclient\\worldmaparea.dbc'},collisions
   assert not any('loadingscreen' in n or n=='dbfilesclient\\map.dbc' for n in chosen)
   target=out/f'patch-{loc}-T.MPQ';expected={name:sha(read(arcs[i],name)) for i,name in chosen.values()}
   if not target.exists():
    a=W.HANDLE();buf=C.create_unicode_buffer(str(target.resolve()));assert dll.SFileCreateArchive(C.cast(buf,C.c_void_p),0,1<<math.ceil(math.log2(len(chosen)+8)),C.byref(a))
    try:
     tmp=out/'member.tmp'
     for lower,(i,name) in sorted(chosen.items()):
      tmp.write_bytes(read(arcs[i],name));buf=C.create_unicode_buffer(str(tmp.resolve()));assert dll.SFileAddFileEx(a,C.cast(buf,C.c_void_p),name.encode(),0x80000200,2,2),name
    finally:dll.SFileCloseArchive(a)
   check=opened(target)
   try:
    actual=inventory(check);assert set(actual)==set(chosen)
    for name,digest in expected.items():assert sha(read(check,name))==digest,name
   finally:dll.SFileCloseArchive(check)
   asset('MapDetails-'+loc,target);records.append(dict(locale=loc,source_sha256=[sha(path.read_bytes()) for path in paths],archive_sha256=sha(target.read_bytes()),members=len(chosen),byte_identical_to_selected_upstream=True,collisions=collisions,no_loading_members=True,member_sha256=expected));print('MAP',loc,len(chosen),flush=True)
  finally:
   for a in arcs:dll.SFileCloseArchive(a)
 tree=json.loads(Path(args.addon_tree).read_text(encoding='utf-8-sig'));seen=set()
 for item in tree['tree']:
  rel=item['path']
  if item['type']!='blob' or not rel.startswith(('WDM/','!Astrolabe/')):continue
  assert ':' not in rel and '..' not in rel.split('/') and rel.lower() not in seen;seen.add(rel.lower())
  path=src/'addons'/rel;data=path.read_bytes();assert len(data)==item['size'];assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==item['sha']
  key='MapAddon-'+sha(rel.encode())[:16];asset(key,path);addons.append(dict(path='Interface\\AddOns\\'+rel.replace('/','\\'),asset=key,sha256=sha(data),bytes=len(data),upstream_blob=item['sha']))
 assert len(addons)==115 and len({a['asset'] for a in addons})==len(addons)
 (out/'catalog.json').write_text(json.dumps(catalog,indent=2)+'\n',encoding='utf-8')
 (out/'map-pack-proof.json').write_text(json.dumps(dict(**META,map_version='WDM 2.4.5 stable + caves 2.4.5 beta',addons_commit='621d4de79f9b9a24586a9d7cdce0f57d8c78e395',maps=records,addons=addons,runtime='PENDING'),indent=2)+'\n',encoding='utf-8')
 lines=['// Author, Creator, Last Modified By: Neil Mitchell','// Exact paths are append-only for historical backup recovery.','using System;','using System.Collections.Generic;','namespace LauSetup { public static class MapAddons {','    public static readonly Dictionary<string,string> Paths=new Dictionary<string,string>(StringComparer.OrdinalIgnoreCase){']
 lines += ['        {@"'+a['path']+'","'+a['asset']+'"},' for a in sorted(addons,key=lambda a:a['path'].lower())]
 lines+=['    };','} }'];(out/'MapAddons.cs').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 print('MAP_PACK_STATIC_PARITY_PASS',len(records),len(addons))
if __name__=='__main__':main()

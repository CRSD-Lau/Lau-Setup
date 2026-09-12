"""Isolated Halion radius experiment. Author/Creator/Modifier: Neil Mitchell."""
import sys,json,struct as S,math,ctypes as C,shutil,hashlib
from pathlib import Path
from ctypes import wintypes as W
sys.path.insert(0,r'D:\Wow Addons\reports\raid-cone-review-20260912')
from apply_buffered_cones import snapshot,opened,dll
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def scale(raw,skin):
 d=bytearray(raw);sk=bytearray(skin);allowed=set();sa=set()
 n,off=S.unpack_from('<2I',d,60);vs=[]
 for i in range(n):
  at=off+48*i;x,y,z=S.unpack_from('<3f',d,at)
  assert abs(z)<.1,'Expected ground marker geometry'
  S.pack_into('<2f',d,at,x*1.3,y*1.3);allowed.update(range(at,at+8));vs.append((x*1.3,y*1.3,z))
 bounds=[min(v[j] for v in vs) for j in range(3)]+[max(v[j] for v in vs) for j in range(3)]+[max(math.sqrt(sum(c*c for c in v)) for v in vs)+.001]
 count,offset=S.unpack_from('<2I',d,28)
 for at in [160]+[offset+i*64+32 for i in range(count)]:
  S.pack_into('<7f',d,at,*bounds);allowed.update(range(at,at+28))
 count,offset=S.unpack_from('<2I',sk,28)
 for i in range(count):
  at=offset+i*48;first,num=S.unpack_from('<10H',sk,at)[2:4];v=vs[first:first+num]
  center=[(min(p[j] for p in v)+max(p[j] for p in v))/2 for j in range(3)]
  radius=max(math.dist(p,center) for p in v)+.001
  S.pack_into('<7f',sk,at+20,*center,*center,radius);sa.update(range(at+20,at+48))
 assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(raw,d)))
 assert all(a==b or i in sa for i,(a,b) in enumerate(zip(skin,sk)))
 return bytes(d),bytes(sk),max(math.hypot(x,y) for x,y,z in vs)
def main():
 out=ROOT/'dist';out.mkdir(exist_ok=True);(out/'payload').mkdir(exist_ok=True)
 catalog=json.loads((BASE/'build/catalog.json').read_text(encoding='utf-8-sig'));prior=json.loads(json.dumps(catalog));index=json.loads((BASE/'build/source-index.json').read_text())['sources'];proof=[]
 dll.SFileAddFileEx.argtypes=[W.HANDLE,C.c_void_p,C.c_char_p,W.DWORD,W.DWORD,W.DWORD];dll.SFileAddFileEx.restype=C.c_bool
 for key,path in index.items():
  if not key.startswith('Y-'):continue
  before=snapshot(Path(path));after=dict(before);radii={};lookup={k.lower():k for k in before}
  for name in ['PW_HalionMeteor_Ground','PW_HalionMeteor_Ring']:
   m=lookup[('Spells\\'+name+'.m2').lower()];sk=lookup[('Spells\\'+name+'00.skin').lower()]
   after[m],after[sk],radii[name]=scale(before[m],before[sk])
  changed=[k for k in before if before[k]!=after[k]];assert len(changed)==4
  target=out/'payload'/(key+'.mpq');shutil.copy2(path,target);h=opened(target,0)
  try:
   for name in changed:
    tmp=out/'member.tmp';tmp.write_bytes(after[name]);buf=C.create_unicode_buffer(str(tmp))
    assert dll.SFileAddFileEx(h,C.cast(buf,C.c_void_p),name.encode(),0x80000200,2,2)
  finally:dll.SFileCloseArchive(h)
  assert snapshot(target)==after
  data=target.read_bytes();digest=sha(data)
  catalog['Assets'][key]=dict(Id=key,Sha256=digest,Bytes=len(data),Parts=[dict(Sha256=digest,Bytes=len(data),FileName=digest+'.bin',Url=None)])
  proof.append(dict(edition=key,changed=changed,radius_scale=1.3,radii=radii,coldflame_and_other_members_identical=True))
 catalog['PublicReady']=False
 (out/'catalog.json').write_text(json.dumps(catalog));(out/'baseline.json').write_text(json.dumps(prior))
 (out/'geometry-validation.json').write_text(json.dumps(dict(Author='Neil Mitchell',Creator='Neil Mitchell',LastModifiedBy='Neil Mitchell',results=proof,in_game='PENDING'),indent=2))
 print('SIX_EDITION_HALION_ONLY_PARITY_PASS')
if __name__=='__main__':main()

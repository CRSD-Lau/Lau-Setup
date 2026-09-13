"""Rebuild native Banshee and marker assets. Author/Creator/Modifier: Neil Mitchell."""
from pathlib import Path
import struct as S, shutil, math
from model_utils import array, append
ROOT=Path(__file__).resolve().parents[1]
T=ROOT/'dist/model';T.mkdir(parents=True,exist_ok=True)
C=ROOT/'editing/native/Creature/Banshee'
creature=T/'Creature/PW_DW_Banshee';creature.mkdir(exist_ok=True,parents=True)
for f in C.iterdir():
 if f.suffix.lower() in ['.m2','.skin','.anim','.blp']:shutil.copyfile(f,creature/f.name)
assert (creature/'Banshee.M2').read_bytes()==(C/'Banshee.M2').read_bytes()
sp=T/'Spells';sp.mkdir(exist_ok=True)
old=ROOT/'editing/native/Spells'
shutil.copyfile(old/'PW_DW_Red.blp',sp/'PW_DW_Red.blp')
# Tint native DXT1 double-ring endpoints; keep shape, block indices, dimensions and mip chain.
ring=bytearray((ROOT/'editing/native/Spells/DoubleRing128.blp').read_bytes())
assert S.unpack_from('<4sI4B',ring)==(b'BLP2',1,2,0,0,1)
for off,size in zip(S.unpack_from('<16I',ring,20),S.unpack_from('<16I',ring,84)):
 if not size:continue
 for at in range(off,off+size,8):
  for j in [0,2]:
   val=S.unpack_from('<H',ring,at+j)[0];rr=(val>>11)&31;gg=(val>>5)&63;bb=val&31
   val=(round(rr*.40)<<11)|(round(gg*.78)<<5)|bb;S.pack_into('<H',ring,at+j,val)
(sp/'PW_DW_Ring.blp').write_bytes(ring)
# Preserve the native Banshee skeleton and append marker geometry to both skin profiles.
d=bytearray((C/'Banshee.M2').read_bytes());bc,bo=S.unpack_from('<II',d,44);root=0
# Bind the marker to the native root; keep all original bones and animation data.
def oldarray(h,stride):
 n,o=S.unpack_from('<II',d,h);return n,bytes(d[o:o+n*stride])
vc,vraw=oldarray(60,48);bl,braw=oldarray(120,2);nt,traw=oldarray(80,16);nm,mraw=oldarray(112,4);nl,lraw=oldarray(128,2);nc,craw=oldarray(136,2);nx,xraw=oldarray(152,2);na,araw=oldarray(88,20);nw,wraw=oldarray(144,2)
full_alpha_lookup=list(S.unpack('<'+str(nw)+'H',wraw)).index(5)
parts=[([(-1.5,-1.5,.055),(1.5,-1.5,.055),(1.5,1.5,.055),(-1.5,1.5,.055)],[(0,1,2),(0,2,3)],1,1.0,[(0,0),(1,0),(1,1),(0,1)])]
for tip in [1.8,2.6,3.4]:
 vs=[(tip-.52,-.48,.075),(tip,0,.075),(tip-.52,.48,.075),(tip-.64,.35,.075),(tip-.25,0,.075),(tip-.64,-.35,.075)]
 parts.append((vs,[(0,1,4),(0,4,5),(1,2,3),(1,3,4)],0,1,[(.5,.5)]*6))
# Faint additive copies around the chevrons provide glow using dim native-format textures.
for tip in [1.8,2.6,3.4]:
 for spread,alpha in [(1.12,.12),(1.24,.045)]:
  v0=[(tip-.52,-.48,.070),(tip,0,.070),(tip-.52,.48,.070),(tip-.64,.35,.070),(tip-.25,0,.070),(tip-.64,-.35,.070)];cx=tip-.32
  vs=[(cx+(x-cx)*spread,y*spread,z) for x,y,z in v0]
  parts.append((vs,[(0,1,4),(0,4,5),(1,2,3),(1,3,4)],2 if spread==1.12 else 3,alpha,[(.5,.5)]*6))
vertices=[];tri=[];partinfo=[]
for i,(vs,fs,ti,alpha,uv) in enumerate(parts):
 start=len(vertices);idx=len(tri)
 for (x,y,z),(u,v) in zip(vs,uv):vertices.append(S.pack('<3f4B4B3f4f',x,y,z+.2,255,0,0,0,root,0,0,0,0,0,1,u,v,u,v))
 tri.extend(start+j for f in fs for j in f);partinfo.append((start,len(vs),idx,len(fs)*3,ti))
array(d,60,vraw+b''.join(vertices),vc+len(vertices));array(d,120,braw+S.pack('<H',root),bl+1)
tex=[]
for name in [r'Spells\PW_DW_Red.blp',r'Spells\PW_DW_Ring.blp',r'Spells\PW_DW_RedSoft.blp',r'Spells\PW_DW_RedSoft2.blp']:
 bb=name.encode()+bytes([0]);off=append(d,bb);tex.append(S.pack('<4I',0,3,len(bb),off))
array(d,80,traw+b''.join(tex),nt+4);array(d,112,mraw+S.pack('<HH',0x15,4)*4,nm+4);array(d,128,lraw+S.pack('<4H',nt,nt+1,nt+2,nt+3),nl+4);array(d,136,craw+S.pack('<H',0),nc+1);array(d,152,xraw+S.pack('<h',-1),nx+1)
# Native constant opacity track is known to render across the creature animations.
# Bake the faint additive halo intensity into separate native-format textures.
for fname,intensity in [('PW_DW_RedSoft.blp',.12),('PW_DW_RedSoft2.blp',.045)]:
 soft=bytearray((sp/'PW_DW_Red.blp').read_bytes())
 for off,size in zip(S.unpack_from('<16I',soft,20),S.unpack_from('<16I',soft,84)):
  if not size:continue
  for at in range(off,off+size,16):
   for j in [8,10]:
    val=S.unpack_from('<H',soft,at+j)[0];rr=(val>>11)&31;gg=(val>>5)&63;bb=val&31
    val=(round(rr*intensity)<<11)|(round(gg*intensity)<<5)|round(bb*intensity);S.pack_into('<H',soft,at+j,val)
 (sp/fname).write_bytes(soft)
bounds=list(S.unpack_from('<6f',d,160));bounds[0]=min(bounds[0],-1.8);bounds[1]=min(bounds[1],-1.8);bounds[3]=max(bounds[3],4);bounds[4]=max(bounds[4],1.8);S.pack_into('<6f',d,160,*bounds);S.pack_into('<f',d,184,max(5,S.unpack_from('<f',d,184)[0]))
for skin in ['Banshee00.skin','Banshee01.skin','Banshee02.skin','Banshee03.skin']:
 k=bytearray((C/skin).read_bytes())
 def ka(h,st):
  n,o=S.unpack_from('<II',k,h);return n,bytes(k[o:o+n*st])
 ic,ir=ka(4,2);tc,tir=ka(12,2);pc,pr=ka(20,4);sc,sr=ka(28,48);nb,br=ka(36,24);assert ic==pc
 sections=[];batches=[]
 for i,(start,nv,idx,ni,ti) in enumerate(partinfo):
  sections.append(S.pack('<10H7f',0,0,ic+start,nv,tc+idx,ni,1,bl,1,root,0,0,.07,0,0,.07,4))
  batches.append(S.pack('<Bb11H',16,0,0,sc+i,sc+i,65535,nm+ti,0,1,nl+ti,nc,full_alpha_lookup,nx))
 array(k,4,ir+S.pack('<'+str(len(vertices))+'H',*range(vc,vc+len(vertices))),ic+len(vertices))
 array(k,12,tir+S.pack('<'+str(len(tri))+'H',*(ic+j for j in tri)),tc+len(tri))
 array(k,20,pr+bytes(4*len(vertices)),pc+len(vertices));array(k,28,sr+b''.join(sections),sc+len(parts));array(k,36,br+b''.join(batches),nb+len(parts))
 assert S.unpack_from('<I',k,44)[0]==S.unpack_from('<I',(C/skin).read_bytes(),44)[0]
 (creature/skin).write_bytes(k)
(creature/'Banshee.M2').write_bytes(d)
assert d[S.unpack_from('<II',d,44)[1]:S.unpack_from('<II',d,44)[1]+bc*88]==(C/'Banshee.M2').read_bytes()[bo:bo+bc*88]

print('Banshee model and four LOD skins built')

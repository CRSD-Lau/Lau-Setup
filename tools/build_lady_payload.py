"""Apply only Lady Deathwhisper edits to supported Patch-Y editions.
Author/Creator/Modifier: Neil Mitchell.
Usage: python tools/build_lady_payload.py BASELINE_DIRECTORY CATALOG_JSON
Set STORMLIB_DLL to a Unicode x64 StormLib DLL. Run build_model.py first.
"""
import sys, json, shutil, hashlib, ctypes as C
from pathlib import Path
from ctypes import wintypes as W
from model_utils import load_wdbc, save_wdbc, by_id, u32, set_u32, set_f32, add_string
from mpq import dll, opened, snapshot
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'; OUT.mkdir(exist_ok=True)

def edit_tables(before, work):
    names=['CreatureDisplayInfo','CreatureModelData','SpellVisual','SpellVisualKit','SpellVisualEffectName','SpellVisualKitModelAttach']
    tables={}; original={}; lookup={k.lower():k for k in before}
    for n in names:
        p=work/(n+'.dbc'); p.write_bytes(before[lookup[('DBFilesClient\\'+n+'.dbc').lower()]])
        tables[n]=load_wdbc(p); original[n]={i:bytes(r) for i,r in by_id(tables[n][1]).items()}
    rows=lambda n:tables[n][1]
    strings=lambda n:tables[n][2]
    ids=lambda n:by_id(rows(n))
    mid=max(ids('CreatureModelData'))+1
    row=bytearray(ids('CreatureModelData')[144]);set_u32(row,0,mid)
    set_u32(row,2,add_string(strings('CreatureModelData'),r'Creature\PW_DW_Banshee\Banshee.mdx'));rows('CreatureModelData').append(row)
    disp=ids('CreatureDisplayInfo')[31553];set_u32(disp,1,mid);set_f32(disp,4,1.2)
    set_u32(disp,6,add_string(strings('CreatureDisplayInfo'),'BansheeSkin'));set_u32(disp,7,0);set_u32(disp,8,0)
    effects=ids('SpellVisualEffectName');icon_id=max(effects)+1;icon=bytearray(effects[6519]);set_u32(icon,0,icon_id)
    set_u32(icon,1,add_string(strings('SpellVisualEffectName'),'PW Deathwhisper Frost Beacon icon'))
    for fld in [4,5,6]:set_f32(icon,fld,1)
    rows('SpellVisualEffectName').append(icon)
    visual=ids('SpellVisual')[15116]
    assert u32(visual,4)==90011, 'Unsupported Deathwhisper state visual'
    kit=ids('SpellVisualKit')[90011];kit[:]=ids('SpellVisualKit')[90002];set_u32(kit,0,90011)
    for fld in range(3,15):set_u32(kit,fld,0)
    at=ids('SpellVisualKitModelAttach');old_attach={i for i,r in at.items() if u32(r,1)==90011}
    attach=bytearray(at[8004]);set_u32(attach,0,max(at)+1);set_u32(attach,1,90011);set_u32(attach,2,icon_id)
    rows('SpellVisualKitModelAttach')[:]=[r for r in rows('SpellVisualKitModelAttach') if u32(r,1)!=90011]+[attach]
    set_u32(visual,3,0);set_u32(visual,4,90011);set_u32(visual,5,0)
    allowed={'CreatureDisplayInfo':{31553},'CreatureModelData':set(),'SpellVisual':{15116},'SpellVisualKit':{90011},'SpellVisualEffectName':set(),'SpellVisualKitModelAttach':old_attach}
    proof={}; updates={}
    for n,(fields,rr,ss) in tables.items():
        new=ids(n);changed={i for i,r in original[n].items() if i not in new or r!=new[i]}
        assert changed<=allowed[n], (n,changed)
        proof[n]={'changed_original_ids':sorted(changed),'added_ids':sorted(set(new)-set(original[n]))}
        p=work/(n+'.dbc');save_wdbc(p,fields,rr,ss)
        updates[lookup[('DBFilesClient\\'+n+'.dbc').lower()]]=p.read_bytes()
    for n,ident in [('CreatureModelData',144),('SpellVisual',15254),('SpellVisualKit',90002),('SpellVisualEffectName',6519),('SpellVisualKitModelAttach',8004)]:
        assert original[n][ident]==ids(n)[ident], (n,ident)
    return updates,proof

def main():
    baseline=Path(sys.argv[1]);catalog=json.loads(Path(sys.argv[2]).read_text(encoding='utf-8-sig'))
    old=json.loads(json.dumps(catalog));proof=[]
    dll.SFileAddFileEx.argtypes=[W.HANDLE,C.c_void_p,C.c_char_p,W.DWORD,W.DWORD,W.DWORD];dll.SFileAddFileEx.restype=C.c_bool
    (OUT/'payload').mkdir(exist_ok=True)
    for key in sorted(k for k in catalog['Assets'] if k.startswith('Y-')):
        path=baseline/(key+'.mpq');raw=path.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==old['Assets'][key]['Sha256'], key
        before=snapshot(path);after=dict(before);work=OUT/'tables'/key;work.mkdir(parents=True,exist_ok=True)
        updates,dbc=edit_tables(before,work);after.update(updates)
        for f in (OUT/'model').rglob('*'):
            if f.is_file():
                name=str(f.relative_to(OUT/'model')).replace('/','\\')
                assert name.lower() not in {k.lower() for k in before}, 'Private asset collision'
                updates[name]=f.read_bytes();after[name]=updates[name]
        target=OUT/'payload'/(key+'.mpq');shutil.copy2(path,target);h=opened(target,0)
        try:
            for name,data in updates.items():
                tmp=work/'member.tmp';tmp.write_bytes(data);buf=C.create_unicode_buffer(str(tmp))
                assert dll.SFileAddFileEx(h,C.cast(buf,C.c_void_p),name.encode(),0x80000200,2,2),name
        finally:dll.SFileCloseArchive(h)
        assert snapshot(target)==after, 'Archive readback mismatch'
        changed=[n for n in before if before[n]!=after[n]]
        assert set(changed)<=set(updates) and len(changed)==6
        data=target.read_bytes();digest=hashlib.sha256(data).hexdigest()
        catalog['Assets'][key]=dict(Id=key,Sha256=digest,Bytes=len(data),Parts=[dict(Sha256=digest,Bytes=len(data),FileName=digest+'.bin',Url=None)])
        proof.append(dict(edition=key,changed=sorted(changed),added=sorted(set(after)-set(before)),dbc=dbc,unrelated_members_byte_identical=True))
        print('PASS Lady-only archive delta and readback:',key,flush=True)
    catalog['PublicReady']=False
    (OUT/'catalog.json').write_text(json.dumps(catalog))
    (OUT/'baseline.json').write_text(json.dumps(old))
    (OUT/'scope-validation.json').write_text(json.dumps(dict(Author='Neil Mitchell',Creator='Neil Mitchell',LastModifiedBy='Neil Mitchell',results=proof,in_game='Local original visual accepted; release editions and 25-player Warmane testing pending'),indent=2))
if __name__=='__main__':main()

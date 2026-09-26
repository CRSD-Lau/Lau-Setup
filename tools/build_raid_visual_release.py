"""Build approved raid-visual Patch-Y payloads from portable sources.

Author/Creator/Modifier: Neil Mitchell
The normal build consumes a verified public 3.0.9 baseline, this source package,
and StormLib. The historical accepted MPQ is optional parity evidence only.
"""
import argparse
import ctypes as C
from ctypes import wintypes as W
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import sys

META=dict(Author="Neil Mitchell",Creator="Neil Mitchell",LastModifiedBy="Neil Mitchell")
ACCEPTED_SHA="cc2dacf106c72b5deeb8b5e0689cb953bf23a726a0f67e939e37014a7b6825d2"
TABLE_PATHS={"Spell":"dbfilesclient\\spell.dbc","SpellVisual":"dbfilesclient\\spellvisual.dbc","SpellVisualKit":"dbfilesclient\\spellvisualkit.dbc","SpellVisualEffectName":"dbfilesclient\\spellvisualeffectname.dbc"}
def sha(data):return hashlib.sha256(data).hexdigest()
def normalized(snapshot):
    result={name.lower():(name,data) for name,data in snapshot.items()}
    assert len(result)==len(snapshot) and all(data is not None for _,data in result.values())
    return result
class DBC:
    def __init__(self,data):
        magic,count,self.fields,self.size,string_bytes=struct.unpack_from("<4s4I",data)
        assert magic==b"WDBC" and self.size==self.fields*4 and len(data)==20+count*self.size+string_bytes
        self.rows={row[0]:list(row) for row in (struct.unpack_from("<"+"I"*self.fields,data,20+i*self.size) for i in range(count))}
        assert len(self.rows)==count;self.strings=data[20+count*self.size:]
    def text(self,offset):return self.strings[offset:self.strings.index(b"\0",offset)].decode("utf-8")
    def bytes(self):return struct.pack("<4s4I",b"WDBC",len(self.rows),self.fields,self.size,len(self.strings))+b"".join(struct.pack("<"+"I"*self.fields,*row) for _,row in sorted(self.rows.items()))+self.strings
def source_bytes(source_root,entry):
    path=source_root/entry["path"];data=path.read_bytes()
    assert len(data)==entry["bytes"] and sha(data)==entry["sha256"],"Source asset hash mismatch: "+str(path)
    return data
def apply_delta(table,delta,name):
    assert table.fields==delta["fields"]
    # Editions have distinct pre-existing string-block lengths. Offsets in the
    # source delta are relative to the HD reference and may need a negative remap.
    base=delta["reference_before_string_bytes"];offset=len(table.strings)-base;table.strings+=b"".join(value.encode("utf-8")+b"\0" for value in delta["append_strings"])
    changed=[]
    for change in delta["changes"]:
        row=table.rows[change["id"]];field=change["field"]
        if "old_string" in change:assert table.text(row[field])==change["old_string"],(name,change["id"],field)
        else:assert row[field]==change["old"],(name,change["id"],field,row[field],change["old"])
        value=change["new"]
        if "old_string" in change:
            assert change["new_string"] in delta["append_strings"];value+=offset
        row[field]=value;changed.append(dict(id=change["id"],field=field,before=change["old"],after=value,after_string=table.text(value) if "old_string" in change else None))
    added={}
    for raw_id,raw_row in delta["added_rows"].items():
        row_id=int(raw_id);assert row_id not in table.rows;row=list(raw_row)
        if name=="SpellVisualEffectName":
            for field in (1,2):
                if row[field]>=base:row[field]+=offset
        table.rows[row_id]=row;added[str(row_id)]=row
    return changed,added
def main():
    here=Path(__file__).resolve().parent.parent/"patch-y"/"raid-release";parser=argparse.ArgumentParser()
    parser.add_argument("--baseline-catalog",required=True,type=Path);parser.add_argument("--baseline-dir",required=True,type=Path);parser.add_argument("--source-dir",type=Path,default=here)
    parser.add_argument("--mpq-helper",type=Path,default=Path(__file__).resolve().parent,help="Directory containing the bundled read-only mpq.py helper.");parser.add_argument("--stormlib",required=True,type=Path);parser.add_argument("--out",required=True,type=Path);parser.add_argument("--game-version",default="3.1.0")
    parser.add_argument("--accepted",type=Path,help="Optional historical donor for local parity verification; never a normal build input.")
    args=parser.parse_args();assert "world of warcraft" not in str(args.out.resolve()).lower()
    spec=json.loads((args.source_dir/"raid-visual-spec.json").read_text(encoding="utf-8"));assert all(spec.get(k)==v for k,v in META.items())
    catalog=json.loads(args.baseline_catalog.read_text(encoding="utf-8-sig"));assert catalog["Version"]=="3.0.9"
    os.environ["STORMLIB_DLL"]=str(args.stormlib);sys.path.insert(0,str(args.mpq_helper));import mpq
    assets={entry["path"].replace("/","\\").lower():entry for entry in spec["assets"]};assert len(assets)==15
    asset_data={name:source_bytes(args.source_dir/"assets",entry) for name,entry in assets.items()}
    skin_path=spec["halion"]["path"].replace("/","\\").lower();skin=source_bytes(args.source_dir/"halion",dict(path=spec["halion"]["path"],sha256=spec["halion"]["sha256"],bytes=spec["halion"]["bytes"]));assert spec["halion"]["expected_changed_offsets"]==[36,38476,38478]
    mpq.dll.SFileAddFileEx.argtypes=[W.HANDLE,C.c_void_p,C.c_char_p,W.DWORD,W.DWORD,W.DWORD];mpq.dll.SFileAddFileEx.restype=C.c_bool;mpq.dll.SFileCompactArchive.argtypes=[W.HANDLE,C.c_wchar_p,C.c_bool];mpq.dll.SFileCompactArchive.restype=C.c_bool
    args.out.mkdir(parents=True,exist_ok=True);proof=[];accepted=None
    if args.accepted:assert sha(args.accepted.read_bytes())==ACCEPTED_SHA;accepted=normalized(mpq.snapshot(args.accepted))
    editions=[key for key in catalog["Assets"] if key.startswith("Y-") and key.endswith("Consecration-On")]
    assert set(editions)=={"Y-HD-NewSpells-On-Consecration-On","Y-HD-NewSpells-Off-Consecration-On","Y-Non-HD-Consecration-On"}
    for edition in editions:
        baseline_path=args.baseline_dir/(edition+".mpq");assert sha(baseline_path.read_bytes())==catalog["Assets"][edition]["Sha256"]
        original=mpq.snapshot(baseline_path);lookup=normalized(original);assert not set(assets)&set(lookup)
        updates={assets[name]["path"].replace("/","\\"):data for name,data in asset_data.items()};table_proof=[]
        for title,path in TABLE_PATHS.items():
            canonical,data=lookup[path];current=DBC(data);changes,added=apply_delta(current,spec["dbc"][title],title);updates[canonical]=current.bytes();table_proof.append(dict(table=title,changed_fields=changes,added_rows=added,original_strings_preserved=True,before_sha256=sha(data),after_sha256=sha(current.bytes())))
        assert lookup[skin_path][1]!=skin and len(lookup[skin_path][1])==len(skin);updates[lookup[skin_path][0]]=skin
        toc_path="interface\\addons\\!pyandre\\!pyandre.toc";toc=lookup[toc_path][1];assert toc.count(b"3.0.9")==2;updates[lookup[toc_path][0]]=toc.replace(b"3.0.9",args.game_version.encode("ascii"))
        target=args.out/(edition+".mpq");assert not target.exists(),"Use a fresh output directory";shutil.copy2(baseline_path,target);handle=mpq.opened(target,0)
        try:
            for name,data in sorted(updates.items()):
                temporary=args.out/"member.tmp";temporary.write_bytes(data);buffer=C.create_unicode_buffer(str(temporary));assert mpq.dll.SFileAddFileEx(handle,C.cast(buffer,C.c_void_p),name.encode("ascii"),0x80000200,2,2)
            assert mpq.dll.SFileCompactArchive(handle,None,False)
        finally:mpq.dll.SFileCloseArchive(handle)
        actual=mpq.snapshot(target);expected=dict(original,**updates);assert actual==expected
        changed=sorted(name for name in original if original[name]!=actual[name]);assert len(changed)==6 and len(actual)-len(original)==15
        if accepted and edition=="Y-HD-NewSpells-On-Consecration-On":
            compared=normalized(actual);assert set(compared)==set(accepted);assert {name for name in compared if compared[name][1]!=accepted[name][1]}=={skin_path,toc_path}
        proof.append(dict(edition=edition,source_sha256=sha(baseline_path.read_bytes()),target=str(target),sha256=sha(target.read_bytes()),bytes=target.stat().st_size,changed_members=changed,added_members=sorted(entry["path"] for entry in spec["assets"]),tables=table_proof,all_other_members_byte_identical=True,roundtrip_verified=True))
    report=dict(**META,status="THREE_EDITION_PORTABLE_ARCHIVE_AND_DBC_VALIDATION_PASS",editions=proof,source_spec_sha256=sha((args.source_dir/"raid-visual-spec.json").read_bytes()),game_version=args.game_version,accepted_parity_verified=bool(accepted),halion_skin_changed_offsets=spec["halion"]["expected_changed_offsets"],in_game_gate="New Halion marks and HD spells-off/SD configurations require in-game validation.")
    (args.out/"visual-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8");print(json.dumps({"status":report["status"],"accepted_parity_verified":bool(accepted),"editions":[{"edition":x["edition"],"sha256":x["sha256"]} for x in proof]},indent=2))
if __name__=="__main__":main()

"""Semantic WDBC record diff. Author/Creator/Modifier: Neil Mitchell.
Compare extracted table directories; unknown numeric fields are unsigned raw words.
"""
import argparse,csv,gzip,hashlib,json,struct
from pathlib import Path

def parse(data):
    magic,n,f,size,ss=struct.unpack_from('<4s4I',data)
    if magic!=b'WDBC' or size!=f*4 or len(data)!=20+n*size+ss:raise ValueError('Unsupported WDBC structure')
    rows={}
    for i in range(n):
        row=struct.unpack_from('<'+'I'*f,data,20+i*size)
        if row[0] in rows:raise ValueError('Duplicate record ID')
        rows[row[0]]=row
    return f,rows,data[20+n*size:]

def string_fields(name):
    if name=='spell.dbc':return set(range(136,152))|set(range(153,169))|set(range(170,186))|set(range(187,203))
    if name=='spellvisualeffectname.dbc':return {1,2}
    return set()

def value(row,i,strings,string_columns):
    word=row[i]
    if i not in string_columns:return word
    if word>=len(strings):raise ValueError('Invalid string offset')
    end=strings.find(b'\0',word)
    if end<0:raise ValueError('Unterminated string')
    return strings[word:end].decode('utf-8',errors='strict')

def compare(before,after,csv_path,bases=None):
    bases=bases or {};records=[];sha=lambda b:hashlib.sha256(b).hexdigest()
    with gzip.open(csv_path,'wt',encoding='utf-8',newline='') as stream:
        w=csv.writer(stream);w.writerow(['table','change','record_id','field_zero_based','type','old_value','new_value'])
        for name in sorted(before.keys()|after.keys()):
            old=before.get(name);new=after.get(name);added=old is None;basis=bases.get(name) if added else None
            effective=old if old is not None else basis
            nf,nr,ns=parse(new) if new is not None else (None,{},b'')
            of,orr,os=parse(effective) if effective is not None else (nf,{},b'')
            if nf is not None and of!=nf:raise ValueError('Schema change requires explicit mapping: '+name)
            columns=string_fields(name);changes=0;changed_ids=set();added_ids=sorted(nr.keys()-orr.keys());removed_ids=sorted(orr.keys()-nr.keys())
            if added:w.writerow([name,'table_added','','','','',sha(new)])
            if new is None:w.writerow([name,'table_removed','','','',sha(old),''])
            for rid in sorted(nr.keys()|orr.keys()):
                a=orr.get(rid);b=nr.get(rid);kind='record_added' if a is None else 'record_removed' if b is None else 'field_changed'
                for i in range(nf or of):
                    av=value(a,i,os,columns) if a else None;bv=value(b,i,ns,columns) if b else None
                    if av==bv:continue
                    w.writerow([name,kind,rid,i,'utf8' if i in columns else 'uint32_raw',av,bv]);changes+=1;changed_ids.add(rid)
            records.append(dict(table=name,before_sha256=sha(old) if old else None,after_sha256=sha(new) if new else None,basis_sha256=sha(basis) if basis else None,table_added=added,table_removed=new is None,before_records=len(orr),after_records=len(nr),fields=nf or of,changed_records=len(changed_ids),changed_fields=changes,added_record_ids=added_ids,removed_record_ids=removed_ids,byte_identical=old==new))
    return records

def directory(path):
    return {p.name.lower():p.read_bytes() for p in Path(path).rglob('*.dbc')}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('before');p.add_argument('after');p.add_argument('output');a=p.parse_args()
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    result=compare(directory(a.before),directory(a.after),out.with_suffix('.csv.gz'))
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')

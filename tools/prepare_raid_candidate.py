"""Assemble a local-only candidate catalog and offline visual payload.
Author/Creator/Modifier: Neil Mitchell
"""
import argparse
import hashlib
import json
from pathlib import Path

META = dict(Author="Neil Mitchell", Creator="Neil Mitchell", LastModifiedBy="Neil Mitchell")

def read(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))

def save(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--project", type=Path, required=True)
    p.add_argument("--visuals", type=Path, required=True)
    p.add_argument("--previous-catalog", type=Path, required=True)
    p.add_argument("--previous-sources", type=Path, required=True)
    p.add_argument("--maps", type=Path)
    a=p.parse_args()
    catalog=read(a.previous_catalog)
    sources=read(a.previous_sources)
    proof=read(a.visuals/"visual-validation.json")
    assert catalog["Version"]=="3.0.9" and proof["game_version"]=="3.1.0"
    payload=a.project/"payload"
    payload.mkdir(exist_ok=True)
    for edition in proof["editions"]:
        path=Path(edition["target"])
        data=path.read_bytes()
        assert hashlib.sha256(data).hexdigest()==edition["sha256"]
        part=dict(Sha256=edition["sha256"],Bytes=len(data),FileName=edition["sha256"]+".bin",Url="")
        destination=payload/part["FileName"]
        if not destination.exists():destination.write_bytes(data)
        assert hashlib.sha256(destination.read_bytes()).hexdigest()==part["Sha256"]
        # Keep legacy IDs so old option records remain readable. Both route to
        # the same standard visual payload; the UI no longer offers Off.
        for key in (edition["edition"], edition["edition"].removesuffix("On")+"Off"):
            catalog["Assets"][key]=dict(Id=key,Bytes=len(data),Sha256=part["Sha256"],Parts=[part])
            sources["sources"][key]=str(path)
    if a.maps:
        delta=read(a.maps/"catalog-delta.json")
        previous=catalog["Assets"]["Maps"]
        catalog["PreviousMapRoots"]=[dict(Sha256=previous["Sha256"],Bytes=previous["Bytes"])]
        catalog["Assets"].update(delta["Assets"])
        sources["sources"].update(read(a.maps/"map-source-index.json")["sources"])
    catalog.update(META, Version="3.1.0", InstallerVersion="1.5.0", PublicReady=False)
    sources.update(META)
    save(a.project/"build/catalog.json",catalog)
    save(a.project/"build/source-index.json",sources)
    print("LOCAL_CANDIDATE_CATALOG_READY; public downloads intentionally unconfigured for new assets")

if __name__=="__main__":main()

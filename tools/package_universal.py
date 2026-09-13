#!/usr/bin/env python3
"""Build the small, shared Windows/Linux Lau Setup ZIP.
Author, Creator, Last Modified By: Neil Mitchell
"""
import argparse, collections, json, os, pathlib, re, tempfile, zipfile

AUTHOR='Neil Mitchell'
ARCHIVE_COMMENT=b'Author: Neil Mitchell\nCreator: Neil Mitchell\nLast Modified By: Neil Mitchell\n'
PACKAGE_FILES={'LauSetup.exe':('exe',0o644),'LauSetup.sh':('sh',0o755),'lau_wine.py':('wine',0o644),'lau-languages.json':('translations',0o644),'README.txt':('readme',0o644)}
PLACEHOLDER=re.compile(r'\{\d+\}')

def _repo_root():return pathlib.Path(__file__).resolve().parents[1]

def _sources(root,exe,translations):
    return {'exe':pathlib.Path(exe) if exe else root/'dist/universal-1.2.0/LauSetup.exe','sh':root/'wine/LauSetup.sh','wine':root/'wine/lau_wine.py','translations':pathlib.Path(translations) if translations else root/'app/translations.json','readme':root/'wine/README.txt'}

def _validate_catalog(data):
    try:value=json.loads(data.decode('utf-8'));languages=value['languages']
    except (UnicodeDecodeError,json.JSONDecodeError,KeyError,TypeError) as error:raise ValueError('Translations must be UTF-8 JSON with a languages dictionary.') from error
    if value.get('Author')!=AUTHOR or value.get('Creator')!=AUTHOR or value.get('LastModifiedBy')!=AUTHOR:raise ValueError('Translation metadata must name Neil Mitchell.')
    allowed={'en-US','de-DE','fr-FR','es-ES','es-MX','pt-BR','ko-KR','ru-RU','zh-CN','zh-TW'}
    if set(languages)!=allowed or any(not isinstance(messages,dict) for messages in languages.values()):raise ValueError('Translations must contain exactly the supported BCP47 English-key dictionaries.')
    english=languages['en-US']
    if not english or any(not isinstance(key,str) or not key or not isinstance(text,str) or not text or key!=text for key,text in english.items()):raise ValueError('English translations must be a nonempty identity dictionary.')
    keys=set(english)
    for locale,messages in languages.items():
        if set(messages)!=keys:raise ValueError('Translations must have exact key parity with English: '+locale)
        for key,text in messages.items():
            if not isinstance(text,str) or not text:raise ValueError('Translations must not contain empty values: '+locale+' / '+key)
            if collections.Counter(PLACEHOLDER.findall(key))!=collections.Counter(PLACEHOLDER.findall(text)):raise ValueError('Translations must preserve placeholders: '+locale+' / '+key)

def _zip_info(name,mode):
    info=zipfile.ZipInfo('LauSetup/'+name);info.create_system=3;info.external_attr=(mode&0xffff)<<16;info.comment=ARCHIVE_COMMENT
    return info

def build_package(root=None,output=None,exe=None,translations=None):
    """Create the allowlisted archive and return its resolved path."""
    root=pathlib.Path(root or _repo_root()).resolve();output=pathlib.Path(output or root/'dist/universal-1.2.0/LauSetup.zip').resolve();sources=_sources(root,exe,translations);contents={}
    for name,(kind,_mode) in PACKAGE_FILES.items():
        source=sources[kind]
        if not source.is_file():raise FileNotFoundError('Required package source is missing: '+str(source))
        contents[name]=source.read_bytes()
    _validate_catalog(contents['lau-languages.json']);output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix='lau-universal-',suffix='.zip',dir=str(output.parent),delete=False) as temporary:temp=pathlib.Path(temporary.name)
    try:
        with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
            archive.comment=ARCHIVE_COMMENT
            for name,(_kind,mode) in PACKAGE_FILES.items():archive.writestr(_zip_info(name,mode),contents[name])
        verify_package(temp,expected=contents);os.replace(temp,output)
    finally:
        if temp.exists():temp.unlink()
    return output

def verify_package(package,expected=None):
    """Reject extra payloads, altered bytes, incomplete metadata, and modes."""
    with zipfile.ZipFile(pathlib.Path(package)) as archive:
        wanted=['LauSetup/'+name for name in PACKAGE_FILES]
        if archive.namelist()!=wanted:raise ValueError('Universal package must contain only the LauSetup allowlist.')
        if archive.comment!=ARCHIVE_COMMENT:raise ValueError('Universal package metadata is missing Neil Mitchell.')
        for name,(_kind,mode) in PACKAGE_FILES.items():
            info=archive.getinfo('LauSetup/'+name)
            if ((info.external_attr>>16)&0o777)!=mode:raise ValueError('Unexpected package mode for '+name)
            if info.comment!=ARCHIVE_COMMENT:raise ValueError('Package entry metadata is missing Neil Mitchell.')
            if expected is not None and archive.read(info)!=expected[name]:raise ValueError('Package bytes differ for '+name)
    return True

def main(argv=None):
    parser=argparse.ArgumentParser(description='Build the Lau Setup shared Windows/Linux ZIP.')
    parser.add_argument('--root',type=pathlib.Path,default=_repo_root());parser.add_argument('--output',type=pathlib.Path);parser.add_argument('--exe',type=pathlib.Path);parser.add_argument('--translations',type=pathlib.Path)
    args=parser.parse_args(argv);print(build_package(args.root,args.output,args.exe,args.translations))

if __name__=='__main__':main()

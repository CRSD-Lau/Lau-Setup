#!/usr/bin/env python3
"""Build and verify the three manual Patch-Y MPQ packages.

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell
"""

import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil
import tempfile
import urllib.parse
import urllib.request
import zipfile


AUTHOR = "Neil Mitchell"
META = {"Author": AUTHOR, "Creator": AUTHOR, "LastModifiedBy": AUTHOR}
COMMENT = b"Author: Neil Mitchell\nCreator: Neil Mitchell\nLast Modified By: Neil Mitchell\n"
SHA = re.compile(r"[0-9a-f]{64}\Z")
VERSION = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+\Z")
KNOWN_LOCALES = {"deDE", "enGB", "enUS", "esES", "esMX", "frFR", "itIT", "koKR", "ptBR", "ruRU", "zhCN", "zhTW"}
FALLBACKS = {"enGB": "enUS", "itIT": "enUS", "ptBR": "enUS"}
EDITIONS = (
    ("HD-New-Spells", ("Y-HD-NewSpells-On-Consecration-On", "SpellAssets", "SpellTables")),
    ("HD-Original-Spells", ("Y-HD-NewSpells-Off-Consecration-On",)),
    ("Non-HD", ("Y-Non-HD-Consecration-On",)),
)
MPQ_NAMES = {"SpellAssets": "patch-s.mpq", "SpellTables": "patch-LOCALE-S.MPQ"}
CHUNK = 1024 * 1024


def canonical_json(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def digest_file(path):
    size = 0
    digest = hashlib.sha256()
    with pathlib.Path(path).open("rb") as source:
        for chunk in iter(lambda: source.read(CHUNK), b""):
            size += len(chunk)
            digest.update(chunk)
    return size, digest.hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_record(record, label):
    require(isinstance(record, dict), label + " must be an object")
    require(type(record.get("Bytes")) is int and record["Bytes"] > 4, label + " has invalid Bytes")
    require(isinstance(record.get("Sha256"), str) and SHA.fullmatch(record["Sha256"]), label + " has invalid Sha256")


def load_catalog(path, expected_version=None):
    catalog = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    require(isinstance(catalog, dict), "catalog must be an object")
    version = catalog.get("Version")
    require(isinstance(version, str) and VERSION.fullmatch(version), "catalog has invalid Version")
    if expected_version is not None:
        require(version == expected_version, "catalog version does not match --version")
    require(catalog.get("PublicReady") is True, "catalog is not PublicReady")
    require(all(catalog.get(key) == value for key, value in META.items()), "catalog author metadata is invalid")
    payload_locales = catalog.get("Locales")
    client_locales = catalog.get("ClientLocales")
    locale_map = catalog.get("VisualAssetLocales")
    require(isinstance(payload_locales, list) and payload_locales and len(set(payload_locales)) == len(payload_locales)
            and set(payload_locales) <= KNOWN_LOCALES, "invalid catalog payload locales")
    require(isinstance(client_locales, list) and set(client_locales) == KNOWN_LOCALES
            and len(client_locales) == len(KNOWN_LOCALES), "catalog must list all 12 supported client locales")
    require(isinstance(locale_map, dict) and set(locale_map) == KNOWN_LOCALES, "invalid VisualAssetLocales")
    for locale in client_locales:
        require(locale_map[locale] == FALLBACKS.get(locale, locale) and locale_map[locale] in payload_locales,
                "invalid locale fallback for " + locale)
    assets = catalog.get("Assets")
    require(isinstance(assets, dict), "catalog Assets must be an object")
    for _, ids in EDITIONS:
        for asset_id in ids:
            record = assets.get(asset_id)
            check_record(record, asset_id)
            require(record.get("Id") == asset_id, "asset Id mismatch: " + asset_id)
            parts = record.get("Parts")
            require(isinstance(parts, list) and parts, "missing parts for " + asset_id)
            total = 0
            for part in parts:
                check_record(part, asset_id + " part")
                filename = part.get("FileName")
                require(filename == part["Sha256"] + ".bin", "unsafe part filename for " + asset_id)
                url = part.get("Url")
                parsed = urllib.parse.urlparse(url) if isinstance(url, str) else None
                require(parsed is not None and parsed.scheme == "https" and parsed.netloc == "github.com"
                        and parsed.params == parsed.query == parsed.fragment == ""
                        and re.fullmatch(r"/CRSD-Lau/Lau-Setup/releases/download/payload-[0-9]+\.[0-9]+\.[0-9]+/[0-9a-f]{64}\.bin", parsed.path)
                        and parsed.path.endswith("/" + filename), "untrusted part URL for " + asset_id)
                total += part["Bytes"]
            require(total == record["Bytes"], "part byte total mismatch for " + asset_id)
    return catalog


def file_matches(path, record):
    return pathlib.Path(path).is_file() and digest_file(path) == (record["Bytes"], record["Sha256"])


def readme(catalog, edition):
    version = catalog["Version"]
    new_spells = edition == "HD-New-Spells"
    hd = edition != "Non-HD"
    lines = [
        "Patch-Y " + version + " - " + edition + " manual MPQ package",
        "Author: Neil Mitchell", "Creator: Neil Mitchell", "Last Modified By: Neil Mitchell", "",
        "For an existing World of Warcraft 3.3.5a build 12340 client. This ZIP contains only Patch-Y visual MPQs.",
        "It does not contain a game executable, loading screens, maps, addons, or a complete client.",
        "Extract this ZIP outside the game directory. Close the client completely before changing MPQs.",
        "Find the active locale from SET locale in WTF/Config.wtf, then confirm",
        "Data/<locale>/locale-<locale>.mpq exists. A client may contain multiple locale folders:",
        "change only the active locale. If Config.wtf has no locale and several locale folders exist,",
        "launch the client once to select a language, close it, and check Config.wtf again.",
        "Use the exact active locale spelling in the filenames below. The manifest lists all 12 destinations.",
        "Back up the exact existing destination files to a folder OUTSIDE Data before replacing or removing them.",
        "If a known older Patch-Y Y was renamed and remains active, move only that identified copy",
        "to the backup before installing; never remove stock archives or unrelated patches.",
        "Keep the backup until you have tested in game. Do not copy files from a personal client.", "",
    ]
    if hd:
        lines.append("Requires the existing HD model F pair: Data/patch-f.mpq and Data/<locale>/patch-<locale>-F.MPQ. F is not included.")
    else:
        lines.append("This Non-HD edition does not require the HD model F pair.")
    lines += [
        "Copy patch-y.mpq into Data/patch-y.mpq. Copy the SAME patch-y.mpq again into",
        "Data/<locale>/patch-<locale>-Y.MPQ. Do not use a second language-specific Y archive.",
    ]
    if new_spells:
        lines += [
            "Copy patch-s.mpq into Data/patch-s.mpq. Rename a copy of patch-LOCALE-S.MPQ",
            "to patch-<locale>-S.MPQ and copy it into Data/<locale>/.",
        ]
    else:
        lines += [
            "To use original spells, move any existing Data/patch-s.mpq and",
            "Data/<locale>/patch-<locale>-S.MPQ to your backup OUTSIDE Data.",
            "These are the only S files this procedure addresses. Do not leave active old S files in Data.",
        ]
    lines += [
        "Start the client and use /pyversion to check that Lau reports Patch-Y " + version + ".",
        "That check identifies the installed version; it does not establish visual or gameplay acceptance.",
        "To undo: close the client; restore each exact file and original path from your backup;",
        "remove only files newly added by this manual installation.",
        "The enGB, itIT, and ptBR clients use English fallback visual assets; keep their actual locale names in destinations.",
        "", "Credits: Andre and the original Patch-Y contributors; Loriendal and Trimitor for the HD client foundation;",
        "Project Reforged contributors for HD artwork; Blizzard for the original game, artwork and localized text;",
        "Suppository and the source contributors credited in his patch for visual sources;",
        "Lau / Lausudo (Neil Mitchell) for the visual edits, integration, testing and release tooling.", "",
    ]
    return ("\n".join(lines)).encode("utf-8")


def package_manifest(catalog, edition, ids):
    version = catalog["Version"]
    files = []
    for asset_id in ids:
        record = catalog["Assets"][asset_id]
        name = "patch-y.mpq" if asset_id.startswith("Y-") else MPQ_NAMES[asset_id]
        destinations = []
        for locale in catalog["ClientLocales"]:
            if name == "patch-y.mpq":
                destinations.extend([{"Locale": locale, "Path": "Data/patch-y.mpq"},
                                     {"Locale": locale, "Path": f"Data/{locale}/patch-{locale}-Y.MPQ"}])
            elif name == "patch-s.mpq":
                destinations.append({"Locale": locale, "Path": "Data/patch-s.mpq"})
            else:
                destinations.append({"Locale": locale, "Path": f"Data/{locale}/patch-{locale}-S.MPQ"})
        files.append({"ArchiveName": name, "AssetId": asset_id, "Bytes": record["Bytes"],
                      "Sha256": record["Sha256"], "Destinations": destinations})
    return {**META, "Version": version, "Edition": edition, "ClientBuild": "3.3.5a.12340",
            "ClientLocales": catalog["ClientLocales"], "VisualAssetLocales": catalog["VisualAssetLocales"],
            "Files": files, "RequiresHDModelF": edition != "Non-HD",
            "RequiresSpellSPair": edition == "HD-New-Spells"}


def zip_info(name):
    info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.comment = COMMENT
    return info


def obtain_asset(record, payload_dir, cache_dir, scratch):
    # A local full asset may differ from its part name when the asset is split.
    if payload_dir is not None:
        full = pathlib.Path(payload_dir) / (record["Sha256"] + ".bin")
        if full.exists():
            require(file_matches(full, record), "corrupt local full asset: " + full.name)
            return full
    part_paths = []
    for part in record["Parts"]:
        name = part["FileName"]
        local = pathlib.Path(payload_dir) / name if payload_dir is not None else None
        cached = pathlib.Path(cache_dir) / name if cache_dir is not None else None
        if local is not None and local.exists():
            require(file_matches(local, part), "corrupt local part: " + name)
            chosen = local
        elif cached is not None and cached.exists():
            require(file_matches(cached, part), "corrupt cached part: " + name)
            chosen = cached
        elif payload_dir is not None:
            raise FileNotFoundError("missing local part: " + name)
        else:
            target_dir = pathlib.Path(cache_dir) if cache_dir is not None else scratch
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / name
            temporary = None
            try:
                with tempfile.NamedTemporaryFile(dir=target_dir, prefix=".download-", delete=False) as temp:
                    temporary = pathlib.Path(temp.name)
                    with urllib.request.urlopen(part["Url"], timeout=90) as response:
                        shutil.copyfileobj(response, temp, CHUNK)
                require(file_matches(temporary, part), "downloaded part hash or size mismatch: " + name)
                os.replace(temporary, target)
            finally:
                if temporary is not None:
                    temporary.unlink(missing_ok=True)
            chosen = target
        part_paths.append(chosen)
    if len(part_paths) == 1:
        require(file_matches(part_paths[0], record), "full asset hash or size mismatch: " + record["Sha256"])
        return part_paths[0]
    full = scratch / (record["Sha256"] + ".bin")
    with full.open("wb") as output:
        for part in part_paths:
            with part.open("rb") as source:
                shutil.copyfileobj(source, output, CHUNK)
    require(file_matches(full, record), "reassembled asset hash or size mismatch: " + record["Sha256"])
    return full


def write_package(path, catalog, edition, ids, sources):
    manifest = canonical_json(package_manifest(catalog, edition, ids))
    with zipfile.ZipFile(path, "w", allowZip64=True) as archive:
        archive.comment = COMMENT
        for asset_id in ids:
            name = "patch-y.mpq" if asset_id.startswith("Y-") else MPQ_NAMES[asset_id]
            with archive.open(zip_info(name), "w", force_zip64=True) as output, sources[asset_id].open("rb") as source:
                shutil.copyfileobj(source, output, CHUNK)
        archive.writestr(zip_info("README.txt"), readme(catalog, edition))
        archive.writestr(zip_info("package-manifest.json"), manifest)


def verify_package(path, catalog, edition, ids):
    manifest = package_manifest(catalog, edition, ids)
    wanted = ["patch-y.mpq" if key.startswith("Y-") else MPQ_NAMES[key] for key in ids]
    wanted += ["README.txt", "package-manifest.json"]
    with zipfile.ZipFile(path) as archive:
        require(archive.namelist() == wanted, "archive has missing or extra entries: " + str(path))
        require(archive.comment == COMMENT, "archive author metadata mismatch: " + str(path))
        for info in archive.infolist():
            require(info.comment == COMMENT and info.date_time == (1980, 1, 1, 0, 0, 0)
                    and info.compress_type == zipfile.ZIP_STORED and info.create_system == 3
                    and (info.external_attr >> 16) == 0o100644, "entry metadata mismatch: " + info.filename)
        for file in manifest["Files"]:
            size = 0
            digest = hashlib.sha256()
            with archive.open(file["ArchiveName"]) as source:
                first = source.read(4)
                require(first == b"MPQ\x1a", "MPQ signature missing: " + file["ArchiveName"])
                size += len(first)
                digest.update(first)
                for chunk in iter(lambda: source.read(CHUNK), b""):
                    size += len(chunk)
                    digest.update(chunk)
            require((size, digest.hexdigest()) == (file["Bytes"], file["Sha256"]),
                    "MPQ hash or size mismatch: " + file["ArchiveName"])
        require(archive.read("README.txt") == readme(catalog, edition), "README mismatch")
        require(archive.read("package-manifest.json") == canonical_json(manifest), "package manifest mismatch")
    return True


def package_filename(version, edition):
    return f"Patch-Y-{version}-{edition}.zip"


def release_index(catalog, rows):
    version = catalog["Version"]
    return {**META, "Version": version, "ClientBuild": "3.3.5a.12340",
            "Packages": [{"Edition": edition, "FileName": name, "Bytes": size, "Sha256": digest,
                          "Url": f"https://github.com/CRSD-Lau/Lau-Setup/releases/download/payload-{version}/{name}"}
                         for edition, name, size, digest in rows]}


def sha_sums(rows):
    return ("# Author: Neil Mitchell\n# Creator: Neil Mitchell\n# Last Modified By: Neil Mitchell\n"
            + "".join(f"{digest}  {name}\n" for _, name, _, digest in rows)).encode("utf-8")


def verify_output(catalog_path, output, version=None):
    catalog = load_catalog(catalog_path, version)
    output = pathlib.Path(output)
    wanted = {package_filename(catalog["Version"], edition) for edition, _ in EDITIONS}
    wanted.update(("manual-downloads.json", "SHA256SUMS-Patch-Y.txt"))
    require(output.is_dir() and {item.name for item in output.iterdir()} == wanted,
            "output must contain exactly the five release artifacts")
    index_path = output / "manual-downloads.json"
    require(index_path.is_file(), "manual-downloads.json is missing")
    index = json.loads(index_path.read_text(encoding="utf-8"))
    rows = []
    for edition, ids in EDITIONS:
        name = package_filename(catalog["Version"], edition)
        archive_path = output / name
        require(archive_path.is_file(), "package is missing: " + name)
        verify_package(archive_path, catalog, edition, ids)
        size, digest = digest_file(archive_path)
        rows.append((edition, name, size, digest))
    require(index == release_index(catalog, rows), "manual-downloads.json does not match packages or catalog")
    require((output / "SHA256SUMS-Patch-Y.txt").read_bytes() == sha_sums(rows), "SHA256SUMS-Patch-Y.txt mismatch")
    return rows


def build(catalog_path, output, cache=None, payload_dir=None, version=None):
    catalog = load_catalog(catalog_path, version)
    output = pathlib.Path(output)
    output.mkdir(parents=True, exist_ok=True)
    cache = pathlib.Path(cache) if cache is not None else None
    payload_dir = pathlib.Path(payload_dir) if payload_dir is not None else None
    if payload_dir is not None:
        require(payload_dir.is_dir(), "--payload-dir must be an existing directory")
    wanted = [package_filename(catalog["Version"], edition) for edition, _ in EDITIONS]
    wanted += ["manual-downloads.json", "SHA256SUMS-Patch-Y.txt"]
    if cache is not None:
        require(cache.resolve() != output.resolve() and output.resolve() not in cache.resolve().parents,
                "--cache must be outside --output")
    require({item.name for item in output.iterdir()} <= set(wanted),
            "output contains unrelated files; use a fresh output directory")
    existing = [output / name for name in wanted if (output / name).exists()]
    if existing:
        # Existing release artifacts are immutable. An identical rerun is safe.
        require(len(existing) == len(wanted), "output contains a partial release; use a fresh output directory")
        return verify_output(catalog_path, output, version)
    with tempfile.TemporaryDirectory(prefix="patch-y-manual-", dir=output) as temporary:
        scratch = pathlib.Path(temporary)
        sources = {}
        for _, ids in EDITIONS:
            for asset_id in ids:
                if asset_id not in sources:
                    sources[asset_id] = obtain_asset(catalog["Assets"][asset_id], payload_dir, cache, scratch)
        rows = []
        for edition, ids in EDITIONS:
            name = package_filename(catalog["Version"], edition)
            path = scratch / name
            write_package(path, catalog, edition, ids, sources)
            verify_package(path, catalog, edition, ids)
            size, digest = digest_file(path)
            rows.append((edition, name, size, digest))
        (scratch / "manual-downloads.json").write_bytes(canonical_json(release_index(catalog, rows)))
        (scratch / "SHA256SUMS-Patch-Y.txt").write_bytes(sha_sums(rows))
        for name in wanted:
            require(not (output / name).exists(), "output file appeared during build: " + name)
        for name in wanted:
            os.replace(scratch / name, output / name)
    verify_output(catalog_path, output, version)
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("build", "verify"))
    parser.add_argument("--catalog", type=pathlib.Path, default=pathlib.Path("build/catalog.json"))
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--cache", type=pathlib.Path)
    parser.add_argument("--payload-dir", type=pathlib.Path)
    parser.add_argument("--version")
    args = parser.parse_args(argv)
    rows = build(args.catalog, args.output, args.cache, args.payload_dir, args.version) if args.action == "build" else verify_output(args.catalog, args.output, args.version)
    for _, name, size, digest in rows:
        print(f"{digest}  {size}  {name}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Resolve a public-ready manual Patch-Y catalog without changing released tags.

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell
"""

import argparse
import base64
import binascii
import json
import os
import pathlib
import re
import subprocess
import tempfile

from package_patch_y_manual import EDITIONS, load_catalog


REPO = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
VERSION = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+\Z")
TAG = re.compile(r"(?:payload-|v)([0-9]+\.[0-9]+\.[0-9]+)\Z")
ASSET_IDS = tuple(dict.fromkeys(asset_id for _, ids in EDITIONS for asset_id in ids))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def gh_json(*args):
    result = subprocess.run(["gh", *args], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def published_release(repo, tag):
    result = gh_json("release", "view", tag, "--repo", repo, "--json", "tagName,isDraft")
    require(isinstance(result, dict) and result.get("tagName") == tag and result.get("isDraft") is False,
            "release is missing, draft, or mismatched: " + tag)


def tag_catalog(repo, tag):
    response = gh_json("api", f"repos/{repo}/contents/build/catalog.json?ref={tag}")
    require(isinstance(response, dict) and response.get("encoding") == "base64"
            and isinstance(response.get("content"), str), "tag catalog response is invalid: " + tag)
    try:
        raw = base64.b64decode(response["content"], validate=False)
        catalog = json.loads(raw.decode("utf-8"))
    except (binascii.Error, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("tag catalog is not valid UTF-8 JSON: " + tag) from error
    require(isinstance(catalog, dict), "tag catalog must be an object: " + tag)
    return raw, catalog


def asset_signature(catalog, asset_id):
    assets = catalog.get("Assets")
    require(isinstance(assets, dict) and isinstance(assets.get(asset_id), dict), "missing asset: " + asset_id)
    asset = assets[asset_id]
    parts = asset.get("Parts")
    require(isinstance(parts, list) and parts, "missing asset parts: " + asset_id)
    require(all(isinstance(part, dict) for part in parts), "invalid asset parts: " + asset_id)
    return (asset.get("Bytes"), asset.get("Sha256"),
            tuple((part.get("Bytes"), part.get("Sha256"), part.get("FileName")) for part in parts))


def matching_payload(source, ready):
    for field in ("Version", "Locales", "ClientLocales", "VisualAssetLocales"):
        require(source.get(field) == ready.get(field), "payload and installer catalogs differ: " + field)
    for asset_id in ASSET_IDS:
        require(asset_signature(source, asset_id) == asset_signature(ready, asset_id),
                "payload and installer catalogs differ: " + asset_id)


def ready_catalog(raw):
    with tempfile.TemporaryDirectory(prefix="manual-catalog-check-") as directory:
        path = pathlib.Path(directory) / "catalog.json"
        path.write_bytes(raw)
        return load_catalog(path)


def resolve(repo, release_tag, output, github_env=None):
    require(isinstance(repo, str) and REPO.fullmatch(repo), "invalid --repo")
    require(isinstance(release_tag, str) and TAG.fullmatch(release_tag), "invalid --release-tag")
    published_release(repo, release_tag)
    raw, source = tag_catalog(repo, release_tag)
    game_version = source.get("Version")
    require(isinstance(game_version, str) and VERSION.fullmatch(game_version), "tag catalog has invalid game Version")
    if release_tag.startswith("payload-"):
        require(game_version == release_tag.removeprefix("payload-"), "payload tag and catalog game Version differ")
        game_tag = release_tag
        if source.get("PublicReady") is True:
            ready = ready_catalog(raw)
            catalog_ref = release_tag
        else:
            installer_version = source.get("InstallerVersion")
            require(isinstance(installer_version, str) and VERSION.fullmatch(installer_version),
                    "payload catalog has invalid InstallerVersion")
            installer_tag = "v" + installer_version
            published_release(repo, installer_tag)
            candidate_raw, candidate = tag_catalog(repo, installer_tag)
            require(candidate.get("InstallerVersion") == installer_version,
                    "installer tag and catalog InstallerVersion differ")
            ready = ready_catalog(candidate_raw)
            matching_payload(source, ready)
            raw = candidate_raw
            catalog_ref = installer_tag
    else:
        require(source.get("InstallerVersion") == release_tag.removeprefix("v"),
                "installer tag and catalog InstallerVersion differ")
        ready = ready_catalog(raw)
        game_tag = "payload-" + game_version
        published_release(repo, game_tag)
        _, payload = tag_catalog(repo, game_tag)
        matching_payload(payload, ready)
        catalog_ref = release_tag
    require(ready["Version"] == game_version, "resolved catalog game Version mismatch")
    output = pathlib.Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        require(output.is_file() and output.read_bytes() == raw,
                "existing output differs from resolved catalog: " + str(output))
    else:
        with tempfile.NamedTemporaryFile(dir=output.parent, prefix=".manual-catalog-", delete=False) as temp:
            temporary = pathlib.Path(temp.name)
            temp.write(raw)
        try:
            os.replace(temporary, output)
        finally:
            temporary.unlink(missing_ok=True)
    if github_env is not None:
        with pathlib.Path(github_env).open("a", encoding="utf-8", newline="\n") as env:
            env.write(f"RELEASE_GAME_TAG={game_tag}\nRELEASE_GAME_VERSION={game_version}\n")
    return {"game_tag": game_tag, "version": game_version, "catalog_ref": catalog_ref}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="CRSD-Lau/Lau-Setup")
    parser.add_argument("--release-tag", required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--github-env", type=pathlib.Path)
    args = parser.parse_args(argv)
    print(json.dumps(resolve(args.repo, args.release_tag, args.output, args.github_env), sort_keys=True))


if __name__ == "__main__":
    main()

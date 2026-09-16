#!/usr/bin/env python3
"""Generate the public Patch-Y member manifest from retained release proof.

This maintainer tool does not extract or redistribute member bytes.
Author / Creator / Last Modified By: Neil Mitchell
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proof", required=True, type=Path)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    proof = json.loads(args.proof.read_text(encoding="utf-8-sig"))
    editions = {}
    for row in sorted(proof["archives"], key=lambda item: item["id"]):
        edition = row["id"]
        members = {
            member["name"]: {"bytes": member["bytes"], "sha256": member["sha256"]}
            for _, member in sorted(row["members"].items(), key=lambda item: item[1]["name"].casefold())
        }
        editions[edition] = {
            "archiveName": edition + ".mpq",
            "bytes": row["after_bytes"],
            "sha256": row["after_sha256"],
            "memberCount": len(members),
            "clientFamily": "Non-HD" if "Non-HD" in edition else "HD",
            "newSpells": "On" if "NewSpells-On" in edition else ("Off" if "NewSpells-Off" in edition else "NotApplicable"),
            "consecration": "On" if edition.endswith("Consecration-On") else "Off",
            "members": members,
        }
    output = {
        "schemaVersion": 1,
        "Author": "Neil Mitchell",
        "Creator": "Neil Mitchell",
        "LastModifiedBy": "Neil Mitchell",
        "gameVersion": "3.0.9",
        "archive": {
            "fileName": args.archive.name,
            "url": "https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.4.0/Lau-Patch-Y-3.0.9-All-Editions.zip",
            "bytes": args.archive.stat().st_size,
            "sha256": sha256(args.archive),
        },
        "editions": editions,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8", newline="\n"
    )


if __name__ == "__main__":
    main()

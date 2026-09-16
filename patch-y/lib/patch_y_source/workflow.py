"""Fetch, inspect, build, verify, and diff the public Patch-Y baseline.

Author / Creator / Last Modified By: Neil Mitchell
"""

from __future__ import annotations

import json
import re
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

from .core import Operation, OverlayError, declared_change_set, load_baseline, load_operations, sha256_bytes, sha256_file
from .blp import recolor_dxt1_endpoints
from .dbc import apply_edits
from .models import replace_texture_reference, rewrite_bounds, scale_xy_vertices
from .mpq import Storm

TOC_MEMBER = "Interface\\AddOns\\!PYAndre\\!PYAndre.toc"
DEV_LABEL_RE = re.compile(r"[a-z0-9][a-z0-9._-]{0,31}")
OUTPUT_MARKER = ".patch-y-generated.json"


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def fetch_baseline(baseline_path: Path, cache: Path, *, source: Path | None = None) -> Path:
    baseline = load_baseline(baseline_path)
    archive_row = baseline["archive"]
    target = cache / archive_row["fileName"]
    cache.mkdir(parents=True, exist_ok=True)
    if not target.exists() or sha256_file(target) != archive_row["sha256"]:
        partial = target.with_suffix(target.suffix + ".partial")
        if partial.exists():
            partial.unlink()
        if source:
            if sha256_file(source) != archive_row["sha256"]:
                raise OverlayError("Supplied baseline ZIP hash does not match baseline.json")
            shutil.copyfile(source, partial)
        else:
            request = urllib.request.Request(archive_row["url"], headers={"User-Agent": "Lau-Setup-Patch-Y-Source/1"})
            with urllib.request.urlopen(request, timeout=120) as response, partial.open("wb") as output:
                shutil.copyfileobj(response, output)
        if sha256_file(partial) != archive_row["sha256"]:
            partial.unlink(missing_ok=True)
            raise OverlayError("Downloaded baseline ZIP failed SHA-256 verification")
        partial.replace(target)
    extracted = cache / "baseline"
    complete = extracted / ".complete.json"
    expected_complete = {edition: row["sha256"] for edition, row in baseline["editions"].items()}
    try:
        cache_complete = json.loads(complete.read_text(encoding="utf-8")) if complete.exists() else None
    except (OSError, json.JSONDecodeError):
        cache_complete = None
    if cache_complete != expected_complete:
        staging = cache / "baseline.staging"
        if staging.exists():
            shutil.rmtree(staging)
        staging.mkdir()
        with zipfile.ZipFile(target) as archive:
            names = set(archive.namelist())
            expected_names = {row["archiveName"] for row in baseline["editions"].values()}
            if not expected_names.issubset(names):
                raise OverlayError("Baseline ZIP is missing one or more edition MPQs")
            for edition, row in baseline["editions"].items():
                data = archive.read(row["archiveName"])
                if len(data) != row["bytes"] or sha256_bytes(data) != row["sha256"]:
                    raise OverlayError(f"Baseline edition failed verification: {edition}")
                (staging / row["archiveName"]).write_bytes(data)
        _write_json(staging / ".complete.json", expected_complete)
        if extracted.exists():
            shutil.rmtree(extracted)
        staging.replace(extracted)
    return extracted


def verify_baseline_members(baseline_path: Path, baseline_dir: Path, storm: Storm) -> dict[str, Any]:
    baseline = load_baseline(baseline_path)
    results = []
    for edition, expected in baseline["editions"].items():
        archive = baseline_dir / expected["archiveName"]
        if sha256_file(archive) != expected["sha256"] or archive.stat().st_size != expected["bytes"]:
            raise OverlayError(f"Baseline archive does not match manifest: {edition}")
        actual = storm.inventory(archive)
        expected_members = {name.casefold(): {"name": name, **row} for name, row in expected["members"].items()}
        if set(actual) != set(expected_members):
            raise OverlayError(f"Baseline member set does not match manifest: {edition}")
        for key, row in actual.items():
            expected_row = expected_members[key]
            if row["bytes"] != expected_row["bytes"] or row["sha256"] != expected_row["sha256"]:
                raise OverlayError(f"Baseline member mismatch in {edition}: {row['name']}")
        results.append({"edition": edition, "archiveSha256": expected["sha256"], "memberCount": len(actual), "status": "PASS"})
    return {"Author": "Neil Mitchell", "Creator": "Neil Mitchell", "LastModifiedBy": "Neil Mitchell", "baseline": baseline["gameVersion"], "results": results}


def _development_toc(content: bytes, label: str) -> bytes:
    text = content.decode("utf-8-sig")
    replacement = f"3.0.9-dev+{label}"
    changed, count = re.subn(r"3\.0\.9(?: Lau)?", replacement, text)
    if count < 2:
        raise OverlayError("Unexpected !PYAndre TOC version layout")
    return changed.encode("utf-8")


def _prepare_operations(
    edition: str,
    operations: list[Operation],
    before: dict[str, dict[str, object]],
    work: Path,
) -> tuple[dict[str, Path], set[str]]:
    replacements: dict[str, Path] = {}
    deletions: set[str] = set()
    for index, operation in enumerate(operations):
        key = operation.member.casefold()
        existing = before.get(key)
        if operation.action == "add":
            if existing:
                raise OverlayError(f"Add operation targets an existing member in {edition}: {operation.member}")
        else:
            if not existing or existing["sha256"] != operation.expected_before_sha256:
                raise OverlayError(f"Operation precondition failed in {edition}: {operation.member}")
        if operation.action == "delete":
            deletions.add(operation.member)
        elif operation.action in {"add", "replace"}:
            replacements[operation.member] = operation.source
        elif operation.action == "dbc":
            output = work / f"dbc-{index}.dbc"
            output.write_bytes(apply_edits(existing["content"], operation.payload["edits"]))
            replacements[operation.member] = output
        elif operation.action == "transform":
            recipe = operation.payload["recipe"]
            kind = recipe["kind"]
            content = existing["content"]
            if kind == "scale_xy_vertices":
                transformed = scale_xy_vertices(
                    content,
                    offset=recipe["offset"],
                    count=recipe["count"],
                    stride=recipe["stride"],
                    factor=recipe["factor"],
                )
            elif kind == "rewrite_bounds":
                transformed = rewrite_bounds(
                    content,
                    offset=recipe["offset"],
                    minimum=tuple(recipe["minimum"]),
                    maximum=tuple(recipe["maximum"]),
                    radius=recipe["radius"],
                )
            elif kind == "replace_texture_reference":
                transformed = replace_texture_reference(
                    content,
                    old=recipe["old"],
                    new=recipe["new"],
                    expected_occurrences=recipe["expectedOccurrences"],
                )
            elif kind == "recolor_dxt1_endpoints":
                transformed = recolor_dxt1_endpoints(
                    content, red=recipe["red"], green=recipe["green"], blue=recipe["blue"]
                )
            else:  # Manifest validation makes this unreachable.
                raise OverlayError(f"Unsupported transform recipe: {kind}")
            output = work / f"transform-{index}{Path(operation.member).suffix.lower()}"
            output.write_bytes(transformed)
            replacements[operation.member] = output
    return replacements, deletions


def build_candidates(
    source_root: Path,
    baseline_path: Path,
    baseline_dir: Path,
    output: Path,
    storm: Storm,
    label: str,
    server: str,
) -> dict[str, Any]:
    if not DEV_LABEL_RE.fullmatch(label):
        raise OverlayError("Development label must be 1-32 lowercase letters, numbers, dots, underscores, or hyphens")
    baseline = load_baseline(baseline_path)
    operations = load_operations(source_root, baseline["editions"], server)
    if output.exists():
        marker = output / OUTPUT_MARKER
        try:
            marker_data = json.loads(marker.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise OverlayError(f"Refusing to replace unmarked candidate output: {output}") from exc
        if marker_data != {"kind": "patch-y-candidate", "server": server}:
            raise OverlayError(f"Candidate output marker does not match --server: {output}")
        shutil.rmtree(output)
    output.mkdir(parents=True)
    _write_json(output / OUTPUT_MARKER, {"kind": "patch-y-candidate", "server": server})
    reports = []
    for edition, row in baseline["editions"].items():
        source = baseline_dir / row["archiveName"]
        target = output / row["archiveName"]
        shutil.copy2(source, target)
        before = storm.inventory(source, include_bytes=True)
        with tempfile.TemporaryDirectory(prefix="patch-y-") as temporary:
            work = Path(temporary)
            replacements, deletions = _prepare_operations(edition, operations[edition], before, work)
            toc_key = TOC_MEMBER.casefold()
            toc = work / "!PYAndre.toc"
            toc.write_bytes(_development_toc(before[toc_key]["content"], f"{server}-{label}"))
            replacements[TOC_MEMBER] = toc
            storm.mutate(target, replacements, deletions)
            storm.compact(target)
        after = storm.inventory(target)
        before_public = {key: {k: v for k, v in value.items() if k != "content"} for key, value in before.items()}
        allowed = declared_change_set(operations[edition]) | {toc_key, "(attributes)", "(listfile)"}
        changed = sorted(
            {key for key in set(before_public) | set(after) if before_public.get(key) != after.get(key)},
            key=str.casefold,
        )
        undeclared = [key for key in changed if key not in allowed]
        if undeclared:
            raise OverlayError(f"Build changed undeclared members in {edition}: {', '.join(undeclared)}")
        reports.append(
            {
                "edition": edition,
                "baselineSha256": row["sha256"],
                "candidateSha256": sha256_file(target),
                "candidateBytes": target.stat().st_size,
                "declaredChanges": sorted(declared_change_set(operations[edition])),
                "changedMembers": changed,
                "memberCountBefore": len(before_public),
                "memberCountAfter": len(after),
                "status": "PASS",
            }
        )
    report = {
        "Author": "Neil Mitchell",
        "Creator": "Neil Mitchell",
        "LastModifiedBy": "Neil Mitchell",
        "baseline": baseline["gameVersion"],
        "server": server,
        "developmentLabel": label,
        "archives": reports,
        "inGameValidation": "NOT_PERFORMED",
    }
    _write_json(output / "scope-report.json", report)
    return report


def verify_candidates(
    baseline_path: Path,
    baseline_dir: Path,
    output: Path,
    source_root: Path,
    storm: Storm,
    server: str,
) -> dict[str, Any]:
    baseline = load_baseline(baseline_path)
    operations = load_operations(source_root, baseline["editions"], server)
    results = []
    for edition, row in baseline["editions"].items():
        before = storm.inventory(baseline_dir / row["archiveName"])
        after = storm.inventory(output / row["archiveName"])
        allowed = declared_change_set(operations[edition]) | {TOC_MEMBER.casefold(), "(attributes)", "(listfile)"}
        changed = {key for key in set(before) | set(after) if before.get(key) != after.get(key)}
        undeclared = sorted(changed - allowed)
        missing = sorted(declared_change_set(operations[edition]) - changed)
        if undeclared or missing:
            raise OverlayError(f"Candidate scope mismatch for {edition}; undeclared={undeclared}, unchanged declarations={missing}")
        results.append({"edition": edition, "changedMembers": sorted(changed), "status": "PASS"})
    return {"Author": "Neil Mitchell", "Creator": "Neil Mitchell", "LastModifiedBy": "Neil Mitchell", "server": server, "results": results}


def render_diff(report: dict[str, Any], markdown_path: Path, json_path: Path) -> None:
    _write_json(json_path, report)
    lines = [
        "# Patch-Y candidate scope report",
        "",
        "<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->",
        "",
        f"Baseline: **{report['baseline']}**  ",
        f"Server profile: **{report['server']}**  ",
        f"Development label: **{report['developmentLabel']}**  ",
        f"In-game validation: **{report['inGameValidation']}**",
        "",
        "| Edition | Declared source changes | Changed archive members | Result |",
        "| --- | ---: | ---: | --- |",
    ]
    for row in report["archives"]:
        lines.append(f"| {row['edition']} | {len(row['declaredChanges'])} | {len(row['changedMembers'])} | {row['status']} |")
    lines.extend(["", "Static archive validation does not replace in-game encounter testing.", ""])
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text("\n".join(lines), encoding="utf-8")

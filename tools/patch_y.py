#!/usr/bin/env python3
"""Public Patch-Y contributor CLI.

Author / Creator / Last Modified By: Neil Mitchell
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "patch-y"
sys.path.insert(0, str(SOURCE_ROOT / "lib"))

from patch_y_source.core import OverlayError, load_baseline  # noqa: E402
from patch_y_source.mpq import Storm  # noqa: E402
from patch_y_source.workflow import (  # noqa: E402
    build_candidates,
    fetch_baseline,
    render_diff,
    verify_baseline_members,
    verify_candidates,
)


def paths(args: argparse.Namespace) -> tuple[Path, Path, Path]:
    baseline = Path(args.baseline).resolve()
    cache = Path(args.cache).resolve()
    baseline_dir = fetch_baseline(baseline, cache, source=Path(args.source).resolve() if args.source else None)
    return baseline, cache, baseline_dir


def emit(value: object) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect and build hash-pinned Lau Patch-Y candidates")
    parser.add_argument("--baseline", default=SOURCE_ROOT / "baseline.json", type=Path)
    parser.add_argument("--cache", default=SOURCE_ROOT / ".cache", type=Path)
    parser.add_argument("--source", type=Path, help="Optional local copy of the pinned baseline ZIP")
    parser.add_argument("--stormlib", help="StormLib library path; otherwise use STORMLIB_DLL/STORMLIB_LIBRARY")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("fetch", help="Download and verify the pinned six-edition baseline")

    inspect = commands.add_parser("inspect", help="Extract one verified edition into an ignored working directory")
    inspect.add_argument("edition")
    inspect.add_argument("--output", type=Path)

    verify_baseline = commands.add_parser("verify-baseline", help="Verify every baseline MPQ member against baseline.json")
    verify_baseline.add_argument("--report", type=Path)

    build = commands.add_parser("build", help="Build all six candidate editions from source overlays")
    build.add_argument("--server", required=True, help="Registered target from patch-y/servers.json")
    build.add_argument("--label", required=True)
    build.add_argument("--output", type=Path)

    verify = commands.add_parser("verify", help="Verify candidate member scope against declared overlays")
    verify.add_argument("--server", required=True, help="Registered target from patch-y/servers.json")
    verify.add_argument("--output", type=Path)

    diff = commands.add_parser("diff", help="Write compact Markdown and JSON proof from a verified build")
    diff.add_argument("--server", required=True, help="Registered target from patch-y/servers.json")
    diff.add_argument("--output", type=Path)
    diff.add_argument("--markdown", type=Path)
    diff.add_argument("--json", type=Path)

    args = parser.parse_args()
    try:
        baseline_path, cache, baseline_dir = paths(args)
        baseline = load_baseline(baseline_path)
        if args.command == "fetch":
            emit({"status": "PASS", "baseline": baseline["gameVersion"], "cache": str(baseline_dir)})
            return 0
        storm = Storm(args.stormlib)
        if args.command == "inspect":
            if args.edition not in baseline["editions"]:
                raise OverlayError(f"Unknown edition: {args.edition}")
            output = (args.output or SOURCE_ROOT / ".work" / "inspect" / args.edition).resolve()
            storm.extract(baseline_dir / baseline["editions"][args.edition]["archiveName"], output)
            emit({"status": "PASS", "edition": args.edition, "output": str(output)})
        elif args.command == "verify-baseline":
            report = verify_baseline_members(baseline_path, baseline_dir, storm)
            if args.report:
                report_path = args.report.resolve()
                report_path.parent.mkdir(parents=True, exist_ok=True)
                report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            emit(report)
        elif args.command == "build":
            output = (args.output or SOURCE_ROOT / ".work" / "candidate" / args.server).resolve()
            emit(build_candidates(SOURCE_ROOT, baseline_path, baseline_dir, output, storm, args.label, args.server))
        elif args.command == "verify":
            output = (args.output or SOURCE_ROOT / ".work" / "candidate" / args.server).resolve()
            emit(verify_candidates(baseline_path, baseline_dir, output, SOURCE_ROOT, storm, args.server))
        elif args.command == "diff":
            output = (args.output or SOURCE_ROOT / ".work" / "candidate" / args.server).resolve()
            markdown = (args.markdown or SOURCE_ROOT / ".work" / f"patch-y-diff-{args.server}.md").resolve()
            json_output = (args.json or SOURCE_ROOT / ".work" / f"patch-y-diff-{args.server}.json").resolve()
            report_path = output / "scope-report.json"
            if not report_path.is_file():
                raise OverlayError("Run build before diff; scope-report.json is missing")
            report = json.loads(report_path.read_text(encoding="utf-8"))
            if report.get("server") != args.server:
                raise OverlayError("Candidate report server does not match --server")
            verify_candidates(baseline_path, baseline_dir, output, SOURCE_ROOT, storm, args.server)
            render_diff(report, markdown, json_output)
            emit({"status": "PASS", "server": args.server, "markdown": str(markdown), "json": str(json_output)})
        return 0
    except (OverlayError, OSError, RuntimeError, ValueError, zipfile.BadZipFile) as exc:  # type: ignore[name-defined]
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

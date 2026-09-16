"""Manifest and overlay validation for the Patch-Y contributor workflow.

Author / Creator / Last Modified By: Neil Mitchell
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from typing import Any, Iterable

SCHEMA_VERSION = 1
SHA256_RE = re.compile(r"[0-9a-f]{64}")
EDITION_RE = re.compile(r"Y-(?:HD-NewSpells-(?:On|Off)|Non-HD)-Consecration-(?:On|Off)")
ALLOWED_ACTIONS = {"add", "replace", "delete", "dbc", "transform"}
ALLOWED_EXTENSIONS = {".m2", ".mdx", ".skin", ".blp", ".dbc", ".lua", ".toc", ".txt"}
INTERNAL_MEMBERS = {"(attributes)", "(listfile)"}


class OverlayError(ValueError):
    """Raised when public source input is ambiguous or unsafe."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def normalize_member_path(value: str, *, allow_internal: bool = False) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise OverlayError("MPQ member path must be a non-empty string without NUL bytes")
    candidate = value.replace("/", "\\")
    if candidate in INTERNAL_MEMBERS:
        if allow_internal:
            return candidate
        raise OverlayError(f"Internal MPQ member cannot be edited: {candidate}")
    path = PureWindowsPath(candidate)
    if path.is_absolute() or path.drive or any(part in {"", ".", ".."} for part in path.parts):
        raise OverlayError(f"Unsafe MPQ member path: {value}")
    normalized = "\\".join(path.parts)
    try:
        normalized.encode("ascii")
    except UnicodeEncodeError as exc:
        raise OverlayError(f"MPQ member paths must be ASCII: {value}") from exc
    if len(normalized) > 240:
        raise OverlayError(f"MPQ member path is too long: {value}")
    if Path(normalized).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise OverlayError(f"Unsupported Patch-Y member type: {value}")
    return normalized


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise OverlayError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise OverlayError(f"JSON root must be an object: {path}")
    return value


def load_baseline(path: Path) -> dict[str, Any]:
    data = _read_json(path)
    if data.get("schemaVersion") != SCHEMA_VERSION:
        raise OverlayError("Unsupported baseline schemaVersion")
    archive = data.get("archive")
    editions = data.get("editions")
    if not isinstance(archive, dict) or not SHA256_RE.fullmatch(str(archive.get("sha256", ""))):
        raise OverlayError("Baseline archive requires a lowercase SHA-256")
    if not isinstance(editions, dict) or len(editions) != 6:
        raise OverlayError("Baseline must describe exactly six Patch-Y editions")
    seen_archive_names: set[str] = set()
    for edition, row in editions.items():
        if not EDITION_RE.fullmatch(edition) or not isinstance(row, dict):
            raise OverlayError(f"Invalid edition: {edition}")
        if row.get("archiveName") != edition + ".mpq":
            raise OverlayError(f"Edition archiveName mismatch: {edition}")
        if not SHA256_RE.fullmatch(str(row.get("sha256", ""))) or not isinstance(row.get("bytes"), int):
            raise OverlayError(f"Edition hash/size is invalid: {edition}")
        members = row.get("members")
        if not isinstance(members, dict) or len(members) != row.get("memberCount"):
            raise OverlayError(f"Edition member count mismatch: {edition}")
        folded: set[str] = set()
        for member, metadata in members.items():
            normalized = normalize_member_path(member, allow_internal=True)
            key = normalized.casefold()
            if key in folded:
                raise OverlayError(f"Case-colliding baseline member in {edition}: {member}")
            folded.add(key)
            if not isinstance(metadata, dict) or not SHA256_RE.fullmatch(str(metadata.get("sha256", ""))):
                raise OverlayError(f"Invalid member metadata in {edition}: {member}")
            if not isinstance(metadata.get("bytes"), int) or metadata["bytes"] < 0:
                raise OverlayError(f"Invalid member size in {edition}: {member}")
        archive_key = row["archiveName"].casefold()
        if archive_key in seen_archive_names:
            raise OverlayError(f"Duplicate baseline archive name: {row['archiveName']}")
        seen_archive_names.add(archive_key)
    return data


@dataclass(frozen=True)
class Operation:
    overlay: str
    edition: str
    action: str
    member: str
    source: Path | None
    expected_before_sha256: str | None
    servers: tuple[str, ...]
    payload: dict[str, Any]


def _validate_hash(value: Any, label: str, *, optional: bool = False) -> str | None:
    if value is None and optional:
        return None
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        raise OverlayError(f"{label} must be a lowercase SHA-256")
    return value


def load_servers(path: Path) -> dict[str, dict[str, Any]]:
    data = _read_json(path)
    profiles = data.get("profiles")
    if data.get("schemaVersion") != SCHEMA_VERSION or not isinstance(profiles, dict) or not profiles:
        raise OverlayError("servers.json must contain at least one server profile")
    for server, profile in profiles.items():
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,31}", server) or not isinstance(profile, dict):
            raise OverlayError(f"Invalid server profile ID: {server}")
        if not str(profile.get("displayName", "")).strip() or not str(profile.get("databaseNotes", "")).strip():
            raise OverlayError(f"Server profile needs displayName and databaseNotes: {server}")
        realms = profile.get("knownRealmNames")
        if not isinstance(realms, list) or not realms or any(not isinstance(realm, str) or not realm.strip() for realm in realms):
            raise OverlayError(f"Server profile needs one or more exact knownRealmNames: {server}")
        if not str(profile.get("serverListEvidence", "")).startswith("https://"):
            raise OverlayError(f"Server profile needs HTTPS naming evidence: {server}")
    return profiles


def _validate_operation(
    raw: Any,
    manifest_path: Path,
    overlay: str,
    edition: str,
    allowed_servers: set[str],
) -> Operation:
    if not isinstance(raw, dict):
        raise OverlayError(f"Operation must be an object: {manifest_path}")
    action = raw.get("action")
    if action not in ALLOWED_ACTIONS:
        raise OverlayError(f"Unsupported action in {manifest_path}: {action}")
    member = normalize_member_path(raw.get("member", ""))
    if not str(raw.get("reason", "")).strip():
        raise OverlayError(f"Operation requires a reason: {member}")
    servers = raw.get("servers")
    if not isinstance(servers, list) or not servers or any(server not in allowed_servers for server in servers):
        raise OverlayError(f"Operation must name one or more registered servers: {member}")
    if len(servers) != len(set(servers)):
        raise OverlayError(f"Operation repeats a server profile: {member}")
    expected = _validate_hash(raw.get("expectedBeforeSha256"), "expectedBeforeSha256", optional=action == "add")
    if action in {"add", "replace"} and Path(member).suffix.lower() == ".dbc":
        raise OverlayError("Opaque DBC add/replace operations are not allowed; use structured dbc edits")
    source = None
    if action in {"add", "replace"}:
        relative = raw.get("source")
        if not isinstance(relative, str) or not relative:
            raise OverlayError(f"{action} operation requires source: {member}")
        source = (manifest_path.parent / relative).resolve()
        if not source.is_relative_to(manifest_path.parent.resolve()) or not source.is_file():
            raise OverlayError(f"Overlay source must be an existing file below {manifest_path.parent}: {relative}")
        expected_source = _validate_hash(raw.get("sourceSha256"), "sourceSha256")
        if sha256_file(source) != expected_source:
            raise OverlayError(f"Overlay source hash mismatch: {source}")
    if action == "dbc":
        edits = raw.get("edits")
        if Path(member).suffix.lower() != ".dbc" or not isinstance(edits, list) or not edits:
            raise OverlayError(f"DBC operation requires a .dbc member and non-empty edits: {member}")
        for edit in edits:
            if not isinstance(edit, dict):
                raise OverlayError(f"DBC edit must be an object: {member}")
            required = {"recordId", "fieldName", "fieldIndex", "valueType", "oldValue", "newValue", "reason"}
            if not required.issubset(edit):
                raise OverlayError(f"DBC edit is missing required fields: {member}")
            if not isinstance(edit["recordId"], int) or not isinstance(edit["fieldIndex"], int):
                raise OverlayError(f"DBC recordId and fieldIndex must be integers: {member}")
            if edit["valueType"] not in {"uint32", "float32", "string"}:
                raise OverlayError(f"Unsupported DBC valueType: {edit['valueType']}")
            if not str(edit["fieldName"]).strip() or not str(edit["reason"]).strip():
                raise OverlayError(f"DBC fieldName and reason are required: {member}")
    if action == "transform":
        recipe = raw.get("recipe")
        if not isinstance(recipe, dict):
            raise OverlayError(f"Transform operation requires a recipe object: {member}")
        kind = recipe.get("kind")
        required_by_kind = {
            "scale_xy_vertices": {"offset", "count", "stride", "factor"},
            "rewrite_bounds": {"offset", "minimum", "maximum", "radius"},
            "replace_texture_reference": {"old", "new", "expectedOccurrences"},
            "recolor_dxt1_endpoints": {"red", "green", "blue"},
        }
        required = required_by_kind.get(kind)
        if required is None or not required.issubset(recipe):
            raise OverlayError(f"Unsupported or incomplete transform recipe for {member}: {kind}")
        if kind == "scale_xy_vertices":
            if not all(isinstance(recipe[name], int) for name in ("offset", "count", "stride")) or not isinstance(
                recipe["factor"], (int, float)
            ):
                raise OverlayError(f"Invalid scale_xy_vertices recipe values: {member}")
        elif kind == "rewrite_bounds":
            if (
                not isinstance(recipe["offset"], int)
                or not isinstance(recipe["minimum"], list)
                or not isinstance(recipe["maximum"], list)
                or len(recipe["minimum"]) != 3
                or len(recipe["maximum"]) != 3
                or not all(isinstance(value, (int, float)) for value in recipe["minimum"] + recipe["maximum"])
                or not isinstance(recipe["radius"], (int, float))
            ):
                raise OverlayError(f"Invalid rewrite_bounds recipe values: {member}")
        elif kind == "replace_texture_reference":
            if (
                not isinstance(recipe["old"], str)
                or not isinstance(recipe["new"], str)
                or not isinstance(recipe["expectedOccurrences"], int)
            ):
                raise OverlayError(f"Invalid replace_texture_reference recipe values: {member}")
        elif kind == "recolor_dxt1_endpoints" and not all(
            isinstance(recipe[name], int) for name in ("red", "green", "blue")
        ):
            raise OverlayError(f"Invalid recolor_dxt1_endpoints recipe values: {member}")
        extension = Path(member).suffix.lower()
        if kind == "recolor_dxt1_endpoints" and extension != ".blp":
            raise OverlayError(f"BLP color recipes require a .blp member: {member}")
        if kind != "recolor_dxt1_endpoints" and extension not in {".m2", ".mdx", ".skin"}:
            raise OverlayError(f"Model recipes require an M2/MDX/SKIN member: {member}")
    return Operation(overlay, edition, action, member, source, expected, tuple(sorted(servers)), raw)


def load_operations(root: Path, editions: Iterable[str], server: str | None = None) -> dict[str, list[Operation]]:
    edition_names = tuple(sorted(editions))
    servers = load_servers(root / "servers.json")
    if server is not None and server not in servers:
        raise OverlayError(f"Unknown server profile: {server}")
    result = {edition: [] for edition in edition_names}
    locations = [("common", root / "overlays" / "common" / "manifest.json", edition_names)]
    locations.extend(
        (edition, root / "overlays" / "editions" / edition / "manifest.json", (edition,))
        for edition in edition_names
    )
    for overlay, path, targets in locations:
        data = _read_json(path)
        if data.get("schemaVersion") != SCHEMA_VERSION or data.get("overlay") != overlay:
            raise OverlayError(f"Overlay identity/schema mismatch: {path}")
        operations = data.get("operations")
        if not isinstance(operations, list):
            raise OverlayError(f"Overlay operations must be a list: {path}")
        for target in targets:
            validated = (_validate_operation(raw, path, overlay, target, set(servers)) for raw in operations)
            result[target].extend(operation for operation in validated if server is None or server in operation.servers)
    for edition, operations in result.items():
        seen: dict[str, set[str]] = {}
        for operation in operations:
            key = operation.member.casefold()
            active_servers = set(operation.servers) if server is None else {server}
            if active_servers.intersection(seen.get(key, set())):
                raise OverlayError(f"Multiple operations target the same member in {edition}: {operation.member}")
            seen.setdefault(key, set()).update(active_servers)
    return result


def declared_change_set(operations: Iterable[Operation]) -> set[str]:
    return {operation.member.casefold() for operation in operations}

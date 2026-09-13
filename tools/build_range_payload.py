"""Build six edition-specific ICC range-circle experimental Patch-Y MPQs.

Only five DBC members are rewritten. Spell.dbc changes are limited to visual
fields 131/132 (this experiment uses field 131 only). Every unrelated archive
member is compared byte-for-byte after StormLib readback.

Author/Creator/Modifier: Neil Mitchell.
Usage: python tools/build_range_payload.py BASELINE_DIRECTORY CATALOG_JSON
Run build_range_model.py first and set STORMLIB_DLL.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import struct
import sys
from pathlib import Path

from range_model_utils import (
    add_string,
    by_id,
    field_diffs,
    load_wdbc,
    save_wdbc,
    set_f32,
    set_u32,
    string_at,
    u32,
)
from range_mpq import add_or_replace, dll, opened, snapshot

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
TABLES = ("Spell", "SpellVisual", "SpellVisualKit", "SpellVisualEffectName", "SpellVisualKitModelAttach")
EXPECTED_FIELDS = {
    "Spell": 234,
    "SpellVisual": 32,
    "SpellVisualKit": 38,
    "SpellVisualEffectName": 7,
    "SpellVisualKitModelAttach": 10,
}
PRIVATE_PREFIX = "Spells\\Lau_ICC_RangeTest"
MODEL_FILES = {
    "shadow_prison": "ShadowPrison12",
    "empowered_vortex": "EmpoweredVortex12",
    "blood_nova": "BloodNova12",
}
CUES = (
    {
        "key": "shadow_prison",
        "spells": (73001,),
        "visual_donor": 15404,
        "visual_slot": 4,  # StateKit: conditional player-area-aura state carrier.
        "kit_donor": 90002,
        "clear_kit_effect_fields": True,
        "color": "cyan-blue",
        "timing": "conditional Shadow Prison state; may be hidden or absent on Warmane",
        "anchor": "state kit on the aura holder if the client renders the area-aura state",
    },
    {
        "key": "empowered_vortex",
        "spells": (72038, 72815, 72816, 72817),
        "visual_donor": 15204,
        "visual_slot": 2,  # CastKit: player force-caster, avoids impact splash victims.
        "kit_donor": 14056,
        "clear_kit_effect_fields": False,
        "color": "purple",
        "timing": "direct player-origin burst/cast cue; not advance warning",
        "anchor": "cloned CastKit on each player force-casting the burst",
    },
    {
        "key": "blood_nova",
        "spells": (72378, 73058),
        "visual_donor": 15283,
        "visual_slot": 3,  # ImpactKit on the parent's selected hit unit.
        "kit_donor": 14140,
        "clear_kit_effect_fields": False,
        "color": "red",
        "timing": "selected-target parent impact cue; not advance warning",
        "anchor": "cloned parent ImpactKit on the selected target; damage/dummy chain untouched",
    },
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_reset_directory(path: Path):
    resolved_root = ROOT.resolve()
    resolved = path.resolve()
    if resolved.parent != (ROOT / "dist").resolve() or resolved_root not in resolved.parents:
        raise ValueError(f"Refusing to reset unexpected directory: {resolved}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def member_for(before, table_name: str) -> str:
    matches = [name for name in before if name.lower().endswith((table_name + ".dbc").lower())]
    if len(matches) != 1:
        raise ValueError(f"Expected one {table_name}.dbc member, found {matches}")
    return matches[0]


def row_values(record: bytes | bytearray):
    return [u32(record, field) for field in range(len(record) // 4)]


def edit_tables(before, work: Path):
    tables = {}
    members = {}
    originals = {}
    original_strings = {}
    for name in TABLES:
        member = member_for(before, name)
        members[name] = member
        path = work / f"{name}.dbc"
        path.write_bytes(before[member])
        fields, rows, strings = load_wdbc(path)
        if fields != EXPECTED_FIELDS[name]:
            raise ValueError(f"Unsupported {name} field count {fields}")
        tables[name] = (fields, rows, strings)
        originals[name] = {ident: bytes(row) for ident, row in by_id(rows).items()}
        original_strings[name] = bytes(strings)

    def rows(name):
        return tables[name][1]

    def strings(name):
        return tables[name][2]

    def ids(name):
        return by_id(rows(name))

    spell_ids = ids("Spell")
    visual_ids = ids("SpellVisual")
    kit_ids = ids("SpellVisualKit")
    effect_ids = ids("SpellVisualEffectName")
    attach_ids = ids("SpellVisualKitModelAttach")
    for required in (73001, 72038, 72815, 72816, 72817, 72378, 73058, 72379, 72380, 72438, 72439, 72440):
        if required not in spell_ids:
            raise ValueError(f"Required Spell.dbc row missing: {required}")
    for required in (15404, 15204, 15283):
        if required not in visual_ids:
            raise ValueError(f"Required SpellVisual donor missing: {required}")
    for required in (90002, 14056, 14140):
        if required not in kit_ids:
            raise ValueError(f"Required SpellVisualKit donor missing: {required}")
    if 9002 not in effect_ids or 8003 not in attach_ids:
        raise ValueError("Native range-circle effect/attachment donors 9002/8003 are missing")

    next_visual = max(visual_ids) + 1
    next_kit = max(kit_ids) + 1
    next_effect = max(effect_ids) + 1
    next_attach = max(attach_ids) + 1
    allocated = {}

    for offset, cue in enumerate(CUES):
        visual_id = next_visual + offset
        kit_id = next_kit + offset
        effect_id = next_effect + offset
        attach_id = next_attach + offset
        stem = MODEL_FILES[cue["key"]]

        effect = bytearray(effect_ids[9002])
        set_u32(effect, 0, effect_id)
        set_u32(effect, 1, add_string(strings("SpellVisualEffectName"), f"Lau ICC range test {cue['key']} 12-unit ring"))
        set_u32(effect, 2, add_string(strings("SpellVisualEffectName"), f"{PRIVATE_PREFIX}\\{stem}.mdx"))
        # AreaEffectSize, Scale, MinAllowedScale, MaxAllowedScale. Geometry is baked.
        for field in range(3, 7):
            set_f32(effect, field, 1.0)
        rows("SpellVisualEffectName").append(effect)

        kit = bytearray(kit_ids[cue["kit_donor"]])
        set_u32(kit, 0, kit_id)
        if cue["clear_kit_effect_fields"]:
            for field in range(3, 15):
                set_u32(kit, field, 0)
        rows("SpellVisualKit").append(kit)

        attach = bytearray(attach_ids[8003])
        set_u32(attach, 0, attach_id)
        set_u32(attach, 1, kit_id)
        set_u32(attach, 2, effect_id)
        rows("SpellVisualKitModelAttach").append(attach)

        visual = bytearray(visual_ids[cue["visual_donor"]])
        set_u32(visual, 0, visual_id)
        set_u32(visual, cue["visual_slot"], kit_id)
        rows("SpellVisual").append(visual)

        spell_changes = []
        for spell_id in cue["spells"]:
            spell = spell_ids[spell_id]
            old_secondary = u32(spell, 132)
            set_u32(spell, 131, visual_id)
            if u32(spell, 132) != old_secondary:
                raise AssertionError(f"Secondary visual changed for spell {spell_id}")
            spell_changes.append(spell_id)
        allocated[cue["key"]] = {
            "spell_ids": spell_changes,
            "visual_id": visual_id,
            "visual_donor": cue["visual_donor"],
            "visual_slot": cue["visual_slot"],
            "kit_id": kit_id,
            "kit_donor": cue["kit_donor"],
            "effect_id": effect_id,
            "effect_donor": 9002,
            "attach_id": attach_id,
            "attach_donor": 8003,
            "model": f"{PRIVATE_PREFIX}\\{stem}.mdx",
            "color": cue["color"],
            "timing": cue["timing"],
            "anchor": cue["anchor"],
        }

    expected_spell_changes = {spell for cue in CUES for spell in cue["spells"]}
    proof = {}
    updates = {}
    for name, (fields, table_rows, table_strings) in tables.items():
        new_ids = by_id(table_rows)
        changed_original = {
            ident for ident, old_row in originals[name].items() if bytes(new_ids[ident]) != old_row
        }
        allowed = expected_spell_changes if name == "Spell" else set()
        if changed_original != allowed:
            raise AssertionError(f"Unexpected changed {name} original rows: {changed_original} vs {allowed}")
        added_ids = sorted(set(new_ids) - set(originals[name]))
        record_changes = []
        for ident in sorted(changed_original):
            diffs = field_diffs(originals[name][ident], new_ids[ident])
            if name == "Spell" and {diff["field"] for diff in diffs} - {131, 132}:
                raise AssertionError(f"Gameplay/nonvisual Spell fields changed for {ident}: {diffs}")
            record_changes.append({"id": ident, "field_diffs": diffs})
        added_rows = []
        for ident in added_ids:
            entry = {"id": ident, "field_values_u32": row_values(new_ids[ident])}
            if name == "SpellVisualEffectName":
                entry["name"] = string_at(table_strings, u32(new_ids[ident], 1))
                entry["model_path"] = string_at(table_strings, u32(new_ids[ident], 2))
                entry["float_fields_3_to_6"] = [
                    struct.unpack_from("<f", new_ids[ident], field * 4)[0] for field in range(3, 7)
                ]
            added_rows.append(entry)
        path = work / f"{name}.dbc"
        save_wdbc(path, fields, table_rows, table_strings)
        updates[members[name]] = path.read_bytes()
        proof[name] = {
            "field_count": fields,
            "before_sha256": digest(before[members[name]]),
            "after_sha256": digest(updates[members[name]]),
            "before_records": len(originals[name]),
            "after_records": len(table_rows),
            "changed_original_ids": sorted(changed_original),
            "record_field_diffs": record_changes,
            "added_ids": added_ids,
            "added_rows": added_rows,
            "original_string_block_prefix_preserved": bytes(table_strings).startswith(original_strings[name]),
        }
        if name != "SpellVisualEffectName" and bytes(table_strings) != original_strings[name]:
            raise AssertionError(f"Unexpected string-block change: {name}")
    proof["allocation"] = allocated
    return updates, proof


def model_updates(before):
    source = DIST / "model"
    files = sorted(path for path in source.rglob("*") if path.is_file())
    expected = {
        f"{PRIVATE_PREFIX}\\{stem}{suffix}"
        for stem in MODEL_FILES.values()
        for suffix in (".m2", "00.skin", ".blp")
    }
    updates = {
        str(path.relative_to(source)).replace("/", "\\"): path.read_bytes() for path in files
    }
    if set(updates) != expected:
        raise ValueError(f"Unexpected generated model set: {sorted(updates)}")
    existing_lower = {name.lower() for name in before}
    collisions = [name for name in updates if name.lower() in existing_lower]
    if collisions:
        raise ValueError(f"Private asset collision: {collisions}")
    return updates


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: build_range_payload.py BASELINE_DIRECTORY CATALOG_JSON")
    baseline_dir = Path(sys.argv[1]).resolve()
    catalog_path = Path(sys.argv[2]).resolve()
    catalog = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
    baseline_catalog = json.loads(json.dumps(catalog))
    editions = sorted(key for key in catalog["Assets"] if key.startswith("Y-"))
    if len(editions) != 6:
        raise ValueError(f"Expected six Y editions, got {editions}")

    DIST.mkdir(exist_ok=True)
    payload_dir = DIST / "payload"
    tables_dir = DIST / "tables"
    safe_reset_directory(payload_dir)
    safe_reset_directory(tables_dir)
    results = []
    for edition in editions:
        baseline_path = baseline_dir / f"{edition}.mpq"
        baseline_bytes = baseline_path.read_bytes()
        expected = baseline_catalog["Assets"][edition]
        if len(baseline_bytes) != expected["Bytes"] or digest(baseline_bytes) != expected["Sha256"]:
            raise ValueError(f"Stable 3.0.8 baseline mismatch: {edition}")
        before = snapshot(baseline_path)
        work = tables_dir / edition
        work.mkdir(parents=True)
        dbc_updates, dbc_proof = edit_tables(before, work)
        asset_updates = model_updates(before)
        updates = {**dbc_updates, **asset_updates}
        expected_after = dict(before)
        expected_after.update(updates)

        target = payload_dir / f"{edition}.mpq"
        shutil.copy2(baseline_path, target)
        archive = opened(target, 0)
        try:
            for index, (member, data) in enumerate(sorted(updates.items())):
                local = work / f"member-{index}.tmp"
                local.write_bytes(data)
                add_or_replace(archive, local, member)
                local.unlink()
        finally:
            dll.SFileCloseArchive(archive)
        after = snapshot(target)
        if after != expected_after:
            missing = sorted(set(expected_after) - set(after))
            extra = sorted(set(after) - set(expected_after))
            mismatched = sorted(name for name in set(after) & set(expected_after) if after[name] != expected_after[name])
            raise AssertionError(
                f"Archive readback mismatch {edition}: missing={missing}, extra={extra}, bytes={mismatched}"
            )
        changed = sorted(name for name in before if before[name] != after[name])
        added = sorted(set(after) - set(before))
        if set(changed) != set(dbc_updates) or set(added) != set(asset_updates):
            raise AssertionError(f"Unexpected archive mutation scope for {edition}")
        output_bytes = target.read_bytes()
        output_hash = digest(output_bytes)
        output_size = len(output_bytes)
        hash_part = payload_dir / f"{output_hash}.bin"
        shutil.copy2(target, hash_part)
        catalog["Assets"][edition] = {
            "Id": edition,
            "Sha256": output_hash,
            "Bytes": output_size,
            "Parts": [
                {
                    "Sha256": output_hash,
                    "Bytes": output_size,
                    "FileName": hash_part.name,
                    "Url": None,
                }
            ],
        }
        results.append(
            {
                "edition": edition,
                "baseline_archive_sha256": digest(baseline_bytes),
                "output_archive_sha256": output_hash,
                "output_archive_bytes": output_size,
                "changed": changed,
                "added": added,
                "changed_member_hashes": {
                    name: {"before": digest(before[name]), "after": digest(after[name])}
                    for name in changed
                },
                "added_member_hashes": {name: digest(after[name]) for name in added},
                "dbc": dbc_proof,
                "unrelated_members_byte_identical": True,
                "archive_snapshot_readback_exact": True,
            }
        )
        print(f"PASS exact scope/readback {edition} -> {output_hash}", flush=True)

    catalog["PublicReady"] = False
    (DIST / "catalog.json").write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    (DIST / "baseline.json").write_text(json.dumps(baseline_catalog, indent=2) + "\n", encoding="utf-8")
    validation = {
        "Author": "Neil Mitchell",
        "Creator": "Neil Mitchell",
        "LastModifiedBy": "Neil Mitchell",
        "prototype": "ICC player range circles",
        "build_sources": {
            str(path.relative_to(ROOT)).replace("\\", "/"): digest(path.read_bytes())
            for path in [
                ROOT / "tools" / "build_range_model.py",
                ROOT / "tools" / "build_range_payload.py",
                ROOT / "tools" / "range_model_utils.py",
                ROOT / "tools" / "range_mpq.py",
                ROOT / "tools" / "test_range_payload.py",
                *sorted((ROOT / "editing" / "range-circles").glob("*")),
            ]
            if path.is_file()
        },
        "build_dependency": {
            "stormlib_sha256": digest(Path(os.environ["STORMLIB_DLL"]).read_bytes()),
            "stormlib_embedded_in_payload": False,
            "path_is_configurable_via": "STORMLIB_DLL",
        },
        "baseline_catalog_source_sha256": digest(catalog_path.read_bytes()),
        "requested_visible_radius_model_units": 12.0,
        "intended_game_radius_yards": 12.0,
        "geometry_basis": {
            "donor_quad_half_width_model_units": 2.859224557876587,
            "source_texture_half_width_pixels": 255.5,
            "bright_visible_outer_axis_pixels": 249.5,
            "threshold": "source PNG alpha >= 64 and max RGB >= 64",
            "generated_quad_half_width_model_units": 12.0 / (249.5 / 255.5),
            "generated_model_sequence_and_skin_radius_model_units": math.sqrt(
                2 * (12.0 / (249.5 / 255.5)) ** 2 + 0.2777777910232544**2
            ),
            "updated_bounds": [
                "M2 global bounds at offset 160",
                "all three M2 sequence bounds at sequence +32",
                "SKIN submesh center/radius block at submesh +20",
            ],
            "dbc_effect_fields": {"3_AreaEffectSize": 1.0, "4_Scale": 1.0, "5_MinAllowedScale": 1.0, "6_MaxAllowedScale": 1.0},
            "runtime_calibration_required": True,
        },
        "mechanics": {
            cue["key"]: {
                "spell_ids": list(cue["spells"]),
                "color": cue["color"],
                "timing": cue["timing"],
                "anchor": cue["anchor"],
            }
            for cue in CUES
        },
        "excluded_spell_ids": {
            "boss_shadow_prison_aura": [72998],
            "blood_nova_dummy_or_damage_chain": [72379, 72380, 72438, 72439, 72440],
        },
        "limitations": [
            "Static model units are intended as yards but require in-game calibration.",
            "The direct Vortex and Blood Nova cues are resolution-time diagnostics, not advance spacing warnings.",
            "Shadow Prison is encounter-wide heroic behavior and may be hidden or unrendered on Warmane.",
            "Blood Nova target-side attachment is inferred from the selected-target parent ImpactKit and must be observed in game.",
            "Circle overlap alone does not mean player centres are within 12 yards.",
        ],
        "results": results,
    }
    (DIST / "scope-validation.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

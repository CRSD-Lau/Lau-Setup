"""Isolated Unicorn validation of the two loading-framing patch sites.

Author / Creator / Last Modified By: Neil Mitchell
"""
from __future__ import annotations

import hashlib
import json
import struct
import sys
from pathlib import Path

import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EFLAGS, UC_X86_REG_EIP, UC_X86_REG_ESP

META = dict(Author="Neil Mitchell", Creator="Neil Mitchell", LastModifiedBy="Neil Mitchell")
BASE = 0x400000
STACK = 0x12000000
STACK_SIZE = 0x20000
STOP = 0x0BADF00D
SITE_DRAW = 0x40A602
SITE_UV = 0x408615
HOOK_DRAW = 0xDFD000
HOOK_UV = 0xDFD100
NATIVE_DRAW = 0x4085A0
NATIVE_UV = 0xAB6400
INITIAL_VIEW = [0.2, 0.8, 0.1, 0.9, 0.3, 0.7]
GET_VIEW = 0x408070
SET_VIEW = 0x681F60
ASPECT = 0xAC0CB0
BACKGROUND = 0xB2FEA8
TEXTURE_FLAG = 0xB2FED8


def f32(value: float) -> bytes:
    return struct.pack("<f", value)


def u32(uc: Uc, address: int) -> int:
    return struct.unpack("<I", bytes(uc.mem_read(address, 4)))[0]


def floats(uc: Uc, address: int, count: int) -> list[float]:
    return list(struct.unpack("<" + "f" * count, bytes(uc.mem_read(address, count * 4))))


def map_pe(path: Path) -> Uc:
    pe = pefile.PE(str(path))
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    uc.mem_map(BASE, 0xA00000)
    for section in pe.sections:
        data = section.get_data()
        uc.mem_write(BASE + section.VirtualAddress, data)
    uc.mem_map(STACK, STACK_SIZE)
    return uc


def ret_to(uc: Uc) -> None:
    esp = uc.reg_read(UC_X86_REG_ESP)
    uc.reg_write(UC_X86_REG_EIP, u32(uc, esp))
    uc.reg_write(UC_X86_REG_ESP, esp + 4)


def run_uv(path: Path, aspect: float, texture: int) -> dict:
    uc = map_pe(path)
    start = STACK + STACK_SIZE - 0x100
    # Caller has already pushed 0, 0, 8 immediately before the five-byte site.
    esp = start - 12
    for offset, value in enumerate((8, 0, 0)):
        uc.mem_write(esp + offset * 4, struct.pack("<I", value))
    uc.mem_write(ASPECT, f32(aspect))
    uc.mem_write(BACKGROUND, struct.pack("<I", 1))
    uc.mem_write(TEXTURE_FLAG, struct.pack("<I", texture))
    before_eax, before_flags = 0x12345678, 0x202
    uc.reg_write(UC_X86_REG_EAX, before_eax)
    uc.reg_write(UC_X86_REG_EFLAGS, before_flags)
    uc.reg_write(UC_X86_REG_ESP, esp)
    uc.reg_write(UC_X86_REG_EIP, SITE_UV)
    seen = {}
    def hook(emu, address, size, _):
        if address == SITE_UV + 5:
            seen["pointer"] = u32(emu, emu.reg_read(UC_X86_REG_ESP))
            seen["esp"] = emu.reg_read(UC_X86_REG_ESP)
            seen["eax"] = emu.reg_read(UC_X86_REG_EAX)
            seen["eflags"] = emu.reg_read(UC_X86_REG_EFLAGS)
            emu.emu_stop()
    uc.hook_add(UC_HOOK_CODE, hook)
    uc.emu_start(SITE_UV, STOP, count=200)
    assert seen["esp"] == esp - 4
    assert seen["eax"] == before_eax and seen["eflags"] == before_flags
    return dict(aspect=aspect, texture_flag=texture, uv_pointer=hex(seen["pointer"]), stack_delta=seen["esp"]-esp, registers_preserved=True)


def run_draw(path: Path, aspect: float, background: int) -> dict:
    uc = map_pe(path)
    uc.mem_write(ASPECT, f32(aspect))
    uc.mem_write(BACKGROUND, struct.pack("<I", background))
    esp = STACK + STACK_SIZE - 0x100
    uc.reg_write(UC_X86_REG_ESP, esp)
    uc.reg_write(UC_X86_REG_EIP, SITE_DRAW)
    calls: list[tuple[str, list[float] | None]] = []
    def hook(emu, address, size, _):
        if address == GET_VIEW:
            stack = emu.reg_read(UC_X86_REG_ESP)
            for i, value in enumerate(INITIAL_VIEW):
                emu.mem_write(u32(emu, stack + 4 + i * 4), f32(value))
            calls.append(("get", None)); ret_to(emu)
        elif address == SET_VIEW:
            stack = emu.reg_read(UC_X86_REG_ESP)
            calls.append(("set", [struct.unpack("<f", struct.pack("<I", u32(emu, stack + 4 + i * 4)))[0] for i in range(6)])); ret_to(emu)
        elif address == NATIVE_DRAW:
            calls.append(("native", None)); ret_to(emu)
        elif address == SITE_DRAW + 5:
            emu.emu_stop()
    uc.hook_add(UC_HOOK_CODE, hook)
    uc.emu_start(SITE_DRAW, STOP, count=1000)
    return dict(aspect=aspect, background=background, calls=calls, stack_balanced=uc.reg_read(UC_X86_REG_ESP) == esp)


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: validate_loading_hooks.py original.exe fixed.exe result.json")
    original, fixed, result = map(Path, sys.argv[1:])
    original_hash = hashlib.sha256(original.read_bytes()).hexdigest()
    fixed_hash = hashlib.sha256(fixed.read_bytes()).hexdigest()
    original_bytes, fixed_bytes = original.read_bytes(), fixed.read_bytes()
    assert original_hash == "6993049f1338b32a0423612093a8c7c6895b112504b83d6826d4c2174692cd37"
    assert fixed_hash == "a6767f7ed4d1f7c67c144eed7bf9707cd270d95af200f4accd0c6fc66ca14889"
    assert len(original_bytes) == len(fixed_bytes) == 7705600
    changed = [i for i, (a, b) in enumerate(zip(original_bytes, fixed_bytes)) if a != b]
    assert changed == [0x7A15, 0x7A16, 0x7A17, 0x7A18, 0x9A03, 0x9A04, 0x9A05, 0x9A06]
    assert original_bytes[0x9A02:0x9A07] == bytes.fromhex("e8f9299f00")
    assert fixed_bytes[0x9A02:0x9A07] == bytes.fromhex("e899dfffff")
    assert original_bytes[0x7A15:0x7A1A] == bytes.fromhex("e8e64a9f00")
    assert fixed_bytes[0x7A15:0x7A1A] == bytes.fromhex("680064ab00")
    # The custom section and unrelated archive-reserve hook remain byte-for-byte intact.
    assert original_bytes[0x759000:0x759400] == fixed_bytes[0x759000:0x759400]
    aspects = [("4:3", 4/3), ("16:10", 1.6), ("16:9-2560x1440", 2560/1440), ("21:9", 21/9)]
    uv_old = [run_uv(original, ratio, flag) | {"mode": name} for name, ratio in aspects for flag in (0, 1)]
    uv_fixed = [run_uv(fixed, ratio, flag) | {"mode": name} for name, ratio in aspects for flag in (0, 1)]
    assert all(row["uv_pointer"] == hex(NATIVE_UV) for row in uv_fixed)
    assert all(row["uv_pointer"] == hex(NATIVE_UV) for row in uv_old if row["mode"] != "16:9-2560x1440")
    assert [row["uv_pointer"] for row in uv_old if row["mode"] == "16:9-2560x1440"] == [hex(0xDFD200), hex(0xDFD220)]
    draw_old = [run_draw(original, ratio, bg) | {"mode": name} for name, ratio in aspects for bg in (0, 1)]
    draw_fixed = [run_draw(fixed, ratio, bg) | {"mode": name} for name, ratio in aspects for bg in (0, 1)]
    for row in draw_fixed:
        assert row["calls"] == [("native", None)] and row["stack_balanced"]
    for row in draw_old:
        if row["mode"] == "16:9-2560x1440" and row["background"]:
            assert [item[0] for item in row["calls"]] == ["get", "set", "native", "set"]
            assert row["calls"][1][1] == [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
            assert all(abs(actual - expected) < 1e-6 for actual, expected in zip(row["calls"][3][1], INITIAL_VIEW))
        else:
            assert row["calls"] == [("native", None)]
        assert row["stack_balanced"]
    output = dict(**META, status="UNICORN_ISOLATED_HOOK_VALIDATION_PASS_IN_GAME_ACCEPTANCE_PENDING", original_sha256=original_hash, fixed_sha256=fixed_hash, changed_byte_offsets=[hex(i) for i in changed], only_eight_bytes_changed=True, ldwide_section_preserved=True, uv_old=uv_old, uv_fixed=uv_fixed, draw_old=draw_old, draw_fixed=draw_fixed, limitations="Emulates only the two instruction paths with native draw/get/set calls stubbed; it does not render or launch WoW.")
    result.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

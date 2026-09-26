"""Read-only archive ownership audit. Author: Neil Mitchell."""
import ctypes as C
from ctypes import wintypes as W
import hashlib
import json
import struct
from pathlib import Path

import os
dll = C.WinDLL(os.environ['STORMLIB_DLL'])
for name, args, result in [
    ('SFileOpenArchive', [C.c_void_p, W.DWORD, W.DWORD, C.POINTER(W.HANDLE)], C.c_bool),
    ('SFileCloseArchive', [W.HANDLE], C.c_bool),
    ('SFileOpenFileEx', [W.HANDLE, C.c_char_p, W.DWORD, C.POINTER(W.HANDLE)], C.c_bool),
    ('SFileGetFileSize', [W.HANDLE, C.POINTER(W.DWORD)], W.DWORD),
    ('SFileReadFile', [W.HANDLE, C.c_void_p, W.DWORD, C.POINTER(W.DWORD), C.c_void_p], C.c_bool),
    ('SFileCloseFile', [W.HANDLE], C.c_bool),
]:
    fn = getattr(dll, name)
    fn.argtypes, fn.restype = args, result


def read_member(archive, name):
    handle = W.HANDLE()
    if not dll.SFileOpenFileEx(archive, name.encode('ascii'), 0, C.byref(handle)):
        return None
    try:
        high = W.DWORD()
        size = dll.SFileGetFileSize(handle, C.byref(high))
        assert high.value == 0 and size < 150_000_000
        out, read = C.create_string_buffer(size), W.DWORD()
        if not dll.SFileReadFile(handle, out, size, C.byref(read), None) or read.value != size:
            raise OSError(f'Failed read: {name}')
        return out.raw
    finally:
        dll.SFileCloseFile(handle)



def opened(p,flags=0x100):
    h=W.HANDLE();buf=C.create_unicode_buffer(str(p))
    if not dll.SFileOpenArchive(C.cast(buf,C.c_void_p),0,flags,C.byref(h)): raise OSError(str(p))
    return h
def snapshot(p):
    h=opened(p)
    try:
        names=set(read_member(h,'(listfile)').decode().splitlines())-{'(listfile)','(attributes)'}
        return {n:read_member(h,n) for n in names}
    finally: dll.SFileCloseArchive(h)

# MPQ conflict scanning

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> **First time installing?** Use [Start here](../START-HERE.txt); this document explains a technical safety check.

Setup 1.3.0 uses a small managed C# reader for classic MPQ headers/hash tables. StormLib was assessed and an official library package obtained, but the hotfix does not bundle or load it. Reading known-name hashes requires neither native code nor decompression; broader archive inspection remains separate work.

The MPQ hash/decryption format was checked against [StormLib](https://github.com/ladislav-zezula/StormLib), particularly SBaseCommon.cpp and StormLib.h. The upstream license is retained below for attribution. The reader's scope and conservative rejection behavior are documented in [Known limitations](../KNOWN-LIMITATIONS.md#setup-118-overlap-detection).

A matching Patch-Y addon member or two distinctive model names flags a possible overlap, not ownership or proof of byte identity. Exact current-catalog copies additionally match size and SHA-256. The reader does not certify arbitrary custom filename loading priority, validate every file payload, or scan other locales.

## Upstream notice

The MIT License (MIT)

Copyright (c) 1999-2013 Ladislav Zezula

Permission is hereby granted, free of charge, to any person obtaining a copy

of this software and associated documentation files (the "Software"), to deal

in the Software without restriction, including without limitation the rights

to use, copy, modify, merge, publish, distribute, sublicense, and/or sell

copies of the Software, and to permit persons to whom the Software is

furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in

all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR

IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,

FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE

AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER

LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,

OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN

THE SOFTWARE.

## Large tables and extra patches

Setup 1.2.1 removes the old 262,144-entry cap. It decrypts tables in 64 KiB chunks with continuous cipher state, retains only four marker-match flags, and checks every entry even after finding a marker. Table bounds, supported format checks, member indices, cancellation, the archive-count limit and the one-minute cooperative budget remain enforced.

The supplied Patch-Armadura.mpq has 524,288 entries (8 MiB). The 1.2.0 reader rejected its size; the new reader passes it without finding the known Patch-Y marker combination. This is not a full archive-integrity or in-game certification.

## Automatic backups in 1.3.0

Recognized extra upgrade patches, including original download names, are backed up automatically when the player clicks **Install upgrade**. Setup continues with the selected edition. **Restore previous install** returns those files to their original paths. No manual moving is needed.

Eligibility requires known Patch-Y markers or an exact catalog archive match. This indicates overlap, not ownership. Only direct `.mpq` children of Data or the active locale may be moved. Stock archives, managed Q/M/S/Y paths, other locales, disabled files and nested folders are excluded from extra-file moves. Readable unknown patches remain untouched; malformed or inaccessible archives still stop safely.

The existing transaction records each original path, byte count and SHA-256 before moving the file into `LauSetupBackups/transactions/<id>/before/`. It verifies the full conflict set again before committing, including otherwise empty plans. Up to 2,048 extra entries are allowed separately from the 13 managed targets. Crash recovery, cancellation and rollback cover both.

Restore rejects changed backups, unsafe paths, forged replacement operations and files recreated by the player. Published archive hashes are retained in an append-only trusted list so older exact-copy backups remain restorable after catalog changes. A journal flag alone never authorizes moving an arbitrary file.

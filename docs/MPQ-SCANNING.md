# MPQ conflict scanning

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> **First time installing?** Use [Start here](../START-HERE.txt); this document explains a technical safety check.

Setup 1.1.8 uses a small managed C# reader for classic MPQ headers/hash tables. StormLib was assessed and an official library package obtained, but the hotfix does not bundle or load it. Reading known-name hashes requires neither native code nor decompression; broader archive inspection remains separate work.

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

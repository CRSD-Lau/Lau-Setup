# Game 3.0.9 and compact Patch-Y packaging

Author, Creator, Last Modified By: Neil Mitchell

Game 3.0.9 includes the optional merged Lau/Trimitor map pack. Setup remains version 1.4.0. All six Patch-Y editions report 3.0.9 through their embedded addon version metadata and /pyversion.

Compaction runs only on new release staging copies. It does not run inside Setup, touch a player's existing archives, or change LauSetupBackups. Backups retain the exact original bytes.

## Measured results

| Edition | Original bytes | Final bytes | Saved bytes |
|---|---:|---:|---:|
| Y-HD-NewSpells-Off-Consecration-Off | 50,626,756 | 47,561,296 | 3,065,460 |
| Y-HD-NewSpells-Off-Consecration-On | 50,626,764 | 47,561,314 | 3,065,450 |
| Y-HD-NewSpells-On-Consecration-Off | 66,603,332 | 47,470,879 | 19,132,453 |
| Y-HD-NewSpells-On-Consecration-On | 66,603,340 | 47,470,883 | 19,132,457 |
| Y-Non-HD-Consecration-Off | 53,797,737 | 46,608,600 | 7,189,137 |
| Y-Non-HD-Consecration-On | 53,797,734 | 46,608,605 | 7,189,129 |

Total reduction: **58,774,086 bytes (56.05 MiB)** across all six editions compared with 3.0.8. Individual users download their selected edition.

Only `Interface\AddOns\!PYAndre\!PYAndre.toc` changes content for the version bump. Every decompressed member is compared before and after compaction, including internal metadata members. Physical archive headers/layout change as unused archive space is removed. **No DBC edits in Patch-Y**; the separate optional map component introduces upstream map DBC overrides documented in [MAP-PACK.md](MAP-PACK.md).

## Reproduce before release packaging

Run `python tools/compact_mpqs.py --catalog build/catalog.json --sources SOURCE_INDEX.json --stormlib PATH_TO_StormLib.dll --output NEW_STAGING_DIRECTORY --game-version 3.0.9` on Windows with StormLib 9.40. The source index maps asset IDs to immutable source archive paths.

Use a fresh directory. The script verifies source hashes, copies each archive, updates only version metadata when needed, verifies member parity, compacts the copy, verifies every member again, and reads the finished ZIP back. It refuses existing archive destinations, source/catalog mismatch, unknown members, incomplete enumeration, unexplained changes and archive growth. On failure, do not publish partial output; keep the originals and investigate the recorded error.

Only after success: publish new hash-named payloads under `payload-3.0.9`, verify public bytes, promote the generated catalog with PublicReady=true, then build the shared installer ZIP. Never overwrite an existing release asset. Keep compaction-proof.json with the release validation records.

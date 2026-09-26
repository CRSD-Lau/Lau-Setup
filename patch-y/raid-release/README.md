# Portable raid-visual source package

**Author:** Neil Mitchell

**Creator:** Neil Mitchell

**Last Modified By:** Neil Mitchell

`raid-visual-spec.json` defines the approved DBC row/field changes and appended strings. `assets/` holds the 15 hash-pinned approved Consecration and boss assets. `halion/` holds only the supplied Halion skin from [Andre issue #39](https://github.com/CRSD-Lau/Lau-Setup/issues/39#issuecomment-5681283458). It contains neither a donor MPQ nor copied DBC blobs.

The normal Windows builder requires a verified public 3.0.9 catalog and three matching baseline Y archives, this source package, and StormLib. The historical accepted September archive is supported only by the optional `--accepted` parity check. The DBC and visual work retains the original Suppository/Andre attribution and the approved Lau edits recorded in the spec.

Run from any working directory, using a fresh output directory:

```powershell
python D:\path\to\Lau-Installer\tools\build_raid_visual_release.py --baseline-catalog D:\path\to\previous-catalog.json --baseline-dir D:\path\to\compacted-y-3.0.9 --stormlib D:\path\to\StormLib.dll --out D:\path\to\visuals-portable
```

The bundled `tools/mpq.py` is read-only and is selected by default; `--mpq-helper` is only for an explicit alternate helper directory.

# Microsoft Defender notice for the optional WoW.exe

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

Microsoft Defender Antivirus can flag the packed `WoW.exe` in the **Compatible WoW.exe + loading screens** option for game release **3.1.0 Lau**. This build uses a Direct3D-to-Vulkan graphics wrapper. Lau suspects the detection is a false positive related to that wrapper. Microsoft analysis is needed to confirm it. `LauSetup.exe` is the separate installer inside `LauSetup.zip`.

## Keep your existing game executable

Keep Defender enabled. On **Your visuals**, leave **Compatible WoW.exe + loading screens** unchecked. You can still install Patch-Y and choose the other compatible visual upgrades. The standalone Patch-Y ZIPs also work with your existing compatible executable. [Manual Patch-Y guide](PATCH-Y-MANUAL-INSTALL.md).

## If Defender reports a detection

1. Leave the flagged file quarantined. In Windows Security, open **Virus & threat protection → Protection history** and record the detection name, affected filename and Lau Setup version.
2. If you already have a copy of the optional file that remains accessible, use PowerShell to check its SHA-256. Replace the example path with the path to that copy.

   ```powershell
   Get-FileHash -Algorithm SHA256 -LiteralPath 'C:\Path\To\WoW.exe'
   ```

   The official 3.1.0 Lau `WoW.exe` SHA-256 is `4218fef354f875d1d27aae9cc6a93c75aaadaa1f0beea1204172793cd39e0505`. Use the hash to identify the exact release file. [Pinned release catalog](../build/catalog.json) · [Official game payload release](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/payload-3.1.0).
3. Include the detection name, affected filename, Setup version and SHA-256 if available when reporting the alert. Microsoft can review the exact file through its submission portal. [Report to Lau Setup](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose) · [Microsoft file analysis portal](https://www.microsoft.com/en-us/wdsi/filesubmission).

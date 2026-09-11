# Lau Setup platform feasibility

Author: Neil Mitchell  
Creator: Neil Mitchell  
Last Modified By: Neil Mitchell  
Assessment date: 2026-09-11

Update: the user selected Wine only. Installer 1.1.0 now provides the tested
Wine 11 / Wine Mono 10.4.1 launcher described in [the Wine guide](wine/README.txt).
The Wine 8 probe and recommendations below are preserved as historical assessment.
Lutris, Proton and macOS integration remain out of scope.

Lau Setup 1.0.1 remains a Windows installer. Linux through Wine is the recommended next compatibility target. This assessment does not certify installation on Linux or macOS. The earlier 63 Docker/Wine cases exercised the game data, not this installer.

| Option | Recommendation | What it means for Lau Setup |
| --- | --- | --- |
| Wine on Linux | First target; feasible in principle, currently unverified | Reuse the Windows installer inside an explicitly selected Wine prefix. Prove its runtime, folder selection, downloads, file safety and recovery before publishing support. |
| Lutris | Next, after direct Wine passes | A small integration recipe can launch setup in the existing game's prefix. No separate payload format is needed. |
| Steam / Proton | Later, conditional | Use the correct existing game's prefix. Adding setup as another non-Steam game can give it a different environment. Steam Deck usability needs separate screen and controller checks. |
| CrossOver on macOS | Plausible, separate test track | Run inside the game's bottle. Validate on actual macOS hardware and supported CrossOver versions; Linux tests cannot establish this. |
| Wine + DXVK | Optional game configuration | DXVK translates Direct3D for the game. It does not solve the installer's .NET, font or file-safety requirements. |
| Whisky | Do not adopt as a new support target | Its upstream project is no longer actively maintained. |

The classification above follows the roles described by [Wine Mono](https://github.com/wine-mono/wine-mono), [Lutris](https://lutris.net/about/), [Proton](https://github.com/ValveSoftware/Proton), [DXVK](https://github.com/doitsujin/dxvk), [CrossOver's Mac guide](https://support.codeweavers.com/en_US/crossover-mac-user-guide), and [Whisky](https://github.com/Whisky-App/Whisky). Recommendations are our assessment, not upstream certification of Lau Setup. CrossOver can run 32-bit Windows applications in 64-bit bottles; loss of native macOS 32-bit support alone does not rule it out.

## Bounded probe results

The local probe used Wine 8.0 (Debian 8.0~repack-4), an isolated win32 prefix and Xvfb. This older locally available runtime is not a test of current Wine releases. No personal game client was mounted or modified.

1. The inherited game-test image disabled mscoree. Enabling it exposed that Wine Mono was missing. This was a test-environment issue.
2. Installed the official Wine Mono 7.4.0 MSI in the disposable prefix after verifying SHA-256 `6413ff328ebbf7ec7689c648feb3546d8102ded865079d1fbf0331b14b3ab0ec`, pinned by [Wine 8.0's source](https://raw.githubusercontent.com/wine-mirror/wine/wine-8.0/dlls/appwiz.cpl/addons.c).
3. A diagnostic harness initialized WinForms and loaded the embedded catalog, then failed constructing the form with `System.ArgumentException: The requested FontFamily could not be found [GDI+ status: FontFamilyNotFound]`. Copying available Liberation fonts into that prefix did not resolve it. No successful installer screenshot or installation resulted.
4. Local evidence is retained under `reports/wine-feasibility/`. The probe container is stopped. The diagnostic harness is not included in the distributed installer or public source bundle.

This identifies runtime/font provisioning work, not proof that Wine is impossible. No install/restore transaction was attempted under Wine in this probe.

## Acceptance work before Wine support

1. Establish a reproducible current Wine/runtime/font combination on a Linux desktop. Show initial, ready, download, recovery and error states at common display scales; verify keyboard access and folder selection.
2. Verify exact host-folder mapping and case handling on a case-sensitive filesystem, including duplicate names that differ only by case. Preserve unrelated patches and personal settings.
3. Prove link, exclusive-lock, free-space, journal and atomic-replace behavior. The installer currently calls Windows file-information APIs; their semantics must be tested under Wine rather than assumed.
4. Prove the running-game guard across prefixes. The current code enumerates Windows processes and compares executable directories. Wine prefix visibility may leave another prefix running the same client undetected. Resolve this before offering safe installation support; a successful same-prefix test alone is insufficient.
5. Run the fixture install/restore and interrupted-recovery matrix, then one clean anonymous GitHub download/install/rollback using exact release assets. Test TLS, redirects, resume, cancellation and offline recovery.
6. Follow with an in-game check in that same supported environment. Only then publish Wine instructions and a Lutris integration. Keep Proton and macOS explicitly unverified until their own checks pass.

Keep one set of immutable game assets on GitHub Releases. Do not add full clients, personal UI, or copies of every payload to the Git repository to enable another launcher. If Wine cannot satisfy the safety checks reliably, assess a native Linux installer around the same manifest and transaction rules as a separate implementation.

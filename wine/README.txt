Lau Setup for Wine on Linux
Author / Creator / Last Modified By: Neil Mitchell

1. Use an existing WoW 3.3.5a build 12340 client on a local Linux filesystem.
2. Close every WoW instance, including games in other Wine prefixes.
3. Extract this ZIP. Keep all four files together.
4. Open a terminal in the extracted folder and run:

   WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh

5. Choose your existing game folder and install. The usual automatic backups
   and Restore previous install button are available.

Requirements for this release:
- Wine 11.0, a 64-bit prefix, and Wine Mono 10.4.1 already installed there.
- Python 3.9 or newer for the host safety helper (standard library only).
- Liberation Sans or DejaVu Sans fonts; the complete Wine font package must
  also be installed so Wine Mono's own default controls can render.
- Local Linux storage. Network shares and Windows-mounted drives are excluded.
- Normal host process visibility. Do not run this launcher through a sandbox
  that hides other Wine processes. Run as your normal user, never sudo/root.

The 64-bit prefix can contain the 32-bit WoW client. This installer does not
create, convert or upgrade your Wine prefix, install Wine/Mono, configure
DXVK, or change your game launcher. Use your distribution's Wine setup
instructions first if its runtime is missing.

Official Wine Mono package for this tested runtime:
https://github.com/wine-mono/wine-mono/releases/tag/wine-mono-10.4.1

Use the Wine Mono runtime with Wine. The Windows .NET Framework installer is
not bundled and is not required by this tested Wine Mono configuration.

Always launch through LauSetup.sh. Running LauSetup.exe directly under Wine
will refuse client operations without the Linux helper. It checks host paths
and processes and holds a host lock shared across Wine prefixes. If it stops,
reopen the launcher and restore the pending installation before trying again.

Keep WoW closed until setup finishes. Process checks reduce races; they cannot
stop another program from launching the game or changing files afterward.
Symlinked paths, hardlinks and ambiguous filename casing are rejected. Data
and backup directories must remain on the same filesystem as the client.

Validation scope: isolated Wine 11.0 / Wine Mono 10.4.1 clients, fixture and
real-payload install/restore tests, two-prefix safety tests and sampled GUI
checks. This is not certification of every Linux distribution, filesystem,
display scale, Wine version, or game encounter. No Lutris, Proton or macOS
integration is included in this release.

The installer interface is English. Client game data supports all nine
existing locales and is selected from the detected game locale.

Setup 1.1.6: New spell visuals off keeps Patch-S as .mpq.disabled next to
its original path. A different disabled copy is never overwritten.
To undo the complete install, use Restore previous install. For files
already removed by older setup versions, recover them from those backups
using Restore previous install before reinstalling. Keep LauSetupBackups.

The current S file always becomes .mpq.disabled. If an older disabled
copy exists, Setup first preserves it as .mpq.disabled.<12-character hash>. No manual rename
is needed to switch options. Re-enabling manually requires removing
.disabled and any following hash, with WoW closed and no different active
file being overwritten. Use Restore previous install for managed rollback.

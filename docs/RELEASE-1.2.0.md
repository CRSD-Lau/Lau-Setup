# Lau Setup 1.2.0

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell

Lau Setup **1.2.0** is a new release with one `LauSetup.zip` containing the Windows installer, the Linux/Wine launcher and the same bundled translations used by both.

- Windows users open `LauSetup.exe`. Linux users run `LauSetup.sh` in their existing supported Wine environment.
- The built-in **Interface language** selector changes setup text immediately and remembers a manual choice. **Automatic** follows the Windows display language or Linux host language preferences again.
- On Linux, `--language <code>` selects and saves the same manual choice; `--language auto` saves Automatic. The selector remains the normal way to change it after setup opens.
- Ten interface options: English, German, French, Spanish (Spain), Spanish (Mexico), Korean, Russian, Simplified Chinese, Traditional Chinese and Brazilian Portuguese.
- Interface language is independent of WoW client language. The existing client inspection still determines the correct game patches.
- Translations are bundled; the installer makes no translation-service requests. The initial translations are machine-assisted and remain open to fluent-reader corrections.

The full translated-guide refresh remains pending because Google returned HTTP 429 during the external smoke check. All 117 snapshot notices were updated, and the English guides are current.

Linux still requires Wine 11.0, Wine Mono 10.4.1, a 64-bit prefix, Python 3.9 or newer, the documented fonts and a supported local Linux filesystem. Korean and Chinese UI text needs Wine-visible Noto Sans CJK fonts (`fonts-noto-cjk` on typical Debian/Ubuntu systems), which Lau Setup auto-selects when installed. Lau Setup does not install fonts or other prerequisites. Existing process, path, backup and recovery checks remain in place.

## DBC changes

No DBC edits. Game release 3.0.8 and all game asset hashes remain unchanged. This release changes the installer interface, language preferences and download packaging only.

## Validation

The accompanying `VALIDATION.json` and `SHA256SUMS.txt` provide the exact build evidence. Validation passed 62 Windows and 62 Wine regression groups; Wine's 35 pre-fix groups plus the affected GUI group and remaining 26 post-fix groups; 50 Windows and 21 normal-user Wine interface states; 185 translation keys in all ten languages; and 31 package, translation, and host tests. All ten interface languages are included, but fluent human review remains the limit for translation quality. Interface validation does not certify every Linux distribution, display configuration, translation nuance, or in-game encounter.

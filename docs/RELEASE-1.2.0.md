# Lau Setup 1.2.0

Author: Neil Mitchell
Creator: Neil Mitchell
Last Modified By: Neil Mitchell

One local candidate `LauSetup.zip` contains the Windows installer, the Linux/Wine launcher and the same bundled translations used by both. Public release links remain on 1.1.8 until this candidate completes separate release validation and publishing.

- Windows users open `LauSetup.exe`. Linux users run `LauSetup.sh` in their existing supported Wine environment.
- The interface follows the Windows display language or Linux host language preferences automatically.
- `--language <code>` selects and saves a manual choice. `--language auto` saves Automatic and follows the system again.
- Ten interface options: English, German, French, Spanish (Spain), Spanish (Mexico), Korean, Russian, Simplified Chinese, Traditional Chinese and Brazilian Portuguese.
- Interface language is independent of WoW client language. The existing client inspection still determines the correct game patches.
- Translations are bundled; the installer makes no translation-service requests. The initial translations are machine-assisted and remain open to fluent-reader corrections.

Linux still requires Wine 11.0, Wine Mono 10.4.1, a 64-bit prefix, Python 3.9 or newer, the documented fonts and a supported local Linux filesystem. Korean and Chinese UI text needs Wine-visible Noto Sans CJK fonts (`fonts-noto-cjk` on typical Debian/Ubuntu systems), which Lau Setup auto-selects when installed. Lau Setup does not install fonts or other prerequisites. Existing process, path, backup and recovery checks remain in place.

## DBC changes

No DBC edits. Game release 3.0.8 and all game asset hashes remain unchanged. This release changes the installer interface, language preferences and download packaging only.

## Validation

See the accompanying `VALIDATION.json` and `SHA256SUMS.txt` for the exact build and validation evidence. All ten interface languages are included, but fluent human review remains the limit for translation quality. Interface validation does not certify every Linux distribution, display configuration, translation nuance or in-game encounter.

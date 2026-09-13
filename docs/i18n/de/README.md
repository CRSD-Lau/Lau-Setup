<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Automatische Übersetzung. [Englische Quelle](../../../README.md). Bei abweichenden Formulierungen ist die englische Quelle maßgeblich.

<p align="center">
  <a href="https://wrath-multilingual-hd.vercel.app/"><img src="../../assets/social-preview.png" alt="Wrath HD — gold W shield on an icy blue background" width="100%" /></a>
</p>

<h1 align="center">Lau Setup</h1>
<p align="center"><strong>Ihr Kunde. Deine Sprache. Ihr Wrath.</strong><br />Das Windows- und Linux/Wine-Installationsprogramm für das visuelle Upgrade von Lau.</p>
<p align="center">
  <a href="https://github.com/CRSD-Lau/Lau-Setup/releases/latest">Neueste Veröffentlichung</a> ·
  <a href="https://wrath-multilingual-hd.vercel.app/">Website & Galerie</a> ·
  <a href="https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose">Melden Sie ein Problem</a>
</p>

---

Mehrsprachiger Zaubertext, Breitbild-Ladegrafiken, benutzerdefinierte Bodenindikatoren und optionale HD-Karten für **WoW 3.3.5a, Build 12340**. Wählen Sie Ihren bestehenden Kunden und Ihr Bildmaterial; Lau Setup lädt die erforderlichen Dateien herunter, überprüft sie, platziert die Patches und sichert die Originale.

**Installer 1.1.7 · Spielveröffentlichung 3.0.8 Lau · Neun Client-Sprachen**

<a id="patch-s-stays-recoverable"></a>

## Patch-S bleibt wiederherstellbar

**Setup 1.1.7 Hotfix:** Durch das erneute Aktivieren neuer Zaubervisualisierungen wird ein passender deaktivierter Patch-S wiederverwendet und die einfache deaktivierte Kopie in `LauSetupBackups` verschoben, sodass Daten kein aktives/deaktiviertes Duplikat behalten. Im Transaktions-Backup bleiben unterschiedliche Kopien erhalten. Beim Ausschalten wird weiterhin `.mpq.disabled` verwendet. Verwenden Sie zur Wiederherstellung **Vorherige Installation wiederherstellen**.

<a id="90-breath-and-slime-spray-warnings"></a>

## 90° Atem- und Schleimspray-Warnungen

**3.0.8 Lau:** Alle unterstützten Atemindikatoren und Rotface Slime Spray sind **90° insgesamt**, nach Warmane Testerbestätigung. Deckt Halion in beiden Reichen ab: Saviana Ragefire, Sartharion, ICC Rimefang und Sindragosa. Reichweite und Animations-Timing bleiben erhalten. Der genehmigte größere Halion-Meteorfeuerradius und die hellblaue Kaltflamme bleiben unverändert.

**Bereits installiert?** Laden Sie zuerst **Setup 1.1.7** herunter, wählen Sie denselben Ordner und dasselbe Bildmaterial aus und installieren Sie es dann. Das Setup überprüft die tatsächlichen SHA-256-Hashes: Selbst eine Änderung um ein Byte mit derselben Größe und demselben Zeitstempel wird erkannt. Nur passende neue Dateien gelten als bereits installiert. `/pyversion` meldet **3.0.8 Lau**. Alte Installationsprogramme behalten ihren alten eingebetteten Katalog.

[Animierte Farbvorschauen und Änderungsprotokoll](https://wrath-multilingual-hd.vercel.app/#changelog)

<a id="download"></a>

## Herunterladen

| Windows | Linux / Wine |
| :--- | :--- |
| **[LauSetup.exe herunterladen](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.exe)** | **[LauSetup-Wine.zip herunterladen](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup-Wine.zip)** |
| Windows 10 / 11 · .NET Framework 4.8 | Wine 11.0 · Wine Mono 10.4.1 · 64-bit Präfix |
| Über **156 KB** | Über **80 KB** · Python 3.9+ |
| [Windows-Anleitung](START-HERE.md) | [Wine Anleitung und Voraussetzungen](wine/README.md) |

Spieledateien werden während der Einrichtung heruntergeladen. Eine englische Kerninstallation kostet etwa **472 MB** bei HD-Modellen und neuen Zaubervisualisierungen oder **259 MB** bei Originalmodellen. Optionale Karten führen zu einem größeren Download; Das Setup zeigt die Gesamtsumme vor der Installation an.

[SHA-256 Prüfsummen](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/SHA256SUMS.txt) · [Versionshinweise](https://github.com/CRSD-Lau/Lau-Setup/releases/latest) · [Validierungsbericht](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/VALIDATION.json)

> **Bringen Sie Ihren vorhandenen Client mit.** Dies ist ein Upgrade, kein vollständiger Spielclient, Sprachpaket oder HD-Modellbasis. Laufzeitinstallationsprogramme sind nicht im Paket enthalten. Die Benutzeroberfläche des Installationsprogramms ist Englisch. Der Spielinhalt unterstützt neun Gebietsschemas.

<a id="one-setup-the-details-handled"></a>

## One setup. The details handled.

| Choose your visuals | Behalten Sie die Kontrolle über Ihre Installation |
| :--- | :--- |
| Erweiterte oder serienmäßige Weihe | Client-Sprach- und Modellerkennung |
| Neue Zaubervisualisierungen für kompatible HD-Clients | Nur die erforderlichen Dateien heruntergeladen |
| Optionale HD-Karten und Minikartentexturen | SHA-256 Überprüfung vor der Installation |
| Regionales Widescreen-Bild wird geladen | Automatische Backups und fortsetzbare Downloads |
| Lokalisierte Zaubernamen, Ränge und Tooltips | Wiederherstellung und Wiederherstellung bei unterbrochenem Betrieb |

<p align="center"><img src="../../assets/installer-windows.png" alt="Lau Setup on Windows: choose a WoW folder, select visuals, install or restore" width="836" /></p>

Ihre Add-ons, SavedVariables, Schriftarten, Login-Grafiken, Realm-Einstellungen und nicht verwandte Patches bleiben erhalten. Es sind keine persönliche Benutzeroberfläche, Anmeldeinformationen oder Analysen enthalten.

<a id="get-started"></a>

## Fangen Sie an

1. **Schließen Sie WoW vollständig.** Schließen Sie auf Wine jede WoW-Instanz über alle Präfixe hinweg.
2. **Starten Sie das Setup und wählen Sie Ihren Client-Ordner.** Windows: Öffnen Sie `LauSetup.exe`. Linux: Extrahieren Sie alle vier Dateien aus der ZIP-Datei Wine und verwenden Sie den Launcher unten.
3. **Wählen Sie Ihr Bildmaterial und installieren Sie es.** Enhanced Consecration startet aktiviert; Deaktivieren Sie es für die Standarddarstellung. Neue Zaubervisualisierungen erfordern eine kompatible HD-Modellbasis. Karten sind optional.
4. **Starten Sie WoW und führen Sie `/pyversion` aus.** Bestätigen Sie die installierte Edition, bevor Sie mit dem Spiel beginnen.

Führen Sie auf Linux Folgendes aus dem extrahierten Ordner mit Ihrem vorhandenen Präfix aus:

```sh
WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh
```

Verwenden Sie den Launcher als Ihr normaler Benutzer. Es überprüft Linux-Pfade, laufende Spiele, freien Speicherplatz und Installationssperren über Präfixe hinweg. Verwenden Sie den lokalen Linux-Speicher. Verknüpfte Ordner, Netzwerkfreigaben und mit Windows bereitgestellte Laufwerke werden nicht unterstützt. Das [Wine-Handbuch](wine/README.md) listet Schriftarten und alle Voraussetzungen auf.

Auf Windows bietet das Setup die offizielle .NET Framework 4.8-Downloadseite von Microsoft an, wenn die Laufzeit fehlt. Die getestete Wine-Konfiguration verwendet **Wine Mono**, nicht das Windows .NET-Installationsprogramm.

<a id="nine-client-languages"></a>

## Neun Clientsprachen

Englisch · Französisch · Deutsch · 한국어 · Russisch · 简体中文 · 繁體中文 · Español (España) · Español (México)

`enUS` · `frFR` · `deDE` · `koKR` · `ruRU` · `zhCN` · `zhTW` · `esES` · `esMX`

Das Setup richtet sich nach dem aktiven Gebietsschema Ihres Clients. Installieren Sie die entsprechenden Sprachdateien und Schriftarten, bevor Sie die Konfiguration ändern. Durch die alleinige Änderung eines Konfigurationswerts wird kein Sprachpaket installiert.

<a id="restore-with-your-backups"></a>

## Mit Ihren Backups wiederherstellen

Schließen Sie WoW, öffnen Sie das Setup erneut über denselben Launcher, wählen Sie denselben Client aus und wählen Sie **Vorherige Installation wiederherstellen**. Bewahren Sie `LauSetupBackups` im Client-Ordner auf: Er enthält die Originale und Wiederherstellungsdatensätze.

Eine unterbrochene Installation oder Wiederherstellung kann auch dann wiederhergestellt werden, wenn `WoW.exe` vorübergehend fehlt. Wenn ein anderes Update die installierten Dateien geändert hat, stoppt die Wiederherstellung und behält die Sicherung zur Auflösung bei. Sobald dieses Installationsprogramm das Karten-Upgrade hinzufügt, behält es es bei Editionsänderungen bei; Stellen Sie die vorherige Installation wieder her, um das Upgrade rückgängig zu machen.

<a id="tested-with-clear-limits"></a>

## Getestet, mit klaren Grenzen

Release 1.1.7 hat **50-Regressionsgruppen auf Windows und auf Wine** bestanden, einschließlich 108-Gebietsschema-/Edition-/Kartenplänen pro Plattform. Die Spielversion 3.0.8 hat zuvor auf beiden Plattformen sechs Editions-Upgrades und eine Ein-Byte-Erkennung bestanden; seine Nutzlasten bleiben unverändert. Das Setup 1.1.7 deckt auch die Sequenz „All-Flags-On“ bis „New Spells Off“ mit älteren deaktivierten Kopien, wiederholten Wechseln und exaktem Rollback ab. Öffentliche Nutzlasten wurden anonym heruntergeladen und Hash-verifiziert; Die tatsächliche Kerninstallation und das Rollback wurden getestet.

Wine wurde mit **Wine 11.0 / Wine Mono 10.4.1** auf lokalem Linux-Speicher getestet, einschließlich des mitgelieferten Launchers als normaler Benutzer. Die Halion-Meteorfeuer-Geometrie entspricht genau der vom Tester genehmigten Version 2. Coldflame, Animationsspuren, natives Feuer und Zaubertabellen bleiben byteidentisch mit 3.0.7. Website-Animationen sind illustrative Modelle. Diese Tests zertifizieren nicht jede Linux-Distribution oder jede Begegnung im Spiel.

Lutris-, Proton- und macOS-Integrationen sind nicht in dieser Version enthalten. Die ausführbare Datei ist nicht digital signiert.

<a id="known-limitations-and-feature-requests"></a>

## Bekannte Einschränkungen und Funktionswünsche

Lesen Sie [Bekannte Einschränkungen und Annahmen](KNOWN-LIMITATIONS.md), bevor Sie eine Funktion vorschlagen: Warmane Serversteuerung, DLL-/Native-Code-Bereich, geschützte Lua-Aktionen, Indikatorgenauigkeit und -timing, DBC-Abhängigkeiten und Plattform-/Wiederherstellungsgrenzen.

<a id="for-contributors"></a>

## Für Mitwirkende

- [Build, Archivplatzierung und Wiederherstellungsdesign](docs/TECHNICAL.md)
- [Beitrag und Anleitung zum Fehlerbericht](CONTRIBUTING.md)
- [Implementierungsüberprüfung](REVIEW.md)
- [Plattformumfang und Machbarkeit](PLATFORM-FEASIBILITY.md)

Spielnutzlasten werden über GitHub-Releases verteilt. Dieses Repository enthält die Quelle, den Katalog, den Launcher und die Dokumentation des Installationsprogramms. Sie müssen es nicht klonen, um das Upgrade zu installieren.

<a id="built-on-community-work"></a>

## Aufbauend auf Gemeinschaftsarbeit

**Andre** – Patch-Y-Grundlinien · **Loriendal & Trimitor** – HD-Client-Grundlage · **Project Reforged-Mitwirkende** – HD-Grafik · **Blizzard** – Originalspiel, Grafik und lokalisierter Text · **Lau** – Bodenindikatoren, Kompatibilität, Anpassungen, Test- und Freigabewerkzeuge.

[Vollständige Credits](https://wrath-multilingual-hd.vercel.app/credits) · [Screenshots und Installationshilfe](https://wrath-multilingual-hd.vercel.app/)

<sub>Inoffizielles Community-Projekt. Nicht verbunden mit oder unterstützt von Blizzard Entertainment. Originalspiele und Kunstwerke Dritter bleiben Eigentum ihrer jeweiligen Eigentümer.</sub>

<a id="dbc-change-tracking"></a>

## DBC-Änderungsverfolgung

Im [DBC-Änderungsprotokoll](DBC-CHANGELOG.md) finden Sie individuelle Tabellen-/Datensatz-/Feldbearbeitungen und Vergleichsnachweise. **3.0.7 → 3.0.8 hatte keine DBC-Änderungen**: Durch die Aktualisierung des Indikators 90° wurde die Modellgeometrie geändert. Setup 1.1.5–1.1.7 lässt auch die DBC-Daten unverändert.

<!-- LANGUAGES:START -->
[English](../../../../README.md) · [Deutsch](../README.md) · [Español (España)](../../es-ES/README.md) · [Español (México)](../../es-MX/README.md) · [Français](../../fr/README.md) · [한국어](../../ko/README.md) · [Русский](../../ru/README.md) · [简体中文](../../zh-CN/README.md) · [繁體中文](../../zh-TW/README.md) · [Português (Brasil)](../../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- HOTFIX-118-NOTICE -->
> **Hotfix 1.1.8** — Setup prüft MPQs in Data und im aktiven Sprachordner auf bekannte umbenannte Patch-Y-Dateien und exakte Katalogkopien. Bei einem möglichen Konflikt oder einem nicht lesbaren bzw. nicht unterstützten Archiv stoppt es und nennt die Datei; es löscht sie nicht automatisch. Nur den Dateinamen zu ändern verändert den Inhalts-Hash nicht. Die Spieldateien bleiben auf 3.0.8.
>
> Die vollständige Übersetzung konnte wegen einer Google-Anfragebegrenzung noch nicht aktualisiert werden. Der bisherige Text unten ist ein älterer Stand. Maßgeblich sind die aktuellen englischen Angaben. [English](../../../TECHNICAL.md) · [1.1.8](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.1.8)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Automatische Übersetzung. [Englische Quelle](../../../TECHNICAL.md). Bei abweichenden Formulierungen ist die englische Quelle maßgeblich.

<a id="technical-reference"></a>

# Technische Referenz



[Zurück zu Lau Setup](../README.md)

<a id="build-and-verification"></a>

## Erstellen und Verifizieren

Führen Sie `tools/build.ps1` auf Windows mit installiertem .NET Framework-Compiler aus. Das öffentliche Quellpaket enthält die Anwendung, den eingebetteten Katalog, das Build-Skript und die Dokumentation. Der vollständige Entwicklungscheck enthält außerdem `tools/test.ps1` für Transaktions-, Download-, Pfad-, Prozess-, Wiederherstellungs- und GUI-Regressionstests; Diese Tests verwenden isolierte Geräte und eine lokale ausführbare Referenzdatei. `tools/build.ps1 -Release` lehnt einen Katalog ab, der das Veröffentlichungstor nicht passiert hat. Die Testumgebung, die Nutzlastgenerierung und die nativen Spieletests hängen von privaten lokalen Quellpfaden ab und sind nicht Teil des öffentlichen Quellpakets.

`build/catalog.json` benennt jedes Asset und Download-Segment nach Größe und SHA-256, zusammen mit den beobachteten GitHub Release-URLs. Der Katalog pinnt das Repository, das Release-Tag und die mit einem Hash versehene Datei. Das Installationsprogramm lädt anonym herunter und überprüft jede Weiterleitung, bevor es ihr folgt. Für das Installationsprogramm sind weder ein GitHub-Konto noch ein angemeldeter Browser oder API-Anmeldeinformationen erforderlich. Beim vollständigen Entwicklungs-Checkout ordnet `tools/refresh_github_catalog.py` hochgeladene Assets zu, ohne Hashes zu ändern, und `tools/verify-public.ps1` überprüft jedes Segment und rekonstruierte Asset über denselben Downloader, der von der App verwendet wird.

<a id="file-placement"></a>

## Dateiplatzierung

| Komponente | Ziel |
|---|---|
| Kompatible ausführbare Datei | `WoW.exe` |
| Ausgewählte regionale Q | Identische Kopien im Stammverzeichnis `Data/patch-q.mpq` und im aktiven Gebietsschema `Data/<locale>/patch-<locale>-Q.MPQ` |
| Ausgewählte Ausgabe Y | Identische Kopien im Stammverzeichnis `Data/patch-y.mpq` und im aktiven Gebietsschema `Data/<locale>/patch-<locale>-Y.MPQ` |
| Neue Zauberressourcen, wenn ausgewählt | Root `Data/patch-s.mpq` |
| Passende lokalisierte Buchstabiertabellen, wenn ausgewählt | Aktives Gebietsschema `Data/<locale>/patch-<locale>-S.MPQ` |
| Optionale Karten/Minikarte | Root `Data/patch-m.mpq`; das ersetzte aktive Gebietsschema M wird gesichert |

Core Q behält das LoadingScreens.dbc der Version, das lokalisierte Map.dbc und lädt Bilder Byte für Byte. Die hinzugefügten Weltkartendefinitionen und Weltkartengrafiken werden weggelassen. Der vollständige Kartenmodus verwendet das ursprüngliche regionale Q und das gemeinsame M, ohne sie neu zu packen. Die beiden S-Platzierungen enthalten unterschiedliche Archive. Durch das Deaktivieren neuer Zauber bleibt das S-Paar aus Root und Gebietsschema mit Gültigkeitsbereich als .mpq.disabled erhalten. Durch die erneute Aktivierung werden die einfach deaktivierten Kopien in verifizierte Transaktionssicherungen verschoben, wie im Abschnitt „Setup 1.1.7“ weiter unten beschrieben. Für die HD-Erkennung sind die passenden vorhandenen Root- und Locale-F-Patches erforderlich.

<a id="recovery-design"></a>

## Wiederherstellungsdesign

Eine Client-Sperre umfasst Download, Staging und Installation. Dateien werden vor der Bereitstellung und erneut nach der Platzierung überprüft. Vorhandene Dateien werden nach `LauSetupBackups/transactions/<id>/before/` verschoben, wobei ihre Bytes und Zeitstempel erhalten bleiben. Das Tagebuch wird dauerhaft geschrieben, bevor es festgeschrieben wird. Bei einem fehlgeschlagenen Commit werden die Originale wiederhergestellt, wenn sie sicher sind. Unterbrochene Commits und unterbrochene Wiederherstellungen bleiben auch ohne WoW.exe erkennbar, wenn die App erneut geöffnet wird.

Die Wiederherstellung lehnt Dateien ab, die durch ein anderes Update geändert wurden, und behält die Sicherung zur manuellen Auflösung bei. Es werden nur genaue Q/M/S/Y-Pfade für Root/aktives Gebietsschema und WoW.exe akzeptiert. Durchquerung, alternative Streams und Analysepunkte werden abgelehnt; Beschreibbare fortgesetzte Dateien müssen einen Hardlink haben. Journal- und Assembly-Provisorien verwenden eindeutige Namen und exklusive Erstellung. Die Anwendung listet niemals ein Archiv im Client-Dateisystem auf.

<a id="release-boundaries"></a>

## Grenzen freigeben

Dieses Installationsprogramm ist nicht digital signiert. Windows- und Wine-Installationstests, Stichproben-GUI-Prüfungen und die gespeicherte Spieldatenbasis werden separat in VALIDATION.json aufgezeichnet. Wine 1.1.0-Prüfungen verwenden Wine 11.0 / Wine Mono 10.4.1 und lokalen Docker-Overlay-Speicher; Der Nested-Mount-Test verspottet die Geräteidentität, da dieser Container keine Mounts erstellen kann. Diese Prüfungen zertifizieren nicht jede Linux-Distribution/Dateisystem, Anzeigeskala, Begegnung oder Client-Änderung von Drittanbietern. Rohe ZIPs der Patch-Y-Edition sind in GitHub-Releases verfügbar. Aktuellen Umfang und Annahmen finden Sie unter [bekannte Einschränkungen](../KNOWN-LIMITATIONS.md).


<a id="306-color-update--setup-112"></a>

## 3.0.6 Farbaktualisierung / Setup 1.1.2

Jedes der sechs Y-Archive ändert drei M2-Mitglieder und das !PYAndre-TOC und fügt zwei BLP-Texturen hinzu. `Spells/PW_Coldflame_Ground.m2` verweist jetzt auf `Spells/PW_Coldflame_Blue.blp`; `Spells/PW_HalionMeteor_Ground.m2` und `Spells/PW_HalionMeteor_Ring.m2` Referenz `Spells/PW_Halion_Red.blp`. Lediglich die Dateinamenlänge/-offset des Texturdeskriptors 4 ändert sich in jedem Originalmodell; Der neue Pfad wird angehängt. Native Partikeltexturen (Indizes 0–3), Skins, Geometrie, globale Animationsspuren, Grenzen und DBC-Bytes bleiben unverändert. Die gemeinsame weiße Textur bleibt für andere Indikatoren unverändert.

Die neuen Texturen behalten das bestehende undurchsichtige 8×8 DXT1 BLP2-Format und alle vier Mip-Ebenen bei. Nur der RGB565-Endpunkt ändert sich: Hellblau dekodiert als (120,216,248,255), Rot als (248,68,40,255). Die Quantisierung ist dem vorhandenen Texturformat eigen. Beide Halion-Modelle verwenden die gleiche rote Textur. Die Wahl der Weihe und der Modellausgabe bleibt unabhängig.

Bei Update-Entscheidungen werden tatsächliche SHA-256 und Größe verglichen, nicht Release-Labels oder Zeitstempel. Regressionstests ändern ein Byte, ohne die Dateigröße oder den Zeitstempel in jeder Y-Platzierung zu ändern, erfordern genau einen Reparaturvorgang, überprüfen den reparierten Hash und stellen dann die vorherige Version wieder her. Eine alte EXE-Datei bettet den alten Katalog ein, sodass für ein Upgrade zunächst die neue EXE/ZIP-Datei heruntergeladen werden muss.

<a id="307-halion-radius--setup-113"></a>

## 3.0.7 Halion-Radius / Setup 1.1.3

Fördert exakte Test-v2-Bytes für `Spells/PW_HalionMeteor_Ground.m2`, `Spells/PW_HalionMeteor_Ring.m2` und ihre `00.skin`-Dateien. Die X/Y-Koordinaten des Netzes sind 1.5 mal 3.0.6. Z/UVs/Normalen und Animationen/Partikelspuren bleiben erhalten. Modellgrenzen (Offset 160), Sequenzgrenzen (Sequenz +32) und Skin-Submesh-Grenzen (Submesh +20) spiegeln die vergrößerte Geometrie wider. Die TOC-Version ändert sich von 3.0.6 zu 3.0.7. Pro Ausgabe wechseln genau fünf bestehende Mitglieder; Keine hinzugefügten oder entfernten Mitglieder. Test-v3-Geometrie ist ausgeschlossen. Coldflame und alle anderen Mitglieder stimmen mit 3.0.6 überein. Vom Benutzer weitergeleitete Testerakzeptanz von v2; Eine breite Begegnungszertifizierung wird nicht beansprucht.

<a id="308-all-cones--setup-114"></a>

## 3.0.8 alle Kegel / Setup 1.1.4

Alle sechs Editionen verwenden die gesamte Lüftergeometrie 90. Die Dateinamen älterer Modelle und alle DBC-Zeilen bleiben unverändert, um die Zauberweiterleitung beizubehalten. Änderungen: PW_White_Fan60_60yd_Glowing (Halion beide Reiche), PW_White_Fan60_30yd_Glowing (Saviana), PW_White_Fan60_100y_Glowing (ICC Rimefang) und PW_Rotface_SlimeSpray_Fan25_Room (Rotface) erweitern von 60 an 90; PW_White_Fan82_60yd_Glowing (Sartharion) erweitert sich von 82 auf 90. PW_White_Fan75_60yd_Glowing (Sindragosa) ist bereits 90 und byteidentisch.

Für jedes geänderte Modell ändern sich nur der Scheitelpunkt XY (48-Byte-Scheitelpunktschritt) und die Grenzen. Winkel um +X skaliert nach 90/old-angle; Jeder Scheitelpunktradius und Z bleiben erhalten. Modellgrenzen bei Offset 160, Sequenzgrenzen bei sequence+32 und Skin-Submesh-Grenzen bei submesh+20 werden aktualisiert. UVs, Normalen, Animationen und Partikelspuren bleiben unverändert. Zehn Modell-/Skin-Mitglieder und zwei Versionszeichenfolgen im Inhaltsverzeichnis ändern sich pro Edition; Es werden keine Mitglieder hinzugefügt oder entfernt. Alle anderen Mitglieder, einschließlich der Geometrie von Halion meteor-fire test-v2 und Coldflame, stimmen Byte für Byte mit 3.0.7 überein.

<a id="setup-115-disabled-patch-s-preservation"></a>

## Setup 1.1.5 hat die Patch-S-Erhaltung deaktiviert

Nur Root- und Active-Locale-S-Pfade erhalten das Suffix .disabled. Bei jeder Deaktivierung wird vor der Deaktivierung von S eine mit einem Hash versehene, lokal bereitgestellte Kopie erstellt. Beide Wege sind mit höchstens elf Zielen protokolliert. Rollback stellt die ursprünglichen aktiven Dateien wieder her und entfernt nur neu erstellte deaktivierte Kopien. Bereits vorhandene identische deaktivierte Kopien bleiben außerhalb der Transaktion und bleiben erhalten. Widersprüchliche Dateien oder Verzeichnisse blockieren die Planung. Durch die erneute Aktivierung werden Katalog-S-Assets installiert und die deaktivierten Kopien werden nicht verbraucht. Bestehende Zeitschriften bleiben weiterhin lesbar. Es werden keine willkürlichen lokalen Quellpfade akzeptiert: Jede lokale Kopie muss mit ihrer gepaarten S-Deaktivierungsoperation übereinstimmen.

<a id="setup-116-disabled-copy-collisions"></a>

## Setup 1.1.6 Kollisionen beim Kopieren deaktiviert

Die aktuell aktive S-Datei erhält immer den einfachen Namen .mpq.disabled. Bevor eine andere vorhandene deaktivierte Datei ersetzt wird, stellt Setup deren Bytes in eine Geschwisterdatei um, die mit den ersten 12-Zeichen ihrer SHA-256 endet. Der vollständige SHA-256 und die Länge werden vor jeder Wiederverwendung überprüft. Dadurch bleiben Namen innerhalb der bestehenden Windows-Pfadgrenzen. Widersprüchliche Archivinhalte können nicht geschlossen werden. Das aktive S, die einfach deaktivierte Datei und die neu erstellte Archivkopie werden unabhängig voneinander mit höchstens dreizehn Einträgen protokolliert. Rollback stellt alle Originale wieder her. Lokale Quellen sind auf gepaarte S-Deaktivierungs- oder Disabled-File-Ersetzungsvorgänge beschränkt. Alte Zeitschriften bleiben lesbar.

<a id="setup-117-re-enable-cleanup"></a>

## Setup 1.1.7 Bereinigung wieder aktivieren

Durch das Aktivieren neuer Zauberjournale werden die einfachen Root- und Active-Locale-deaktivierten S-Dateien entfernt. Die Transaktion verschiebt ihre verifizierten Originalbytes vor der Sicherung außerhalb der Daten. If a disabled file matches the catalog SHA-256 and size, it is staged locally for the matching S destination and excluded from downloads. Lokale Quellen müssen mit dem genauen Deaktivierungsdateientfernungs- und Katalog-Asset gepaart werden. Active S, das bereits übereinstimmt, erzeugt immer noch eine Bereinigungstransaktion. Vorhandene Archive mit Hash-Suffix werden nicht bereinigt. Vorherige Zeitschriften bleiben weiterhin lesbar. Ein/Aus/Ein, Quelldrift, Unterbrechungen bei jedem neuen Festschreibungs-/Wiederherstellungsschritt, alle Gebietsschemas und gestapelte Wiederherstellung werden abgedeckt.

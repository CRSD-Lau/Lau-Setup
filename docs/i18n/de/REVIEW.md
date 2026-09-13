<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- HOTFIX-118-NOTICE -->
> **Hotfix 1.1.8** — Setup prüft MPQs in Data und im aktiven Sprachordner auf bekannte umbenannte Patch-Y-Dateien und exakte Katalogkopien. Bei einem möglichen Konflikt oder einem nicht lesbaren bzw. nicht unterstützten Archiv stoppt es und nennt die Datei; es löscht sie nicht automatisch. Nur den Dateinamen zu ändern verändert den Inhalts-Hash nicht. Die Spieldateien bleiben auf 3.0.8.
>
> Die vollständige Übersetzung konnte wegen einer Google-Anfragebegrenzung noch nicht aktualisiert werden. Der bisherige Text unten ist ein älterer Stand. Maßgeblich sind die aktuellen englischen Angaben. [English](../../../REVIEW.md) · [1.1.8](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.1.8)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Automatische Übersetzung. [Englische Quelle](../../../REVIEW.md). Bei abweichenden Formulierungen ist die englische Quelle maßgeblich.

<a id="installer-review"></a>

# Überprüfung durch den Installateur

Autor: Neil Mitchell  
Ersteller: Neil Mitchell  
Zuletzt geändert von: Neil Mitchell

Überprüfung der neuen Anwendung anhand der GStack-Überprüfungscheckliste, einschließlich einer unabhängigen schreibgeschützten Sicherheitsüberprüfung. Alle identifizierten Implementierungsprobleme wurden im Rahmen der Arbeit des autorisierten Installateurs behoben:

– Eine fehlende ausführbare Datei könnte die Auswahl des Clients für die Wiederherstellung nach einem Absturz verhindern. Die Ordnerauswahl erkennt und validiert jetzt Wiederherstellungsdatensätze, bevor WoW.exe überprüft wird. Ein GUI-Regressionstest deckt den Fall fehlender ausführbarer Dateien ab.
- Downloads erfolgten vor der Betriebssperre. Eine Miete deckt nun den Download-Cache durch Commit ab; Die ausstehende Wiederherstellung wird in diesem Mietvertrag überprüft.
- Vorhersehbare beschreibbare temporäre Dateien könnten NTFS-Hardlinks folgen. Journal- und Assembly-Provisorien verwenden jetzt GUID-Namen mit CreateNew. Wiederaufgenommene Teildateien werden ausschließlich geöffnet und ihre Linkanzahl wird vor dem Abschneiden oder Schreiben überprüft. Ein tatsächlicher Hardlink-Regressionstest beweist, dass die nicht verwandte Datei unverändert bleibt.
– Ein manipuliertes Wiederherstellungsjournal könnte vor der Validierung eine Sperre unter einem anderen Root erstellen. Größe, Speicherort, Stammverzeichnis, Gebietsschema, Einträge und bereichsbezogene Pfade werden jetzt überprüft, bevor die Wiederherstellungssperre erworben wird. Ein Regressionstest beweist, dass keine Fremdsperre erstellt wird.
- Die unterbrochene Wiederherstellung hatte keinen eigenen fortsetzbaren Zustand. WIEDERHERSTELLUNG wird vor der Mutation protokolliert und in der gesamten Benutzeroberfläche und im Wiederherstellungspfad erkannt. Fehlerinjektion nach jedem erfolgreichen Wiederherstellungsschritt.
- Installierte/wiederhergestellte Kartenoptionen könnten in der Benutzeroberfläche veraltet bleiben. Die Clienterkennung wird nach jedem erfolgreichen Vorgang aktualisiert. Der GUI-Test installiert die Kartenauswahl, überprüft ihren beibehaltenen Zustand, stellt den vorherigen Zustand wieder her und überprüft ihn.

Die GitHub-Migration fixiert zusätzlich das Repository, das Release-Tag und den Dateinamen im eingebetteten Katalog. Weiterleitungen werden manuell verfolgt, sodass jedes HTTPS-Ziel vor einer Anfrage überprüft wird, einschließlich Anmeldeinformationen und Portprüfungen. Der alte HTML-Bestätigungsparser von Google Drive wurde entfernt. Die hinzugefügten Tests umfassen die Manipulation von Katalog-URLs, eine umgeleitete fortsetzbare Übertragung und abgelehnte Umleitungsziele.

Eine unabhängige Überprüfung der Migration ergab, dass durch die Python-Optimierung als Behauptungen geschriebene Veröffentlichungsprüfungen entfernt werden konnten. Upload-, Katalogaktualisierungs- und Release-Gate-Prüfungen lösen jetzt explizite Ausnahmen aus. Der Uploader löst außerdem jede Quelle auf und verlangt, dass sie direkt im Payload-Verzeichnis verbleibt. Veröffentlichungsschutztests bestehen unter `python -O` für Dateipfade, Größen, Hashes und Remote-URL-/Digest-Manipulationen.

Neueste vollständige Regressionssuite: `reports/tests-20260911-200603/results.json`; 38-Testgruppen wurden bestanden, einschließlich 108-Kombinationen zur tatsächlichen Installation/Wiederherstellung von Fixtures, allen Festschreibungs-/Wiederherstellungsunterbrechungspunkten, Pfad-/Junction-/Hardlink-Schutz, Prozess- und Dateisperren, Korruption/Drift, HTTP-Bereichsbehandlung, Abbruch, Offline-Assemblierung und GUI-Installation/-Wiederherstellung unter Verwendung der echten versionierten ausführbaren Datei.

Die Überprüfung der 1.0.1-Benutzeroberfläche umfasst helleren unterstützenden Text, größeren Fußzeilentext und benutzerdefiniertes Malen mit deaktivierten Steuerelementen. Die native aktivierte Semantik bleibt bestehen. Nur das deaktivierte Erscheinungsbild wird manuell gezeichnet. Die ersten, fertigen und ausgelasteten Windows-Vorschauen wurden visuell überprüft. Core.cs, Downloader.cs und alle Spielnutzlasten bleiben byteidentisch mit v1.0.0. Seine Spiel-/Netzwerkbeweise bleiben erhalten; Die Windows-Regressionssuite wird für dieses Update erneut ausgeführt. Die Machbarkeitsprüfung Wine hat die Formkonstruktion nicht bestanden und stellt keine Plattformunterstützung her.

Veröffentlichungsprüfungen und endgültige binäre Metadaten sind separate Tore. Informationen zum Beweisumfang finden Sie in der Version VALIDATION.json, einschließlich der Überprüfungen, die aus der unveränderten Spielbasislinie übernommen wurden.

<a id="installer-110"></a>

## Installer 1.1.0

Der Wine-Implementierung folgten drei Stellungnahmen des Rates und zwei Peer-Reviews.
Es behält die C#-Transaktions-Engine bei und erfordert einen live authentifizierten Linux
Helfer für Wine Pfadinspektion, Host-Prozessprüfungen und präfixübergreifende Sperrung.
Der Helfer lehnt Links, mehrdeutige Groß- und Kleinschreibung, eingeschränkte Prozesssichtbarkeit usw. ab
nicht unterstützte Dateisysteme. Wine Laufwerkszuordnungen werden erst nach nativer Zuordnung akzeptiert
Zielinspektion. Die Prozessrichtlinie erfordert konservativ alle WoW
Instanzen, die geschlossen werden sollen. Wiederholte Kontrollen reduzieren Rennen; sie sperren nicht aus
Entfernen Sie nicht verwandte Programme oder beseitigen Sie schädliche gleichzeitige Dateisystemänderungen.

Die gezielte Überprüfung der Implementierung ergab eine verschachtelte Mount-Abdeckung und Sperrenfreigabe
nach einer Root-Umbenennung Lücken. Beide wurden behoben: verwaltete Pfade und deren nächstgelegene
Vorhandene Vorfahren müssen im lokalen Dateisystem des Clients verbleiben und freigegeben werden
verwendet den gespeicherten nativen Pfad und das Token, ohne dass der Root noch vorhanden sein muss.
Die entsprechenden nativen Tests bestehen.

Freiraumprüfungen fragen jetzt den tatsächlichen Linux-Cache und die Client-Dateisysteme ab.
anstelle des zugeordneten Laufwerksstammverzeichnisses von Wine. Aktuelle Wine Download- und Installationstests
Wenn kein freier Speicherplatz gemeldet wird, lehnen Sie den Vorgang ab und behalten Sie die Originaldateien bei.

Die Validierung umfasst die Gruppen 38 für Windows und 38 für native Hilfstests Wine, 15.
8 Wine Sicherheitsfälle einschließlich zwei Präfixen und Helferverlust nach einem Umzug, a
Neue anonyme GitHub-Installation/Rollback unter Wine und ein normaler Benutzer-Launcher
und Fixgeschäft. Der W-and-Shield ICO wird Byte für Byte aus dem kopiert
Favicon der vorhandenen Release-Site. UI-Snapshots umfassen „Initial“, „Ready“ und „Busy“.
Staaten; Der vorausgesetzte Zweig Windows wurde überprüft und die installierte Laufzeit
Weg ausgeübt. Für einen Test wurde kein Windows-Computer ohne .NET geändert.
Der endgültige Code wiederholt auch die Kerninstallation und das genaue Rollback mit dem
zuvor heruntergeladene und erneut aufbereitete GitHub-Nutzlastbytes.

<a id="setup-117-review"></a>

## Setup 1.1.7 Überprüfung

Überprüfte den aktuellen Unterschied in Bezug auf Pfadumfang, Vertrauen der lokalen Quelle, Download-Auswahl, Preflight-/Commit-Drift-Prüfungen, Transaktionssicherungen und Rollback-Kompatibilität. Keine ungeklärten Feststellungen. Die lokale Wiederverwendung ist auf das mit dem Katalog übereinstimmende Root/Active-Locale-S-Paar beschränkt. Deaktivierte Dateien werden durch das vorhandene verifizierte Sicherungsjournal verschoben. Beide Plattformen haben die 50-Regressionsgruppen und die tatsächliche Release-Datei ein/aus/ein mit exaktem gestapeltem Rollback bestanden. Keine Änderungen an der Spiellast.

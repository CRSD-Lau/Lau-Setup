<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — Ein ZIP enthält jetzt das Windows-Installationsprogramm und den Linux/Wine-Starter. Die Oberfläche folgt automatisch der Betriebssystemsprache mit zehn Optionen; eine manuelle Auswahl wird gespeichert. Spielversion 3.0.8 und die Spieldateien bleiben unverändert. Es gibt keine DBC-Änderungen.
>
> Die vollständige Aktualisierung der Anleitungen steht wegen Google-HTTP-429 noch aus. Der bisherige Text unten kann älter sein; maßgeblich sind die aktuelle englische Quelle und die Hinweise zu 1.3.0. [English](../../../PLATFORM-FEASIBILITY.md) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
>
> **Aktueller Download:** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) für Windows und Linux/Wine. Entpacken Sie den Ordner `LauSetup/` mit fünf Dateien: Windows öffnet `LauSetup.exe`; Linux/Wine führt `LauSetup.sh` aus. Die älteren Anweisungen unten zu getrennten EXE- oder Wine-ZIPs gelten nicht für 1.3.0.
>
> **1.3.0:** Erkannte zusätzliche Upgrade-Dateien werden automatisch gesichert; die Installation läuft weiter. Die Wiederherstellung bringt sie zurück. Kein manuelles Verschieben nötig.

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Automatische Übersetzung. [Englische Quelle](../../../PLATFORM-FEASIBILITY.md). Bei abweichenden Formulierungen ist die englische Quelle maßgeblich.

<a id="lau-setup-platform-feasibility"></a>

# Lau Setup Plattform-Machbarkeit

Autor: Neil Mitchell  
Ersteller: Neil Mitchell  
Zuletzt geändert von: Neil Mitchell  
Bewertungsdatum: 2026-09-11

> **Historische Bewertung unten:** Die folgenden Abschnitte zu 1.0.1/1.1.0 beschreiben den damaligen Prüfstand. Für die aktuelle Installation mit einem gemeinsamen ZIP beachten Sie den Hinweis zu Setup 1.2.0 oben.
Update: vom Benutzer ausgewählt Wine nur. Installateur 1.1.0 liefert jetzt das getestete
Wine 11 / Wine Mono 10.4.1 Launcher beschrieben in [Die Wine Führung](wine/README.md).
Der Wine 8 Die nachstehenden Untersuchungen und Empfehlungen werden als historische Bewertung gespeichert.
Die Integration von Lutris, Proton und macOS bleibt außerhalb des Anwendungsbereichs.

Lau Setup 1.0.1 bleibt ein Windows-Installationsprogramm. Linux bis Wine ist das empfohlene nächste Kompatibilitätsziel. Diese Bewertung zertifiziert nicht die Installation auf Linux oder macOS. Die früheren 63 Docker/Wine-Fälle verwendeten die Spieldaten, nicht dieses Installationsprogramm.

| Option | Empfehlung | Was bedeutet es für Lau Setup |
| --- | --- | --- |
| Wine auf Linux | Erstes Ziel; grundsätzlich machbar, derzeit ungeprüft | Verwenden Sie das Windows-Installationsprogramm innerhalb eines explizit ausgewählten Wine-Präfixes erneut. Prüfen Sie Laufzeit, Ordnerauswahl, Downloads, Dateisicherheit und Wiederherstellung, bevor Sie die Unterstützung veröffentlichen. |
| Lutris | Als nächstes, nachdem direkt Wine übergeben wurde | Ein kleines Integrationsrezept kann das Setup im Präfix des vorhandenen Spiels starten. Es ist kein separates Nutzlastformat erforderlich. |
| Dampf / Proton | Später, bedingt | Verwenden Sie das korrekte Präfix des vorhandenen Spiels. Das Hinzufügen eines Setups als weiteres Nicht-Steam-Spiel kann zu einer anderen Umgebung führen. Die Benutzerfreundlichkeit des Steam Decks erfordert separate Bildschirm- und Controller-Prüfungen. |
| CrossOver unter macOS | Plausible, separate Teststrecke | Laufen Sie in die Flasche des Spiels. Validierung auf aktueller macOS-Hardware und unterstützten CrossOver-Versionen; Linux-Tests können dies nicht feststellen. |
| Wine + DXVK | Optionale Spielkonfiguration | DXVK übersetzt Direct3D für das Spiel. Die .NET-, Schriftarten- oder Dateisicherheitsanforderungen des Installationsprogramms werden dadurch nicht erfüllt. |
| Whisky | Nicht als neues Unterstützungsziel übernehmen | Das Upstream-Projekt wird nicht mehr aktiv gepflegt. |

Die obige Klassifizierung folgt den Rollen, die von [Wine Mono](https://github.com/wine-mono/wine-mono), [Lutris](https://lutris.net/about/), [Proton](https://github.com/ValveSoftware/Proton), [DXVK](https://github.com/doitsujin/dxvk), [CrossOvers Mac] beschrieben werden Führer](https://support.codeweavers.com/en_US/crossover-mac-user-guide) und [Whisky](https://github.com/Whisky-App/Whisky). Bei den Empfehlungen handelt es sich um unsere Einschätzung, nicht um die vorgelagerte Zertifizierung von Lau Setup. CrossOver kann 32-bit Windows-Anwendungen in 64-bit-Flaschen ausführen; Der Verlust der nativen macOS 32-bit-Unterstützung allein schließt dies nicht aus.

<a id="bounded-probe-results"></a>

## Begrenzte Prüfergebnisse

Die lokale Sonde verwendete Wine 8.0 (Debian 8.0~repack-4), ein isoliertes Win32-Präfix und Xvfb. Diese ältere lokal verfügbare Laufzeit ist kein Test der aktuellen Wine-Versionen. Es wurde kein persönlicher Spielclient gemountet oder geändert.

1. Das geerbte Game-Test-Image hat mscoree deaktiviert. Durch die Aktivierung wurde dies sichtbar Wine Mono fehlte. Dies war ein Problem in der Testumgebung.
2. Installiert den Beamten Wine Mono 7.4.0 MSI im Einwegpräfix nach der Überprüfung SHA-256 `6413ff328ebbf7ec7689c648feb3546d8102ded865079d1fbf0331b14b3ab0ec`, gepinnt von [Wine 8.0's Quelle](https://raw.githubusercontent.com/wine-mirror/wine/wine-8.0/dlls/appwiz.cpl/addons.c).
3. Ein Diagnosekabelbaum wurde initialisiert WinForms und den eingebetteten Katalog geladen, dann ist die Erstellung des Formulars mit fehlgeschlagen `System.ArgumentException: The requested FontFamily could not be found [GDI+ status: FontFamilyNotFound]`. Durch das Kopieren verfügbarer Liberation-Schriftarten in dieses Präfix konnte das Problem nicht behoben werden. Es ergab sich kein erfolgreicher Installer-Screenshot bzw. keine erfolgreiche Installation.
4. Lokale Beweise werden unter aufbewahrt `reports/wine-feasibility/`. Der Sondenbehälter wird gestoppt. Der Diagnose-Kabelbaum ist nicht im verteilten Installationsprogramm oder öffentlichen Quellpaket enthalten.

Dies identifiziert Laufzeit-/Schriftartbereitstellungsarbeiten und ist kein Beweis dafür, dass Wine unmöglich ist. In dieser Probe wurde unter Wine keine Installations-/Wiederherstellungstransaktion versucht.

<a id="acceptance-work-before-wine-support"></a>

## Abnahmearbeiten vor der Wine-Unterstützung

1. Erstellen Sie eine reproduzierbare aktuelle Kombination aus Wine/Laufzeit/Schriftart auf einem Linux-Desktop. Zeigen Sie den Anfangs-, Bereitschafts-, Download-, Wiederherstellungs- und Fehlerstatus in gängigen Anzeigemaßstäben an. Überprüfen Sie den Tastaturzugriff und die Ordnerauswahl.
2. Überprüfen Sie die genaue Host-Ordner-Zuordnung und die Groß-/Kleinschreibung in einem Dateisystem, bei dem die Groß-/Kleinschreibung beachtet wird, einschließlich doppelter Namen, die sich nur in der Groß-/Kleinschreibung unterscheiden. Behalten Sie nicht verwandte Patches und persönliche Einstellungen bei.
3. Beweisen Sie das Link-, Exclusive-Lock-, Free-Space-, Journal- und Atomic-Replace-Verhalten. Das Installationsprogramm ruft derzeit Windows-Dateiinformations-APIs auf; Ihre Semantik muss unter Wine getestet und nicht angenommen werden.
4. Beweisen Sie den laufenden Spielwächter über Präfixe hinweg. Der aktuelle Code zählt Windows-Prozesse auf und vergleicht ausführbare Verzeichnisse. Die Sichtbarkeit des Präfixes Wine kann dazu führen, dass ein anderes Präfix, auf dem derselbe Client ausgeführt wird, unentdeckt bleibt. Beheben Sie dieses Problem, bevor Sie sicheren Installationssupport anbieten. Ein erfolgreicher Same-Prefix-Test allein reicht nicht aus.
5. Führen Sie die Fixture-Installation/-Wiederherstellung und die unterbrochene Wiederherstellungsmatrix aus und führen Sie dann einen sauberen, anonymen GitHub-Download/-Installation/-Rollback unter Verwendung der exakten Release-Assets aus. Testen Sie TLS, Weiterleitungen, Wiederaufnahme, Stornierung und Offline-Wiederherstellung.
6. Führen Sie anschließend einen In-Game-Check in derselben unterstützten Umgebung durch. Erst dann Wine-Anweisungen und eine Lutris-Integration veröffentlichen. Lassen Sie Proton und macOS explizit nicht überprüft, bis ihre eigenen Prüfungen erfolgreich sind.

Behalten Sie einen Satz unveränderlicher Spielressourcen in GitHub-Releases. Fügen Sie dem Git-Repository keine vollständigen Clients, persönliche Benutzeroberflächen oder Kopien aller Nutzlasten hinzu, um einen anderen Launcher zu aktivieren. Wenn Wine die Sicherheitsprüfungen nicht zuverlässig erfüllen kann, bewerten Sie ein natives Linux-Installationsprogramm anhand derselben Manifest- und Transaktionsregeln wie eine separate Implementierung.

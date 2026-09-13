<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- RELEASE-120-NOTICE -->
> **Setup 1.2.0** — Ein ZIP enthält jetzt das Windows-Installationsprogramm und den Linux/Wine-Starter. Die Oberfläche folgt automatisch der Betriebssystemsprache mit zehn Optionen; eine manuelle Auswahl wird gespeichert. Spielversion 3.0.8 und die Spieldateien bleiben unverändert. Es gibt keine DBC-Änderungen.
>
> Die vollständige Aktualisierung der Anleitungen steht wegen Google-HTTP-429 noch aus. Der bisherige Text unten kann älter sein; maßgeblich sind die aktuelle englische Quelle und die Hinweise zu 1.2.0. [English](../../../CONTRIBUTING.md) · [1.2.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.2.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Automatische Übersetzung. [Englische Quelle](../../../CONTRIBUTING.md). Bei abweichenden Formulierungen ist die englische Quelle maßgeblich.

<a id="contributing-to-lau-setup"></a>

# Beitrag zu Lau Setup



Vielen Dank, dass Sie der Wrath-Community dabei geholfen haben, die Installation und Wiederherstellung zu verbessern.

<a id="community-roadmap"></a>

## Community-Roadmap

Folgen Sie der [Community-Roadmap](https://github.com/users/CRSD-Lau/projects/2), um Arbeit als Probleme zu sehen und Pull-Requests dem Board automatisch über **Backlog**, **Ready**, **In Progress**, **Testing** und **Done** zuzuführen. **Testkarten** enthalten Akzeptanzchecklisten und sammeln die für den Abschluss der Validierung erforderlichen Nachweise; Verwenden Sie [Ideen](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas), um Vorschläge zu besprechen, bevor Sie ein Problem einreichen. [Versionshinweise](https://github.com/CRSD-Lau/Lau-Setup/releases) bleiben die Autorität für den Lieferumfang der einzelnen Versionen.

<a id="report-a-problem"></a>

## Ein Problem melden

Verwenden Sie das [Fehlerberichtsformular](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose). Geben Sie die Version des Installationsprogramms, die Plattform, das Client-Gebietsschema, die ausgewählten visuellen Elemente, das erwartete Verhalten und die Schritte zur Reproduktion an. Geben Sie bei Problemen im Spiel `/pyversion`, den Boss oder die Fähigkeit, den Schwierigkeitsgrad und einen Screenshot an. Wine-Berichte sollten die Versionen Wine und Wine Mono enthalten.

Entfernen Sie Kontonamen, Passwörter, Token und persönliche Pfade aus Screenshots oder Auszügen. Laden Sie nicht Ihren Client, WTF-Ordner, SavedVariables oder ganze Protokolle hoch. Bewahren Sie lokale Backups auf, wenn die Wiederherstellung aussteht.

<a id="propose-a-change"></a>

## Schlagen Sie eine Änderung vor

Beginnen Sie mit [Bekannte Einschränkungen und Annahmen](KNOWN-LIMITATIONS.md). Verwenden Sie [Ideen](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas) für Empfehlungen; Identifizieren Sie alle Abhängigkeiten von Servern, nativem Code oder geschützten Aktionen, bevor Sie eine Implementierung vorschlagen.

Konzentrieren Sie sich auf Pull-Anfragen. Erläutern Sie das für den Benutzer sichtbare Problem, die Änderung und die von Ihnen durchgeführten Prüfungen. Testen Sie Dateivorgänge nur in isolierten Geräten, niemals in einem aktiven persönlichen Spielclient.

Behalten Sie die Archiv-Zulassungsliste, Hash-Prüfungen, Sicherungsjournale, Prozessprüfungen und präfixübergreifende Sperren bei. Ändern Sie die Payload-Datensätze des Spiels nicht im Rahmen einer Dokumentation oder einer Schnittstellenaktualisierung.

Die [technische Referenz](docs/TECHNICAL.md) erläutert den öffentlichen Build und die Tests, die private lokale Geräte erfordern. Trennen Sie in Ihrer PR klar einen erfolgreichen Build, Fixture-Tests und die tatsächliche In-Game-Validierung.

<a id="artwork-and-attribution"></a>

## Bildmaterial und Namensnennung

Behalten Sie das etablierte W-and-Shield-Branding und die Upstream-Credits bei. Geben Sie die Quelle und die geltenden Berechtigungen für das vorgeschlagene Kunstwerk an. Führen Sie keinen persönlichen Kundenstatus in öffentliche Vermögenswerte ein.

<a id="dbc-release-records"></a>

## DBC-Veröffentlichungsdatensätze

Jede Spiel- oder Installationsversion muss [DBC-CHANGELOG.md](DBC-CHANGELOG.md) aktualisieren und einen Abschnitt zu **DBC-Änderungen** in die Versionshinweise zu GitHub aufnehmen. Listen Sie für tatsächliche DBC-Änderungen die Tabelle, die Datensatz-ID, das benannte Feld und den nullbasierten Index, alte/neue Werte, betroffene Editionen/Gebietsschemas und den Grund auf, mit Vorher/Nachher-Hashes und Vergleichsnachweisen. Erfassen Sie für unveränderte DBCs explizit **Keine DBC-Änderungen**. Trennen Sie Geometrie-, Textur- und Installer-Änderungen von DBC-Änderungen. Informationen zum erforderlichen Format und den Validierungsgrenzen finden Sie im Änderungsprotokoll.

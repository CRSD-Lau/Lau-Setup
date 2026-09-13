<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Automatische Übersetzung. [Englische Quelle](../../../DBC-CHANGELOG.md). Bei abweichenden Formulierungen ist die englische Quelle maßgeblich.

<a id="dbc-changelog"></a>

# DBC-Änderungsprotokoll



Verfolgen Sie Client-DBC-Änderungen getrennt von Modell-, Textur- und Installer-Änderungen. Spielversionen und Installationsversionen sind getrennt: `/pyversion` meldet die Spielversion.

<a id="handoff-history-andre-303-onward"></a>

## Übergabeverlauf: Andre 3.0.3 ab

[Einzelne DBC-Änderungen und Entwicklungsverlauf](docs/dbc/history/INDIVIDUAL-EDITS.md) · [Vergleich von sechs Editionen und Basis-Hashes](../../dbc/history/andre-to-3.0.4.json)

Andre hat **Spell.dbc** absichtlich weggelassen, um Lokalisierungskonflikte zu vermeiden. Die anfängliche Überschreibung Lau hat diese Abhängigkeit offengelegt; **Lau und Andre haben es gemeinsam debuggt** und die mehrsprachige Neuerstellung hat das Problem mit der Kompatibilität von Rechtschreibung und Text behoben. Die aufbewahrten Andre-Archive enthalten sechs weitere visuelle/Modell-DBCs, daher sollte dies nicht als Fehlen aller DBCs bezeichnet werden.

Lau beschreibt die Meilensteine ​​als **3.0.4: anfängliche Tabellenerweiterung**, **3.0.5: mehrsprachige Auflösung** und **3.0.6–3.0.8: Hotfixes mit Versionsänderungen**. Frühe Versionsbezeichnungen überschneiden sich: Der archivierte veröffentlichte Build mit der Bezeichnung 3.0.4 enthält bereits den mehrsprachigen Fix. Die folgenden Artefaktvergleiche verwenden exakte Hashes und löschen den Entwicklungsverlauf nicht.

Die Initiale Patch-Y Der Vergleich umfasst fünfzehn Änderungen an visuellen Spell-Links pro Ausgabe, neue Indikator-Visual-/Kit-/Anhang-Datensätze, Weiheunterschiede und entschlüsselte Lokalisierungsänderungen. Der Tabellenzusatz wird mit dem zugrunde liegenden Bestand oder der HD-Spell-Basis verglichen, sodass übernommene Datensätze nicht als neu verfasste Arbeit dargestellt werden. [Überprüfung der Lokalisierungsphase](../../dbc/history/localization-stage.json) bestätigt die Textwiederherstellung der erhaltenen numerischen Daten in den vier beibehaltenen HD-/Nicht-HD-Editionen vor der Lokalisierung.

<a id="archived-releases-304--308"></a>

## Archivierte Veröffentlichungen 3.0.4 → 3.0.8

| Archivierter Übergang | DBC-Ergebnis | Sonstige Änderungen |
| --- | --- | --- |
| 3.0.4 → 3.0.5 | Keine DBC-Änderungen; 42 identische Tabellen | Sindragosa- und Rotface-Kegelgeometrie, Versionsbezeichnung |
| 3.0.5 → 3.0.6 | Keine DBC-Änderungen; 42 identische Tabellen | Farbelemente und Referenzen für Coldflame/Halion-Marker, Versionsbezeichnung |
| 3.0.6 → 3.0.7 | Keine DBC-Änderungen; 42 identische Tabellen | Genehmigte Halion-Meteorfeuer-Geometrie, Versionsbezeichnung |
| 3.0.7 → 3.0.8 | Keine DBC-Änderungen; 42 identische Tabellen | Verbleibender Atem/Schleim-Sprühkegelgeometrie, Versionsbezeichnung |

[Alle 168 Tabellenvergleiche und Archiv-Hashes](../../dbc/history/3.0.4-through-3.0.8.json). Hierbei handelt es sich um Vergleiche beibehaltener Release-Artefakte und nicht um eine Behauptung, dass der frühere Lokalisierungsvorfall nicht stattgefunden hat.

<a id="307--308--no-dbc-edits"></a>

## 3.0.7 → 3.0.8 – keine DBC-Änderungen

Veröffentlicht mit [Setup 1.1.4](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.1.4). Alle **42 DBC-Vergleiche wurden byteweise durchgeführt**: sieben Tabellen in jeder der sechs Patch-Y-Editionen. Es gibt keine hinzugefügten/gelöschten Tabellen, geänderten Datensätze, geänderten Felder oder geänderten Zeichenfolgenblöcke.

| Tabelle | Änderungen aufzeichnen | Feldbearbeitungen | Ergebnis |
| --- | ---: | ---: | --- |
| CreatureDisplayInfo.dbc | 0 | 0 | Identisch |
| CreatureModelData.dbc | 0 | 0 | Identisch |
| Spell.dbc | 0 | 0 | Identisch |
| SpellVisual.dbc | 0 | 0 | Identisch |
| SpellVisualEffectName.dbc | 0 | 0 | Identisch |
| SpellVisualKit.dbc | 0 | 0 | Identisch |
| SpellVisualKitModelAttach.dbc | 0 | 0 | Identisch |

[Vollständiger Vergleichsbeweis](../../dbc/3.0.7-to-3.0.8.json) zeichnet die Quell-/Ziel-MPQ jeder Edition auf SHA-256, jedes DBC ist vorher/nachher SHA-256, Größe, Zeilenanzahl und Feldanzahl. Die MPQ-Hashes wurden mit den Release-Katalogen verglichen. Der andere 22 Katalog-Assets, einschließlich Locale-Q- und Shared-S-Assets, bleiben unverändert.

<a id="what-actually-changed-in-308"></a>

### Was sich tatsächlich in 3.0.8 geändert hat

Fünf vorhandene Kegelmodelle wurden auf **90° total** erweitert, indem ihre `.m2`-Geometrie und die entsprechenden `00.skin`-Grenzen bearbeitet wurden. Vorhandene DBC-Anbindungen wurden beibehalten.

| Modellstamm | Vorheriger Winkel | Neuer Blickwinkel |
| --- | ---: | ---: |
| PW_Rotface_SlimeSpray_Fan25_Room | 60° | 90° |
| PW_White_Fan60_60yd_Glowing | 60° | 90° |
| PW_White_Fan60_30yd_Glowing | 60° | 90° |
| PW_White_Fan60_100y_Glowing | 60° | 90° |
| PW_White_Fan82_60yd_Glowing | 82° | 90° |

Dateinamen behalten historische Winkelbezeichnungen; Die Geometrie bestimmt den angezeigten Winkel. Sindragosa war bereits 90° und hat sich bei diesem Übergang nicht geändert. Dadurch wurden alle unterstützten Atem- und Schleimspray-Indikatoren auf 90° übertragen. Reichweite und Animationszeitpunkt blieben unverändert. Der Radius des Halion-Meteorfeuers, die Farben der Kaltflamme und die Weihe blieben unverändert.

Jede Edition hat genau die **11-Archivmitglieder** geändert: fünf `.m2`-Dateien, fünf `.skin`-Dateien und das `!pyandre.toc`-Spielversionslabel von 3.0.7 zu 3.0.8. Alle anderen aufgelisteten Inhaltsmitglieder sind identisch. Die MPQ-Containerbuchhaltung liegt außerhalb des Content-Member-Vergleichs.

Dadurch werden Client-Dateiänderungen überprüft, nicht die Servermechanik von Warmane oder eine genaue Schadensgrenze.

<a id="setup-115-116-and-117--no-dbc-edits"></a>

## Setup 1.1.5, 1.1.6 und 1.1.7 – keine DBC-Änderungen

Dabei handelt es sich um Installer-Hotfixes. Ihre Spielnutzlasten bleiben 3.0.8, mit unveränderten DBC-Daten. Der neueste Hotfix ändert die Installation, Aufbewahrung und Wiederverwendung von Patch-S, nicht jedoch den internen DBC-Inhalt.

<a id="required-entry-for-future-releases"></a>

## Erforderlicher Eintrag für zukünftige Versionen

Jede Version muss hier einen Eintrag und einen Abschnitt **DBC-Änderungen** zu ihren GitHub-Versionshinweisen hinzufügen, einschließlich Versionen, die nur für Installationsprogramme bestimmt sind. Geben Sie bei Bedarf ausdrücklich **Keine DBC-Änderungen** an. Vergleichen Sie es mit der vorherigen stabilen Spielversion, nicht mit einem unveröffentlichten Test-Build. Beschreiben Sie eine Modell-/Texturbearbeitung nicht als DBC-Bearbeitung.

Zeichnen Sie für jede tatsächliche DBC-Bearbeitung eine Zeile pro Feld auf (oder einen verknüpften maschinenlesbaren Unterschied auf Zeilenebene für große Lokalisierungsänderungen):

| Spielübergang | Tabelle | Datensatz-ID | Feldname / nullbasierter Index | Alter Wert | Neuer Wert | Editionen / Gebietsschemas | Grund |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VERSION → VERSION | TABLE.dbc | ID | Benanntes Feld [Index] | Vorheriger Wert | Neuer Wert | Betroffene Varianten | Zweck |

Zeichnen Sie außerdem hinzugefügte/gelöschte Datensätze und Tabellen, Schemaänderungen und Zeichenfolgenwertänderungen auf. Dekodieren Sie String-Werte, anstatt bei Inhaltsänderungen eine Änderung des String-Block-Offsets zu melden. Geben Sie die Feldindexkonvention und die Schemaquelle an. Beschriften Sie unbekannte Felder, anstatt zu raten. Hängen Sie Vorher/Nachher-Archiv- und Tabellen-Hashes, die Vergleichsmethode und Validierungsgrenzen an. Behaupten Sie niemals, dass ein Vergleich ohne Beweise stattgefunden hat.

Die Übergabeprüfung deckt Patch-Y ab den beibehaltenen Andre 3.0.3-Baselines ab. Separate Q/S/Karten-Lokalisierungspipelines und unabhängige experimentelle Builds liegen außerhalb dieser ersten Retrospektive. Keinem früheren kaputten Artefakt wird eine Veröffentlichungsnummer ohne übereinstimmende Herkunft zugewiesen.

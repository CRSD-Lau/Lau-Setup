<!-- LANGUAGES:START -->
[English](../../../../../../README.md) · [Deutsch](../../../README.md) · [Español (España)](../../../../es-ES/README.md) · [Español (México)](../../../../es-MX/README.md) · [Français](../../../../fr/README.md) · [한국어](../../../../ko/README.md) · [Русский](../../../../ru/README.md) · [简体中文](../../../../zh-CN/README.md) · [繁體中文](../../../../zh-TW/README.md) · [Português (Brasil)](../../../../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Automatische Übersetzung. [Englische Quelle](../../../../../dbc/history/INDIVIDUAL-EDITS.md). Bei abweichenden Formulierungen ist die englische Quelle maßgeblich.

<a id="individual-patch-y-dbc-edits-andre-baseline-to-retained-multilingual-lau-build"></a>

# Einzelne Patch-Y DBC-Änderungen: Andre-Basislinie zum beibehaltenen mehrsprachigen Lau-Build



<a id="read-the-chronology-first"></a>

## Lesen Sie zuerst die Chronologie

Laut Lau hat Andre **Spell.dbc** aufgrund von Lokalisierungskonflikten absichtlich weggelassen. Die aufbewahrten Andre 3.0.3-Archive enthalten sechs visuelle/Modell-DBCs; Sie enthalten nicht Spell.dbc. Mit der ersten Hinzufügung Lau wurde die Sprachabhängigkeit eingeführt. Lau und Andre haben das Problem gemeinsam behoben und durch die mehrsprachige Neuerstellung behoben.

Lau identifiziert diese Entwicklungsmeilensteine ​​als 3.0.4 (erste Ergänzung) und 3.0.5 (mehrsprachiger Fix), wobei 3.0.6–3.0.8 Hotfixes sind, deren Versionsnummern erhöht wurden. Behaltene Artefakte lassen sich nicht sauber dieser Erinnerung zuordnen: Die veröffentlichte Baseline mit der Bezeichnung 3.0.4 enthält bereits den mehrsprachigen Fix. Dieser Bericht benennt Artefakte und Hashes explizit, anstatt stillschweigend einen früh defekten Build dieser veröffentlichten Bezeichnung zuzuordnen.

[Lokalisierungsphasennachweis](../../../../../dbc/history/localization-stage.json) vergleicht vier beibehaltene Archive vor der Lokalisierung v35 mit den mehrsprachigen Versionen: Nur Spell.dbc ändert sich, alle numerischen Felder bleiben identisch und vorhandene visuelle Links bleiben erhalten. HD New Spells Off wurde separat anhand der numerischen Bestandsdaten zusammengestellt.

<a id="format-and-scope"></a>

## Format und Umfang

Hierbei handelt es sich um den Patch-Y-Handoff-Vergleich, nicht um eine Prüfung jeder einzelnen Q/S/Map-Lokalisierungspipeline. Sechs Edition-CSVs listen einzelne Tabellen-/Datensatz-/Feldbearbeitungen und alle hinzugefügten Datensatzwerte auf. Zwei gemeinsam genutzte JSON-gzip-Dateien enthalten dekodierte Änderungen an Zaubertexten, ohne Text für Weihungsvarianten zu duplizieren. Jede Textzelle ist `[record_id, zero_based_field, old_string_index, new_string_index]`; Lösen Sie die letzten beiden über das `strings`-Array dieser Datei auf.

Numerische Werte sind rohe, vorzeichenlose 32-bit-Wörter, einschließlich Float-Bitmuster; Unbekannte Schemanamen werden nicht erraten. Das Feld Spell.dbc 131 ist der visuelle Link, der von den Build-Skripten verwendet wird. String-Offsets werden vor dem Vergleich dekodiert. Das hinzugefügte Spell.dbc verwendet beibehaltene HD-Patch-S-Daten für HD New Spells On und vom Server extrahierte Bestandsdaten für HD New Spells Off und Non-HD. Geerbte Zeilen werden nicht als neu erstellte Datensätze anerkannt.

<a id="what-the-edit-groups-mean"></a>

### Was die Bearbeitungsgruppen bedeuten

- Zauberfeld 131: Fünfzehn akzeptierte visuelle Links für Raid-Indikatoren in jeder Ausgabe.
- Textzellen buchstabieren: mehrsprachige/Fallback-Slot-Population; Bei diesen Zählungen handelt es sich nicht um Zählungen neu verfasster Übersetzungen.
- SpellVisual, SpellVisualKit und Befestigungsreihen: Blinkerführung, Kits und Modellbefestigungseinrichtung.
- SpellVisualEffectName: Modellreferenzen und Unterschiede im Erscheinungsbild der Weihe hinzugefügt.
- CreatureDisplayInfo und CreatureModelData: unverändert gegenüber der entsprechenden Andre-Basislinie.
- HD New Spells Off: Das private Rimefang-Kit verwendet 90059, um das Upstream-Kit 90046 zu erhalten.

<a id="y-hd-newspells-off-consecration-on"></a>

## Y-HD-NewSpells-Aus-Weihe-Ein

| Tabelle | Geänderte/hinzugefügte Datensätze | Feldwertunterschiede | IDs hinzugefügt | Entfernte IDs |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Keine | Keine |
| creaturemodeldata.dbc | 0 | 0 | Keine | Keine |
| spell.dbc | 49839 | 824619 | Keine | Keine |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Keine |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Keine |
| spellvisualkit.dbc | 14 | 495 | 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058, 90059 | Keine |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Keine |

| Tisch | Datensatz-ID | Feld [0-basierend] | Alt | Neu |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualeffectname.dbc | 2542 | 2 | Zaubersprüche\consecration_impact_base.mdx | Zauber\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Alle Datensatz-/Feldbearbeitungen und hinzugefügten Datensätze](../../../../../dbc/history/Y-HD-NewSpells-Off-Consecration-On.csv) · [Entschlüsselte Textänderungen](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-hd-newspells-off-consecration-off"></a>

## Y-HD-NewSpells-Off-Consecration-Off

| Tabelle | Geänderte/hinzugefügte Datensätze | Feldwertunterschiede | IDs hinzugefügt | Entfernte IDs |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Keine | Keine |
| creaturemodeldata.dbc | 0 | 0 | Keine | Keine |
| spell.dbc | 49839 | 824619 | Keine | Keine |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Keine |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Keine |
| spellvisualkit.dbc | 14 | 495 | 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058, 90059 | Keine |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Keine |

| Tisch | Datensatz-ID | Feld [0-basierend] | Alt | Neu |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Alle Datensatz-/Feldbearbeitungen und hinzugefügten Datensätze](../../../../../dbc/history/Y-HD-NewSpells-Off-Consecration-Off.csv) · [Entschlüsselte Textänderungen](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-hd-newspells-on-consecration-on"></a>

## Y-HD-NewSpells-On-Consecration-On

| Tabelle | Geänderte/hinzugefügte Datensätze | Feldwertunterschiede | IDs hinzugefügt | Entfernte IDs |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Keine | Keine |
| creaturemodeldata.dbc | 0 | 0 | Keine | Keine |
| spell.dbc | 33950 | 227113 | Keine | Keine |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Keine |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Keine |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | Keine |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Keine |

| Tisch | Datensatz-ID | Feld [0-basierend] | Alt | Neu |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualeffectname.dbc | 2542 | 2 | Zaubersprüche\consecration_impact_base.mdx | Zauber\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Alle Datensatz-/Feldbearbeitungen und hinzugefügten Datensätze](../../../../../dbc/history/Y-HD-NewSpells-On-Consecration-On.csv) · [Entschlüsselte Textänderungen](../../../../../dbc/history/spell-text-hd.json.gz)

<a id="y-hd-newspells-on-consecration-off"></a>

## Y-HD-NewSpells-Ein-Weihe-Aus

| Tabelle | Geänderte/hinzugefügte Datensätze | Feldwertunterschiede | IDs hinzugefügt | Entfernte IDs |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Keine | Keine |
| creaturemodeldata.dbc | 0 | 0 | Keine | Keine |
| spell.dbc | 33950 | 227113 | Keine | Keine |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Keine |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Keine |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | Keine |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Keine |

| Tisch | Datensatz-ID | Feld [0-basierend] | Alt | Neu |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Alle Datensatz-/Feldbearbeitungen und hinzugefügten Datensätze](../../../../../dbc/history/Y-HD-NewSpells-On-Consecration-Off.csv) · [Entschlüsselte Textänderungen](../../../../../dbc/history/spell-text-hd.json.gz)

<a id="y-non-hd-consecration-on"></a>

## Y-Non-HD-Consecration-On

| Tabelle | Geänderte/hinzugefügte Datensätze | Feldwertunterschiede | IDs hinzugefügt | Entfernte IDs |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Keine | Keine |
| creaturemodeldata.dbc | 0 | 0 | Keine | Keine |
| spell.dbc | 49839 | 824619 | Keine | Keine |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Keine |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Keine |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | Keine |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Keine |

| Tisch | Datensatz-ID | Feld [0-basierend] | Alt | Neu |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualeffectname.dbc | 2542 | 2 | Zaubersprüche\consecration_impact_base.mdx | Zauber\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Alle Datensatz-/Feldbearbeitungen und hinzugefügten Datensätze](../../../../../dbc/history/Y-Non-HD-Consecration-On.csv) · [Dekodierte Textänderungen](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-non-hd-consecration-off"></a>

## Y-Non-HD-Consecration-Off

| Tabelle | Geänderte/hinzugefügte Datensätze | Feldwertunterschiede | IDs hinzugefügt | Entfernte IDs |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Keine | Keine |
| creaturemodeldata.dbc | 0 | 0 | Keine | Keine |
| spell.dbc | 49839 | 824619 | Keine | Keine |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Keine |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Keine |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | Keine |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Keine |

| Tisch | Datensatz-ID | Feld [0-basierend] | Alt | Neu |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Alle Datensatz-/Feldbearbeitungen und hinzugefügten Datensätze](../../../../../dbc/history/Y-Non-HD-Consecration-Off.csv) · [Entschlüsselte Textänderungen](../../../../../dbc/history/spell-text-nonhd.json.gz)

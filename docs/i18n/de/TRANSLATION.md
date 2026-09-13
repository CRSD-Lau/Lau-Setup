<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.2.0** — Ein ZIP enthält jetzt das Windows-Installationsprogramm und den Linux/Wine-Starter. Die Oberfläche folgt automatisch der Betriebssystemsprache mit zehn Optionen; eine manuelle Auswahl wird gespeichert. Spielversion 3.0.8 und die Spieldateien bleiben unverändert. Es gibt keine DBC-Änderungen.
>
> Die vollständige Aktualisierung der Anleitungen steht wegen Google-HTTP-429 noch aus. Der bisherige Text unten kann älter sein; maßgeblich sind die aktuelle englische Quelle und die Hinweise zu 1.2.0. [English](../../../TRANSLATION.md) · [1.2.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.2.0)
>
> **Aktueller Download:** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) für Windows und Linux/Wine. Entpacken Sie den Ordner `LauSetup/` mit fünf Dateien: Windows öffnet `LauSetup.exe`; Linux/Wine führt `LauSetup.sh` aus. Die älteren Anweisungen unten zu getrennten EXE- oder Wine-ZIPs gelten nicht für 1.2.0.

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Automatische Übersetzung. [Englische Quelle](../../../TRANSLATION.md). Bei abweichenden Formulierungen ist die englische Quelle maßgeblich.

<a id="repository-translations"></a>

# Repository-Übersetzungen

Die Aktion **Dokumentation übersetzen** GitHub nutzt die **kostenlose Website von Google Translate**, um die Repository-Dokumentation in jeder unterstützten Spielsprache sowie **Brasilianisches Portugiesisch** verfügbar zu halten. Es ist kein API-Schlüssel, kein kostenpflichtiges Cloud Translation-Konto, kein Abonnement oder kein Modell-Download erforderlich.

Verwenden Sie die Sprachlinks oben in der README-Datei. GitHub zeigt standardmäßig die Root-README-Datei an. Besucher wählen über diese Links ihre Sprache. Dieser Workflow übersetzt die Dokumentation, einschließlich Installationshandbüchern und technischen Referenzen. Die Benutzeroberfläche, Probleme, Versionsbeschreibungen, die separate Website oder die Installationsoberfläche von GitHub werden nicht übersetzt und es wird kein portugiesisches Spielgebietsschema hinzugefügt.

<a id="languages"></a>

## Sprachen

Die Abdeckung wird anhand von `build/catalog.json` überprüft, wobei `ptBR` zur Dokumentation hinzugefügt wird. Die Leseoptionen sind Englisch, Deutsch, Spanisch für Spanien und Mexiko, Französisch, Koreanisch, Russisch, vereinfachtes Chinesisch, traditionelles Chinesisch und brasilianisches Portugiesisch.

Die Web-Sprachauswahl von Google identifiziert `pt` als Portugiesisch (Brasilien); Portugiesisch (Portugal) ist ein anderes Ziel. Google stellt ein `es`-Ziel bereit, sodass die Seiten für Spanien und Mexiko dieselbe allgemeine spanische Übersetzung verwenden. Die chinesischen Ziele sind getrennt. Google-Zielcodes und muttersprachliche Namen sind in `tools/translation-locales.json` enthalten. Das Hinzufügen eines Spielgebietsschemas erfordert das Hinzufügen seiner Dokumentationszuordnung. Fehlende Abdeckung schlägt bei der Validierung fehl.

<a id="automatic-updates"></a>

## Automatische Updates

Wenn sich die englische Dokumentation, der Katalog oder die Übersetzungstools ändern, wird die Aktion ausgelöst. Betreuer können auch **Aktionen → Dokumentation übersetzen → Workflow ausführen → Haupt** auswählen. Es erkennt verfolgte Markdown- und Textdateien im Repository-Stammverzeichnis und `docs/` sowie `wine/README.txt`. Generierte Übersetzungen und `AGENTS.md` sind ausgeschlossen. Textführungen werden im Markdown unter `docs/i18n/<language>/` gerendert.

Nur geänderte Dokumente müssen übersetzt werden. Quell- und Ausgabe-Hashes sowie ein Segment-Cache vermeiden wiederholte Anfragen. Bump `TRANSLATION_REVISION` beim Ändern der Übersetzungskonventionen. Es werden höchstens drei Sprachjobs gleichzeitig ausgeführt, mit einer Pause zwischen den Anforderungen in jedem Job. Eine Ratenbegrenzung stoppt den betroffenen Job; Versuchen Sie es später noch einmal. Das kostenlose Webinterface ist für die Automatisierung inoffiziell und kann Anfragen ändern oder blockieren. Es gibt keinen kostenpflichtigen Fallback. Vorhandene veröffentlichte Seiten bleiben verfügbar, wenn die Generierung fehlschlägt.

Die Standardausführung des von GitHub gehosteten Runners ist für dieses öffentliche Repository kostenlos. Jobs werden deaktiviert, wenn das Repository privat wird. Kleine Zwischenartefakte verfallen nach einem Tag; Es wird kein Modell oder eine große Abhängigkeit gespeichert.

<a id="integrity-and-publication"></a>

## Integrität und Veröffentlichung

Code, Befehle, URLs, Versionsnummern, Produktnamen, Credits und Signaturstatusangaben sind geschützt. Relative Dokument-Links verweisen auf dieselbe Sprache, während Bild- und Code-Links auf die Originale verweisen. Stabile englische Überschriftenanker bewahren Abschnittsverknüpfungen. Jede Seite identifiziert sich als automatische Übersetzung, verlinkt auf ihre englische Quelle und behält die Metadaten „Autor“, „Ersteller“ und „Zuletzt geändert von“ für **Neil Mitchell** bei.

Alle neun übersetzten Leseoptionen müssen vor der Veröffentlichung an `main` die Quell-/Ausgabe-Integritätsprüfungen bestehen. Die Veröffentlichung lehnt eine geänderte Quellenrevision ab und drängt niemals dazu. Pull-Requests führen Unit-Checks und eine echte brasilianische README-Smoke-Übersetzung mit schreibgeschütztem Zugriff durch. Wenn der Filialschutz später ein Commit verhindert, passen Sie die Veröffentlichung an den genehmigten PR-Prozess an.

Die maschinelle Übersetzung bedarf noch einer gründlichen Überprüfung durch den Leser. Englisch bleibt maßgebend. Für dauerhafte Korrekturen aktualisieren Sie die englische Quelle oder die Übersetzungstools. Direkte Bearbeitungen an generierten Dateien werden neu generiert. Fehlgeschlagene oder unvollständige Chargen ersetzen keine vorhandenen Dokumente.

<a id="local-use"></a>

## Lokale Verwendung

Python 3.11 oder neuer ist ausreichend; Es sind keine zusätzlichen Pakete erforderlich. Struktur ohne Netzwerkzugriff prüfen:

```sh
python -m unittest discover -s tests -p test_translate_docs.py -v
python tools/translate_docs.py --check
```

Übersetzen Sie öffentliche Dokumentation mit der kostenlosen Google-Website:

```sh
python tools/translate_docs.py --locale ptBR
python tools/translate_docs.py --navigation
```

Referenzen: [Google Translate](https://translate.google.com/), [GitHub Abrechnung von Aktionen](https://docs.github.com/en/billing/concepts/product-billing/github-actions). Die separate [Google Cloud Translation API](https://cloud.google.com/translate/pricing) ist ein kostenpflichtiger Dienst und wird hier nicht verwendet.

<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- HOTFIX-118-NOTICE -->
> **Hotfix 1.1.8** — Setup prüft MPQs in Data und im aktiven Sprachordner auf bekannte umbenannte Patch-Y-Dateien und exakte Katalogkopien. Bei einem möglichen Konflikt oder einem nicht lesbaren bzw. nicht unterstützten Archiv stoppt es und nennt die Datei; es löscht sie nicht automatisch. Nur den Dateinamen zu ändern verändert den Inhalts-Hash nicht. Die Spieldateien bleiben auf 3.0.8.
>
> Die vollständige Übersetzung konnte wegen einer Google-Anfragebegrenzung noch nicht aktualisiert werden. Der bisherige Text unten ist ein älterer Stand. Maßgeblich sind die aktuellen englischen Angaben. [English](../../../KNOWN-LIMITATIONS.md) · [1.1.8](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.1.8)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Automatische Übersetzung. [Englische Quelle](../../../KNOWN-LIMITATIONS.md). Bei abweichenden Formulierungen ist die englische Quelle maßgeblich.

<a id="known-limitations-and-assumptions"></a>

# Bekannte Einschränkungen und Annahmen



[Zurück zu Lau Setup](README.md) · [Empfehlungen und Funktionswünsche](https://github.com/CRSD-Lau/Lau-Setup/discussions/1) · [DBC-Änderungsverlauf](DBC-CHANGELOG.md)

Lesen Sie dies, bevor Sie eine Funktion vorschlagen. Lau Setup installiert ein clientseitiges visuelles Upgrade für **WoW 3.3.5a Build 12340**. Es handelt sich nicht um ein Server-Modifikations-Framework. Die folgenden Grenzen beschreiben das aktuelle Projekt; Außerhalb des Geltungsbereichs bedeutet dies nicht zwangsläufig, dass es technisch unmöglich ist.

<a id="what-we-can-and-cannot-change"></a>

## Was wir ändern können und was nicht

| Anfrage | Aktuelle Grenze |
| --- | --- |
| Verbessern Sie unterstützte Bodenindikatoren, Texturen, Modelle oder lokalisierte Client-Tabellen | Im Rahmen, vorbehaltlich Dateiabhängigkeiten und Tests. Eine optische Verbesserung darf nicht als Änderung des Serverschadens oder der Mechanik beschrieben werden. |
| Verbessern Sie Installation, Backups, Zugänglichkeit oder Dokumentation | Im Rahmen. Behalten Sie nicht verwandte Dateien bei und überprüfen Sie die Installation und Wiederherstellung. |
| Ändern Sie Warmane Schaden, Treffererkennung, Fähigkeitsdauer, Ziel- oder Begegnungsskripte | Außerhalb unserer Kontrolle. Warmane führt seinen eigenen Servercode aus; Dieses Projekt hat keinen Zugriff, um diesen Code zu ändern oder bereitzustellen. Ein MPQ oder Add-on kann den Server nicht dazu bringen, andere Mechanismen anzunehmen. |
| Fügen Sie benutzerdefinierten C++-Code zum Kern von Warmane hinzu | Das kann diese Veröffentlichung nicht leisten. Änderungen an einem separat gesteuerten Testserver haben keine Auswirkungen auf Warmane. |
| Fügen Sie eine DLL ein, verknüpfen Sie den Client oder fügen Sie neues natives Engine-Verhalten hinzu | Außerhalb des unterstützten Patch-/Add-On-Workflows. Dies erfordert eine separate technische und Kompatibilitätsuntersuchung, nicht nur eine DBC-Bearbeitung. Es wird kein DLL-Injection-Framework oder allgemeine Client-Hook-Unterstützung bereitgestellt. |
| Geschützte Lua-Aktionen oder fehlende Spiel-APIs freischalten | Keine unterstützte Funktion. Bearbeitbare Add-On-Lua- und geschützte Client-Aktionen sind verschiedene Dinge. Das Umschreiben von Lua selbst gewährt keine Berechtigungen und erstellt keine API, die der Client nicht verfügbar macht. Melden Sie die genaue Aktion/API, bevor Sie davon ausgehen, dass es eine Problemumgehung gibt. |
| Stellen Sie einen vollständigen Client, ein anderes Sprachpaket oder eine HD-Modellbasis bereit | Nicht im Lieferumfang enthalten. Bringen Sie einen vorhandenen kompatiblen Client mit den erforderlichen Sprachdateien, Schriftarten und Modellkonfigurationen mit. |

The compatible `WoW.exe` supplied by setup has a specific role in the approved loading renderer, archive capacity and large-address support. Seine Aufnahme ist **kein** Versprechen beliebiger Änderungen an ausführbaren Dateien oder DLLs. Ebenso ist nicht jede Lua-Datei geschützt oder nicht bearbeitbar: Gewöhnliche Add-On- und UI-Änderungen können im Rahmen des vom Client unterstützten Verhaltens möglich sein.

<a id="indicators-are-visual-guidance"></a>

## Indicators are visual guidance

- **Warmane ist die Laufzeitreferenz für Warmane-Berichte.** AzerothCore und isolierte Clients helfen bei der Überprüfung der Dateiintegrität und des Verhaltens in diesen Umgebungen. Sie können die benutzerdefinierte Treffererkennung, das Timing oder das Begegnungsverhalten von Warmane nicht nachweisen.
- **Eine gezogene Kante ist keine garantierte sichere Grenze.** Die unterstützten Atemzüge und das Schleimspray verwenden gemäß dem Feedback des Testers 90°-Gesamtkegel. Halion Meteor-Fire verwendet die akzeptierte Test-v2-Erweiterung. Hierbei handelt es sich um visuelle Warnungen, die auf Beobachtungen basieren, nicht auf Messungen aus der Serverquelle von Warmane.
- **Gelände können flache Indikatoren abschneiden.** Ein flaches Bodennetz kann Hänge, Stufen und unebene Oberflächen überschneiden. Eine Vergrößerung oder Anhebung garantiert nicht überall eine geländegerechte Projektion.
- **Für die Wirkungsdauer sind Begegnungsnachweise erforderlich.** Das Verfolgungs-/Geister-Feedback beinhaltete, dass Effekte nach ein oder zwei Sekunden verschwinden. Das Ändern einer Textur, einer Form oder einer Schleifenanimation allein beweist nicht, dass der Kunde die Effektinstanz für die gesamte Dauer am Leben erhält. Für einen Timing-Fix sind Filmmaterial und Ereignisnachweise für diese spezielle Fähigkeit erforderlich. Behandeln Sie ein Modell oder einen experimentellen Build nicht als bestätigten Fix.
- **Modelle dienen der Veranschaulichung.** Website-/Chat-Animationen veranschaulichen das Erscheinungsbild. Es handelt sich nicht um Aufzeichnungen oder Beweise für die Darstellung, Dauer oder Berichterstattung im Spiel.

Geben Sie für Grenz- oder Zeitberichte die Begegnung, die Fähigkeit, den Schwierigkeitsgrad, die Client-Edition, `/pyversion` und einen Clip an, der den Vorlauf und das Ende des Schadens oder der Wirkung zeigt. Screenshots sind nützlich, aber Perspektive und Überlappungseffekte schränken genaue Radiusmessungen ein.

<a id="dbc-and-patch-compatibility"></a>

## DBC- und Patch-Kompatibilität

DBC-Tabellen sind verbundene Daten, keine unabhängigen Schalter. Das Hinzufügen eines Bildmaterials erfordert möglicherweise übereinstimmende Zauber-, Bildmaterial-, Kit-, Effekt- und Modellreferenzen. Das Ersetzen einer vollständigen Tabelle kann auch deren lokalisierten Text ersetzen und zu Konflikten mit einem anderen Patch führen, der dieselbe Tabelle bereitstellt.

Die Lokalisierungsabhängigkeit war während der Entwicklung dieses Projekts ein echtes Problem. Andre und Lau haben es gemeinsam durchgearbeitet. Das [historische DBC-Audit](DBC-CHANGELOG.md) trennt den gemeldeten Entwicklungszeitplan von den aufbewahrten Archivbeweisen: In der Basislinie von Andre wurde `Spell.dbc` weggelassen, nicht bei jedem DBC. Gehen Sie nicht davon aus, dass das Kopieren einer englischen Tabelle in ein anderes Gebietsschema sicher ist.

- Verwenden Sie die Edition, die zu Ihrer aktuellen HD-/Originalmodellkonfiguration passt. Neue Zaubervisualisierungen erfordern die kompatiblen HD-Abhängigkeiten; Die Erkennung zertifiziert nicht jedes Modellpaket eines Drittanbieters.
– Wenn Sie die HD-Modell-Patches nach der Installation entfernen oder deaktivieren, führen Sie das neueste Setup für die resultierende Konfiguration erneut aus. Eine installierte HD-Edition führt keine dynamische Konvertierung durch. Nicht übereinstimmende Assets können zu fehlenden oder falschen Bildern führen und eine Untersuchung von Abstürzen erforderlich machen. Es wird weder ein Absturz noch ein absturzfreies Verhalten garantiert.
– Root- und Active-Locale-Platzierungen haben unterschiedliche Rollen. Insbesondere sind die beiden S-Archive unterschiedlich. Befolgen Sie die [Platzierungsanleitung](docs/TECHNICAL.md#file-placement), keine allgemeine Anweisung zum Duplizieren jedes MPQ.
- Nicht verwandte Patches bleiben erhalten, die Beibehaltung ist jedoch keine Kompatibilitätsgarantie. Ein anderes Archiv, das dieselben Daten überschreibt, kann das Ergebnis ändern.
- Spielinhalte unterstützen neun Gebietsschemas; Die Benutzeroberfläche des Installationsprogramms ist derzeit Englisch. Durch die alleinige Änderung von `Config.wtf` werden keine Dateien oder Schriftarten einer anderen Sprache installiert.

<a id="installer-and-recovery-assumptions"></a>

## Installations- und Wiederherstellungsannahmen

Schließen Sie WoW vor der Installation oder Wiederherstellung vollständig. Verwenden Sie genau den vorgesehenen Client-Ordner und lassen Sie `LauSetupBackups` intakt.

Setup vergleicht tatsächliche Datei-Hashes mit seinem **eingebetteten Katalog**. Eine Änderung um ein Byte kann auch dann erkannt werden, wenn Größe und Zeitstempel übereinstimmen, ein altes Installationsprogramm jedoch immer noch nur seinen alten Katalog kennt. Laden Sie beim Upgrade das neueste Installationsprogramm herunter. Setup überwacht einen Client nicht kontinuierlich, nachdem er beendet wurde, und gleicht spätere manuelle Patch-Änderungen nicht automatisch ab.

Durch Deaktivieren der neuen Zaubervisualisierung bleiben die S-Dateien mit Gültigkeitsbereich als `.mpq.disabled` erhalten. Bei der erneuten Aktivierung werden übereinstimmende deaktivierte Bytes verwendet, sofern verfügbar, und die einfache deaktivierte Kopie wird in die verifizierte Transaktionssicherung verschoben. Ältere Kopien mit Hash-Suffix bleiben erhalten. Siehe die [aktuelle Wiederherstellungsimplementierung](docs/TECHNICAL.md#setup-117-re-enable-cleanup).

Die Wiederherstellung hängt von den Backups und Wiederherstellungsdatensätzen ab. Es stoppt, wenn spätere Änderungen die automatische Wiederherstellung unsicher machen. Es kann keine Wiederherstellung von Dateien versprochen werden, deren einzige Sicherung gelöscht wurde. Das alleinige Entfernen von Patch-Y ist kein vollständiges Rollback der ausführbaren Datei und anderer vom Setup installierter Patches. Verwenden Sie **Vorherige Installation wiederherstellen** für die verwaltete Transaktion.

<a id="platform-and-validation-limits"></a>

## Plattform- und Validierungsgrenzen

Das dokumentierte Windows-Ziel ist Windows 10/11 mit .NET Framework 4.8. Die getestete Linux-Konfiguration verwendet Wine 11.0, Wine Mono 10.4.1, ein vorhandenes 64-bit-Präfix und Python 3.9+. Laufzeitinstallationsprogramme sind nicht im Paket enthalten. Befolgen Sie die [Wine-Voraussetzungen](wine/README.md); Verwenden Sie den lokalen Linux-Speicher. Verknüpfte Ordner, Netzwerkfreigaben und mit Windows bereitgestellte Laufwerke liegen außerhalb der unterstützten Wine-Pfadkonfiguration.

Lutris, Proton, Steam Deck-spezifische Integration und macOS sind in dieser Version keine unterstützten Integrationsziele. Dies bedeutet nicht, dass jede andere Umgebung unmöglich ist; Das bedeutet, dass wir keine Unterstützung dafür haben. Die Windows-Pakete sind nicht digital signiert.

Builds, Hash-Checks, Installer-Regressionstests, Wine-Tests und In-Game-Tests beantworten verschiedene Fragen. Das Bestehen einer davon ersetzt nicht die anderen. Bei visuellen Kontrollen handelt es sich um Stichproben, nicht um eine Zertifizierung jeder Zone, Begegnung, Anzeigeskala, Linux-Verteilung oder Client-Änderung durch Dritte. Sehen Sie im Validierungsbericht jeder Version nach, was tatsächlich überprüft wurde.

<a id="before-requesting-a-feature"></a>

## Bevor Sie eine Funktion anfordern

Beschreiben Sie das für den Spieler sichtbare Problem, Ihren Aufbau und die Beweise. Vorschläge innerhalb des unterstützten Umfangs sind in [Ideen](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas) willkommen. Reproduzierbare Fehler gehören in [Probleme](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose).

Identifizieren Sie bei DLL-, Native-Code-, Protected-Action- oder serverabhängigen Vorschlägen die Abhängigkeit explizit. Sie benötigen Machbarkeitsstudien und eine entsprechende Kontrolle des betroffenen Systems, bevor eine Umsetzung versprochen werden kann. Bitte archivieren Sie sie nicht als einfach fehlende DBC-Optionen.

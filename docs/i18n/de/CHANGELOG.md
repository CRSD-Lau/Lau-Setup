<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- RELEASE-120-NOTICE -->
> **Setup 1.2.0** — Ein ZIP enthält jetzt das Windows-Installationsprogramm und den Linux/Wine-Starter. Die Oberfläche folgt automatisch der Betriebssystemsprache mit zehn Optionen; eine manuelle Auswahl wird gespeichert. Spielversion 3.0.8 und die Spieldateien bleiben unverändert. Es gibt keine DBC-Änderungen.
>
> Die vollständige Aktualisierung der Anleitungen steht wegen Google-HTTP-429 noch aus. Der bisherige Text unten kann älter sein; maßgeblich sind die aktuelle englische Quelle und die Hinweise zu 1.2.0. [English](../../../CHANGELOG.md) · [1.2.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.2.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Automatische Übersetzung. [Englische Quelle](../../../CHANGELOG.md). Bei abweichenden Formulierungen ist die englische Quelle maßgeblich.

<a id="lau-setup-116-hotfix---switch-options-with-existing-disabled-patch-s"></a>

# Lau Setup 1.1.6 Hotfix – Optionen bei vorhandenem deaktiviertem Patch-S wechseln

Behebt die 1.1.5-Meldung „Ein anderer deaktivierter Patch-S ist bereits vorhanden“, wenn die visuelle Darstellung neuer Zauber nach einer früheren Installation deaktiviert wird.

Das Setup behält beide Dateien automatisch bei. Die aktuelle S-Datei wird immer zu `.mpq.disabled`. Wenn bereits eine andere ältere deaktivierte Kopie vorhanden ist, behält Setup diese ältere Kopie zunächst als `.mpq.disabled.<12-character hash>` bei. Eine identische gespeicherte Kopie wird wiederverwendet. Beide Versionen bleiben erhalten. Eine Kopie mit Hash-Namen, deren Inhalt nicht mit der älteren Datei übereinstimmt, die beibehalten wird, stoppt den Vorgang dennoch zur Überprüfung.

Dies gilt für Root- und Active-Locale-S-Dateien, einschließlich der Sequenz **alle drei Flags an -> Neue Zaubervisualisierungen aus**, wiederholte Wechsel und Rollback. Die Kartenauswahl bleibt erhalten.

Laden Sie die neue EXE- oder Wine-ZIP-Datei herunter und wiederholen Sie Ihre Auswahl. Sie müssen die vorhandene deaktivierte Kopie nicht löschen oder umbenennen, um die von 1.1.5 angezeigte normale Kollision zu beheben.

Um die vollständige Installation rückgängig zu machen, verwenden Sie **Vorherige Installation wiederherstellen**. Um eine gespeicherte S-Datei manuell wieder zu aktivieren, schließen Sie WoW und entfernen Sie `.disabled` und alle folgenden Hashes, um den ursprünglichen `.mpq`-Dateinamen wiederherzustellen. Überschreiben Sie niemals eine andere aktive Datei. Manuelle Änderungen können das verwaltete Rollback bei Dateidrift stoppen; Behalten Sie Ihre Backups. Dateien, die von Installationsprogrammen vor 1.1.5 entfernt wurden, müssen weiterhin über ihre Backups wiederhergestellt werden.

Die Spielveröffentlichung bleibt bestehen **3.0.8 Lau** und alle Spieldaten bleiben unverändert. Alle 90-Gradkegel, der Meteorfeuerradius und die Kaltflamme bleiben erhalten.

Die Prüfungen Windows und Wine umfassen 46-Regressionsgruppen, alle neun Gebietsschemas, vorhandene deaktivierte Dateien, wiederholtes Ein-/Ausschalten, Schutz vor manipuliertem Kopieren, Wiederherstellung nach Unterbrechung und exaktes Rollback. Neue öffentliche Downloads werden mit echten On/Off-Release-Dateien und einer älteren deaktivierten Kopie getestet. Dies ist eine Installer-Validierung, keine Validierung neuer Begegnungen im Spiel.

[Raw Six-Edition Patch-Y ZIP](https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.1.4/Lau-Patch-Y-3.0.8-All-Editions.zip)

[Installationshilfe und Änderungsprotokoll](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-115-hotfix---keep-disabled-patch-s-files"></a>

# Lau Setup 1.1.5 Hotfix – Deaktivierte Patch-S-Dateien beibehalten

Wenn Sie **Neue Zaubervisualisierungen** deaktivieren, bleiben die Root- und Active-Locale-Dateien Patch-S jetzt neben ihren ursprünglichen Speicherorten als `.mpq.disabled` erhalten, anstatt sie nur in Installer-Backups zu belassen. Ihre Bytes werden vor und nach der Änderung überprüft. WoW lädt den deaktivierten Dateinamen nicht.

– Eine andere vorhandene `.disabled`-Kopie blockiert die Installation; es wird nie überschrieben.
- Eine identische deaktivierte Kopie wird wiederverwendet und erhalten.
– Wenn Sie die Option aktivieren, werden die aktiven S-Dateien der ausgewählten Version installiert und deaktivierte Kopien bleiben erhalten.
- Wiederholte Installationen, Rollback und Unterbrechungswiederherstellung decken sowohl aktive als auch deaktivierte Pfade ab.

Um eine deaktivierte Datei manuell wieder zu aktivieren, schließen Sie WoW und entfernen Sie nur das Suffix `.disabled`. Überschreiben Sie keine andere aktive Datei. Um die vollständige Lau-Installation rückgängig zu machen, verwenden Sie **Vorherige Installation wiederherstellen**; Das Löschen von nur Patch-Y macht Q/M/ausführbare oder andere Änderungen nicht rückgängig. Manuelle Dateiänderungen können dazu führen, dass das verwaltete Rollback bei Abweichung gestoppt wird. Behalten Sie daher die Sicherungen.

**Bereits von einem älteren Installationsprogramm betroffen?** Dieses Update extrahiert alte Backups nicht automatisch. Verwenden Sie „Vorherige Installation wiederherstellen“, um diese Dateien wiederherzustellen. Arbeiten Sie dabei alle gestapelten Installationen rückwärts durch, bevor Sie mit dem neuen Setup eine Neuinstallation durchführen. Behalten Sie LauSetupBackups.

Die Spielveröffentlichung bleibt bestehen **3.0.8 Lau**. Alle MPQs bleiben unverändert: 90-Grad-Atemzüge/Schleimspray, genehmigt +50% Halion-Meteorfeuerradius und Kaltflamme bleiben erhalten. Laden Sie die neue EXE- oder Wine-ZIP-Datei für den Installer-Fix herunter.

Die Windows- und Wine-Validierung ist in VALIDATION.json enthalten. Die Tests umfassen alle neun Standorte, Kollisionen mit deaktiviertem Kopiervorgang, Ein-/Aus-Übergänge, wiederholte Installation, Unterbrechung bei jedem Verschiebungs-/Wiederherstellungsschritt, Dateidrift und exaktes Rollback. Der Fix beansprucht keine neue Validierung von Begegnungen im Spiel.

[Raw Six-Edition Patch-Y ZIP (unverändert 3.0.8)](https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.1.4/Lau-Patch-Y-3.0.8-All-Editions.zip)

[Installationshilfe und Änderungsprotokoll](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-114--game-release-308-lau"></a>

# Lau Setup 1.1.4 · Spielveröffentlichung 3.0.8 Lau

<a id="117-hotfix---patch-s-re-enable-cleanup"></a>

## 1.1.7 Hotfix – Patch-S Bereinigung wieder aktivieren

- Durch das erneute Aktivieren neuer Zaubervisualisierungen wird ein deaktivierter Patch-S wiederverwendet, wenn sein SHA-256 und seine Größe mit der ausgewählten Version übereinstimmen, wodurch dieser Download vermieden wird.
– Die einfach deaktivierte Kopie wird in die verifizierte Transaktionssicherung außerhalb von Daten verschoben, auch wenn aktive Patch-S bereits übereinstimmt. Verschiedene deaktivierte Dateien können durch „Vorherige Installation wiederherstellen“ weiterhin wiederhergestellt werden.
– Gilt für Root und aktives Gebietsschema Patch-S. Off verwendet weiterhin den einfachen Dateinamen `.mpq.disabled`. Vorhandene Archive mit Hash-Suffix bleiben erhalten.
– Spielnutzlasten bleiben 3.0.8 Lau. Windows und Wine haben jeweils die 50-Regressionsgruppen, das Ein-/Aus-/Einschalten realer Dateien und ein exaktes Rollback bestanden.

<a id="all-breath-and-slime-spray-warnings-are-now-90"></a>

## Alle Atem- und Schleimspray-Warnungen lauten jetzt 90°

Nach der Bestätigung des Warmane-Testers verwenden Halion (beide Realms), Saviana Ragefire, Sartharion, ICC Rimefang und Rotface Slime Spray jetzt **90° Gesamtkegel**, was der bestehenden 90°-Warnung von Sindragosa entspricht. Dies gilt für alle sechs Editionen und neun Clientsprachen, einschließlich der vorhandenen normalen/heroischen Zauberzuordnungen.

Nur die Kegelbreite ändert sich. Reichweite, Animationszeitpunkt, native Zaubereffekte und Zaubertabellen bleiben erhalten. Der genehmigte 50% größere Halion-Meteorfeuerradius, hellblaue Kaltflamme, Farben und Weihe bleiben unverändert. Dabei handelt es sich um optische Warnpuffer; Serverschaden und Mechanik bleiben unverändert. Unebenes Gelände kann dennoch zu flachen Kegeln führen.

<a id="updating"></a>

## Aktualisierung

Laden Sie zuerst **LauSetup.exe** oder **LauSetup-Wine.zip** aus dieser Version herunter. Schließen Sie WoW, wählen Sie denselben Client und dieselben Visuals aus und klicken Sie dann auf **Upgrade installieren**. Alte Installateure behalten ihre alten Kataloge. Überprüfen Sie `/pyversion` auf **3.0.8 Lau**.

Das Setup überprüft die tatsächlichen SHA-256-Hashes, sodass frühere Versionen und sogar Ein-Byte-Änderungen mit unveränderter Größe und Zeitstempel erkannt werden. Als bereits installiert gelten nur exakt aktuelle Dateien. Backups und die Wiederherstellung früherer Installationen bleiben verfügbar.

Windows erfordert .NET Framework 4.8. Wine-Benutzer extrahieren alle vier Dateien und führen `LauSetup.sh` als normaler Benutzer mit dem unterstützten bestehenden Wine/Mono-Präfix aus. Laufzeitinstallationsprogramme sind nicht im Paket enthalten.

<a id="validation"></a>

## Validierung

Siehe VALIDATION.json für Windows- und Wine-Regression, Sechs-Editionen-Upgrades von 3.0.7, Wiederholungserkennung, Ein-Byte-Prüfungen, Rollback und öffentliche Download-Prüfungen. Geometrieprüfungen überprüfen die 90°-Kegel, den erhaltenen Bereich, gültige Grenzen und die Dreieckswicklung in jeder Ausgabe. Genau elf bestehende Archivmitglieder ändern sich: fünf Modelle, ihre fünf Skins und das Versions-TOC. Alle anderen Mitglieder sind byteidentisch mit 3.0.7.

Die Breitenentscheidung folgt den gemeldeten Warmane-Tests. Bei dieser Version handelt es sich nicht um eine Zertifizierung für jede Begegnung oder eine exakte Servergrenzenzertifizierung.

[Website-Änderungsprotokoll und Installationshilfe](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-113--game-release-307-lau"></a>

# Lau Setup 1.1.3 · Spielveröffentlichung 3.0.7 Lau

<a id="larger-halion-meteor-fire-warnings"></a>

## Größere Halion-Meteorfeuerwarnungen

Fördert den vom Tester genehmigten **Test v2**: Der rote Bodenmarkierungsradius von Halion ist **50% größer als bei der Version 3.0.6**, rund um Wege und Landefeuer. Test v3 ist nicht enthalten. Kalte Flamme, Farben, Animationsspuren, einheimische Flammen, Weihe und die Sindragosa/Rotface-Kegel bleiben unverändert. Alle sechs Editionen und neun Clientsprachen werden unterstützt.

Der Tester bestätigte Version 2, nachdem er einen nicht aktualisierten Patch korrigiert hatte. Dies ist ein visueller Warnpuffer, keine Änderung des Serverschadens oder eine Zertifizierung jeder Position oder Begegnung.

<a id="update-with-the-new-installer"></a>

## Update mit dem neuen Installer

Laden Sie zuerst **LauSetup.exe** oder **LauSetup-Wine.zip** aus dieser Version herunter. Schließen Sie WoW, wählen Sie denselben Client und dieselben Visuals aus und klicken Sie dann auf **Upgrade installieren**. Alte Installateure behalten alte Kataloge. `/pyversion` meldet **3.0.7 Lau**.

Bestehende 3.0.6- und Test v2-Benutzer erhalten das Update. Setup vergleicht tatsächliche Datei-Hashes, einschließlich Ein-Byte-Änderungen mit unveränderter Größe und Zeitstempel; Als bereits installiert gelten nur exakt aktuelle Dateien. Backups und die Wiederherstellung früherer Installationen bleiben verfügbar.

Windows erfordert .NET Framework 4.8. Wine-Benutzer extrahieren alle vier Dateien und führen `LauSetup.sh` als normaler Benutzer mit dem unterstützten bestehenden Wine/Mono-Präfix aus. Es sind keine Laufzeitinstallationsprogramme im Paket enthalten.

<a id="validation-1"></a>

## Validierung

Windows- und Wine-Installer-Regression, Upgrades auf sechs Editionen, Wiederholungserkennung, Ein-Byte-Prüfungen, Rollback und öffentliche Download-Prüfungen werden in VALIDATION.json aufgezeichnet. Die Halion-Modelle und -Skins sind byteidentisch mit Test v2. Nur ihre Geometrie/Grenzen und das Versions-TOC unterscheiden sich von 3.0.6; Coldflame und andere Archivmitglieder bleiben unverändert.

[Website-Änderungsprotokoll und Installationshilfe](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-112--game-release-306-lau"></a>

# Lau Setup 1.1.2 · Spielveröffentlichung 3.0.6 Lau

<a id="blue-coldflame-red-meteor-fire"></a>

## Blaue Kaltflamme, rotes Meteorfeuer

- **Marrowgar Coldflame:** hellblaue Kreise mit vorhandenem nach innen gerichtetem Leuchten und Animation im Uhrzeigersinn, einschließlich heroischer Darstellung.
- **Halion-Meteorfeuer:** Feuern Sie rote Kreise um Pfade und Landungsfeuer mit der vorhandenen Animation im Uhrzeigersinn ab.
– Alle sechs HD-/Nicht-HD-Editionen und neun Client-Sprachen. Einheimische Flammen, Dauer, Weihungsoptionen und die 90° Sindragosa / 60° Rotface-Kegel bleiben unverändert.

[Animierte Farbvorschauen und vollständiges Änderungsprotokoll](https://wrath-multilingual-hd.vercel.app/#changelog). Bei den Vorschauen handelt es sich um illustrative Modelle, nicht um In-Game-Aufnahmen. Serverschaden und Mechanik bleiben unverändert; Warnkanten bleiben optische Puffer.

<a id="already-installed-download-the-new-installer-first"></a>

## Bereits installiert? Laden Sie zuerst das neue Installationsprogramm herunter

Laden Sie **LauSetup.exe** oder **LauSetup-Wine.zip** aus dieser Version herunter. Schließen Sie WoW, wählen Sie denselben Ordner und dieselben visuellen Einstellungen und klicken Sie dann auf **Upgrade installieren**. Alte heruntergeladene Installationsprogramme behalten ihren alten eingebetteten Katalog.

Das Setup hasht die tatsächlichen Dateien. Ältere 3.0.5-Dateien werden ersetzt; Selbst eine Änderung um ein Byte bei identischer Dateigröße und identischem Zeitstempel wird erkannt. Nur exakt neue Dateien werden als bereits installiert behandelt. `/pyversion` meldet **3.0.6 Lau**. Backups und die Wiederherstellung früherer Installationen bleiben verfügbar.

Wine-Benutzer: Extrahieren Sie alle vier Dateien zusammen und führen Sie `LauSetup.sh` als Ihr normaler Benutzer mit Ihrem vorhandenen 64-bit Wine 11.0 / Mono 10.4.1-Präfix aus. Python 3.9+ und lokaler Linux-Speicher sind erforderlich. Windows benötigt .NET Framework 4.8. Laufzeiten sind nicht gebündelt.

<a id="fresh-verification-on-windows-and-wine"></a>

## Neue Verifizierung für Windows und Wine

- 38 Regressionsgruppen pro Plattform, jeweils einschließlich 108 Gebietsschema-/Editions-/Kartenplänen.
- Alle sechs tatsächlichen Upgrades von 3.0.5 auf 3.0.6, wiederholte No-Op-Installationen und exaktes Rollback auf beiden Plattformen.
– Ein-Byte-Änderungen gleicher Größe/gleicher Zeitstempel wurden auf beiden Plattformen im Stammverzeichnis und im Gebietsschema Y unabhängig voneinander erkannt und repariert.
- Anonyme GitHub-Payload-Downloads, tatsächliche Kerninstallationen und Rollback auf Windows und Wine.
- 15 Linux Host-Sicherheitstests und der exakte Vier-Dateien-Launcher Wine unter einem normalen Benutzer; Windows Formular-Rendering überprüft.
- Drei Marker-M2-Texturreferenzen und das Versionsinhaltsverzeichnis wurden je Edition geändert; zwei Farbtexturen hinzugefügt. Alle anderen Mitglieder behalten Byte für Byte bei.

Diese Installationsprüfungen zertifizieren nicht jede Linux-Distribution oder jede Begegnung im Spiel. Die ausführbare Datei ist nicht digital signiert. Detaillierte Nachweise, Prüfsummen und Quelle sind beigefügt.

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-111--game-release-305-lau"></a>

# Lau Setup 1.1.1 · Spielveröffentlichung 3.0.5 Lau

<a id="wider-raid-warnings"></a>

## Umfangreichere Raid-Warnungen

- Sindragosa Frost Breath: **75° → 90° insgesamt** (7.5° extra pro Seite).
- Rotface Slime Spray: **25° → 60° insgesamt** (17.5° extra pro Seite).
– Gilt für alle sechs HD-/Nicht-HD-Editionen und ist mit allen neun Client-Gebietsschemata verfügbar. Andere Indikatoren, Weiheeinstellungen, lokalisierte Tabellen und Grafiken bleiben unverändert.

Dabei handelt es sich um gepufferte visuelle Warnungen, die auf Warmane-Raid-Aufnahmen und Zaubertrefferprotokollen basieren. Sie ändern weder den Serverschaden noch die Mechanik, noch geben sie eine genaue Schadensgrenze an.

<a id="updating-an-existing-installation"></a>

## Aktualisieren einer vorhandenen Installation

Laden Sie zuerst das neue **LauSetup.exe** oder **LauSetup-Wine.zip** herunter. Schließen Sie WoW, wählen Sie denselben Ordner und dieselben visuellen Optionen aus und klicken Sie dann auf **Upgrade installieren**. Das Installationsprogramm vergleicht tatsächliche Datei-Hashes: Ältere 3.0.4-Patches werden ersetzt, während eine genaue 3.0.5-Installation als bereits installiert gemeldet wird. `/pyversion` meldet **3.0.5 Lau** nach der Aktualisierung. Alte heruntergeladene Installationsprogramme behalten ihren alten Katalog.

Die Downloads von Windows und Wine enthalten dieselbe neu erstellte Setup-Programmdatei. Extrahieren Sie für Wine alle vier Dateien zusammen und verwenden Sie `LauSetup.sh` wie in der mitgelieferten README-Datei beschrieben. Bestehende Laufzeitanforderungen bleiben unverändert.

<a id="verification"></a>

## Verifizierung

Alle 38 Windows-Regressionsgruppen wurden bestanden, einschließlich der 108-Gebietsschema-/Editions-/Kartenpläne. Alle sechs Editionen haben das tatsächliche 3.0.4-auf-3.0.5-Upgrade, die wiederholte Installation und die genauen Rollback-Prüfungen bestanden. Neue Nutzlasten haben anonyme Download-/Hash-Prüfungen bestanden; eine isolierte Kerninstallation von GitHub und Rollback bestanden. Jede Edition behält jedes Mitglied mit Ausnahme von vier Modell-/Geometriedateien und dem Versions-TOC bei.

Der Launcher-Code Wine bleibt unverändert und die ZIP-Datei enthält die exakt neu erstellte EXE-Datei. Frühere Laufzeitnachweise Wine 11.0 / Mono 10.4.1 bleiben erhalten; Die neue Ausführung von Wine war nicht verfügbar, da die Docker-Engine nicht gestartet wurde. Die neue Kegelgeometrie wird statisch überprüft und nicht im Spiel neu zertifiziert.

Download-Prüfsummen, Quelle und der detaillierte Validierungsbericht sind beigefügt. Bewahren Sie `LauSetupBackups` zur Wiederherstellung auf.

Author / Creator / Last Modified By: Neil Mitchell

<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — Ein ZIP enthält jetzt das Windows-Installationsprogramm und den Linux/Wine-Starter. Die Oberfläche folgt automatisch der Betriebssystemsprache mit zehn Optionen; eine manuelle Auswahl wird gespeichert. Spielversion 3.0.8 und die Spieldateien bleiben unverändert. Es gibt keine DBC-Änderungen.
>
> Die vollständige Aktualisierung der Anleitungen steht wegen Google-HTTP-429 noch aus. Der bisherige Text unten kann älter sein; maßgeblich sind die aktuelle englische Quelle und die Hinweise zu 1.3.0. [English](../../../START-HERE.txt) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
>
> **Aktueller Download:** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) für Windows und Linux/Wine. Entpacken Sie den Ordner `LauSetup/` mit fünf Dateien: Windows öffnet `LauSetup.exe`; Linux/Wine führt `LauSetup.sh` aus. Die älteren Anweisungen unten zu getrennten EXE- oder Wine-ZIPs gelten nicht für 1.3.0.
>
> **1.3.0:** Erkannte zusätzliche Upgrade-Dateien werden automatisch gesichert; die Installation läuft weiter. Die Wiederherstellung bringt sie zurück. Kein manuelles Verschieben nötig.


<!-- BEGINNER-120-STEPS -->
## Erste Schritte

1. Schließen Sie WoW vollständig.
2. Laden Sie nur `LauSetup.zip` herunter. Unter Windows: Rechtsklick, **Alle extrahieren**, `LauSetup` öffnen und `LauSetup.exe` doppelklicken.
3. Wählen Sie **Ordner auswählen…** und den Ordner mit `WoW.exe` direkt darin – nicht `Data` und keinen Launcher-Ordner.
4. **Oberflächensprache** ändert nur Setup-Text: Automatisch folgt dem System, eine Auswahl wird gespeichert; die neun Spielsprachen ändern sich nicht.
5. **Verbesserte Weihe** ist standardmäßig aktiv. Neue Zaubereffekte brauchen erkannte kompatible HD-Modelle; Karten/Minikarte sind optional.
6. Wählen Sie **Upgrade installieren**, warten Sie bis zum Ende und schließen Sie Setup nicht. Starten Sie WoW und geben Sie `/pyversion` ein. Wiederherstellung: WoW schließen, denselben Ordner wählen und **Vorherige Installation wiederherstellen** wählen.

### Linux/Wine

Nutzen Sie dieselbe ZIP erst mit vorhandenem 64-bit-Wine-Präfix, Wine 11.0, Wine Mono 10.4.1, Python 3.9+, dokumentierten Schriften und lokalem Linux-Speicher. Entpacken Sie sie und führen Sie `WINEPREFIX="/path/to/prefix" sh LauSetup.sh` aus; starten Sie die EXE nie direkt unter Wine.
<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Automatische Übersetzung. [Englische Quelle](../../../START-HERE.txt). Bei abweichenden Formulierungen ist die englische Quelle maßgeblich.

LAU-SETUP – RELEASE 3.0.8

Windows und Linux/Wine: Laden Sie `LauSetup.zip` herunter und entpacken Sie `LauSetup/`. Windows: öffnen Sie `LauSetup/LauSetup.exe`. Linux/Wine: führen Sie `LauSetup/LauSetup.sh` aus.
Für Wine ist der mitgelieferte Linux-Launcher erforderlich. Führen Sie die EXE-Datei nicht direkt aus.

1. Schließen Sie World of Warcraft.
2. Öffnen Sie LauSetup.exe und wählen Sie Ihren WoW-Ordner.
3. Wählen Sie Ihr Bildmaterial aus und klicken Sie auf „Upgrade installieren“.

Aktualisieren Sie von einer älteren Version oder Testversion 2? Laden Sie zuerst das neue Installationsprogramm herunter; alte Exemplare betten den alten Katalog ein.
Wählen Sie denselben Kunden und dasselbe Bildmaterial aus. Datei-Hash-Prüfungen erkennen die geänderten Patches.
Starten Sie WoW und geben Sie /pyversion ein. Es sollte 3.0.8 Lau gemeldet werden.

Das Installationsprogramm erkennt Ihre Client-Sprache und HD-Modellkonfiguration.
„Erweiterte Weihe“ ist standardmäßig ausgewählt. Deaktivieren Sie es für den Bestand
Aussehen; Der Zauber selbst funktioniert immer noch. Neue Zaubervisualisierungen erfordern eine
vorhandenen kompatiblen HD-Modell-Client. Aktualisierte Karten/Minikarten sind optional.

Sie benötigen einen vorhandenen WoW 3.3.5a-Client, Build 12340, auf Windows 10 oder 11.
Bei diesem Download handelt es sich um ein Upgrade, nicht um einen vollständigen Client oder ein Sprachpaket.
Die erforderliche kompatible WoW.exe wird automatisch installiert.

Es ist kein manuelles Kopieren oder Umbenennen von Patches erforderlich. Laden Sie nicht das gesamte herunter
gemeinsame Datenfreigabe. Die App lädt nur die für Ihre Auswahl erforderlichen Dateien herunter.

Backups und fortsetzbare Downloads bleiben in LauSetupBackups in Ihrem WoW
Ordner, außerhalb von Data. Um das Update rückgängig zu machen, schließen Sie WoW, öffnen Sie LauSetup.exe erneut.
Wählen Sie denselben Ordner und klicken Sie auf Vorherige Installation wiederherstellen. Erholung auch
Funktioniert, wenn WoW.exe aufgrund eines unterbrochenen Updates vorübergehend fehlt.

Ihre Add-ons, SavedVariables, Schriftarten, Login-Grafik, Realm-Einstellungen und
Nicht verwandte Patches bleiben erhalten. Kein Pizza Warriors-Branding, persönlich
ElvUI-Setup, LoginUI, Kontodaten oder der vollständige Spielclient sind im Paket enthalten.

Downloads stammen von GitHub Releases; Es ist kein GitHub-Konto erforderlich.
Wenn ein Download abbricht, versuchen Sie es später noch einmal. Verifizierte Dateien
werden wiederverwendet und teilweise Downloads werden fortgesetzt. Spieldateien werden erst danach geändert
Alle erforderlichen Downloads haben die Überprüfung bestanden. Behalten Sie LauSetupBackups, wenn
Die App meldet, dass eine Wiederherstellung erforderlich ist.

Dieses Installationsprogramm ist nicht digital signiert, sodass Windows möglicherweise einen unbekannten Herausgeber anzeigt
Warnung. Verwenden Sie die bereitgestellte Prüfsumme, um Ihren Download zu überprüfen. Das ist nicht der Fall
erfordern die Deaktivierung der Windows-Sicherheit oder die Installation von Python/PowerShell-Tools.
Die .NET Framework 4.8-Laufzeit ist erforderlich.

Sobald dieses Installationsprogramm das Karten-Upgrade hinzugefügt hat, behält es dieses Upgrade bei
Editionsänderungen. Verwenden Sie „Vorherige Installation wiederherstellen“, um die Karteninstallation rückgängig zu machen.

Credits: Andre (Patch-Y-Grundlinien), Loriendal und Trimitor (HD-Grundlage),
Project Reforged Mitwirkende (HD-Kunstwerk), Blizzard (Originalkunstwerk und
lokalisierter Text), Lau (Anpassung, Kompatibilität, Indikatoren, Tests).

Author / Creator / Last Modified By: Neil Mitchell

Setup 1.1.7: Neue Zaubervisualisierungen bleiben ausgeschaltet, Patch-S bleibt als .mpq.disabled daneben
seinen ursprünglichen Weg. Eine andere deaktivierte Kopie wird niemals überschrieben.
Um die vollständige Installation rückgängig zu machen, verwenden Sie „Vorherige Installation wiederherstellen“. Für Dateien
bereits durch ältere Setup-Versionen entfernt wurden, stellen Sie sie aus diesen Backups wieder her
Verwenden Sie Vorherige Installation wiederherstellen, bevor Sie eine Neuinstallation durchführen. Behalten Sie LauSetupBackups.

Die aktuelle S-Datei wird immer zu .mpq.disabled. Wenn ein älterer Behinderter
Wenn eine Kopie vorhanden ist, behält Setup sie zunächst als `.mpq.disabled.<12-character hash>` bei. Kein manuelles Umbenennen
wird zum Wechseln der Optionen benötigt. Für die manuelle erneute Aktivierung ist eine Entfernung erforderlich
.disabled und jeder folgende Hash, wobei WoW geschlossen und kein anderes aktiv ist
Datei wird überschrieben. Verwenden Sie „Vorherige Installation wiederherstellen“ für ein verwaltetes Rollback.

1.1.7 Hotfix: Durch die Aktivierung neuer Zaubervisualisierungen wird ein passender deaktivierter Patch-S wiederverwendet, ohne ihn erneut herunterzuladen. Die einfach deaktivierte Kopie wird in die verifizierte Transaktionssicherung in LauSetupBackups verschoben, auch wenn die aktive Kopie Patch-S bereits übereinstimmt. Verschiedene Versionen bleiben mit „Vorherige Installation wiederherstellen“ wiederherstellbar. Beim Ausschalten wird weiterhin .mpq.disabled verwendet. Vorhandene Archive mit Hash-Suffix bleiben erhalten.

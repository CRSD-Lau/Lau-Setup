<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- HOTFIX-118-NOTICE -->
> **Hotfix 1.1.8** — Setup prüft MPQs in Data und im aktiven Sprachordner auf bekannte umbenannte Patch-Y-Dateien und exakte Katalogkopien. Bei einem möglichen Konflikt oder einem nicht lesbaren bzw. nicht unterstützten Archiv stoppt es und nennt die Datei; es löscht sie nicht automatisch. Nur den Dateinamen zu ändern verändert den Inhalts-Hash nicht. Die Spieldateien bleiben auf 3.0.8.
>
> Die vollständige Übersetzung konnte wegen einer Google-Anfragebegrenzung noch nicht aktualisiert werden. Der bisherige Text unten ist ein älterer Stand. Maßgeblich sind die aktuellen englischen Angaben. [English](../../../START-HERE.txt) · [1.1.8](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.1.8)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Automatische Übersetzung. [Englische Quelle](../../../START-HERE.txt). Bei abweichenden Formulierungen ist die englische Quelle maßgeblich.

LAU-SETUP – RELEASE 3.0.8

Windows: LauSetup.exe herunterladen.
Linux/Wine: Laden Sie LauSetup-Wine.zip herunter und folgen Sie seinem README.txt.
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

<!-- LANGUAGES:START -->
[English](../../../../README.md) · [Deutsch](../README.md) · [Español (España)](../../es-ES/README.md) · [Español (México)](../../es-MX/README.md) · [Français](../../fr/README.md) · [한국어](../../ko/README.md) · [Русский](../../ru/README.md) · [简体中文](../../zh-CN/README.md) · [繁體中文](../../zh-TW/README.md) · [Português (Brasil)](../../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.4.0** — Ein ZIP enthält jetzt das Windows-Installationsprogramm und den Linux/Wine-Starter. Die Oberfläche folgt automatisch der Betriebssystemsprache mit zehn Optionen; eine manuelle Auswahl wird gespeichert. Spielversion 3.0.8 und die Spieldateien bleiben unverändert. Es gibt keine DBC-Änderungen.
>
> Die vollständige Aktualisierung der Anleitungen steht wegen Google-HTTP-429 noch aus. Der bisherige Text unten kann älter sein; maßgeblich sind die aktuelle englische Quelle und die Hinweise zu 1.4.0. [English](../../../../wine/README.txt) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)
>
> **Aktueller Download:** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) für Windows und Linux/Wine. Entpacken Sie den Ordner `LauSetup/` mit fünf Dateien: Windows öffnet `LauSetup.exe`; Linux/Wine führt `LauSetup.sh` aus. Die älteren Anweisungen unten zu getrennten EXE- oder Wine-ZIPs gelten nicht für 1.4.0.
>
> **1.4.0:** Erkannte zusätzliche Upgrade-Dateien werden automatisch gesichert; die Installation läuft weiter. Die Wiederherstellung bringt sie zurück. Kein manuelles Verschieben nötig. Setup bewahrt vorhandene Dateien automatisch auf, bevor es sie ersetzt oder verschiebt. Unbeteiligte Dateien bleiben unverändert.



> **1.4.0:** Spielordner wählen → Weiter → Grafik wählen → Weiter → Auswahl prüfen → Upgrade installieren → Fertigstellen. Patch-Y HD oder Patch-Y Non-HD wird fest für den erkannten Client ausgewählt. Extras starten ausgeschaltet; bereits installierte Karten bleiben erhalten. Die Prüfung zeigt Patch-Y (Laus Version) plus gewählte Extras sowie WoW.exe, Patch-Q, Sprachdateien, Downloadgröße und Sicherungen. Weiter ändert keine Spieldateien. Die Oberflächensprache lässt sich in jedem Schritt manuell wählen und wird gespeichert; Automatisch folgt wieder dem System. Vorherige Installation wiederherstellen bleibt verfügbar.

<!-- BEGINNER-140-STEPS -->
1. Schließen Sie WoW vollständig.
2. Laden Sie nur `LauSetup.zip` herunter. Unter Windows: Rechtsklick, **Alle extrahieren**, `LauSetup` öffnen und `LauSetup.exe` doppelklicken.

Spielordner wählen → Weiter → Grafik wählen → Weiter → Auswahl prüfen → Upgrade installieren → Fertigstellen. Patch-Y HD oder Patch-Y Non-HD wird fest für den erkannten Client ausgewählt. Extras starten ausgeschaltet; bereits installierte Karten bleiben erhalten. Die Prüfung zeigt Patch-Y (Laus Version) plus gewählte Extras sowie WoW.exe, Patch-Q, Sprachdateien, Downloadgröße und Sicherungen. Weiter ändert keine Spieldateien. Die Oberflächensprache lässt sich in jedem Schritt manuell wählen und wird gespeichert; Automatisch folgt wieder dem System. Vorherige Installation wiederherstellen bleibt verfügbar.

Linux/Wine: Wine 11.0, Wine Mono 10.4.1, Python 3.9+, 64-bit WINEPREFIX. `WINEPREFIX="/path/to/prefix" sh LauSetup.sh`. [Guide](https://github.com/CRSD-Lau/Lau-Setup/blob/main/wine/README.txt).

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Automatische Übersetzung. [Englische Quelle](../../../../wine/README.txt). Bei abweichenden Formulierungen ist die englische Quelle maßgeblich.

Lau Setup für Wine auf Linux
Author / Creator / Last Modified By: Neil Mitchell

1. Verwenden Sie einen vorhandenen WoW 3.3.5a Build 12340-Client auf einem lokalen Linux-Dateisystem.
2. Schließen Sie jede WoW-Instanz, einschließlich Spiele mit anderen Wine-Präfixen.
3. Extrahieren Sie `LauSetup.zip`. Halten Sie die fünf Dateien in `LauSetup/` zusammen: `LauSetup.exe`, `LauSetup.sh`, `lau_wine.py`, `lau-languages.json` und `README.txt`.
4. Öffnen Sie ein Terminal im extrahierten Ordner und führen Sie Folgendes aus:

```sh
WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh
```

5. Wählen Sie Ihren vorhandenen Spielordner und installieren Sie ihn. Die üblichen automatischen Backups
   und die Schaltfläche „Vorherige Installation wiederherstellen“ sind verfügbar.

Anforderungen für diese Version:
- Wine 11.0, ein 64-bit-Präfix und Wine Mono 10.4.1 dort bereits installiert.
- Python 3.9 oder neuer für den Host-Sicherheitshelfer (nur Standardbibliothek).
- Liberation Sans- oder DejaVu Sans-Schriftarten; Das komplette Wine-Schriftpaket muss vorhanden sein
  ebenfalls installiert werden, damit die eigenen Standardsteuerelemente von Wine Mono gerendert werden können.
- Lokaler Linux-Speicher. Netzwerkfreigaben und auf Windows gemountete Laufwerke sind ausgeschlossen.
- Normale Sichtbarkeit des Host-Prozesses. Führen Sie diesen Launcher nicht über eine Sandbox aus
  Dadurch werden andere Wine-Prozesse ausgeblendet. Führen Sie es als normaler Benutzer aus, niemals sudo/root.

Das Präfix 64-bit kann den Client 32-bit WoW enthalten. Dieses Installationsprogramm funktioniert nicht
Erstellen, konvertieren oder aktualisieren Sie Ihr Wine-Präfix, installieren Sie Wine/Mono und konfigurieren Sie es
DXVK oder ändern Sie Ihren Game Launcher. Verwenden Sie das Wine-Setup Ihrer Distribution
Anweisungen zuerst, wenn die Laufzeit fehlt.

Offizielles Wine Mono-Paket für diese getestete Laufzeit:
https://github.com/wine-mono/wine-mono/releases/tag/wine-mono-10.4.1

Verwenden Sie die Laufzeit Wine Mono mit Wine. Das Windows .NET Framework-Installationsprogramm ist
nicht im Lieferumfang enthalten und für diese getestete Wine Mono-Konfiguration nicht erforderlich.

Starten Sie immer über LauSetup.sh. LauSetup.exe direkt unter Wine ausführen
lehnt Clientoperationen ohne den Linux-Helfer ab. Es überprüft Hostpfade
und verarbeitet und hält eine Hostsperre, die für alle Wine-Präfixe gilt. Wenn es aufhört,
Öffnen Sie den Launcher erneut und stellen Sie die ausstehende Installation wieder her, bevor Sie es erneut versuchen.

Halten Sie WoW geschlossen, bis die Einrichtung abgeschlossen ist. Prozesskontrollen reduzieren Rennen; sie können es nicht
Verhindern Sie, dass ein anderes Programm das Spiel startet oder anschließend Dateien ändert.
Symlinkierte Pfade, Hardlinks und mehrdeutige Dateinamenschreibweisen werden abgelehnt. Daten
und Backup-Verzeichnisse müssen auf demselben Dateisystem wie der Client bleiben.

Validierungsumfang: isoliert Wine 11.0 / Wine Mono 10.4.1 Kunden, Vorrichtungen und
Installations-/Wiederherstellungstests für echte Nutzlasten, Sicherheitstests mit zwei Präfixen und Beispiel-GUI
Schecks. Dies ist nicht die Zertifizierung aller Linux Verteilung, Dateisystem,
Anzeigeskala, Wine Version oder Spielbegegnung. Kein Lutris, Proton oder macOS
Die Integration ist in dieser Version enthalten.

Die Installationsoberfläche folgt automatisch der Betriebssystemsprache mit zehn Optionen; eine manuelle Auswahl wird gespeichert. Die Client-Spieldaten unterstützen weiterhin neun Gebietsschemas und richten sich nach dem erkannten Spielgebietsschema.

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

1.1.7 Bereinigung erneut aktivieren: Matching deaktiviert. Patch-S wird lokal wiederverwendet. Die einfach deaktivierte Kopie wird in die verifizierte Transaktionssicherung in LauSetupBackups verschoben, sodass ein aktives S übrig bleibt. Verschiedene Kopien können durch „Vorherige Installation wiederherstellen“ weiterhin wiederhergestellt werden. Vorhandene Archive mit Hash-Suffix werden nicht bereinigt.

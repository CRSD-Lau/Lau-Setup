"""Make delayed translated snapshots point to the single 1.2.0 installer ZIP.

Author/Creator/Modifier: Neil Mitchell. This intentionally does not claim a
fresh full translation or alter translation cache/freshness records.
"""
from pathlib import Path
import re
import json


ROOT = Path(__file__).resolve().parents[1]
ZIP = "https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip"
OLD = re.compile(
    r"<!-- RELEASE-120-NOTICE -->\n(?P<body>.*?)(?=\n<!-- Author:)", re.DOTALL
)
ZIP_NOTICE = "<!-- ZIP-ONLY-120-NOTICE -->"
ZIP_LABEL = re.compile(
    r"(\[[^\]\n]*?)LauSetup(?:\.exe|-Wine\.zip)([^\]\n]*\]\(" + re.escape(ZIP) + r"\))"
)
QUICKSTART = {
    "de": "**Aktueller Download:** [LauSetup.zip](" + ZIP + ") für Windows und Linux/Wine. Entpacken Sie den Ordner `LauSetup/` mit fünf Dateien: Windows öffnet `LauSetup.exe`; Linux/Wine führt `LauSetup.sh` aus. Die älteren Anweisungen unten zu getrennten EXE- oder Wine-ZIPs gelten nicht für 1.2.0.",
    "fr": "**Téléchargement actuel :** [LauSetup.zip](" + ZIP + ") pour Windows et Linux/Wine. Extrayez le dossier `LauSetup/` avec cinq fichiers : Windows ouvre `LauSetup.exe` ; Linux/Wine lance `LauSetup.sh`. Les anciennes instructions ci-dessous sur des ZIP Wine ou EXE séparés ne s’appliquent pas à 1.2.0.",
    "es-ES": "**Descarga actual:** [LauSetup.zip](" + ZIP + ") para Windows y Linux/Wine. Extrae la carpeta `LauSetup/` con cinco archivos: en Windows abre `LauSetup.exe`; en Linux/Wine ejecuta `LauSetup.sh`. Las instrucciones antiguas de abajo sobre ZIP Wine o EXE separados no se aplican a 1.2.0.",
    "es-MX": "**Descarga actual:** [LauSetup.zip](" + ZIP + ") para Windows y Linux/Wine. Extrae la carpeta `LauSetup/` con cinco archivos: en Windows abre `LauSetup.exe`; en Linux/Wine ejecuta `LauSetup.sh`. Las instrucciones antiguas de abajo sobre ZIP Wine o EXE separados no se aplican a 1.2.0.",
    "ko": "**현재 다운로드:** Windows와 Linux/Wine용 [LauSetup.zip](" + ZIP + ")입니다. 다섯 파일이 있는 `LauSetup/` 폴더를 추출하세요. Windows에서는 `LauSetup.exe`를 열고 Linux/Wine에서는 `LauSetup.sh`를 실행합니다. 아래의 별도 EXE 또는 Wine ZIP 관련 이전 안내는 1.2.0에 적용되지 않습니다.",
    "pt-BR": "**Download atual:** [LauSetup.zip](" + ZIP + ") para Windows e Linux/Wine. Extraia a pasta `LauSetup/` com cinco arquivos: no Windows, abra `LauSetup.exe`; no Linux/Wine, execute `LauSetup.sh`. As instruções antigas abaixo sobre EXE ou ZIP Wine separados não se aplicam à versão 1.2.0.",
    "ru": "**Текущая загрузка:** [LauSetup.zip](" + ZIP + ") для Windows и Linux/Wine. Распакуйте папку `LauSetup/` с пятью файлами: в Windows откройте `LauSetup.exe`; в Linux/Wine запустите `LauSetup.sh`. Старые инструкции ниже об отдельных EXE или Wine ZIP не относятся к 1.2.0.",
    "zh-CN": "**当前下载：** Windows 和 Linux/Wine 都使用 [LauSetup.zip](" + ZIP + ")。解压含五个文件的 `LauSetup/` 文件夹：Windows 打开 `LauSetup.exe`；Linux/Wine 运行 `LauSetup.sh`。下方关于单独 EXE 或 Wine ZIP 的旧说明不适用于 1.2.0。",
    "zh-TW": "**目前下載：** Windows 和 Linux/Wine 都使用 [LauSetup.zip](" + ZIP + ")。解壓含五個檔案的 `LauSetup/` 資料夾：Windows 開啟 `LauSetup.exe`；Linux/Wine 執行 `LauSetup.sh`。下方關於個別 EXE 或 Wine ZIP 的舊說明不適用於 1.2.0。",
}

# These three visible instructions were part of the older translated snapshots.
# Keep the translations otherwise intact, but make the operational steps true for
# the one-file 1.2.0 release.  The five-file folder is named explicitly so a
# newcomer does not mistake the old standalone EXE/Wine ZIP aliases for current
# downloads.
OPERATIONAL = {
    "de": (
        "2. **Starten Sie das Setup und wählen Sie Ihren Client-Ordner.** Entpacken Sie `LauSetup.zip` in den Ordner `LauSetup/`. Windows: Öffnen Sie daraus `LauSetup.exe`. Linux/Wine: führen Sie daraus `LauSetup.sh` aus.",
        "Windows und Linux/Wine: Laden Sie `LauSetup.zip` herunter und entpacken Sie `LauSetup/`. Windows: öffnen Sie `LauSetup/LauSetup.exe`. Linux/Wine: führen Sie `LauSetup/LauSetup.sh` aus.\nFür Wine ist der mitgelieferte Linux-Launcher erforderlich. Führen Sie die EXE-Datei nicht direkt aus.",
        "3. Extrahieren Sie `LauSetup.zip`. Halten Sie die fünf Dateien in `LauSetup/` zusammen: `LauSetup.exe`, `LauSetup.sh`, `lau_wine.py`, `lau-languages.json` und `README.txt`.",
    ),
    "fr": (
        "2. **Lancez l’installation et choisissez votre dossier client.** Extrayez `LauSetup.zip` dans le dossier `LauSetup/`. Sous Windows, ouvrez `LauSetup.exe`; sous Linux/Wine, lancez `LauSetup.sh`.",
        "Windows et Linux/Wine : téléchargez `LauSetup.zip` et extrayez `LauSetup/`. Sous Windows, ouvrez `LauSetup/LauSetup.exe`; sous Linux/Wine, lancez `LauSetup/LauSetup.sh`.\nPour Wine, utilisez le lanceur Linux inclus. N’exécutez pas directement l’EXE.",
        "3. Extrayez `LauSetup.zip`. Conservez les cinq fichiers de `LauSetup/` ensemble : `LauSetup.exe`, `LauSetup.sh`, `lau_wine.py`, `lau-languages.json` et `README.txt`.",
    ),
    "es-ES": (
        "2. **Inicie la configuración y elija su carpeta de cliente.** Extraiga `LauSetup.zip` en la carpeta `LauSetup/`. En Windows abra `LauSetup.exe`; en Linux/Wine ejecute `LauSetup.sh`.",
        "Windows y Linux/Wine: descargue `LauSetup.zip` y extraiga `LauSetup/`. En Windows abra `LauSetup/LauSetup.exe`; en Linux/Wine ejecute `LauSetup/LauSetup.sh`.\nPara Wine use el iniciador Linux incluido. No ejecute directamente el EXE.",
        "3. Extraiga `LauSetup.zip`. Mantenga juntos los cinco archivos de `LauSetup/`: `LauSetup.exe`, `LauSetup.sh`, `lau_wine.py`, `lau-languages.json` y `README.txt`.",
    ),
    "es-MX": (
        "2. **Inicie la configuración y elija su carpeta de cliente.** Extraiga `LauSetup.zip` en la carpeta `LauSetup/`. En Windows abra `LauSetup.exe`; en Linux/Wine ejecute `LauSetup.sh`.",
        "Windows y Linux/Wine: descargue `LauSetup.zip` y extraiga `LauSetup/`. En Windows abra `LauSetup/LauSetup.exe`; en Linux/Wine ejecute `LauSetup/LauSetup.sh`.\nPara Wine use el iniciador Linux incluido. No ejecute directamente el EXE.",
        "3. Extraiga `LauSetup.zip`. Mantenga juntos los cinco archivos de `LauSetup/`: `LauSetup.exe`, `LauSetup.sh`, `lau_wine.py`, `lau-languages.json` y `README.txt`.",
    ),
    "pt-BR": (
        "2. **Inicie a configuração e escolha sua pasta de cliente.** Extraia `LauSetup.zip` na pasta `LauSetup/`. No Windows, abra `LauSetup.exe`; no Linux/Wine, execute `LauSetup.sh`.",
        "Windows e Linux/Wine: baixe `LauSetup.zip` e extraia `LauSetup/`. No Windows, abra `LauSetup/LauSetup.exe`; no Linux/Wine, execute `LauSetup/LauSetup.sh`.\nPara Wine, use o inicializador Linux incluído. Não execute o EXE diretamente.",
        "3. Extraia `LauSetup.zip`. Mantenha juntos os cinco arquivos de `LauSetup/`: `LauSetup.exe`, `LauSetup.sh`, `lau_wine.py`, `lau-languages.json` e `README.txt`.",
    ),
    "ru": (
        "2. **Запустите установку и выберите папку клиента.** Распакуйте `LauSetup.zip` в папку `LauSetup/`. В Windows откройте `LauSetup.exe`; в Linux/Wine запустите `LauSetup.sh`.",
        "Windows и Linux/Wine: загрузите `LauSetup.zip` и распакуйте `LauSetup/`. В Windows откройте `LauSetup/LauSetup.exe`; в Linux/Wine запустите `LauSetup/LauSetup.sh`.\nДля Wine используйте входящий в комплект запускатель Linux. Не запускайте EXE напрямую.",
        "3. Распакуйте `LauSetup.zip`. Храните вместе пять файлов из `LauSetup/`: `LauSetup.exe`, `LauSetup.sh`, `lau_wine.py`, `lau-languages.json` и `README.txt`.",
    ),
    "ko": (
        "2. **설정을 실행하고 클라이언트 폴더를 선택하세요.** `LauSetup.zip`을 `LauSetup/` 폴더로 추출하세요. Windows에서는 `LauSetup.exe`를 열고 Linux/Wine에서는 `LauSetup.sh`를 실행합니다.",
        "Windows와 Linux/Wine: `LauSetup.zip`을 내려받아 `LauSetup/`을 추출하세요. Windows에서는 `LauSetup/LauSetup.exe`를 열고 Linux/Wine에서는 `LauSetup/LauSetup.sh`를 실행합니다.\nWine에서는 포함된 Linux 실행기를 사용하세요. EXE를 직접 실행하지 마세요.",
        "3. `LauSetup.zip`을 추출하세요. `LauSetup/`의 다섯 파일을 함께 보관하세요: `LauSetup.exe`, `LauSetup.sh`, `lau_wine.py`, `lau-languages.json`, `README.txt`.",
    ),
    "zh-CN": (
        "2。 **启动安装程序并选择您的客户端文件夹。** 将 `LauSetup.zip` 解压到 `LauSetup/` 文件夹。Windows 打开 `LauSetup.exe`；Linux/Wine 运行 `LauSetup.sh`。",
        "Windows 和 Linux/Wine：下载 `LauSetup.zip` 并解压 `LauSetup/`。Windows 打开 `LauSetup/LauSetup.exe`；Linux/Wine 运行 `LauSetup/LauSetup.sh`。\nWine 请使用随附的 Linux 启动器，不要直接运行 EXE。",
        "3。解压 `LauSetup.zip`。将 `LauSetup/` 中的五个文件放在一起：`LauSetup.exe`、`LauSetup.sh`、`lau_wine.py`、`lau-languages.json` 和 `README.txt`。",
    ),
    "zh-TW": (
        "2。 **啟動安裝程式並選擇您的用戶端資料夾。** 將 `LauSetup.zip` 解壓到 `LauSetup/` 資料夾。Windows 開啟 `LauSetup.exe`；Linux/Wine 執行 `LauSetup.sh`。",
        "Windows 和 Linux/Wine：下載 `LauSetup.zip` 並解壓 `LauSetup/`。Windows 開啟 `LauSetup/LauSetup.exe`；Linux/Wine 執行 `LauSetup/LauSetup.sh`。\nWine 請使用隨附的 Linux 啟動器，不要直接執行 EXE。",
        "3。解壓 `LauSetup.zip`。將 `LauSetup/` 中的五個檔案放在一起：`LauSetup.exe`、`LauSetup.sh`、`lau_wine.py`、`lau-languages.json` 和 `README.txt`。",
    ),
}

LIMITATION_UI = {
    "de": "- Die Installationsoberfläche folgt automatisch der Betriebssystemsprache mit zehn Optionen; eine manuelle Auswahl wird gespeichert. Die Spielinhalte unterstützen weiterhin neun Gebietsschemas. Durch die alleinige Änderung von `Config.wtf` werden keine Dateien oder Schriftarten einer anderen Sprache installiert.",
    "fr": "- L’interface de l’installateur suit automatiquement la langue du système parmi dix options ; un choix manuel est mémorisé. Le contenu du jeu prend toujours en charge neuf langues. Modifier uniquement `Config.wtf` n’installe pas les fichiers ou polices d’une autre langue.",
    "es-ES": "- La interfaz del instalador sigue automáticamente el idioma del sistema entre diez opciones; la elección manual se guarda. El contenido del juego sigue admitiendo nueve configuraciones regionales. Cambiar solo `Config.wtf` no instala archivos ni fuentes de otro idioma.",
    "es-MX": "- La interfaz del instalador sigue automáticamente el idioma del sistema entre diez opciones; la elección manual se guarda. El contenido del juego sigue admitiendo nueve configuraciones regionales. Cambiar solo `Config.wtf` no instala archivos ni fuentes de otro idioma.",
    "pt-BR": "- A interface do instalador segue automaticamente o idioma do sistema entre dez opções; a escolha manual é salva. O conteúdo do jogo continua a oferecer suporte a nove localidades. Alterar apenas `Config.wtf` não instala arquivos ou fontes de outro idioma.",
    "ru": "- Интерфейс установщика автоматически следует языку ОС из десяти вариантов; ручной выбор сохраняется. Игровой контент по-прежнему поддерживает девять языков. Изменение только `Config.wtf` не устанавливает файлы или шрифты другого языка.",
    "ko": "- 설치 프로그램 인터페이스는 열 가지 옵션 중 운영 체제 언어를 자동으로 따르며 수동 선택은 저장됩니다. 게임 콘텐츠는 계속 9개 로케일을 지원합니다. `Config.wtf`만 변경해도 다른 언어의 파일이나 글꼴은 설치되지 않습니다.",
    "zh-CN": "- 安装程序界面会在十种选项中自动跟随操作系统语言，手动选择会被保存。游戏内容仍支持九种语言环境。仅更改 `Config.wtf` 不会安装其他语言的文件或字体。",
    "zh-TW": "- 安裝程式介面會在十種選項中自動跟隨作業系統語言，手動選擇會被儲存。遊戲內容仍支援九種語言環境。僅變更 `Config.wtf` 不會安裝其他語言的檔案或字型。",
}

HISTORICAL_PLATFORM = {
    "de": "> **Historische Bewertung unten:** Die folgenden Abschnitte zu 1.0.1/1.1.0 beschreiben den damaligen Prüfstand. Für die aktuelle Installation mit einem gemeinsamen ZIP beachten Sie den Hinweis zu Setup 1.2.0 oben.",
    "fr": "> **Évaluation historique ci-dessous :** les sections suivantes sur 1.0.1/1.1.0 décrivent l’état évalué à cette époque. Pour l’installation actuelle avec un ZIP commun, consultez l’avis Setup 1.2.0 ci-dessus.",
    "es-ES": "> **Evaluación histórica a continuación:** las secciones siguientes sobre 1.0.1/1.1.0 describen el estado evaluado entonces. Para la instalación actual con un ZIP compartido, consulte el aviso de Setup 1.2.0 de arriba.",
    "es-MX": "> **Evaluación histórica a continuación:** las secciones siguientes sobre 1.0.1/1.1.0 describen el estado evaluado entonces. Para la instalación actual con un ZIP compartido, consulte el aviso de Setup 1.2.0 de arriba.",
    "pt-BR": "> **Avaliação histórica abaixo:** as seções seguintes sobre 1.0.1/1.1.0 descrevem o estado avaliado naquela época. Para a instalação atual com um ZIP compartilhado, consulte o aviso do Setup 1.2.0 acima.",
    "ru": "> **Историческая оценка ниже:** следующие разделы о 1.0.1/1.1.0 описывают состояние на момент оценки. Для текущей установки с единым ZIP смотрите уведомление о Setup 1.2.0 выше.",
    "ko": "> **아래는 과거 평가입니다:** 다음 1.0.1/1.1.0 섹션은 당시의 평가 상태를 설명합니다. 하나의 공유 ZIP을 사용하는 현재 설치는 위의 Setup 1.2.0 안내를 따르세요.",
    "zh-CN": "> **以下为历史评估：** 后续关于 1.0.1/1.1.0 的章节描述的是当时的评估状态。当前使用单个共享 ZIP 的安装请参阅上方 Setup 1.2.0 提示。",
    "zh-TW": "> **以下為歷史評估：** 後續關於 1.0.1/1.1.0 的章節描述的是當時的評估狀態。目前使用單一共享 ZIP 的安裝請參閱上方 Setup 1.2.0 提示。",
}

UI_CURRENT = {
    "de": "Die Installationsoberfläche folgt automatisch der Betriebssystemsprache mit zehn Optionen; eine manuelle Auswahl wird gespeichert. Die Client-Spieldaten unterstützen weiterhin neun Gebietsschemas und richten sich nach dem erkannten Spielgebietsschema.",
    "fr": "L’interface de l’installateur suit automatiquement la langue du système parmi dix options ; un choix manuel est mémorisé. Les données de jeu du client prennent toujours en charge neuf paramètres régionaux et suivent les paramètres régionaux détectés du jeu.",
    "es-ES": "La interfaz del instalador sigue automáticamente el idioma del sistema entre diez opciones; la elección manual se guarda. Los datos del juego del cliente siguen admitiendo nueve configuraciones regionales y siguen la configuración regional detectada del juego.",
    "es-MX": "La interfaz del instalador sigue automáticamente el idioma del sistema entre diez opciones; la elección manual se guarda. Los datos del juego del cliente siguen admitiendo nueve configuraciones regionales y siguen la configuración regional detectada del juego.",
    "pt-BR": "A interface do instalador segue automaticamente o idioma do sistema entre dez opções; a escolha manual é salva. Os dados do jogo do cliente continuam a oferecer suporte a nove localidades e seguem a localidade detectada do jogo.",
    "ru": "Интерфейс установщика автоматически следует языку ОС из десяти вариантов; ручной выбор сохраняется. Данные игры клиента по-прежнему поддерживают девять языков и следуют обнаруженному языку игры.",
    "ko": "설치 프로그램 인터페이스는 열 가지 옵션 중 운영 체제 언어를 자동으로 따르며 수동 선택은 저장됩니다. 클라이언트 게임 데이터는 계속 9개 로케일을 지원하며 감지된 게임 로케일을 따릅니다.",
    "zh-CN": "安装程序界面会在十种选项中自动跟随操作系统语言，手动选择会被保存。客户端游戏数据仍支持九种语言环境，并遵循检测到的游戏语言环境。",
    "zh-TW": "安裝程式介面會在十種選項中自動跟隨作業系統語言，手動選擇會被儲存。用戶端遊戲資料仍支援九種語言環境，並遵循偵測到的遊戲語言環境。",
}

CATALOG = json.loads((Path(__file__).resolve().parents[1] / "app" / "translations.json").read_text(encoding="utf-8"))["languages"]
CATALOG_TAGS = {"de": "de-DE", "fr": "fr-FR", "es-ES": "es-ES", "es-MX": "es-MX", "ko": "ko-KR", "ru": "ru-RU", "zh-CN": "zh-CN", "zh-TW": "zh-TW", "pt-BR": "pt-BR"}
BEGINNER_MARKER = "<!-- BEGINNER-120-STEPS -->"


def beginner_steps(tag):
    ui = CATALOG[CATALOG_TAGS[tag]]
    choose = ui["Choose folder…"]
    language = ui["Interface language"]
    consecration = ui["Enhanced Consecration"]
    install = ui["Install upgrade"]
    restore = ui["Restore previous install"]
    text = {
"de":("## Erste Schritte","1. Schließen Sie WoW vollständig.\n2. Laden Sie nur `LauSetup.zip` herunter. Unter Windows: Rechtsklick, **Alle extrahieren**, `LauSetup` öffnen und `LauSetup.exe` doppelklicken.\n3. Wählen Sie **{choose}** und den Ordner mit `WoW.exe` direkt darin – nicht `Data` und keinen Launcher-Ordner.\n4. **{language}** ändert nur Setup-Text: Automatisch folgt dem System, eine Auswahl wird gespeichert; die neun Spielsprachen ändern sich nicht.\n5. **{consecration}** ist standardmäßig aktiv. Neue Zaubereffekte brauchen erkannte kompatible HD-Modelle; Karten/Minikarte sind optional.\n6. Wählen Sie **{install}**, warten Sie bis zum Ende und schließen Sie Setup nicht. Starten Sie WoW und geben Sie `/pyversion` ein. Wiederherstellung: WoW schließen, denselben Ordner wählen und **{restore}** wählen.","### Linux/Wine","Nutzen Sie dieselbe ZIP erst mit vorhandenem 64-bit-Wine-Präfix, Wine 11.0, Wine Mono 10.4.1, Python 3.9+, dokumentierten Schriften und lokalem Linux-Speicher. Entpacken Sie sie und führen Sie `WINEPREFIX=\"/path/to/prefix\" sh LauSetup.sh` aus; starten Sie die EXE nie direkt unter Wine."),
"fr":("## Premiers pas","1. Fermez complètement WoW.\n2. Téléchargez seulement `LauSetup.zip`. Sous Windows : clic droit, **Extraire tout**, ouvrez `LauSetup` puis double-cliquez `LauSetup.exe`.\n3. Choisissez **{choose}** puis le dossier contenant directement `WoW.exe`, pas `Data` ni un dossier de lanceur.\n4. **{language}** ne change que le texte de Setup : Automatique suit le système et le choix est mémorisé ; les neuf langues du jeu ne changent pas.\n5. **{consecration}** est activée par défaut. Les nouveaux effets exigent des modèles HD compatibles détectés ; cartes/minicarte sont facultatives.\n6. Choisissez **{install}**, attendez la fin sans fermer Setup, puis lancez WoW et tapez `/pyversion`. Pour annuler : fermez WoW, reprenez le même dossier et choisissez **{restore}**.","### Linux/Wine","Utilisez la même ZIP seulement avec un préfixe Wine 64-bit existant, Wine 11.0, Wine Mono 10.4.1, Python 3.9+, les polices documentées et un stockage Linux local. Extrayez-la puis lancez `WINEPREFIX=\"/path/to/prefix\" sh LauSetup.sh`; ne lancez jamais l’EXE directement sous Wine."),
"es-ES":("## Primeros pasos","1. Cierre WoW por completo.\n2. Descargue solo `LauSetup.zip`. En Windows: clic derecho, **Extraer todo**, abra `LauSetup` y haga doble clic en `LauSetup.exe`.\n3. Elija **{choose}** y la carpeta que contiene directamente `WoW.exe`, no `Data` ni una carpeta de lanzador.\n4. **{language}** solo cambia el texto de Setup: Automático sigue el sistema y guarda la elección; no cambia los nueve idiomas del juego.\n5. **{consecration}** está activada por defecto. Los nuevos efectos requieren modelos HD compatibles detectados; mapas/minimapa son opcionales.\n6. Elija **{install}**, espere sin cerrar Setup, inicie WoW y escriba `/pyversion`. Para restaurar, cierre WoW, use la misma carpeta y elija **{restore}**.","### Linux/Wine","Use el mismo ZIP solo con un prefijo Wine 64-bit existente, Wine 11.0, Wine Mono 10.4.1, Python 3.9+, fuentes documentadas y almacenamiento Linux local. Extraiga y ejecute `WINEPREFIX=\"/path/to/prefix\" sh LauSetup.sh`; nunca ejecute el EXE directamente en Wine."),
"es-MX":("## Primeros pasos","1. Cierre WoW por completo.\n2. Descargue solo `LauSetup.zip`. En Windows: clic derecho, **Extraer todo**, abra `LauSetup` y haga doble clic en `LauSetup.exe`.\n3. Elija **{choose}** y la carpeta que contiene directamente `WoW.exe`, no `Data` ni una carpeta de lanzador.\n4. **{language}** solo cambia el texto de Setup: Automático sigue el sistema y guarda la elección; no cambia los nueve idiomas del juego.\n5. **{consecration}** está activada por defecto. Los nuevos efectos requieren modelos HD compatibles detectados; mapas/minimapa son opcionales.\n6. Elija **{install}**, espere sin cerrar Setup, inicie WoW y escriba `/pyversion`. Para restaurar, cierre WoW, use la misma carpeta y elija **{restore}**.","### Linux/Wine","Use el mismo ZIP solo con un prefijo Wine 64-bit existente, Wine 11.0, Wine Mono 10.4.1, Python 3.9+, fuentes documentadas y almacenamiento Linux local. Extraiga y ejecute `WINEPREFIX=\"/path/to/prefix\" sh LauSetup.sh`; nunca ejecute el EXE directamente en Wine."),
    }.get(tag, {
"pt-BR":("## Primeiros passos","1. Feche o WoW completamente.\n2. Baixe apenas `LauSetup.zip`; no Windows, clique com o botão direito, **Extrair tudo**, abra `LauSetup` e clique duas vezes em `LauSetup.exe`.\n3. Use **{choose}** e escolha a pasta que contém `WoW.exe`, não `Data`.\n4. **{language}** muda apenas o texto do Setup; Automático segue o sistema e não muda os nove idiomas do jogo.\n5. **{consecration}** vem ativada; efeitos exigem modelos HD compatíveis e mapas são opcionais.\n6. Use **{install}**, espere sem fechar o Setup; abra WoW e digite `/pyversion`. Para restaurar, feche WoW, escolha a mesma pasta e use **{restore}**.","### Linux/Wine","Use o mesmo ZIP somente com prefixo Wine 64-bit existente, Wine 11.0, Wine Mono 10.4.1, Python 3.9+, fontes documentadas e armazenamento Linux local. Extraia e execute `WINEPREFIX=\"/path/to/prefix\" sh LauSetup.sh`; nunca execute o EXE diretamente no Wine."),
"ru":("## Начало работы","1. Полностью закройте WoW.\n2. Скачайте только `LauSetup.zip`; в Windows выберите **Извлечь все**, откройте `LauSetup` и дважды щёлкните `LauSetup.exe`.\n3. Выберите **{choose}** и папку с `WoW.exe`, не `Data`.\n4. **{language}** меняет только текст Setup; Автоматически следует ОС и не меняет девять языков игры.\n5. **{consecration}** включено; эффекты требуют совместимых HD-моделей, карты необязательны.\n6. Выберите **{install}**, дождитесь конца; запустите WoW и введите `/pyversion`. Для восстановления закройте WoW, выберите ту же папку и **{restore}**.","### Linux/Wine","Тот же ZIP используйте только с 64-bit префиксом Wine, Wine 11.0, Wine Mono 10.4.1, Python 3.9+, документированными шрифтами и локальным Linux-хранилищем. Распакуйте и выполните `WINEPREFIX=\"/path/to/prefix\" sh LauSetup.sh`; EXE в Wine напрямую не запускайте."),
"ko":("## 처음 시작하기","1. WoW를 완전히 종료하세요.\n2. `LauSetup.zip`만 내려받으세요. Windows에서는 마우스 오른쪽 버튼을 눌러 **모두 추출**을 선택하고 `LauSetup`을 연 뒤 `LauSetup.exe`를 두 번 클릭합니다.\n3. **{choose}**을 선택하고 `Data`나 런처 폴더가 아닌 `WoW.exe`가 바로 들어 있는 폴더를 고르세요.\n4. **{language}**는 Setup 텍스트만 바꿉니다. 자동은 시스템 언어를 따르고 선택은 저장되며, 게임의 9개 로케일은 바뀌지 않습니다.\n5. **{consecration}**은 기본으로 켜져 있습니다. 새 주문 효과에는 감지된 호환 HD 모델이 필요하며 지도/미니맵은 선택 다운로드입니다.\n6. **{install}**을 선택하고 Setup을 닫지 말고 끝날 때까지 기다리세요. WoW를 시작한 뒤 `/pyversion`을 입력합니다. 복원하려면 WoW를 닫고 같은 폴더를 선택한 뒤 **{restore}**을 선택하세요.","### Linux/Wine","동일한 ZIP은 기존 64-bit Wine 접두사, Wine 11.0, Wine Mono 10.4.1, Python 3.9+, 문서화된 글꼴 및 로컬 Linux 저장소가 준비된 경우에만 사용하세요. 압축을 풀고 `WINEPREFIX=\"/path/to/prefix\" sh LauSetup.sh`를 실행하세요. Wine에서 EXE를 직접 실행하지 마세요."),
"zh-CN":("## 新手步骤","1。完全关闭 WoW。\n2。只下载 `LauSetup.zip`。在 Windows 中右键点击，选择**全部提取**，打开 `LauSetup`，然后双击 `LauSetup.exe`。\n3。选择 **{choose}**，并选择直接包含 `WoW.exe` 的文件夹，不要选择 `Data` 或启动器文件夹。\n4。**{language}** 只改变 Setup 文本：自动跟随系统语言，手动选择会保存；它不会改变游戏的九种语言环境。\n5。**{consecration}** 默认启用。新法术效果需要检测到兼容的 HD 模型；地图和小地图是可选下载。\n6。选择 **{install}**，等待完成且不要关闭 Setup。启动 WoW 后输入 `/pyversion`。如需恢复，请关闭 WoW，选择相同的游戏文件夹，再选择 **{restore}**。","### Linux/Wine","同一个 ZIP 只能在已有 64-bit Wine 前缀、Wine 11.0、Wine Mono 10.4.1、Python 3.9+、文档要求的字体和本地 Linux 存储准备好后使用。解压后运行 `WINEPREFIX=\"/path/to/prefix\" sh LauSetup.sh`；不要在 Wine 中直接运行 EXE。"),
"zh-TW":("## 新手步驟","1。完全關閉 WoW。\n2。只下載 `LauSetup.zip`。在 Windows 中按右鍵，選擇**全部解壓縮**，開啟 `LauSetup`，然後按兩下 `LauSetup.exe`。\n3。選擇 **{choose}**，並選擇直接包含 `WoW.exe` 的資料夾，不要選擇 `Data` 或啟動器資料夾。\n4。**{language}** 只會變更 Setup 文字：自動會跟隨系統語言，手動選擇會被儲存；它不會變更遊戲的九種語言環境。\n5。**{consecration}** 預設啟用。新法術效果需要偵測到相容的 HD 模型；地圖和小地圖是選用下載。\n6。選擇 **{install}**，等待完成且不要關閉 Setup。啟動 WoW 後輸入 `/pyversion`。如需還原，請關閉 WoW，選擇相同的遊戲資料夾，再選擇 **{restore}**。","### Linux/Wine","同一個 ZIP 只能在已有 64-bit Wine 前綴、Wine 11.0、Wine Mono 10.4.1、Python 3.9+、文件要求的字型和本機 Linux 儲存空間準備好後使用。解壓後執行 `WINEPREFIX=\"/path/to/prefix\" sh LauSetup.sh`；不要在 Wine 中直接執行 EXE。"),
}.get(tag, ("## Getting started","1. Close WoW.\n2. Download `LauSetup.zip`, extract it, then open `LauSetup.exe`.\n3. Choose **{choose}** and the folder containing `WoW.exe`, not `Data`.\n4. **{language}** changes Setup only; Automatic follows the system and does not change the nine game locales.\n5. **{consecration}** is on by default; HD effects need compatible models and maps are optional.\n6. Choose **{install}**, wait without closing Setup, then type `/pyversion` in WoW. To restore, close WoW and choose **{restore}**.","### Linux/Wine","Use the same ZIP only with the documented existing 64-bit Wine prerequisites. Run `WINEPREFIX=\"/path/to/prefix\" sh LauSetup.sh`, never the EXE directly.")))
    return BEGINNER_MARKER+"\n"+text[0]+"\n\n"+text[1].format(choose=choose,language=language,consecration=consecration,install=install,restore=restore)+"\n\n"+text[2]+"\n\n"+text[3]


def replace_readme_ui(tag, match):
    line = match.group(0)
    if tag == "zh-CN":
        return line.split("。运行时")[0] + "。 " + UI_CURRENT[tag]
    if tag == "zh-TW":
        return line.split("。運行時")[0] + "。 " + UI_CURRENT[tag]
    return line.split(". ")[0] + ". " + UI_CURRENT[tag]

changed = 0
links = 0
for tag, quickstart in QUICKSTART.items():
    for path in (ROOT / "docs" / "i18n" / tag).glob("**/*.md"):
        text = path.read_text(encoding="utf-8")
        is_wine_readme = path.name == "README.md" and path.parent.name == "wine"
        if ZIP_NOTICE not in text:
            match = OLD.search(text)
            if not match:
                raise ValueError(f"missing 1.2.0 notice: {path}")
            replacement = ZIP_NOTICE + "\n" + match.group("body").rstrip() + "\n>\n> " + quickstart + "\n"
            text, count = OLD.subn(replacement, text, count=1)
            if count != 1:
                raise ValueError(f"unexpected notice count: {path}")
        if BEGINNER_MARKER in text:
            text = re.sub(BEGINNER_MARKER + r".*?(?=\n<!-- Author:)", beginner_steps(tag).rstrip(), text, count=1, flags=re.DOTALL)
        if path.name in {"README.md", "START-HERE.md"} and (path.name == "START-HERE.md" or not is_wine_readme):
            if BEGINNER_MARKER not in text:
                anchor = "\n<!-- Author:"
                if anchor not in text:
                    raise ValueError(f"missing beginner-step anchor: {path}")
                text = text.replace(anchor, "\n\n" + beginner_steps(tag) + anchor, 1)
        elif is_wine_readme and BEGINNER_MARKER not in text:
            anchor = "\n<!-- Author:"
            if anchor not in text:
                raise ValueError(f"missing Wine beginner-step anchor: {path}")
            text = text.replace(anchor, "\n\n" + beginner_steps(tag) + anchor, 1)
        if path.name == "README.md" and not is_wine_readme:
            before = text
            text = text.replace(
                "https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.exe", ZIP
            ).replace(
                "https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup-Wine.zip", ZIP
            )
            text, labels = ZIP_LABEL.subn(r"\1LauSetup.zip\2", text)
            links += int(text != before) + labels
        if path.name == "README.md" and not is_wine_readme:
            text, count = re.subn(
                r"2[.。] \*\*(?:Starten|Lancez|Inicie|Запустите|설정을|启动|啟動).*?(?=\n3[.。])",
                OPERATIONAL[tag][0],
                text,
                count=1,
            )
            if count != 1:
                raise ValueError(f"missing README quickstart: {path}")
            text, count = re.subn(
                r"(?m)^> \*\*.*?(?:Installationsprogramms ist Englisch|programme d'installation est en anglais|interfaz(?: de usuario)? del instalador est[áa] en ingl[eé]s|(?:interface|UI) do instalador [ée] em ingl[eê]s|интерфейс установщика.*?английский|설치 프로그램 UI는 영어입니다|安装程序用户界面是英文的|安裝程式使用者介面是英文的).*?$",
                lambda m: replace_readme_ui(tag, m),
                text, count=1,
            )
            if count != 1 and UI_CURRENT[tag] not in text:
                raise ValueError(f"missing README UI-language claim: {path}")
        elif path.name == "START-HERE.md":
            text, count = re.subn(
                r"^Windows[^\n]*\n^Linux/Wine[^\n]*\n^[^\n]*(?=\n\n1[.。])",
                OPERATIONAL[tag][1],
                text,
                count=1,
                flags=re.MULTILINE,
            )
            if count != 1 and OPERATIONAL[tag][1] not in text:
                raise ValueError(f"missing START-HERE download block: {path}")
        elif is_wine_readme:
            text, count = re.subn(
                r"3[.。]\s*.*?(?=\n4[.。])", OPERATIONAL[tag][2], text, count=1
            )
            if count != 1:
                raise ValueError(f"missing Wine extraction step: {path}")
            text, count = re.subn(
                r"(?m)^(?:Die Installationsoberfläche ist Englisch|L'interface du programme d'installation est en anglais|La interfaz del instalador es en ingl[eé]s|A interface do instalador [ée] em ingl[eê]s|Интерфейс установщика английский|설치 프로그램 인터페이스는 영어입니다|安装程序界面是英文的|安裝程式介面是英文的).*?\n.*?(?=\n\n)",
                UI_CURRENT[tag], text, count=1,
            )
            if count != 1 and UI_CURRENT[tag] not in text:
                raise ValueError(f"missing Wine README UI-language claim: {path}")
        elif path.name == "KNOWN-LIMITATIONS.md":
            text, count = re.subn(
                r"(?m)^[-–] .*?`Config\.wtf`.*$",
                LIMITATION_UI[tag], text, count=1,
            )
            if count != 1 and LIMITATION_UI[tag] not in text:
                raise ValueError(f"missing UI-language limitation: {path}")
        elif path.name == "PLATFORM-FEASIBILITY.md":
            if HISTORICAL_PLATFORM[tag] not in text:
                marker = "\nUpdate:"
                if marker not in text:
                    marker = "\nMise à jour :"
                if marker not in text:
                    marker = "\nActualización:"
                if marker not in text:
                    marker = "\nAtualização:"
                if marker not in text:
                    marker = "\nОбновление:"
                if marker not in text:
                    marker = "\n업데이트:"
                if marker not in text:
                    marker = "\n更新："
                if marker not in text:
                    raise ValueError(f"missing historical platform marker: {path}")
                text = text.replace(marker, "\n" + HISTORICAL_PLATFORM[tag] + marker, 1)
        elif path.name == "README.md" and not is_wine_readme:
            # Kept after the guide-step replacement: replace only the old
            # current UI-language claim in the public download disclaimer.
            text, count = re.subn(
                r"(?m)^> \*\*.*?(?:Installationsprogramms ist Englisch|programme d'installation est en anglais|interfaz(?: de usuario)? del instalador est[áa] en ingl[eé]s|interface do instalador [ée] em ingl[eê]s|интерфейс установщика.*?английский|설치 프로그램 UI는 영어입니다|安装程序用户界面是英文的|安裝程式使用者介面是英文的).*?$",
                lambda m: replace_readme_ui(tag, m),
                text,
                count=1,
            )
            if count != 1 and UI_CURRENT[tag] not in text:
                raise ValueError(f"missing README UI-language claim: {path}")
        elif is_wine_readme:
            text, count = re.subn(
                r"(?m)^(?:Die Installationsoberfläche ist Englisch|L'interface du programme d'installation est en anglais|La interfaz del instalador es en ingl[eé]s|A interface do instalador [ée] em ingl[eê]s|Интерфейс установщика английский|설치 프로그램 인터페이스는 영어입니다|安装程序界面是英文的|安裝程式介面是英文的).*?\n.*?(?=\n\n)",
                UI_CURRENT[tag], text, count=1,
            )
            if count != 1 and UI_CURRENT[tag] not in text:
                raise ValueError(f"missing Wine README UI-language claim: {path}")
        path.write_text(text, encoding="utf-8", newline="\n")
        changed += 1

assert changed == 117, changed
assert links in (0, 9, 18, 27), links
print(f"ZIP_ONLY_NOTICE_ON_{changed}_TRANSLATED_PAGES; UPDATED_LATEST_LINKS_AND_LABELS_ON_{links}_README_SNAPSHOTS; freshness records unchanged")

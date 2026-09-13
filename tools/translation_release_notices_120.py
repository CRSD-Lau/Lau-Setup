"""Replace delayed translated-document notices for Setup 1.2.0.

Author/Creator/Modifier: Neil Mitchell. This does not update translation cache or
freshness state: the complete Google-backed guide refresh remains pending.
"""
from pathlib import Path
import posixpath
import re
import sys


root = Path(__file__).resolve().parents[1] / "build" / "publish-repo"
sys.path.insert(0, str(root / "tools"))
import translate_docs as t


notices = {
    "de": (
        "Setup 1.2.0",
        "Ein ZIP enthält jetzt das Windows-Installationsprogramm und den Linux/Wine-Starter. Die Oberfläche folgt automatisch der Betriebssystemsprache mit zehn Optionen; eine manuelle Auswahl wird gespeichert. Spielversion 3.0.8 und die Spieldateien bleiben unverändert. Es gibt keine DBC-Änderungen.",
        "Die vollständige Aktualisierung der Anleitungen steht wegen Google-HTTP-429 noch aus. Der bisherige Text unten kann älter sein; maßgeblich sind die aktuelle englische Quelle und die Hinweise zu 1.2.0.",
    ),
    "fr": (
        "Setup 1.2.0",
        "Une seule archive ZIP contient désormais l’installateur Windows et le lanceur Linux/Wine. L’interface suit automatiquement la langue du système d’exploitation parmi dix options ; un choix manuel est mémorisé. La version 3.0.8 et les fichiers du jeu restent inchangés. Aucune modification DBC.",
        "La mise à jour complète des guides reste en attente à cause d’une erreur Google HTTP 429. Le texte ci-dessous peut être ancien ; consultez la source anglaise actuelle et les notes 1.2.0.",
    ),
    "es-ES": (
        "Setup 1.2.0",
        "Un solo ZIP incluye ahora el instalador de Windows y el iniciador para Linux/Wine. La interfaz sigue automáticamente el idioma del sistema operativo entre diez opciones; la elección manual se guarda. La versión 3.0.8 y los archivos del juego no cambian. No hay cambios en DBC.",
        "La actualización completa de las guías sigue pendiente por un HTTP 429 de Google. El texto anterior puede estar desactualizado; consulta la fuente inglesa actual y las notas 1.2.0.",
    ),
    "es-MX": (
        "Setup 1.2.0",
        "Un solo ZIP incluye ahora el instalador de Windows y el iniciador para Linux/Wine. La interfaz sigue automáticamente el idioma del sistema operativo entre diez opciones; la elección manual se guarda. La versión 3.0.8 y los archivos del juego no cambian. No hay cambios en DBC.",
        "La actualización completa de las guías sigue pendiente por un HTTP 429 de Google. El texto anterior puede estar desactualizado; consulta la fuente inglesa actual y las notas 1.2.0.",
    ),
    "pt-BR": (
        "Setup 1.2.0",
        "Um único ZIP agora contém o instalador do Windows e o iniciador para Linux/Wine. A interface segue automaticamente o idioma do sistema operacional entre dez opções; a escolha manual é salva. A versão 3.0.8 e os arquivos do jogo não mudam. Não há alterações de DBC.",
        "A atualização completa dos guias continua pendente devido a um HTTP 429 do Google. O texto abaixo pode estar desatualizado; consulte a fonte atual em inglês e as notas da versão 1.2.0.",
    ),
    "ru": (
        "Setup 1.2.0",
        "Один ZIP теперь содержит установщик Windows и программу запуска Linux/Wine. Интерфейс автоматически выбирает язык ОС из десяти вариантов; ручной выбор сохраняется. Версия игры 3.0.8 и игровые файлы не изменяются. Изменений DBC нет.",
        "Полное обновление руководств отложено из-за Google HTTP 429. Текст ниже может быть устаревшим; используйте текущий английский источник и примечания к версии 1.2.0.",
    ),
    "ko": (
        "Setup 1.2.0",
        "하나의 ZIP에 이제 Windows 설치 관리자와 Linux/Wine 실행기가 함께 들어 있습니다. 인터페이스는 열 가지 옵션 중 운영 체제 언어를 자동으로 따르며, 수동 선택은 저장됩니다. 게임 버전 3.0.8과 게임 파일은 변경되지 않습니다. DBC 변경도 없습니다.",
        "Google HTTP 429로 전체 안내서 갱신은 아직 보류 중입니다. 아래 본문은 오래되었을 수 있으므로 현재 영어 원문과 1.2.0 릴리스 노트를 확인하세요.",
    ),
    "zh-CN": (
        "Setup 1.2.0",
        "一个 ZIP 现在同时包含 Windows 安装程序和 Linux/Wine 启动器。界面会在十种选项中自动跟随操作系统语言，手动选择会被保存。游戏版本 3.0.8 和游戏文件没有变化，也没有 DBC 修改。",
        "由于 Google HTTP 429，完整指南刷新仍在等待中。下方正文可能已过时；请以当前英文来源和 1.2.0 发布说明为准。",
    ),
    "zh-TW": (
        "Setup 1.2.0",
        "一個 ZIP 現在同時包含 Windows 安裝程式和 Linux/Wine 啟動器。介面會在十種選項中自動跟隨作業系統語言，手動選擇會被儲存。遊戲版本 3.0.8 和遊戲檔案均未變更，也沒有 DBC 修改。",
        "由於 Google HTTP 429，完整指南更新仍在等待中。下方正文可能已過時；請以目前英文來源和 1.2.0 發行說明為準。",
    ),
}

old_banner = re.compile(
    r"<!-- HOTFIX-118-NOTICE -->\n> .*?\n>\n> .*?\n\n", re.DOTALL
)
count = 0
for source in t.sources(root):
    for tag, (heading, change, status) in notices.items():
        path = root / t.destination(source, tag)
        if not path.exists():
            # New English documents are handled by the normal translation flow;
            # this notice refresh only preserves already published snapshots.
            continue
        old = path.read_text(encoding="utf-8")
        if "<!-- RELEASE-120-NOTICE -->" in old:
            assert "HOTFIX-118-NOTICE" not in old, path
            count += 1
            continue
        assert old_banner.search(old), path
        english = posixpath.relpath(source, posixpath.dirname(t.destination(source, tag)))
        banner = (
            "<!-- RELEASE-120-NOTICE -->\n"
            f"> **{heading}** — {change}\n>\n"
            f"> {status} [English]({english}) · "
            "[1.2.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.2.0)\n\n"
        )
        new, replacements = old_banner.subn(banner, old, count=1)
        assert replacements == 1, path
        assert "HOTFIX-118-NOTICE" not in new, path
        path.write_text(new, encoding="utf-8", newline="\n")
        count += 1

expected = sum(
    1
    for source in t.sources(root)
    for tag in notices
    if (root / t.destination(source, tag)).exists()
)
assert count == expected, (count, expected)
print(
    f"RELEASE_120_NOTICE_ON_{count}_TRANSLATED_PAGES; "
    "translation cache and freshness state unchanged; full refresh remains pending"
)

"""Build and verify Lau Setup's bounded installer translation catalog.

Author, Creator, Last Modified By: Neil Mitchell

Translation is an authoring-time operation.  It uses Google's free web
translator without an API key, stores a local segment cache, and never adds a
runtime network dependency.  Verification is entirely offline.
"""

import argparse
import ast
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import re
import time
import urllib.error
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "app" / "translations.json"
CACHE = ROOT / "reports" / "translation-installer-cache.json"
REPORT = ROOT / "reports" / "translation-installer-report.json"
META = {"Author": "Neil Mitchell", "Creator": "Neil Mitchell", "LastModifiedBy": "Neil Mitchell"}
LOCALES = {
    "en-US": "en", "de-DE": "de", "fr-FR": "fr", "es-ES": "es",
    "es-MX": "es", "ko-KR": "ko", "ru-RU": "ru", "zh-CN": "zh-CN",
    "zh-TW": "zh-TW", "pt-BR": "pt",
}
CS_SOURCES = ("app/Core.cs", "app/Downloader.cs", "app/MpqScan.cs", "app/Main.cs", "app/Localization.cs")
PY_SOURCES = ("wine/lau_wine.py",)
CS_STRING = re.compile(r'(?<!@)"(?:\\.|[^"\\])*"')
PLACEHOLDER = re.compile(r"\{\d+(?::[^{}]+)?\}")
MASK_TOKEN = re.compile(r"ZXQKEEP\d{5}QXZ")
PROTECTED = re.compile(
    r"https?://[^\s]+|/pyversion|--language|\bauto\b|\.mpq\.disabled|"
    r"\b(?:Lau Setup|Lau|WRATH|World of Warcraft|WoW\.exe|LauSetup\.exe|lau_wine\.py|lau-languages\.json|"
    r"Wine Mono|Wine|Linux|Patch-S|Data|WINEPREFIX|Python|\.NET Framework|Microsoft|Liberation Sans|ext4|XFS|Btrfs)\b|"
    r"\b\d+(?:\.\d+)+(?:a)?\b|\b(?:build|Build)\s+\d+\b|\{\d+(?::[^{}]+)?\}"
)
CALL_NAMES = ("Ui.T", "Ui.F", "Label", "Button", "Check", "SetText", "Phrase")
EXCLUDED_INTERNAL = {"error", "Non-ASCII probe"}
EXTRA_KEYS = {
    "Game folder", "Your visuals", "Review", "Finished",
    # The Wine launcher translates this prefix before appending the allowlisted
    # language codes, so it is intentionally present alongside the full format
    # template extracted from parse_language().
    "The --language option needs one of: ",
}
LANGUAGE_OPTION_REVIEWED = {
    "de": ("Für die Option --language ist einer der folgenden Werte erforderlich: ", "Verwenden Sie --language gefolgt von einem Sprachcode oder auto."),
    "fr": ("L’option --language nécessite l’une des valeurs suivantes : ", "Utilisez --language suivi d’un code de langue ou du mot auto."),
    "es": ("La opción --language requiere uno de los siguientes valores: ", "Use --language seguido de un código de idioma o auto."),
    "ko": ("--language 옵션에는 다음 중 하나가 필요합니다: ", "--language 다음에 언어 코드 하나 또는 auto를 입력하세요."),
    "ru": ("Для параметра --language требуется одно из следующих значений: ", "Укажите после --language один код языка или auto."),
    "zh-CN": ("--language 选项需要以下值之一：", "请使用 --language，后跟一个语言代码或 auto。"),
    "zh-TW": ("--language 選項需要以下值之一：", "請使用 --language，後接一個語言代碼或 auto。"),
    "pt": ("A opção --language precisa de um destes: ", "Use --language seguido de um código de idioma ou auto."),
}
REVIEWED = {target: {
    "The --language option needs one of: ": values[0],
    "The --language option needs one of: {0}.": values[0] + "{0}.",
    "Use --language followed by one language code or auto.": values[1],
} for target, values in LANGUAGE_OPTION_REVIEWED.items()}
# Preserve the clearer extra-patch wording when rebuilding translations.
REVIEWED['de'].update({'Possible extra upgrade patch: {0}. Keep a backup and move this copy outside Data before retrying. Setup will not delete it.': 'Möglicher zusätzlicher Upgrade-Patch: {0}. Erstellen Sie eine Sicherungskopie und verschieben Sie diese Kopie außerhalb von Data, bevor Sie es erneut versuchen. Setup löscht es nicht.'})
REVIEWED['fr'].update({'Possible extra upgrade patch: {0}. Keep a backup and move this copy outside Data before retrying. Setup will not delete it.': "Possible correctif de mise à niveau supplémentaire : {0}. Conservez une sauvegarde et déplacez cette copie en dehors de Data avant de réessayer. Le programme d'installation ne le supprimera pas."})
REVIEWED['es'].update({'Possible extra upgrade patch: {0}. Keep a backup and move this copy outside Data before retrying. Setup will not delete it.': 'Posible parche de actualización adicional: {0}. Mantenga una copia de seguridad y mueva esta copia fuera de Data antes de volver a intentarlo. El programa de instalación no lo eliminará.'})
REVIEWED['ko'].update({'Possible extra upgrade patch: {0}. Keep a backup and move this copy outside Data before retrying. Setup will not delete it.': '추가 업그레이드 패치 가능성: {0}. 다시 시도하기 전에 백업을 유지하고 이 복사본을 Data 외부로 이동하세요. 설치 프로그램에서는 해당 항목을 삭제하지 않습니다.'})
REVIEWED['ru'].update({'Possible extra upgrade patch: {0}. Keep a backup and move this copy outside Data before retrying. Setup will not delete it.': 'Возможный дополнительный патч обновления: {0}. Сохраните резервную копию и переместите эту копию за пределы Data, прежде чем повторить попытку. Программа установки не удалит его.'})
REVIEWED['zh-CN'].update({'Possible extra upgrade patch: {0}. Keep a backup and move this copy outside Data before retrying. Setup will not delete it.': '可能存在额外的升级补丁：{0}。重试之前，请保留备份并将此副本移至 Data 之外。安装程序不会删除它。'})
REVIEWED['zh-TW'].update({'Possible extra upgrade patch: {0}. Keep a backup and move this copy outside Data before retrying. Setup will not delete it.': '可能存在額外的升級補丁：{0}。重試之前，請保留備份並將此副本移至 Data 之外。安裝程式不會刪除它。'})
REVIEWED['pt'].update({'Possible extra upgrade patch: {0}. Keep a backup and move this copy outside Data before retrying. Setup will not delete it.': 'Possível patch de atualização adicional: {0}. Mantenha um backup e mova esta cópia para fora de Data antes de tentar novamente. A instalação não irá excluí-lo.'})
REVIEWED["pt"].update({
    "Already installed": "Já instalado",
    "An interrupted install was found. Restore it before continuing.": "Foi encontrada uma instalação interrompida. Restaure-a antes de continuar.",
    "Automatic (system language)": "Automático (idioma do sistema)",
    "Install .NET Framework 4.8": "Instalar o .NET Framework 4.8",
    "Lau Setup requires .NET Framework 4.8. Open Microsoft's official runtime download page?": "O Lau Setup requer o .NET Framework 4.8. Abrir a página oficial de download do runtime da Microsoft?",
    "LauSetup.exe, lau_wine.py and lau-languages.json must stay together.": "LauSetup.exe, lau_wine.py e lau-languages.json devem permanecer juntos.",
    "Linux file locking is unavailable.": "O bloqueio de arquivos do Linux não está disponível.",
    "loading screens and regional artwork": "telas de carregamento e arte regional",
    "Local application data is unavailable.": "Os dados locais do aplicativo não estão disponíveis.",
    "maps and minimap": "mapas e minimapa",
    "Patch-S becomes .mpq.disabled. Any older disabled copy is preserved separately. Restore previous install reverses the change.": "O Patch-S passa a ser .mpq.disabled. Qualquer cópia desativada mais antiga é preservada separadamente. Restaurar instalação anterior reverte a alteração.",
    "Restore the game files from the most recent Lau Setup backup? Your addons and saved settings are preserved.": "Restaurar os arquivos do jogo do backup mais recente do Lau Setup? Seus addons e configurações salvas são preservados.",
    "spell indicators": "indicadores de feitiços",
    "the compatible game executable": "o executável de jogo compatível",
    "Unknown setup option.": "Opção de configuração desconhecida.",
    "Unsupported interface language.": "Idioma da interface não compatível.",
})
for _target, _value in {
    "de": "Lokale Anwendungsdaten sind nicht verfügbar.",
    "fr": "Les données locales de l’application ne sont pas disponibles.",
    "es": "Los datos locales de la aplicación no están disponibles.",
    "ko": "로컬 애플리케이션 데이터를 사용할 수 없습니다.",
    "ru": "Локальные данные приложения недоступны.",
    "zh-CN": "本地应用程序数据不可用。",
    "zh-TW": "本機應用程式資料無法使用。",
}.items(): REVIEWED[_target]["Local application data is unavailable."] = _value
REVIEWED["zh-CN"]["Lau Setup requires .NET Framework 4.8. Open Microsoft's official runtime download page?"] = "Lau Setup 需要 .NET Framework 4.8。要打开 Microsoft 官方运行时下载页面吗？"
REVIEWED["zh-TW"]["Lau Setup requires .NET Framework 4.8. Open Microsoft's official runtime download page?"] = "Lau Setup 需要 .NET Framework 4.8。要開啟 Microsoft 官方執行階段下載頁面嗎？"

VISIBLE_REVIEWED = {
    "de": ("Oberflächensprache", "Ordner auswählen…", "Upgrade installieren", "Vorherige Installation wiederherstellen", "Abbrechen", "Automatisch (Systemsprache)", "Dein Spielclient. Deine Sprache. Einfach installiert.", "Verbesserte Weihe", "LAU  /  WRATH – VISUELLES UPGRADE"),
    "fr": ("Langue de l’interface", "Choisir le dossier…", "Installer la mise à niveau", "Restaurer l’installation précédente", "Annuler", "Automatique (langue du système)", "Votre client de jeu. Votre langue. Une installation simple.", "Consécration améliorée", "LAU  /  WRATH – AMÉLIORATION VISUELLE"),
    "es": ("Idioma de la interfaz", "Elegir carpeta…", "Instalar actualización", "Restaurar instalación anterior", "Cancelar", "Automático (idioma del sistema)", "Tu cliente de juego. Tu idioma. Una instalación sencilla.", "Consagración mejorada", "LAU  /  WRATH – MEJORA VISUAL"),
    "ko": ("인터페이스 언어", "폴더 선택…", "업그레이드 설치", "이전 설치 복원", "취소", "자동(시스템 언어)", "내 게임 클라이언트. 내 언어. 간편한 설치.", "강화된 신성화", "LAU  /  WRATH 비주얼 업그레이드"),
    "ru": ("Язык интерфейса", "Выбрать папку…", "Установить обновление", "Восстановить предыдущую установку", "Отмена", "Автоматически (язык системы)", "Ваш игровой клиент. Ваш язык. Простая установка.", "Улучшенное освящение", "LAU  /  WRATH — ВИЗУАЛЬНОЕ ОБНОВЛЕНИЕ"),
    "zh-CN": ("界面语言", "选择文件夹…", "安装升级", "恢复上一次安装", "取消", "自动（系统语言）", "你的游戏客户端，你的语言，轻松安装。", "强化奉献", "LAU  /  WRATH 视觉升级"),
    "zh-TW": ("介面語言", "選擇資料夾…", "安裝升級", "還原上一次安裝", "取消", "自動（系統語言）", "你的遊戲用戶端，你的語言，輕鬆安裝。", "強化奉獻", "LAU  /  WRATH 視覺升級"),
    "pt": ("Idioma da interface", "Escolher pasta…", "Instalar atualização", "Restaurar instalação anterior", "Cancelar", "Automático (idioma do sistema)", "Seu cliente de jogo. Seu idioma. Uma instalação simples.", "Consagração aprimorada", "LAU  /  WRATH — MELHORIA VISUAL"),
}
VISIBLE_KEYS = ("Interface language", "Choose folder…", "Install upgrade", "Restore previous install", "Cancel",
                "Automatic (system language)", "Your client. Your language. One simple install.",
                "Enhanced Consecration", "LAU  /  WRATH VISUAL UPGRADE")
for _target, _values in VISIBLE_REVIEWED.items(): REVIEWED[_target].update(dict(zip(VISIBLE_KEYS, _values)))


def read(path):
    return path.read_text(encoding="utf-8-sig")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text, encoding="utf-8", newline="\n")
    temporary.replace(path)


def decode_cs(token):
    value = token[1:-1]
    replacements = {r"\\": "\\", r'\"': '"', r"\n": "\n", r"\r": "\r", r"\t": "\t", r"\0": "\0"}
    return re.sub(r"\\(?:[\\\"nrt0])", lambda match: replacements[match.group()], value)


def balanced(text, opening):
    depth, quote, escaped = 0, False, False
    for index in range(opening, len(text)):
        char = text[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quote = False
            continue
        if char == '"':
            quote = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[opening + 1:index]
    raise ValueError("Unbalanced C# call")


def split_args(expression):
    parts, start, depth, quote, escaped = [], 0, 0, False, False
    for index, char in enumerate(expression):
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quote = False
            continue
        if char == '"': quote = True
        elif char in "([{": depth += 1
        elif char in ")]}": depth -= 1
        elif char == "," and depth == 0:
            parts.append(expression[start:index].strip()); start = index + 1
    parts.append(expression[start:].strip())
    return parts


def cs_template(expression):
    """Convert a string concatenation to a String.Format-style source key."""
    strings = list(CS_STRING.finditer(expression))
    if not strings:
        return None
    if "?" in expression:
        return None
    output, cursor, argument = [], 0, 0
    for match in strings:
        gap = expression[cursor:match.start()]
        if cursor and re.search(r"[^+\s()]", gap):
            output.append("{" + str(argument) + "}"); argument += 1
        output.append(decode_cs(match.group()))
        cursor = match.end()
    if re.search(r"[^+\s();]", expression[cursor:]):
        output.append("{" + str(argument) + "}")
    value = "".join(output)
    return value if re.search(r"[A-Za-z]", value) else None


def cs_values(expression):
    value = cs_template(expression)
    if value: return {value}
    if "?" in expression:
        return {decode_cs(match.group()) for match in CS_STRING.finditer(expression)
                if re.search(r"[A-Za-z]", decode_cs(match.group()))}
    return set()


def iter_calls(text, name):
    pattern = re.compile(r"(?<![\w.])" + re.escape(name) + r"\s*\(")
    for match in pattern.finditer(text):
        yield split_args(balanced(text, text.find("(", match.start())))


def extract_cs(path):
    text, found = read(path), set()
    for name in CALL_NAMES:
        for args in iter_calls(text, name):
            position = 1 if name == "SetText" else 0
            if len(args) > position:
                found.update(cs_values(args[position]))
    for match in re.finditer(r"throw\s+new\s+[\w.]+\s*\(", text):
        args = split_args(balanced(text, text.find("(", match.start())))
        if not args: continue
        value = cs_template(args[0])
        if value:
            found.add(value)
        elif "?" in args[0]:
            found.update(decode_cs(item.group()) for item in CS_STRING.finditer(args[0]) if re.search(r"[A-Za-z]", item.group()))
    for name in ("report",):
        for args in iter_calls(text, name):
            if args:
                value = cs_template(args[0])
                if value: found.add(value)
    return found


def py_template(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str): return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = py_template(node.left), py_template(node.right)
        if left is None: left = "{0}"
        if right is None: right = "{0}"
        value = left + right
        indexes = iter(range(100))
        return re.sub(r"\{0\}", lambda _: "{" + str(next(indexes)) + "}", value)
    return None


def extract_py(path):
    found = set()
    for node in ast.walk(ast.parse(read(path), filename=str(path))):
        if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call) and node.exc.args:
            if isinstance(node.exc.func, ast.Name) and node.exc.func.id in ("ValueError", "RuntimeError", "OSError"):
                value = py_template(node.exc.args[0])
                if value and re.search(r"[A-Za-z]", value): found.add(value)
    return found


def extract_keys(root=ROOT):
    keys = set(EXTRA_KEYS)
    for relative in CS_SOURCES:
        path = root / relative
        if path.exists(): keys.update(extract_cs(path))
    for relative in PY_SOURCES:
        path = root / relative
        if path.exists(): keys.update(extract_py(path))
    localization = root / "app" / "Localization.cs"
    if localization.exists():
        for args in iter_calls(read(localization), "new LanguageOption"):
            if len(args) > 1 and cs_template(args[0]) == "auto": keys.update(cs_values(args[1]))
    main = root / "app" / "Main.cs"
    if main.exists():
        friendly = re.search(r"static\s+string\s+Friendly\s*\([^)]*\)\s*\{([^}]*)\}", read(main), re.S)
        if friendly:
            keys.update(decode_cs(item.group()) for item in CS_STRING.finditer(friendly.group(1))
                        if " " in decode_cs(item.group()) and re.search(r"[a-z]", decode_cs(item.group())))
    keys.difference_update(EXCLUDED_INTERNAL)
    return sorted(keys, key=lambda value: (value.casefold(), value))


def mask(text):
    saved = []
    def replace(match):
        saved.append(match.group())
        return f"ZXQKEEP{len(saved)-1:05d}QXZ"
    return PROTECTED.sub(replace, text), saved


def unmask(translated, original, saved):
    if Counter(MASK_TOKEN.findall(translated)) != Counter(MASK_TOKEN.findall(original)):
        raise ValueError("Translation changed a protected name, file, URL, version, or placeholder")
    result = MASK_TOKEN.sub(lambda match: saved[int(match.group()[7:12])], translated)
    if Counter(PLACEHOLDER.findall(result)) != Counter(PLACEHOLDER.findall(PROTECTED.sub(lambda m: m.group(), unmask_source(original, saved)))):
        raise ValueError("Translation changed format placeholders")
    return result.strip()


def unmask_source(original, saved):
    return MASK_TOKEN.sub(lambda match: saved[int(match.group()[7:12])], original)


def request_translation(text, target):
    # Google's keyless web endpoint is used only while authoring the checked-in
    # catalog.  There is no separately billed API, credential, or runtime call.
    url = "https://translate.googleapis.com/translate_a/single?" + urllib.parse.urlencode(
        {"client": "gtx", "sl": "en", "tl": target, "dt": "t", "q": text})
    for attempt in range(5):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Lau-Setup-authoring-translation/1.0"})
            with urllib.request.urlopen(request, timeout=45) as response:
                payload = json.loads(response.read().decode("utf-8"))
            if len(payload) >= 3 and payload[2] == "en" and payload[0]:
                return "".join(part[0] for part in payload[0] if part and part[0]).strip()
            raise ValueError("Google returned no confirmed English translation")
        except (urllib.error.URLError, TimeoutError, ValueError) as error:
            if attempt == 4: raise ValueError(f"Google web translation failed for {target}: {error}") from None
            time.sleep((10 if isinstance(error, urllib.error.HTTPError) and error.code == 429 else 2) * (attempt + 1))


def translate_value(source, target, cache):
    cache_key = hashlib.sha256((target + "\0" + source).encode()).hexdigest()
    if source in REVIEWED.get(target, {}):
        cache[cache_key] = REVIEWED[target][source]
        return cache[cache_key]
    if cache_key in cache: return cache[cache_key]
    prepared, saved = mask(source)
    translated = unmask(request_translation(prepared, target), prepared, saved)
    visible = PROTECTED.sub("", source)
    if len(re.findall(r"[A-Za-z]{3,}", visible)) >= 2 and translated == source:
        raise ValueError(f"Provider returned unchanged English for {target}: {source}")
    cache[cache_key] = translated
    return translated


def load_cache():
    if not CACHE.exists(): return dict(META)
    value = json.loads(read(CACHE))
    if any(value.get(key) != expected for key, expected in META.items()): raise ValueError("Translation cache metadata is invalid")
    return value


def build(root=ROOT, workers=3):
    keys, cache = extract_keys(root), load_cache()
    languages = {"en-US": {key: key for key in keys}}
    for locale, target in LOCALES.items():
        if locale == "en-US": continue
        completed = {}
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(translate_value, key, target, cache): key for key in keys}
            for future in as_completed(futures):
                key = futures[future]
                completed[key] = future.result()
        languages[locale] = {key: completed[key] for key in keys}
        write(CACHE, json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        print(f"{locale}: translated {len(keys)} keys", flush=True)
    data = dict(META, languages=languages)
    validate(data, keys)
    write(CATALOG, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    report = dict(META, Method="Machine-assisted authoring with the free Google web translator; no API key and no runtime translation. Common visible controls and game terminology received explicit reviewed overrides.",
                  Coverage={locale: len(values) for locale, values in languages.items()}, SourceKeys=len(keys),
                  ReviewedVisibleKeys=list(VISIBLE_KEYS),
                  SpellTerminologyEvidence=["https://www.wowhead.com/de/spell=204242/weihe", "https://www.wowhead.com/fr/spell=81297/cons%C3%A9cration", "https://www.wowhead.com/es/spell=413267/consagraci%C3%B3n", "https://www.wowhead.com/ko/spell=221645/%EC%8B%A0%EC%84%B1%ED%99%94", "https://www.wowhead.com/wotlk/ru/spell=20924/%D0%BE%D1%81%D0%B2%D1%8F%D1%89%D0%B5%D0%BD%D0%B8%D0%B5", "https://www.wowhead.com/classic/cn/spell=20924/%E5%A5%89%E7%8C%AE", "https://www.wowhead.com/tbc/tw/spell=27173/%E5%A5%89%E7%8D%BB", "https://www.wowhead.com/pt/spell=190010/consagra%C3%A7%C3%A3o"],
                  Protected="Format placeholders, URLs, product and game names, filenames, flags, /pyversion, and version/build numbers are validated exactly.")
    write(REPORT, json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote {CATALOG} with {len(keys)} keys in {len(languages)} languages")


def validate(data=None, keys=None, root=ROOT):
    if data is None: data = json.loads(read(root / "app" / "translations.json"))
    if keys is None: keys = extract_keys(root)
    if any(data.get(key) != expected for key, expected in META.items()): raise ValueError("Translation catalog metadata is invalid")
    languages = data.get("languages")
    if not isinstance(languages, dict) or list(languages) != list(LOCALES): raise ValueError("Translation catalog locale order or coverage is invalid")
    expected = set(keys)
    for locale, values in languages.items():
        if not isinstance(values, dict) or set(values) != expected:
            missing, extra = sorted(expected - set(values or {})), sorted(set(values or {}) - expected)
            raise ValueError(f"{locale} catalog keys differ; missing={missing[:3]}, extra={extra[:3]}")
        for source, translated in values.items():
            if not isinstance(translated, str) or not translated.strip(): raise ValueError(f"{locale} has an empty translation: {source}")
            if Counter(PLACEHOLDER.findall(source)) != Counter(PLACEHOLDER.findall(translated)):
                raise ValueError(f"{locale} changed placeholders: {source}")
            for token in set(PROTECTED.findall(source)):
                if translated.count(token) != source.count(token):
                    raise ValueError(f"{locale} changed protected token {token!r}: {source}")
            visible = PROTECTED.sub("", source)
            if source not in {"Patch-Y HD", "Patch-Y Non-HD", "LAU SETUP"} and locale != "en-US" and len(re.findall(r"[A-Za-z]{3,}", visible)) >= 2 and translated == source:
                raise ValueError(f"{locale} silently falls back to English: {source}")
            if locale == "en-US" and translated != source: raise ValueError(f"en-US must be identity: {source}")
    print(f"Verified {len(keys)} source keys across {len(languages)} complete languages")



# Reviewed automatic-backup copy; retain exact button labels.
REVIEWED['de'].update({'{0} extra upgrade patches will be backed up automatically in LauSetupBackups. Click Install upgrade to continue.': '{0} zusätzliche Upgrade-Patches werden automatisch in LauSetupBackups gesichert. Klicken Sie zum Fortfahren auf Upgrade installieren.', 'Backing up {0}…': 'Sicherung von {0}…'})
REVIEWED['fr'].update({'{0} extra upgrade patches will be backed up automatically in LauSetupBackups. Click Install upgrade to continue.': '{0} correctifs supplémentaires seront sauvegardés automatiquement dans LauSetupBackups. Cliquez sur Installer la mise à niveau pour continuer.', 'Backing up {0}…': 'Sauvegarde de {0}…'})
REVIEWED['es'].update({'{0} extra upgrade patches will be backed up automatically in LauSetupBackups. Click Install upgrade to continue.': 'Se guardará una copia de seguridad automática de {0} parches adicionales en LauSetupBackups. Haz clic en Instalar actualización para continuar.', 'Backing up {0}…': 'Creando copia de seguridad de {0}…'})
REVIEWED['es'].update({'{0} extra upgrade patches will be backed up automatically in LauSetupBackups. Click Install upgrade to continue.': 'Se guardará una copia de seguridad automática de {0} parches adicionales en LauSetupBackups. Haz clic en Instalar actualización para continuar.', 'Backing up {0}…': 'Creando copia de seguridad de {0}…'})
REVIEWED['pt'].update({'{0} extra upgrade patches will be backed up automatically in LauSetupBackups. Click Install upgrade to continue.': '{0} patches extras serão salvos automaticamente em LauSetupBackups. Clique em Instalar atualização para continuar.', 'Backing up {0}…': 'Fazendo backup de {0}…'})
REVIEWED['ko'].update({'{0} extra upgrade patches will be backed up automatically in LauSetupBackups. Click Install upgrade to continue.': '추가 업그레이드 패치 {0}개를 LauSetupBackups에 자동으로 백업합니다. 계속하려면 업그레이드 설치를 클릭하세요.', 'Backing up {0}…': '{0} 백업 중…'})
REVIEWED['ru'].update({'{0} extra upgrade patches will be backed up automatically in LauSetupBackups. Click Install upgrade to continue.': '{0} дополнительных патчей будут автоматически сохранены в LauSetupBackups. Нажмите «Установить обновление», чтобы продолжить.', 'Backing up {0}…': 'Резервное копирование {0}…'})
REVIEWED['zh-CN'].update({'{0} extra upgrade patches will be backed up automatically in LauSetupBackups. Click Install upgrade to continue.': '将自动把 {0} 个额外升级补丁备份到 LauSetupBackups。点击“安装升级”继续。', 'Backing up {0}…': '正在备份 {0}…'})
REVIEWED['zh-TW'].update({'{0} extra upgrade patches will be backed up automatically in LauSetupBackups. Click Install upgrade to continue.': '將自動把 {0} 個額外升級修補程式備份至 LauSetupBackups。按一下「安裝升級」繼續。', 'Backing up {0}…': '正在備份 {0}…'})


# Wizard wording; keep these translations reproducible without network requests.
REVIEWED['de'].update({'Adds upgraded spell effects. Requires an existing HD model client.': 'Fügt verbesserte Zaubereffekte hinzu. Erfordert einen vorhandenen Spielclient mit HD-Modellen.', 'Back': 'Zurück', 'Choose the look you want.': 'Wähle das gewünschte Aussehen.', 'Enhanced Consecration: {0}\nNew spell visuals: {1}\nMaps and minimap: {2}': 'Verbesserte Weihe: {0}\nNeue Zaubereffekte: {1}\nKarten und Minikarte: {2}', 'Finish': 'Fertigstellen', 'Finished': 'Fertig', 'Folder: {0}': 'Ordner: {0}', 'Game folder': 'Spielordner', 'Included automatically\nWoW.exe: compatible game executable\nPatch-Y (Lau patch): spell indicators and your Consecration choice\nPatch-Q: loading screens and regional artwork\nMatching language patches: {0}': 'Automatisch enthalten\nWoW.exe: kompatible ausführbare Spieldatei\nPatch-Y (Lau-Patch): Zauberindikatoren und deine Weihe-Auswahl\nPatch-Q: Ladebilder und regionale Grafiken\nPassende Sprach-Patches: {0}', 'Next': 'Weiter', 'Off': 'Aus', 'On': 'Ein', 'Review': 'Prüfen', 'Review your choices before installing.': 'Prüfe deine Auswahl vor der Installation.', 'Setup preserves existing files before replacing or moving them. Keep LauSetupBackups to restore the originals.': 'Setup sichert vorhandene Dateien, bevor es sie ersetzt oder verschiebt. Bewahre LauSetupBackups auf, um die Originale wiederherzustellen.', 'Sharper world maps and minimap textures. Downloads extra files; installed map upgrades are kept.': 'Schärfere Weltkarten und Minikartentexturen. Lädt zusätzliche Dateien herunter; installierte Karten-Upgrades bleiben erhalten.', "Uses Lau's custom ground effect for Consecration. Turn off for the original appearance.": 'Verwendet Laus eigenen Bodeneffekt für Weihe. Für das ursprüngliche Aussehen ausschalten.', 'Your game is ready.': 'Dein Spiel ist bereit.', 'Your visuals': 'Deine Grafik'})
REVIEWED['fr'].update({'Adds upgraded spell effects. Requires an existing HD model client.': 'Ajoute des effets de sorts améliorés. Nécessite un client de jeu disposant déjà de modèles HD.', 'Back': 'Retour', 'Choose the look you want.': 'Choisissez l’apparence souhaitée.', 'Enhanced Consecration: {0}\nNew spell visuals: {1}\nMaps and minimap: {2}': 'Consécration améliorée : {0}\nNouveaux effets de sorts : {1}\nCartes et minicarte : {2}', 'Finish': 'Terminer', 'Finished': 'Terminé', 'Folder: {0}': 'Dossier : {0}', 'Game folder': 'Dossier du jeu', 'Included automatically\nWoW.exe: compatible game executable\nPatch-Y (Lau patch): spell indicators and your Consecration choice\nPatch-Q: loading screens and regional artwork\nMatching language patches: {0}': 'Inclus automatiquement\nWoW.exe : exécutable du jeu compatible\nPatch-Y (patch Lau) : indicateurs de sorts et votre choix de Consécration\nPatch-Q : écrans de chargement et illustrations régionales\nCorrectifs de langue correspondants : {0}', 'Next': 'Suivant', 'Off': 'Désactivé', 'On': 'Activé', 'Review': 'Vérification', 'Review your choices before installing.': 'Vérifiez vos choix avant l’installation.', 'Setup preserves existing files before replacing or moving them. Keep LauSetupBackups to restore the originals.': 'Setup sauvegarde les fichiers existants avant de les remplacer ou de les déplacer. Conservez LauSetupBackups pour restaurer les originaux.', 'Sharper world maps and minimap textures. Downloads extra files; installed map upgrades are kept.': 'Cartes du monde et textures de minicarte plus nettes. Télécharge des fichiers supplémentaires ; les améliorations de cartes installées sont conservées.', "Uses Lau's custom ground effect for Consecration. Turn off for the original appearance.": 'Utilise l’effet au sol personnalisé de Lau pour Consécration. Désactivez pour conserver l’apparence d’origine.', 'Your game is ready.': 'Votre jeu est prêt.', 'Your visuals': 'Votre apparence'})
REVIEWED['es'].update({'Adds upgraded spell effects. Requires an existing HD model client.': 'Añade efectos de hechizos mejorados. Requiere un cliente que ya tenga modelos HD.', 'Back': 'Atrás', 'Choose the look you want.': 'Elige el aspecto que quieres.', 'Enhanced Consecration: {0}\nNew spell visuals: {1}\nMaps and minimap: {2}': 'Consagración mejorada: {0}\nNuevos efectos de hechizos: {1}\nMapas y minimapa: {2}', 'Finish': 'Finalizar', 'Finished': 'Finalizado', 'Folder: {0}': 'Carpeta: {0}', 'Game folder': 'Carpeta del juego', 'Included automatically\nWoW.exe: compatible game executable\nPatch-Y (Lau patch): spell indicators and your Consecration choice\nPatch-Q: loading screens and regional artwork\nMatching language patches: {0}': 'Incluido automáticamente\nWoW.exe: ejecutable del juego compatible\nPatch-Y (parche Lau): indicadores de hechizos y tu elección de Consagración\nPatch-Q: pantallas de carga e ilustraciones regionales\nParches del idioma correspondiente: {0}', 'Next': 'Siguiente', 'Off': 'Desactivado', 'On': 'Activado', 'Review': 'Revisar', 'Review your choices before installing.': 'Revisa tus elecciones antes de instalar.', 'Setup preserves existing files before replacing or moving them. Keep LauSetupBackups to restore the originals.': 'Setup guarda los archivos existentes antes de reemplazarlos o moverlos. Conserva LauSetupBackups para restaurar los originales.', 'Sharper world maps and minimap textures. Downloads extra files; installed map upgrades are kept.': 'Mapas del mundo y texturas del minimapa más nítidos. Descarga archivos adicionales; conserva las mejoras de mapas ya instaladas.', "Uses Lau's custom ground effect for Consecration. Turn off for the original appearance.": 'Usa el efecto de suelo personalizado de Lau para Consagración. Desactívalo para usar el aspecto original.', 'Your game is ready.': 'Tu juego está listo.', 'Your visuals': 'Tu aspecto'})
REVIEWED['pt'].update({'Adds upgraded spell effects. Requires an existing HD model client.': 'Adiciona efeitos de feitiços aprimorados. Requer um cliente que já tenha modelos HD.', 'Back': 'Voltar', 'Choose the look you want.': 'Escolha a aparência que você quer.', 'Enhanced Consecration: {0}\nNew spell visuals: {1}\nMaps and minimap: {2}': 'Consagração aprimorada: {0}\nNovos efeitos de feitiços: {1}\nMapas e minimapa: {2}', 'Finish': 'Concluir', 'Finished': 'Concluído', 'Folder: {0}': 'Pasta: {0}', 'Game folder': 'Pasta do jogo', 'Included automatically\nWoW.exe: compatible game executable\nPatch-Y (Lau patch): spell indicators and your Consecration choice\nPatch-Q: loading screens and regional artwork\nMatching language patches: {0}': 'Incluído automaticamente\nWoW.exe: executável do jogo compatível\nPatch-Y (patch Lau): indicadores de feitiços e sua escolha de Consagração\nPatch-Q: telas de carregamento e arte regional\nPatches do idioma correspondente: {0}', 'Next': 'Avançar', 'Off': 'Desativado', 'On': 'Ativado', 'Review': 'Revisar', 'Review your choices before installing.': 'Revise suas escolhas antes de instalar.', 'Setup preserves existing files before replacing or moving them. Keep LauSetupBackups to restore the originals.': 'O Setup salva os arquivos existentes antes de substituí-los ou movê-los. Guarde LauSetupBackups para restaurar os originais.', 'Sharper world maps and minimap textures. Downloads extra files; installed map upgrades are kept.': 'Mapas do mundo e texturas do minimapa mais nítidos. Baixa arquivos extras; mantém as melhorias de mapas já instaladas.', "Uses Lau's custom ground effect for Consecration. Turn off for the original appearance.": 'Usa o efeito de chão personalizado de Lau para Consagração. Desative para usar a aparência original.', 'Your game is ready.': 'Seu jogo está pronto.', 'Your visuals': 'Sua aparência'})
REVIEWED['ko'].update({'Adds upgraded spell effects. Requires an existing HD model client.': '향상된 주문 효과를 추가합니다. HD 모델이 이미 설치된 클라이언트가 필요합니다.', 'Back': '이전', 'Choose the look you want.': '원하는 모습을 선택하세요.', 'Enhanced Consecration: {0}\nNew spell visuals: {1}\nMaps and minimap: {2}': '향상된 신성화: {0}\n새 주문 효과: {1}\n지도 및 미니맵: {2}', 'Finish': '마침', 'Finished': '완료', 'Folder: {0}': '폴더: {0}', 'Game folder': '게임 폴더', 'Included automatically\nWoW.exe: compatible game executable\nPatch-Y (Lau patch): spell indicators and your Consecration choice\nPatch-Q: loading screens and regional artwork\nMatching language patches: {0}': '자동 포함 항목\nWoW.exe: 호환 게임 실행 파일\nPatch-Y (Lau 패치): 주문 표시 및 선택한 신성화 효과\nPatch-Q: 로딩 화면 및 지역 이미지\n해당 언어 패치: {0}', 'Next': '다음', 'Off': '끄기', 'On': '켜기', 'Review': '검토', 'Review your choices before installing.': '설치하기 전에 선택 사항을 확인하세요.', 'Setup preserves existing files before replacing or moving them. Keep LauSetupBackups to restore the originals.': 'Setup은 기존 파일을 교체하거나 이동하기 전에 보관합니다. 원본을 복원하려면 LauSetupBackups를 보관하세요.', 'Sharper world maps and minimap textures. Downloads extra files; installed map upgrades are kept.': '더 선명한 세계 지도와 미니맵 텍스처입니다. 추가 파일을 다운로드하며 이미 설치된 지도 업그레이드는 유지합니다.', "Uses Lau's custom ground effect for Consecration. Turn off for the original appearance.": '신성화에 Lau의 사용자 지정 지면 효과를 사용합니다. 원래 모습을 사용하려면 끄세요.', 'Your game is ready.': '게임이 준비되었습니다.', 'Your visuals': '시각 효과'})
REVIEWED['ru'].update({'Adds upgraded spell effects. Requires an existing HD model client.': 'Добавляет улучшенные эффекты заклинаний. Требуется клиент с уже установленными HD-моделями.', 'Back': 'Назад', 'Choose the look you want.': 'Выберите желаемый внешний вид.', 'Enhanced Consecration: {0}\nNew spell visuals: {1}\nMaps and minimap: {2}': 'Улучшенное освящение: {0}\nНовые эффекты заклинаний: {1}\nКарты и мини-карта: {2}', 'Finish': 'Завершить', 'Finished': 'Готово', 'Folder: {0}': 'Папка: {0}', 'Game folder': 'Папка игры', 'Included automatically\nWoW.exe: compatible game executable\nPatch-Y (Lau patch): spell indicators and your Consecration choice\nPatch-Q: loading screens and regional artwork\nMatching language patches: {0}': 'Включено автоматически\nWoW.exe: совместимый исполняемый файл игры\nPatch-Y (патч Lau): индикаторы заклинаний и выбранный эффект освящения\nPatch-Q: экраны загрузки и региональные изображения\nСоответствующие языковые патчи: {0}', 'Next': 'Далее', 'Off': 'Выкл.', 'On': 'Вкл.', 'Review': 'Проверка', 'Review your choices before installing.': 'Проверьте выбранные параметры перед установкой.', 'Setup preserves existing files before replacing or moving them. Keep LauSetupBackups to restore the originals.': 'Setup сохраняет существующие файлы перед заменой или перемещением. Сохраните LauSetupBackups для восстановления оригиналов.', 'Sharper world maps and minimap textures. Downloads extra files; installed map upgrades are kept.': 'Более чёткие карты мира и текстуры мини-карты. Загружает дополнительные файлы; установленные улучшения карт сохраняются.', "Uses Lau's custom ground effect for Consecration. Turn off for the original appearance.": 'Использует созданный Lau эффект освящения на земле. Отключите для исходного вида.', 'Your game is ready.': 'Ваша игра готова.', 'Your visuals': 'Внешний вид'})
REVIEWED['zh-CN'].update({'Adds upgraded spell effects. Requires an existing HD model client.': '添加升级版法术效果。需要已安装高清模型的游戏客户端。', 'Back': '上一步', 'Choose the look you want.': '选择您想要的外观。', 'Enhanced Consecration: {0}\nNew spell visuals: {1}\nMaps and minimap: {2}': '增强奉献：{0}\n新法术效果：{1}\n地图和小地图：{2}', 'Finish': '完成', 'Finished': '已完成', 'Folder: {0}': '文件夹：{0}', 'Game folder': '游戏文件夹', 'Included automatically\nWoW.exe: compatible game executable\nPatch-Y (Lau patch): spell indicators and your Consecration choice\nPatch-Q: loading screens and regional artwork\nMatching language patches: {0}': '自动包含\nWoW.exe：兼容的游戏执行文件\nPatch-Y（Lau 补丁）：法术指示效果及所选奉献效果\nPatch-Q：加载画面和地区图像\n对应语言补丁：{0}', 'Next': '下一步', 'Off': '关闭', 'On': '开启', 'Review': '确认', 'Review your choices before installing.': '安装前请确认您的选择。', 'Setup preserves existing files before replacing or moving them. Keep LauSetupBackups to restore the originals.': 'Setup 会在替换或移动现有文件前保存这些文件。请保留 LauSetupBackups 以便恢复原文件。', 'Sharper world maps and minimap textures. Downloads extra files; installed map upgrades are kept.': '更清晰的世界地图和小地图纹理。需要下载额外文件；保留已安装的地图升级。', "Uses Lau's custom ground effect for Consecration. Turn off for the original appearance.": '使用 Lau 自定义的奉献地面效果。关闭即可使用原始外观。', 'Your game is ready.': '您的游戏已准备就绪。', 'Your visuals': '视觉效果'})
REVIEWED['zh-TW'].update({'Adds upgraded spell effects. Requires an existing HD model client.': '新增升級版法術效果。需要已安裝高畫質模型的遊戲用戶端。', 'Back': '上一步', 'Choose the look you want.': '選擇您想要的外觀。', 'Enhanced Consecration: {0}\nNew spell visuals: {1}\nMaps and minimap: {2}': '強化奉獻：{0}\n新法術效果：{1}\n地圖與小地圖：{2}', 'Finish': '完成', 'Finished': '已完成', 'Folder: {0}': '資料夾：{0}', 'Game folder': '遊戲資料夾', 'Included automatically\nWoW.exe: compatible game executable\nPatch-Y (Lau patch): spell indicators and your Consecration choice\nPatch-Q: loading screens and regional artwork\nMatching language patches: {0}': '自動包含\nWoW.exe：相容的遊戲執行檔\nPatch-Y（Lau 修補程式）：法術指示效果及所選奉獻效果\nPatch-Q：載入畫面和地區圖像\n對應語言修補程式：{0}', 'Next': '下一步', 'Off': '關閉', 'On': '開啟', 'Review': '確認', 'Review your choices before installing.': '安裝前請確認您的選擇。', 'Setup preserves existing files before replacing or moving them. Keep LauSetupBackups to restore the originals.': 'Setup 會在取代或移動現有檔案前保存這些檔案。請保留 LauSetupBackups 以便還原原始檔案。', 'Sharper world maps and minimap textures. Downloads extra files; installed map upgrades are kept.': '更清晰的世界地圖與小地圖材質。需要下載額外檔案；保留已安裝的地圖升級。', "Uses Lau's custom ground effect for Consecration. Turn off for the original appearance.": '使用 Lau 自訂的奉獻地面效果。關閉即可使用原始外觀。', 'Your game is ready.': '您的遊戲已準備就緒。', 'Your visuals': '視覺效果'})


# Detected base patch and plain-language choice summary.
REVIEWED['de'].update({'Map Upgrade': 'Karten-Upgrade', 'Map Upgrade — already installed, kept': 'Karten-Upgrade — bereits installiert, bleibt erhalten', 'New Spells': 'Neue Zaubereffekte', 'Patch-Y (Lau’s version)': 'Patch-Y (Laus Version)', 'Patch-Y HD': 'Patch-Y HD', 'Patch-Y Non-HD': 'Patch-Y Non-HD', 'Selected for your detected client. A full HD model pack is not included.': 'Für deinen erkannten Spielclient ausgewählt. Ein vollständiges HD-Modellpaket ist nicht enthalten.', 'Your choices: {0}': 'Deine Auswahl: {0}'})
REVIEWED['fr'].update({'Map Upgrade': 'Amélioration des cartes', 'Map Upgrade — already installed, kept': 'Cartes améliorées — déjà installées, conservées', 'New Spells': 'Nouveaux effets de sorts', 'Patch-Y (Lau’s version)': 'Patch-Y (version de Lau)', 'Patch-Y HD': 'Patch-Y HD', 'Patch-Y Non-HD': 'Patch-Y Non-HD', 'Selected for your detected client. A full HD model pack is not included.': 'Sélectionné pour votre client détecté. Un pack complet de modèles HD n’est pas inclus.', 'Your choices: {0}': 'Vos choix : {0}'})
REVIEWED['es'].update({'Map Upgrade': 'Mejora de mapas', 'Map Upgrade — already installed, kept': 'Mejora de mapas — ya instalada, se conserva', 'New Spells': 'Nuevos hechizos', 'Patch-Y (Lau’s version)': 'Patch-Y (versión de Lau)', 'Patch-Y HD': 'Patch-Y HD', 'Patch-Y Non-HD': 'Patch-Y Non-HD', 'Selected for your detected client. A full HD model pack is not included.': 'Seleccionado para tu cliente detectado. No incluye un paquete completo de modelos HD.', 'Your choices: {0}': 'Tus elecciones: {0}'})
REVIEWED['pt'].update({'Map Upgrade': 'Melhoria de mapas', 'Map Upgrade — already installed, kept': 'Melhoria de mapas — já instalada, mantida', 'New Spells': 'Novos feitiços', 'Patch-Y (Lau’s version)': 'Patch-Y (versão do Lau)', 'Patch-Y HD': 'Patch-Y HD', 'Patch-Y Non-HD': 'Patch-Y Non-HD', 'Selected for your detected client. A full HD model pack is not included.': 'Selecionado para o cliente detectado. Não inclui um pacote completo de modelos HD.', 'Your choices: {0}': 'Suas escolhas: {0}'})
REVIEWED['ko'].update({'Map Upgrade': '지도 업그레이드', 'Map Upgrade — already installed, kept': '지도 업그레이드 — 이미 설치됨, 유지', 'New Spells': '새 주문 효과', 'Patch-Y (Lau’s version)': 'Patch-Y (Lau 버전)', 'Patch-Y HD': 'Patch-Y HD', 'Patch-Y Non-HD': 'Patch-Y Non-HD', 'Selected for your detected client. A full HD model pack is not included.': '감지된 클라이언트에 맞게 선택됩니다. 전체 HD 모델 팩은 포함되지 않습니다.', 'Your choices: {0}': '선택 사항: {0}'})
REVIEWED['ru'].update({'Map Upgrade': 'Улучшение карт', 'Map Upgrade — already installed, kept': 'Улучшение карт — уже установлено, сохраняется', 'New Spells': 'Новые заклинания', 'Patch-Y (Lau’s version)': 'Patch-Y (версия Lau)', 'Patch-Y HD': 'Patch-Y HD', 'Patch-Y Non-HD': 'Patch-Y Non-HD', 'Selected for your detected client. A full HD model pack is not included.': 'Выбрано для обнаруженного клиента. Полный набор HD-моделей не включён.', 'Your choices: {0}': 'Ваш выбор: {0}'})
REVIEWED['zh-CN'].update({'Map Upgrade': '地图升级', 'Map Upgrade — already installed, kept': '地图升级 — 已安装，将保留', 'New Spells': '新法术', 'Patch-Y (Lau’s version)': 'Patch-Y（Lau 版本）', 'Patch-Y HD': 'Patch-Y HD', 'Patch-Y Non-HD': 'Patch-Y Non-HD', 'Selected for your detected client. A full HD model pack is not included.': '根据检测到的客户端选择。不包含完整的高清模型包。', 'Your choices: {0}': '您的选择：{0}'})
REVIEWED['zh-TW'].update({'Map Upgrade': '地圖升級', 'Map Upgrade — already installed, kept': '地圖升級 — 已安裝，將保留', 'New Spells': '新法術', 'Patch-Y (Lau’s version)': 'Patch-Y（Lau 版本）', 'Patch-Y HD': 'Patch-Y HD', 'Patch-Y Non-HD': 'Patch-Y Non-HD', 'Selected for your detected client. A full HD model pack is not included.': '根據偵測到的用戶端選擇。不包含完整的高畫質模型包。', 'Your choices: {0}': '您的選擇：{0}'})

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("extract", "build", "verify"), nargs="?", default="verify")
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    if args.command == "extract": print(json.dumps(extract_keys(), ensure_ascii=False, indent=2))
    elif args.command == "build": build(workers=max(1, min(args.workers, 4)))
    else: validate()


# Setup 1.4.0 optional components and Patch-V preservation.
REVIEWED['de'].update({'Install': 'Installieren', 'Keep existing': 'Vorhandene behalten', 'Install compatible WoW.exe': 'Kompatible WoW.exe installieren', 'Loading screens and artwork (Patch-Q)': 'Ladebildschirme und Grafiken (Patch-Q)', 'Turn on to replace your game executable. Off keeps your current WoW.exe.': 'Aktivieren, um die Spieldatei zu ersetzen. Deaktiviert bleibt Ihre aktuelle WoW.exe erhalten.', "Turn on for Lau's loading screens and artwork. Off keeps your current files.": 'Aktivieren für Laus Ladebildschirme und Grafiken. Deaktiviert bleiben Ihre Dateien erhalten.', 'Patch-Y and matching language patches: {0}\nWoW.exe: {1}\nLoading screens and artwork (Patch-Q): {2}': 'Patch-Y und passende Sprachpatches: {0}\nWoW.exe: {1}\nLadebildschirme und Grafiken (Patch-Q): {2}', 'Unrecognized Patch-V kept in Data. Compatibility could not be verified. You can continue installing; this file will not be changed.': 'Unbekannte Patch-V bleibt in Data. Kompatibilität konnte nicht geprüft werden. Sie können fortfahren; diese Datei bleibt unverändert.', 'Setup {2}  •  Game {0} Lau  •  {1}  •  Build 12340': 'Setup {2}  •  Spiel {0} Lau  •  {1}  •  Build 12340'})
REVIEWED['fr'].update({'Install': 'Installer', 'Keep existing': 'Conserver les fichiers actuels', 'Install compatible WoW.exe': 'Installer WoW.exe compatible', 'Loading screens and artwork (Patch-Q)': 'Écrans de chargement et illustrations (Patch-Q)', 'Turn on to replace your game executable. Off keeps your current WoW.exe.': 'Activez pour remplacer le fichier du jeu. Désactivé, votre WoW.exe actuel est conservé.', "Turn on for Lau's loading screens and artwork. Off keeps your current files.": 'Activez pour les écrans et illustrations de Lau. Désactivé, vos fichiers actuels sont conservés.', 'Patch-Y and matching language patches: {0}\nWoW.exe: {1}\nLoading screens and artwork (Patch-Q): {2}': 'Patch-Y et correctifs de langue correspondants : {0}\nWoW.exe : {1}\nÉcrans et illustrations (Patch-Q) : {2}', 'Unrecognized Patch-V kept in Data. Compatibility could not be verified. You can continue installing; this file will not be changed.': 'Patch-V non reconnu conservé dans Data. Compatibilité non vérifiée. Vous pouvez poursuivre l’installation ; ce fichier restera inchangé.', 'Setup {2}  •  Game {0} Lau  •  {1}  •  Build 12340': 'Installation {2}  •  Jeu {0} Lau  •  {1}  •  Build 12340'})
REVIEWED['es'].update({'Install': 'Instalar', 'Keep existing': 'Conservar los archivos actuales', 'Install compatible WoW.exe': 'Instalar WoW.exe compatible', 'Loading screens and artwork (Patch-Q)': 'Pantallas de carga e ilustraciones (Patch-Q)', 'Turn on to replace your game executable. Off keeps your current WoW.exe.': 'Activa para sustituir el ejecutable del juego. Desactivado conserva tu WoW.exe actual.', "Turn on for Lau's loading screens and artwork. Off keeps your current files.": 'Activa para usar las pantallas e ilustraciones de Lau. Desactivado conserva tus archivos actuales.', 'Patch-Y and matching language patches: {0}\nWoW.exe: {1}\nLoading screens and artwork (Patch-Q): {2}': 'Patch-Y y parches del idioma correspondiente: {0}\nWoW.exe: {1}\nPantallas e ilustraciones (Patch-Q): {2}', 'Unrecognized Patch-V kept in Data. Compatibility could not be verified. You can continue installing; this file will not be changed.': 'Patch-V desconocido se conserva en Data. No se pudo verificar su compatibilidad. Puedes continuar; este archivo no se modificará.', 'Setup {2}  •  Game {0} Lau  •  {1}  •  Build 12340': 'Instalador {2}  •  Juego {0} Lau  •  {1}  •  Build 12340'})
REVIEWED['pt'].update({'Install': 'Instalar', 'Keep existing': 'Manter arquivos atuais', 'Install compatible WoW.exe': 'Instalar WoW.exe compatível', 'Loading screens and artwork (Patch-Q)': 'Telas de carregamento e imagens (Patch-Q)', 'Turn on to replace your game executable. Off keeps your current WoW.exe.': 'Ative para substituir o executável do jogo. Desativado mantém seu WoW.exe atual.', "Turn on for Lau's loading screens and artwork. Off keeps your current files.": 'Ative para usar as telas e imagens de Lau. Desativado mantém seus arquivos atuais.', 'Patch-Y and matching language patches: {0}\nWoW.exe: {1}\nLoading screens and artwork (Patch-Q): {2}': 'Patch-Y e patches do idioma correspondente: {0}\nWoW.exe: {1}\nTelas e imagens (Patch-Q): {2}', 'Unrecognized Patch-V kept in Data. Compatibility could not be verified. You can continue installing; this file will not be changed.': 'Patch-V desconhecido mantido em Data. Não foi possível verificar a compatibilidade. Você pode continuar; este arquivo não será alterado.', 'Setup {2}  •  Game {0} Lau  •  {1}  •  Build 12340': 'Instalador {2}  •  Jogo {0} Lau  •  {1}  •  Build 12340'})
REVIEWED['ru'].update({'Install': 'Установить', 'Keep existing': 'Сохранить текущие файлы', 'Install compatible WoW.exe': 'Установить совместимый WoW.exe', 'Loading screens and artwork (Patch-Q)': 'Экраны загрузки и изображения (Patch-Q)', 'Turn on to replace your game executable. Off keeps your current WoW.exe.': 'Включите для замены файла игры. Если выключено, текущий WoW.exe сохраняется.', "Turn on for Lau's loading screens and artwork. Off keeps your current files.": 'Включите для экранов загрузки и изображений Lau. Если выключено, текущие файлы сохраняются.', 'Patch-Y and matching language patches: {0}\nWoW.exe: {1}\nLoading screens and artwork (Patch-Q): {2}': 'Patch-Y и соответствующие языковые патчи: {0}\nWoW.exe: {1}\nЭкраны загрузки и изображения (Patch-Q): {2}', 'Unrecognized Patch-V kept in Data. Compatibility could not be verified. You can continue installing; this file will not be changed.': 'Неизвестный Patch-V сохранён в Data. Совместимость не проверена. Можно продолжить установку; этот файл не изменится.', 'Setup {2}  •  Game {0} Lau  •  {1}  •  Build 12340': 'Установщик {2}  •  Игра {0} Lau  •  {1}  •  Build 12340'})
REVIEWED['ko'].update({'Install': '설치', 'Keep existing': '기존 파일 유지', 'Install compatible WoW.exe': '호환 WoW.exe 설치', 'Loading screens and artwork (Patch-Q)': '로딩 화면 및 이미지 (Patch-Q)', 'Turn on to replace your game executable. Off keeps your current WoW.exe.': '켜면 게임 실행 파일을 교체합니다. 끄면 현재 WoW.exe를 유지합니다.', "Turn on for Lau's loading screens and artwork. Off keeps your current files.": '켜면 Lau의 로딩 화면과 이미지를 사용합니다. 끄면 현재 파일을 유지합니다.', 'Patch-Y and matching language patches: {0}\nWoW.exe: {1}\nLoading screens and artwork (Patch-Q): {2}': 'Patch-Y 및 해당 언어 패치: {0}\nWoW.exe: {1}\n로딩 화면 및 이미지 (Patch-Q): {2}', 'Unrecognized Patch-V kept in Data. Compatibility could not be verified. You can continue installing; this file will not be changed.': '인식되지 않은 Patch-V를 Data에 유지합니다. 호환성을 확인할 수 없습니다. 설치를 계속할 수 있으며 이 파일은 변경되지 않습니다.', 'Setup {2}  •  Game {0} Lau  •  {1}  •  Build 12340': '설치 프로그램 {2}  •  게임 {0} Lau  •  {1}  •  Build 12340'})
REVIEWED['zh-CN'].update({'Install': '安装', 'Keep existing': '保留现有文件', 'Install compatible WoW.exe': '安装兼容的 WoW.exe', 'Loading screens and artwork (Patch-Q)': '加载画面和图片 (Patch-Q)', 'Turn on to replace your game executable. Off keeps your current WoW.exe.': '开启以替换游戏程序。关闭则保留当前 WoW.exe。', "Turn on for Lau's loading screens and artwork. Off keeps your current files.": '开启以使用 Lau 的加载画面和图片。关闭则保留当前文件。', 'Patch-Y and matching language patches: {0}\nWoW.exe: {1}\nLoading screens and artwork (Patch-Q): {2}': 'Patch-Y 及对应语言补丁：{0}\nWoW.exe：{1}\n加载画面和图片 (Patch-Q)：{2}', 'Unrecognized Patch-V kept in Data. Compatibility could not be verified. You can continue installing; this file will not be changed.': '无法识别的 Patch-V 将保留在 Data 中。无法验证兼容性。可以继续安装，此文件不会更改。', 'Setup {2}  •  Game {0} Lau  •  {1}  •  Build 12340': '安装程序 {2}  •  游戏 {0} Lau  •  {1}  •  Build 12340'})
REVIEWED['zh-TW'].update({'Install': '安裝', 'Keep existing': '保留現有檔案', 'Install compatible WoW.exe': '安裝相容的 WoW.exe', 'Loading screens and artwork (Patch-Q)': '載入畫面和圖片 (Patch-Q)', 'Turn on to replace your game executable. Off keeps your current WoW.exe.': '開啟以替換遊戲程式。關閉則保留目前的 WoW.exe。', "Turn on for Lau's loading screens and artwork. Off keeps your current files.": '開啟以使用 Lau 的載入畫面和圖片。關閉則保留目前的檔案。', 'Patch-Y and matching language patches: {0}\nWoW.exe: {1}\nLoading screens and artwork (Patch-Q): {2}': 'Patch-Y 及對應語言修補檔：{0}\nWoW.exe：{1}\n載入畫面和圖片 (Patch-Q)：{2}', 'Unrecognized Patch-V kept in Data. Compatibility could not be verified. You can continue installing; this file will not be changed.': '無法識別的 Patch-V 將保留在 Data 中。無法驗證相容性。可以繼續安裝，此檔案不會變更。', 'Setup {2}  •  Game {0} Lau  •  {1}  •  Build 12340': '安裝程式 {2}  •  遊戲 {0} Lau  •  {1}  •  Build 12340'})

REVIEWED['de']['New map upgrades require Patch-Q.']='Neue Karten-Upgrades erfordern Patch-Q.'
REVIEWED['fr']['New map upgrades require Patch-Q.']='Les nouvelles améliorations de cartes nécessitent Patch-Q.'
REVIEWED['es']['New map upgrades require Patch-Q.']='Las nuevas mejoras de mapas requieren Patch-Q.'
REVIEWED['pt']['New map upgrades require Patch-Q.']='Novas melhorias de mapas exigem Patch-Q.'
REVIEWED['ru']['New map upgrades require Patch-Q.']='Для нового улучшения карт требуется Patch-Q.'
REVIEWED['ko']['New map upgrades require Patch-Q.']='새 지도 업그레이드에는 Patch-Q가 필요합니다.'
REVIEWED['zh-CN']['New map upgrades require Patch-Q.']='新的地图升级需要 Patch-Q。'
REVIEWED['zh-TW']['New map upgrades require Patch-Q.']='新的地圖升級需要 Patch-Q。'


# Reviewed wizard scope: independent maps and no broad patch scan.
REVIEWED['de'].update({"Lau's maps and minimaps plus Trimitor's dungeon, raid and cave maps. Includes WDM support addons. Loading screens are separate.": 'Laus Karten und Minikarten plus Trimitors Dungeon-, Schlachtzugs- und Höhlenkarten. Mit WDM-Addons. Ladebilder sind separat.', 'Files Setup replaces are backed up. Other patches and personal settings stay untouched. Manage renamed duplicate patches yourself.': 'Setup sichert ersetzte Dateien. Andere Patches und persönliche Einstellungen bleiben unverändert. Umbenannte doppelte Patches verwaltest du selbst.'})
REVIEWED['fr'].update({"Lau's maps and minimaps plus Trimitor's dungeon, raid and cave maps. Includes WDM support addons. Loading screens are separate.": 'Cartes et mini-cartes de Lau avec les cartes de donjons, raids et grottes de Trimitor. Addons WDM inclus. Écrans de chargement séparés.', 'Files Setup replaces are backed up. Other patches and personal settings stay untouched. Manage renamed duplicate patches yourself.': 'Les fichiers remplacés sont sauvegardés. Les autres patchs et réglages personnels restent intacts. Gérez vous-même les doublons renommés.'})
REVIEWED['es'].update({"Lau's maps and minimaps plus Trimitor's dungeon, raid and cave maps. Includes WDM support addons. Loading screens are separate.": 'Mapas y minimapas de Lau con mapas de mazmorras, bandas y cuevas de Trimitor. Incluye addons WDM. Pantallas de carga independientes.', 'Files Setup replaces are backed up. Other patches and personal settings stay untouched. Manage renamed duplicate patches yourself.': 'Se guardan copias de los archivos reemplazados. Otros parches y ajustes personales no cambian. Gestiona tú los parches duplicados renombrados.'})
REVIEWED['pt'].update({"Lau's maps and minimaps plus Trimitor's dungeon, raid and cave maps. Includes WDM support addons. Loading screens are separate.": 'Mapas e minimapas de Lau com mapas de masmorras, raides e cavernas de Trimitor. Inclui addons WDM. Telas de carregamento separadas.', 'Files Setup replaces are backed up. Other patches and personal settings stay untouched. Manage renamed duplicate patches yourself.': 'Os arquivos substituídos recebem backup. Outros patches e configurações pessoais ficam intactos. Gerencie você os patches duplicados renomeados.'})
REVIEWED['ru'].update({"Lau's maps and minimaps plus Trimitor's dungeon, raid and cave maps. Includes WDM support addons. Loading screens are separate.": 'Карты и миникарты Lau вместе с картами подземелий, рейдов и пещер Trimitor. Включает аддоны WDM. Экраны загрузки выбираются отдельно.', 'Files Setup replaces are backed up. Other patches and personal settings stay untouched. Manage renamed duplicate patches yourself.': 'Заменяемые файлы сохраняются в резервной копии. Другие патчи и личные настройки не изменяются. Переименованные дубликаты патчей проверяйте самостоятельно.'})
REVIEWED['ko'].update({"Lau's maps and minimaps plus Trimitor's dungeon, raid and cave maps. Includes WDM support addons. Loading screens are separate.": 'Lau 지도와 미니맵에 Trimitor 던전, 공격대, 동굴 지도를 추가합니다. WDM 애드온 포함. 로딩 화면은 별도 선택입니다.', 'Files Setup replaces are backed up. Other patches and personal settings stay untouched. Manage renamed duplicate patches yourself.': '교체하는 파일은 백업됩니다. 다른 패치와 개인 설정은 그대로 유지됩니다. 이름을 바꾼 중복 패치는 직접 관리하세요.'})
REVIEWED['zh-CN'].update({"Lau's maps and minimaps plus Trimitor's dungeon, raid and cave maps. Includes WDM support addons. Loading screens are separate.": 'Lau 地图和小地图，加入 Trimitor 的地下城、团队副本及洞穴地图。包含 WDM 插件。加载画面单独选择。', 'Files Setup replaces are backed up. Other patches and personal settings stay untouched. Manage renamed duplicate patches yourself.': '安装程序会备份被替换的文件。其他补丁和个人设置保持不变。请自行管理重命名的重复补丁。'})
REVIEWED['zh-TW'].update({"Lau's maps and minimaps plus Trimitor's dungeon, raid and cave maps. Includes WDM support addons. Loading screens are separate.": 'Lau 地圖和小地圖，加入 Trimitor 的地城、團隊副本及洞穴地圖。包含 WDM 插件。載入畫面單獨選擇。', 'Files Setup replaces are backed up. Other patches and personal settings stay untouched. Manage renamed duplicate patches yourself.': '安裝程式會備份被替換的檔案。其他修補檔和個人設定保持不變。請自行管理重新命名的重複修補檔。'})

# Combined executable/loading-screen option.
REVIEWED['de'].update({'Compatible WoW.exe + loading screens': 'Kompatible WoW.exe + Ladebilder', "Installs the compatible WoW.exe and Lau's loading screens together. Off keeps both unchanged.": 'Installiert die kompatible WoW.exe und Laus Ladebilder zusammen. Aus lässt beide unverändert.'})
REVIEWED['fr'].update({'Compatible WoW.exe + loading screens': 'WoW.exe compatible + écrans de chargement', "Installs the compatible WoW.exe and Lau's loading screens together. Off keeps both unchanged.": 'Installe ensemble WoW.exe compatible et les écrans de chargement de Lau. Désactivé conserve les deux.'})
REVIEWED['es'].update({'Compatible WoW.exe + loading screens': 'WoW.exe compatible + pantallas de carga', "Installs the compatible WoW.exe and Lau's loading screens together. Off keeps both unchanged.": 'Instala juntos WoW.exe compatible y las pantallas de carga de Lau. Desactivado conserva ambos.'})
REVIEWED['pt'].update({'Compatible WoW.exe + loading screens': 'WoW.exe compatível + telas de carregamento', "Installs the compatible WoW.exe and Lau's loading screens together. Off keeps both unchanged.": 'Instala juntos WoW.exe compatível e as telas de carregamento de Lau. Desativado mantém ambos inalterados.'})
REVIEWED['ru'].update({'Compatible WoW.exe + loading screens': 'Совместимый WoW.exe + экраны загрузки', "Installs the compatible WoW.exe and Lau's loading screens together. Off keeps both unchanged.": 'Устанавливает совместимый WoW.exe вместе с экранами загрузки Lau. Если выключено, оба компонента остаются без изменений.'})
REVIEWED['ko'].update({'Compatible WoW.exe + loading screens': '호환 WoW.exe + 로딩 화면', "Installs the compatible WoW.exe and Lau's loading screens together. Off keeps both unchanged.": '호환 WoW.exe와 Lau 로딩 화면을 함께 설치합니다. 끄면 둘 다 그대로 유지됩니다.'})
REVIEWED['zh-CN'].update({'Compatible WoW.exe + loading screens': '兼容 WoW.exe + 加载画面', "Installs the compatible WoW.exe and Lau's loading screens together. Off keeps both unchanged.": '一起安装兼容的 WoW.exe 和 Lau 加载画面。关闭则两者保持不变。'})
REVIEWED['zh-TW'].update({'Compatible WoW.exe + loading screens': '相容 WoW.exe + 載入畫面', "Installs the compatible WoW.exe and Lau's loading screens together. Off keeps both unchanged.": '一起安裝相容的 WoW.exe 和 Lau 載入畫面。關閉則兩者保持不變。'})
REVIEWED['de'].update({'Your client has HD models active. The appropriate Patch-Y HD version will be installed.': 'Ihr Client verwendet HD-Modelle. Die passende Version von Patch-Y HD wird installiert.', 'Your client does not have HD models active. The appropriate Patch-Y Non-HD version will be installed.': 'Ihr Client verwendet keine HD-Modelle. Die passende Version von Patch-Y Non-HD wird installiert.'})
REVIEWED['fr'].update({'Your client has HD models active. The appropriate Patch-Y HD version will be installed.': 'Votre client utilise des modèles HD. La version adaptée de Patch-Y HD sera installée.', 'Your client does not have HD models active. The appropriate Patch-Y Non-HD version will be installed.': 'Votre client ne possède pas de modèles HD actifs. La version adaptée de Patch-Y Non-HD sera installée.'})
REVIEWED['es'].update({'Your client has HD models active. The appropriate Patch-Y HD version will be installed.': 'Tu cliente tiene modelos HD activos. Se instalará la versión adecuada de Patch-Y HD.', 'Your client does not have HD models active. The appropriate Patch-Y Non-HD version will be installed.': 'Tu cliente no tiene modelos HD activos. Se instalará la versión adecuada de Patch-Y Non-HD.'})
REVIEWED['pt'].update({'Your client has HD models active. The appropriate Patch-Y HD version will be installed.': 'Seu cliente tem modelos HD ativos. A versão adequada do Patch-Y HD será instalada.', 'Your client does not have HD models active. The appropriate Patch-Y Non-HD version will be installed.': 'Seu cliente não tem modelos HD ativos. A versão adequada do Patch-Y Non-HD será instalada.'})
REVIEWED['ru'].update({'Your client has HD models active. The appropriate Patch-Y HD version will be installed.': 'В клиенте активны HD-модели. Будет установлена подходящая версия Patch-Y HD.', 'Your client does not have HD models active. The appropriate Patch-Y Non-HD version will be installed.': 'В клиенте нет активных HD-моделей. Будет установлена подходящая версия Patch-Y Non-HD.'})
REVIEWED['ko'].update({'Your client has HD models active. The appropriate Patch-Y HD version will be installed.': '클라이언트에 HD 모델이 활성화되어 있습니다. 적합한 Patch-Y HD 버전이 설치됩니다.', 'Your client does not have HD models active. The appropriate Patch-Y Non-HD version will be installed.': '클라이언트에 HD 모델이 활성화되어 있지 않습니다. 적합한 Patch-Y Non-HD 버전이 설치됩니다.'})
REVIEWED['zh-CN'].update({'Your client has HD models active. The appropriate Patch-Y HD version will be installed.': '客户端已启用 HD 模型。将安装适用的 Patch-Y HD 版本。', 'Your client does not have HD models active. The appropriate Patch-Y Non-HD version will be installed.': '客户端未启用 HD 模型。将安装适用的 Patch-Y Non-HD 版本。'})
REVIEWED['zh-TW'].update({'Your client has HD models active. The appropriate Patch-Y HD version will be installed.': '用戶端已啟用 HD 模型。將安裝適用的 Patch-Y HD 版本。', 'Your client does not have HD models active. The appropriate Patch-Y Non-HD version will be installed.': '用戶端未啟用 HD 模型。將安裝適用的 Patch-Y Non-HD 版本。'})
for values in REVIEWED.values():
    values['LAU SETUP']='LAU SETUP'
    if '1   Choose your existing WoW 3.3.5a folder' in values:values['Choose your existing WoW 3.3.5a folder']=values['1   Choose your existing WoW 3.3.5a folder'].lstrip('1 .　')
if __name__ == "__main__": main()

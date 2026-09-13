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
            if locale != "en-US" and len(re.findall(r"[A-Za-z]{3,}", visible)) >= 2 and translated == source:
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("extract", "build", "verify"), nargs="?", default="verify")
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    if args.command == "extract": print(json.dumps(extract_keys(), ensure_ascii=False, indent=2))
    elif args.command == "build": build(workers=max(1, min(args.workers, 4)))
    else: validate()


if __name__ == "__main__": main()

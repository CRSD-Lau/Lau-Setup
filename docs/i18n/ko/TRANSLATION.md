<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — 하나의 ZIP에 이제 Windows 설치 관리자와 Linux/Wine 실행기가 함께 들어 있습니다. 인터페이스는 열 가지 옵션 중 운영 체제 언어를 자동으로 따르며, 수동 선택은 저장됩니다. 게임 버전 3.0.8과 게임 파일은 변경되지 않습니다. DBC 변경도 없습니다.
>
> Google HTTP 429로 전체 안내서 갱신은 아직 보류 중입니다. 아래 본문은 오래되었을 수 있으므로 현재 영어 원문과 1.3.0 릴리스 노트를 확인하세요. [English](../../../TRANSLATION.md) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
>
> **현재 다운로드:** Windows와 Linux/Wine용 [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)입니다. 다섯 파일이 있는 `LauSetup/` 폴더를 추출하세요. Windows에서는 `LauSetup.exe`를 열고 Linux/Wine에서는 `LauSetup.sh`를 실행합니다. 아래의 별도 EXE 또는 Wine ZIP 관련 이전 안내는 1.3.0에 적용되지 않습니다.
>
> **1.3.0:** 인식된 추가 업그레이드 파일은 자동으로 백업되고 설치가 계속됩니다. 복원하면 파일이 원래 위치로 돌아갑니다. 직접 옮길 필요가 없습니다. 설치 프로그램은 기존 파일을 교체하거나 이동하기 전에 자동으로 보존합니다. 관련 없는 파일은 변경하지 않습니다.

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 자동 번역. [영어 출처](../../../TRANSLATION.md). 표현이 다를 경우 영어 출처가 권위가 있습니다.

<a id="repository-translations"></a>

# 저장소 번역

**문서 번역** GitHub Action은 **Google 번역의 무료 웹사이트**를 사용하여 지원되는 모든 게임 언어와 **브라질 포르투갈어**로 저장소 문서를 사용할 수 있도록 유지합니다. API 키, 유료 Cloud Translation 계정, 구독 또는 모델 다운로드가 필요하지 않습니다.

README 상단에 있는 언어 링크를 사용하세요. GitHub는 기본적으로 루트 README를 표시합니다. 방문자는 이 링크를 사용하여 언어를 선택합니다. 이 워크플로우는 설치 안내서 및 기술 참조를 포함한 문서를 번역합니다. GitHub의 인터페이스, 문제, 릴리스 설명, 별도의 웹사이트 또는 설치 프로그램 인터페이스를 번역하지 않으며 포르투갈어 게임 로케일을 추가하지 않습니다.

<a id="languages"></a>

## 언어

적용 범위는 `build/catalog.json`에 대해 확인되며 문서화를 위해 `ptBR`가 추가됩니다. 읽기 옵션은 영어, 독일어, 스페인 및 멕시코용 스페인어, 프랑스어, 한국어, 러시아어, 중국어 간체, 중국어 번체 및 브라질 포르투갈어입니다.

Google의 웹 언어 선택기는 `pt`를 포르투갈어(브라질)로 식별합니다. 포르투갈어(포르투갈)는 다른 타겟입니다. Google은 하나의 `es` 대상을 제공하므로 스페인 및 멕시코 페이지에서는 동일한 일반 스페인어 번역을 사용합니다. 중국 타깃은 따로 있다. Google 대상 코드와 모국어 이름은 `tools/translation-locales.json`에 있습니다. 게임 로케일을 추가하려면 해당 문서 매핑을 추가해야 합니다. 누락된 적용 범위는 검증에 실패합니다.

<a id="automatic-updates"></a>

## 자동 업데이트

영어 문서 변경을 푸시하면 카탈로그 또는 번역 도구가 작업을 트리거합니다. 유지관리자는 **작업 → 문서 번역 → 워크플로 실행 → 기본**을 선택할 수도 있습니다. 저장소 루트, `docs/` 및 `wine/README.txt`에서 추적된 마크다운 및 텍스트 파일을 검색합니다. 생성된 번역 및 `AGENTS.md`는 제외됩니다. 텍스트 가이드는 `docs/i18n/<language>/` 아래에서 마크다운으로 렌더링됩니다.

변경된 문서만 번역이 필요합니다. 소스 및 출력 해시와 세그먼트 캐시는 반복되는 요청을 방지합니다. 번역 규칙을 변경할 때 `TRANSLATION_REVISION`를 범프합니다. 최대 3개의 언어 작업이 한 번에 실행되며 각 작업의 요청 사이에 일시 중지가 있습니다. 속도 제한으로 인해 영향을 받는 작업이 중지됩니다. 나중에 다시 시도하세요. 무료 웹 인터페이스는 자동화를 위한 비공식 인터페이스이며 요청을 변경하거나 차단할 수 있습니다. 유료 대체는 없습니다. 생성이 실패해도 기존에 게시된 페이지를 계속 사용할 수 있습니다.

이 공용 저장소에서는 표준 GitHub 호스팅 실행기 실행이 무료입니다. 저장소가 비공개가 되면 작업이 비활성화됩니다. 작은 중간 아티팩트는 하루 후에 만료됩니다. 모델이나 큰 종속성은 저장되지 않습니다.

<a id="integrity-and-publication"></a>

## 무결성 및 출판

코드, 명령, URL, 버전 번호, 제품 이름, 크레딧 및 서명 상태 설명이 보호됩니다. 상대 문서 링크는 동일한 언어를 가리키고, 이미지와 코드 링크는 원본을 가리킵니다. 안정적인 영어 제목 앵커는 섹션 링크를 유지합니다. 모든 페이지는 자신을 자동 번역으로 식별하고 영어 소스에 대한 링크를 제공하며 **Neil Mitchell**에 대한 작성자, 작성자 및 최종 수정자 메타데이터를 유지합니다.

9개의 번역된 읽기 옵션은 모두 `main`에 게시하기 전에 소스/출력 무결성 검사를 통과해야 합니다. 게시는 변경된 소스 개정을 거부하고 절대 강제로 푸시하지 않습니다. 풀 요청은 단위 검사를 실행하고 읽기 전용 액세스가 가능한 실제 브라질 포르투갈어 README 연기 번역을 실행합니다. 나중에 분기 보호로 인해 커밋이 방지되는 경우 승인된 PR 프로세스에 맞게 게시를 조정하세요.

기계 번역에는 여전히 유창한 독자의 검토가 필요합니다. 영어는 여전히 권위적입니다. 지속적인 수정을 위해 영어 소스 또는 번역 도구를 업데이트하세요. 생성된 파일에 대한 직접 편집 내용이 다시 생성됩니다. 실패했거나 부분 배치는 기존 문서를 대체하지 않습니다.

<a id="local-use"></a>

## 로컬 사용

Python 3.11 이상이면 충분합니다. 추가 패키지가 필요하지 않습니다. 네트워크 액세스 없이 구조를 확인하십시오.

```sh
python -m unittest discover -s tests -p test_translate_docs.py -v
python tools/translate_docs.py --check
```

무료 Google 웹사이트를 사용하여 공개 문서를 번역하세요.

```sh
python tools/translate_docs.py --locale ptBR
python tools/translate_docs.py --navigation
```

참조: [Google 번역](https://translate.google.com/), [GitHub 작업 결제](https://docs.github.com/en/billing/concepts/product-billing/github-actions). 별도의 [Google Cloud Translation API](https://cloud.google.com/translate/pricing)는 유료 서비스이므로 여기서는 사용하지 않습니다.

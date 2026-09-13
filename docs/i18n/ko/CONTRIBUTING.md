<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — 하나의 ZIP에 이제 Windows 설치 관리자와 Linux/Wine 실행기가 함께 들어 있습니다. 인터페이스는 열 가지 옵션 중 운영 체제 언어를 자동으로 따르며, 수동 선택은 저장됩니다. 게임 버전 3.0.8과 게임 파일은 변경되지 않습니다. DBC 변경도 없습니다.
>
> Google HTTP 429로 전체 안내서 갱신은 아직 보류 중입니다. 아래 본문은 오래되었을 수 있으므로 현재 영어 원문과 1.3.0 릴리스 노트를 확인하세요. [English](../../../CONTRIBUTING.md) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
>
> **현재 다운로드:** Windows와 Linux/Wine용 [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)입니다. 다섯 파일이 있는 `LauSetup/` 폴더를 추출하세요. Windows에서는 `LauSetup.exe`를 열고 Linux/Wine에서는 `LauSetup.sh`를 실행합니다. 아래의 별도 EXE 또는 Wine ZIP 관련 이전 안내는 1.3.0에 적용되지 않습니다.
>
> **1.3.0:** 인식된 추가 업그레이드 파일은 자동으로 백업되고 설치가 계속됩니다. 복원하면 파일이 원래 위치로 돌아갑니다. 직접 옮길 필요가 없습니다.

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 자동 번역. [영어 출처](../../../CONTRIBUTING.md). 표현이 다를 경우 영어 출처가 권위가 있습니다.

<a id="contributing-to-lau-setup"></a>

# Lau Setup에 기여



Wrath 커뮤니티의 설치 및 복구 개선에 도움을 주셔서 감사합니다.

<a id="community-roadmap"></a>

## 커뮤니티 로드맵

[커뮤니티 로드맵](https://github.com/users/CRSD-Lau/projects/2)에 따라 작업을 문제로 확인하고 끌어오기 요청은 **백로그**, **준비**, **진행 중**, **테스트 중** 및 **완료**를 통해 보드에 자동으로 피드됩니다. **테스트** 카드에는 승인 체크리스트가 포함되어 있으며 검증을 완료하는 데 필요한 증거를 수집합니다. 이슈를 제출하기 전에 [아이디어](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas)를 사용하여 제안을 논의하세요. [릴리스 노트](https://github.com/CRSD-Lau/Lau-Setup/releases)는 각 버전에 제공된 내용에 대한 권한을 유지합니다.

<a id="report-a-problem"></a>

## 문제 신고

[버그 신고 양식](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose)을 사용하세요. 설치 프로그램 버전, 플랫폼, 클라이언트 로캘, 선택한 시각적 개체, 예상되는 동작 및 재현 단계를 포함합니다. 게임 내 문제의 경우 `/pyversion`, 보스 또는 능력, 난이도 및 스크린샷을 포함하세요. Wine 보고서에는 Wine 및 Wine Mono 버전이 포함되어야 합니다.

스크린샷이나 발췌문에서 계정 이름, 비밀번호, 토큰, 개인 경로를 제거하세요. 클라이언트, WTF 폴더, SavedVariables 또는 전체 로그를 업로드하지 마십시오. 복구가 보류 중인 경우 로컬 백업을 유지하십시오.

<a id="propose-a-change"></a>

## 변경 제안

[알려진 제한 사항 및 가정](KNOWN-LIMITATIONS.md)부터 시작하세요. 권장사항은 [아이디어](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas)를 사용하세요. 구현을 제안하기 전에 서버, 네이티브 코드 또는 보호 작업 종속성을 식별합니다.

끌어오기 요청에 집중하세요. 사용자에게 보이는 문제, 변경 사항 및 실행한 점검 사항을 설명하십시오. 활성 개인 게임 클라이언트가 아닌 격리된 장치에서만 파일 작업을 테스트하십시오.

아카이브 허용 목록, 해시 검사, 백업 저널, 프로세스 검사 및 교차 접두사 잠금을 유지합니다. 문서화 또는 인터페이스 업데이트의 일부로 게임 페이로드 기록을 변경하지 마십시오.

[기술 참조](docs/TECHNICAL.md)에서는 공개 빌드와 비공개 로컬 고정 장치가 필요한 테스트에 대해 설명합니다. PR에서 성공적인 빌드, 고정 장치 테스트 및 실제 게임 내 검증을 명확하게 구분하세요.

<a id="artwork-and-attribution"></a>

## 작품 및 저작자 표시

확립된 W-and-shield 브랜딩과 업스트림 크레딧을 그대로 유지하세요. 제안된 작품에 대한 출처와 관련 권한을 포함하세요. 개인 클라이언트 상태를 공용 자산에 도입하지 마십시오.

<a id="dbc-release-records"></a>

## DBC 출시 기록

모든 게임 또는 설치 프로그램 릴리스는 [DBC-CHANGELOG.md](DBC-CHANGELOG.md)를 업데이트하고 GitHub 릴리스 노트에 **DBC 변경 사항** 섹션을 포함해야 합니다. 실제 DBC 편집의 경우 목록 테이블, 레코드 ID, 명명된 필드 및 0부터 시작하는 인덱스, 이전/새 값, 영향을 받은 버전/로캘 및 이유와 이전/이후 해시 및 비교 증거가 포함됩니다. 변경되지 않은 DBC의 경우 **DBC 편집 없음**을 명시적으로 기록합니다. DBC 변경 사항에서 지오메트리, 텍스처 및 설치 프로그램 편집을 분리합니다. 필요한 형식과 검증 경계는 변경 로그를 참조하세요.

<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 자동 번역. [영어 출처](../../../README.md). 표현이 다를 경우 영어 출처가 권위가 있습니다.

<p align="center">
  <a href="https://wrath-multilingual-hd.vercel.app/"><img src="../../assets/social-preview.png" alt="Wrath HD — gold W shield on an icy blue background" width="100%" /></a>
</p>

<h1 align="center">Lau Setup</h1>
<p align="center"><strong>귀하의 고객. 귀하의 언어. 귀하의 Wrath.</strong><br />Lau 비주얼 업그레이드용 Windows 및 Linux/Wine 설치 프로그램.</p>
<p align="center">
  <a href="https://github.com/CRSD-Lau/Lau-Setup/releases/latest">최신 릴리스</a> ·
  <a href="https://wrath-multilingual-hd.vercel.app/">웹사이트 & 갤러리</a> ·
  <a href="https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose">문제 신고</a>
</p>

---

**WoW 3.3.5a, 빌드 12340**용 다국어 철자 텍스트, 와이드스크린 로딩 아트워크, 맞춤형 지면 표시기 및 선택적 HD 지도. 기존 클라이언트와 영상을 선택하세요. Lau Setup는 필요한 파일을 다운로드하고 확인한 후 패치를 배치하고 원본을 백업합니다.

**설치 프로그램 1.1.7 · 게임 출시 3.0.8 Lau · 9개 클라이언트 언어**

<a id="patch-s-stays-recoverable"></a>

## Patch-S는 복구 가능한 상태로 유지됩니다.

**1.1.7 핫픽스 설정:** 새 주문 시각적 개체를 다시 활성화하면 일치하는 비활성화된 Patch-S를 재사용하고 비활성화된 일반 복사본을 `LauSetupBackups`로 이동하므로 데이터는 활성/비활성화된 복제본을 유지하지 않습니다. 트랜잭션 백업에는 다양한 복사본이 보존됩니다. 끄면 여전히 `.mpq.disabled`가 사용됩니다. 복구하려면 **이전 설치 복원**을 사용하세요.

<a id="90-breath-and-slime-spray-warnings"></a>

## 90° 호흡 및 슬라임 스프레이 경고

**3.0.8 Lau:** 지원되는 모든 호흡 표시기와 Rotface Slime 스프레이는 Warmane 테스터 확인에 따라 **90° 총**입니다. Saviana Ragefire, Sartharion, ICC Rimefang 및 Sindragosa의 두 영역 모두에서 Halion을 다루고 있습니다. 범위와 애니메이션 타이밍이 유지됩니다. 승인된 더 큰 Halion 유성 발사 반경과 하늘색 Coldflame은 변경되지 않았습니다.

**이미 설치되었습니까?** 먼저 **Setup 1.1.7**를 다운로드하고 동일한 폴더와 비주얼을 선택한 다음 설치하십시오. 설치 프로그램은 실제 SHA-256 해시를 확인합니다. 크기와 타임스탬프가 동일한 1바이트 변경도 감지됩니다. 일치하는 새 파일만 이미 설치된 것으로 간주됩니다. `/pyversion`는 **3.0.8 Lau**를 보고합니다. 이전 설치 프로그램은 이전에 포함된 카탈로그를 유지합니다.

[애니메이션 색상 미리보기 및 변경 로그](https://wrath-multilingual-hd.vercel.app/#changelog)

<a id="download"></a>

## 다운로드

| Windows | Linux / Wine |
| :--- | :--- |
| **[LauSetup.exe 다운로드](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.exe)** | **[LauSetup-Wine.zip 다운로드](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup-Wine.zip)** |
| Windows 10 / 11 · .NET 프레임워크 4.8 | Wine 11.0 · Wine Mono 10.4.1 · 64-bit 접두사 |
| **156 KB** 정보 | **80 KB** 정보 · Python 3.9+ |
| [Windows 가이드](START-HERE.md) | [Wine 가이드 및 전제 조건](wine/README.md) |

설정 중에 게임 파일이 다운로드됩니다. 영어 코어 설치는 HD 모델과 새로운 주문 영상이 포함된 **472 MB** 또는 원본 모델이 포함된 **259 MB** 정도입니다. 선택적 지도는 더 큰 다운로드를 추가합니다. setup은 설치하기 전의 전체 내용을 보여줍니다.

[SHA-256 체크섬](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/SHA256SUMS.txt) · [릴리스 노트](https://github.com/CRSD-Lau/Lau-Setup/releases/latest) · [검증 보고서](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/VALIDATION.json)

> **기존 클라이언트를 가져오세요.** 이는 전체 게임 클라이언트, 언어 팩 또는 HD 모델 기반이 아닌 업그레이드입니다. 런타임 설치 프로그램은 번들로 제공되지 않습니다. 설치 프로그램 UI는 영어입니다. 게임 콘텐츠는 9개의 로케일을 지원합니다.

<a id="one-setup-the-details-handled"></a>

## 하나의 설정. 세부 사항을 처리했습니다.

| 영상을 선택하세요 | 설치를 지속적으로 제어하세요 |
| :--- | :--- |
| 강화 또는 재고 봉헌 | 클라이언트 언어 및 모델 감지 |
| 호환되는 HD 클라이언트를 위한 새로운 주문 시각 효과 | 필수 파일만 다운로드됨 |
| 선택적인 HD 맵 및 미니맵 텍스처 | 설치 전 SHA-256 확인 |
| 지역 와이드스크린 로딩 아트워크 | 자동 백업 및 재개 가능한 다운로드 |
| 현지화된 주문 이름, 순위 및 툴팁 | 복원 및 중단된 작업 복구 |

<p align="center"><img src="../../assets/installer-windows.png" alt="Lau Setup on Windows: choose a WoW folder, select visuals, install or restore" width="836" /></p>

애드온, SavedVariables, 글꼴, 로그인 아트워크, 영역 설정 및 관련 없는 패치는 그대로 유지됩니다. 개인 UI, 자격 증명 또는 분석은 포함되지 않습니다.

<a id="get-started"></a>

## 시작하기

1. **WoW를 완전히 닫습니다.** Wine에서 모든 접두사에 걸쳐 모든 WoW 인스턴스를 닫습니다.
2. **설정을 실행하고 클라이언트 폴더를 선택하세요.** Windows: `LauSetup.exe`를 엽니다. Linux: Wine ZIP에서 4개 파일을 모두 추출하고 아래 실행기를 사용합니다.
3. **영상을 선택하고 설치하세요.** 강화된 봉헌이 선택되어 시작됩니다. 재고 모양을 확인하려면 선택을 취소하세요. 새로운 주문 비주얼에는 호환되는 HD 모델 기반이 필요합니다. 지도는 선택사항입니다.
4. **WoW를 실행하고 `/pyversion`를 실행하세요.** 게임을 시작하기 전에 설치된 버전을 확인하세요.

Linux에서는 추출된 폴더에서 기존 접두사를 사용하여 다음을 실행합니다.

```sh
WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh
```

일반 사용자로 런처를 사용하세요. Linux 경로, 실행 중인 게임, 여유 공간 및 접두사 전체의 설치 프로그램 잠금을 확인합니다. 로컬 Linux 스토리지를 사용하십시오. 연결된 폴더, 네트워크 공유 및 Windows 탑재 드라이브는 지원되지 않습니다. [Wine 가이드](wine/README.md)에는 글꼴과 모든 필수 구성 요소가 나열되어 있습니다.

Windows에서 런타임이 누락된 경우 설치 프로그램은 Microsoft의 공식 .NET Framework 4.8 다운로드 페이지를 제공합니다. 테스트된 Wine 구성은 Windows .NET 설치 프로그램이 아닌 **Wine Mono**를 사용합니다.

<a id="nine-client-languages"></a>

## 9가지 클라이언트 언어

영어 · Français · Deutsch · 한국어 · Русский · 简体中文 · 繁體中文 · Español(에스파냐) · Español(멕시코)

`enUS` · `frFR` · `deDE` · `koKR` · `ruRU` · `zhCN` · `zhTW` · `esES` · `esMX`

설치는 클라이언트의 활성 로케일을 따릅니다. 구성을 변경하기 전에 적절한 언어 파일과 글꼴을 설치하십시오. 구성 값만 변경하면 언어 팩이 설치되지 않습니다.

<a id="restore-with-your-backups"></a>

## 백업으로 복원

WoW를 닫고, 동일한 실행기를 통해 설정을 다시 열고, 동일한 클라이언트를 선택한 다음 **이전 설치 복원**을 선택하세요. `LauSetupBackups`를 클라이언트 폴더 안에 보관하세요. 여기에는 원본과 복구 기록이 포함되어 있습니다.

`WoW.exe`가 일시적으로 누락된 경우에도 중단된 설치 또는 복원을 복구할 수 있습니다. 다른 업데이트가 설치된 파일을 변경한 경우 복원이 중지되고 해결을 위해 백업이 보존됩니다. 이 설치 프로그램이 지도 업그레이드를 추가하면 버전 변경 중에도 이를 유지합니다. 업그레이드를 취소하려면 이전 설치를 복원하세요.

<a id="tested-with-clear-limits"></a>

## 테스트되었으며 명확한 한계가 있음

릴리스 1.1.7는 플랫폼별 108 로케일/에디션/맵 계획을 포함하여 Windows 및 Wine**에 대한 **50 회귀 그룹을 통과했습니다. 게임 출시 3.0.8는 이전에 두 플랫폼 모두에서 6개 에디션 업그레이드와 1바이트 감지를 통과했습니다. 페이로드는 변경되지 않습니다. 설정 1.1.7는 또한 오래된 비활성화된 복사본, 반복된 스위치 및 정확한 롤백을 통해 모든 플래그 온에서 새로운 주문 오프 시퀀스를 다룹니다. 공개 페이로드는 익명으로 다운로드되었으며 해시 검증되었습니다. 실제 코어 설치 및 롤백이 테스트되었습니다.

Wine는 일반 사용자로서 제공된 런처를 포함하여 로컬 Linux 스토리지에서 **Wine 11.0 / Wine Mono 10.4.1**로 테스트되었습니다. Halion 유성불 기하학은 테스터가 승인한 v2와 정확히 일치합니다. Coldflame, 애니메이션 트랙, 기본 화재 및 주문 테이블은 3.0.7와 바이트 동일하게 유지됩니다. 웹사이트 애니메이션은 예시적인 모형입니다. 이 테스트는 모든 Linux 배포 또는 게임 내 만남을 인증하지 않습니다.

Lutris, Proton 및 macOS 통합은 이 릴리스 외부에 있습니다. 실행 파일에는 디지털 서명이 없습니다.

<a id="known-limitations-and-feature-requests"></a>

## 알려진 제한 사항 및 기능 요청

기능을 제안하기 전에 [알려진 제한 사항 및 가정](KNOWN-LIMITATIONS.md)을 읽어보세요. Warmane 서버 제어, DLL/네이티브 코드 범위, 보호된 Lua 작업, 표시기 정확도 및 타이밍, DBC 종속성, 플랫폼/복구 제한.

<a id="for-contributors"></a>

## 기여자용

- [빌드, 아카이브 배치 및 복구 설계](docs/TECHNICAL.md)
- [기여 및 버그 신고 안내](CONTRIBUTING.md)
- [구현 검토](REVIEW.md)
- [플랫폼 범위 및 타당성](PLATFORM-FEASIBILITY.md)

게임 페이로드는 GitHub 릴리스를 통해 배포됩니다. 이 저장소에는 설치 프로그램 소스, 카탈로그, 실행 프로그램 및 문서가 포함되어 있습니다. 업그레이드를 설치하기 위해 복제할 필요는 없습니다.

<a id="built-on-community-work"></a>

## 커뮤니티 활동을 기반으로 구축됨

**Andre** — Patch-Y 기준선 · **Loriendal & Trimitor** — HD 클라이언트 기반 · **Project Reforged 기여자** — HD 아트워크 · **Blizzard** — 오리지널 게임, 아트워크 및 현지화된 텍스트 · **Lau** — 접지 표시기, 호환성, 적응, 테스트 및 릴리스 툴링.

[전체 크레딧](https://wrath-multilingual-hd.vercel.app/credits) · [스크린샷 및 설치 도움말](https://wrath-multilingual-hd.vercel.app/)

<sub>비공식 커뮤니티 프로젝트. Blizzard Entertainment와 제휴하거나 승인하지 않습니다. 원본 게임 및 타사 삽화는 해당 소유자의 자산으로 유지됩니다.</sub>

<a id="dbc-change-tracking"></a>

## DBC 변경 추적

개별 테이블/레코드/필드 편집 및 비교 증거는 [DBC 변경 로그](DBC-CHANGELOG.md)를 참조하세요. **3.0.7 → 3.0.8에는 DBC 편집 내용이 없습니다**: 90° 표시기가 업데이트되어 모델 형상이 변경되었습니다. 1.1.5–1.1.7 설정도 DBC 데이터를 변경하지 않고 그대로 둡니다.

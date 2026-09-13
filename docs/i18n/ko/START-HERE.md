<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.2.0** — 하나의 ZIP에 이제 Windows 설치 관리자와 Linux/Wine 실행기가 함께 들어 있습니다. 인터페이스는 열 가지 옵션 중 운영 체제 언어를 자동으로 따르며, 수동 선택은 저장됩니다. 게임 버전 3.0.8과 게임 파일은 변경되지 않습니다. DBC 변경도 없습니다.
>
> Google HTTP 429로 전체 안내서 갱신은 아직 보류 중입니다. 아래 본문은 오래되었을 수 있으므로 현재 영어 원문과 1.2.0 릴리스 노트를 확인하세요. [English](../../../START-HERE.txt) · [1.2.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.2.0)
>
> **현재 다운로드:** Windows와 Linux/Wine용 [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)입니다. 다섯 파일이 있는 `LauSetup/` 폴더를 추출하세요. Windows에서는 `LauSetup.exe`를 열고 Linux/Wine에서는 `LauSetup.sh`를 실행합니다. 아래의 별도 EXE 또는 Wine ZIP 관련 이전 안내는 1.2.0에 적용되지 않습니다.


<!-- BEGINNER-120-STEPS -->
## 처음 시작하기

1. WoW를 완전히 종료하세요.
2. `LauSetup.zip`만 내려받으세요. Windows에서는 마우스 오른쪽 버튼을 눌러 **모두 추출**을 선택하고 `LauSetup`을 연 뒤 `LauSetup.exe`를 두 번 클릭합니다.
3. **폴더 선택…**을 선택하고 `Data`나 런처 폴더가 아닌 `WoW.exe`가 바로 들어 있는 폴더를 고르세요.
4. **인터페이스 언어**는 Setup 텍스트만 바꿉니다. 자동은 시스템 언어를 따르고 선택은 저장되며, 게임의 9개 로케일은 바뀌지 않습니다.
5. **강화된 신성화**은 기본으로 켜져 있습니다. 새 주문 효과에는 감지된 호환 HD 모델이 필요하며 지도/미니맵은 선택 다운로드입니다.
6. **업그레이드 설치**을 선택하고 Setup을 닫지 말고 끝날 때까지 기다리세요. WoW를 시작한 뒤 `/pyversion`을 입력합니다. 복원하려면 WoW를 닫고 같은 폴더를 선택한 뒤 **이전 설치 복원**을 선택하세요.

### Linux/Wine

동일한 ZIP은 기존 64-bit Wine 접두사, Wine 11.0, Wine Mono 10.4.1, Python 3.9+, 문서화된 글꼴 및 로컬 Linux 저장소가 준비된 경우에만 사용하세요. 압축을 풀고 `WINEPREFIX="/path/to/prefix" sh LauSetup.sh`를 실행하세요. Wine에서 EXE를 직접 실행하지 마세요.
<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 자동 번역. [영어 출처](../../../START-HERE.txt). 표현이 다를 경우 영어 출처가 권위가 있습니다.

LAU 설정 — 3.0.8 릴리스

Windows와 Linux/Wine: `LauSetup.zip`을 내려받아 `LauSetup/`을 추출하세요. Windows에서는 `LauSetup/LauSetup.exe`를 열고 Linux/Wine에서는 `LauSetup/LauSetup.sh`를 실행합니다.
Wine에서는 포함된 Linux 실행기를 사용하세요. EXE를 직접 실행하지 마세요.

1. World of Warcraft를 닫습니다.
2. LauSetup.exe를 열고 WoW 폴더를 선택합니다.
3. 시각적 개체를 선택하고 업그레이드 설치를 클릭합니다.

이전 릴리스 또는 테스트 v2에서 업데이트하시겠습니까? 먼저 새 설치 프로그램을 다운로드하세요. 이전 복사본에는 이전 카탈로그가 포함됩니다.
동일한 클라이언트와 시각적 개체를 선택합니다. 파일 해시 검사는 변경된 패치를 감지합니다.
WoW를 시작하고 /pyversion를 입력합니다. 3.0.8 Lau를 보고해야 합니다.

설치 프로그램은 클라이언트 언어와 HD 모델 구성을 감지합니다.
강화된 봉헌이 기본적으로 선택됩니다. 재고 확인을 취소하세요.
외모; 주문 자체는 여전히 작동합니다. 새로운 주문 시각 효과에는 다음이 필요합니다.
기존 호환 HD 모델 클라이언트. 업그레이드된 지도/미니맵은 선택 사항입니다.

기존 WoW 3.3.5a 클라이언트가 필요하고 12340를 Windows 10 또는 11에 빌드해야 합니다.
이 다운로드는 완전한 클라이언트 또는 언어 팩이 아닌 업그레이드입니다.
필요한 호환 WoW.exe가 자동으로 설치됩니다.

수동으로 패치를 복사하거나 이름을 바꿀 필요가 없습니다. 전체를 다운로드하지 마세요
공유 데이터 공개. 앱은 선택에 필요한 파일만 다운로드합니다.

백업 및 재개 가능한 다운로드는 WoW 내부의 LauSetupBackups에 유지됩니다.
폴더, 데이터 외부. 업데이트를 실행 취소하려면 WoW를 닫고 LauSetup.exe를 다시 엽니다.
동일한 폴더를 선택하고 이전 설치 복원을 클릭합니다. 회복도
중단된 업데이트로 인해 WoW.exe가 일시적으로 누락된 경우 작동합니다.

애드온, SavedVariables, 글꼴, 로그인 아트워크, 영역 설정 및
관련되지 않은 패치는 보존됩니다. Pizza Warriors 브랜딩 없음, 개인
ElvUI 설정, LoginUI, 계정 데이터 또는 전체 게임 클라이언트가 번들로 제공됩니다.

다운로드는 GitHub 릴리스에서 제공됩니다. GitHub 계정이 필요하지 않습니다.
다운로드가 중지되면 나중에 다시 시도하세요. 확인된 파일
재사용되고 부분 다운로드가 재개됩니다. 게임 파일은 다음 이후에만 변경됩니다.
필요한 모든 다운로드가 검증을 통과했습니다. 다음과 같은 경우 LauSetupBackups를 유지하세요.
앱에서 복구가 필요하다고 보고합니다.

이 설치 프로그램에는 디지털 서명이 없습니다, 따라서 Windows는 알 수 없는 게시자를 표시할 수 있습니다.
경고. 제공된 체크섬을 사용하여 다운로드를 확인하세요. 그렇지 않다
Windows 보안을 비활성화하거나 Python/PowerShell 도구를 설치해야 합니다.
.NET Framework 4.8 런타임이 필요합니다.

이 설치 프로그램이 지도 업그레이드를 추가하면 설치 중에도 해당 업그레이드가 유지됩니다.
에디션 변경. 지도 설치를 취소하려면 이전 설치 복원을 사용하세요.

크레딧: Andre(Patch-Y 기준선), Loriendal 및 Trimitor(HD 기반),
Project Reforged 기여자(HD 아트워크), Blizzard(원본 아트워크 및
지역화된 텍스트), Lau(적응, 호환성, 표시기, 테스트).

Author / Creator / Last Modified By: Neil Mitchell

1.1.7 설정: 새로운 주문 시각적 효과가 꺼져 있으면 Patch-S가 옆에 .mpq.disabled로 유지됩니다.
원래 경로입니다. 비활성화된 다른 복사본은 덮어쓰지 않습니다.
전체 설치를 취소하려면 이전 설치 복원을 사용하세요. 파일의 경우
이전 설치 버전에서 이미 제거된 경우 해당 백업에서 복구하세요.
다시 설치하기 전에 이전 설치 복원을 사용하세요. LauSetupBackups를 유지하세요.

현재 S 파일은 항상 .mpq.disabled가 됩니다. 노인이 장애인인 경우
복사본이 존재하는 경우 설치 프로그램에서는 먼저 해당 복사본을 `.mpq.disabled.<12-character hash>`로 유지합니다. 수동 이름 바꾸기 없음
옵션을 전환하려면 필요합니다. 수동으로 다시 활성화하려면 제거가 필요합니다.
.disabled 및 다음 해시(WoW가 닫혀 있고 다른 활성 없음)
파일을 덮어쓰는 중입니다. 관리형 롤백을 위해 이전 설치 복원을 사용하세요.

1.1.7 핫픽스: 새 주문 시각적 개체를 활성화하면 일치하는 비활성화된 Patch-S를 다시 다운로드하지 않고도 재사용할 수 있습니다. 일반 비활성화된 복사본은 활성 Patch-S가 이미 일치하는 경우에도 LauSetupBackups의 확인된 트랜잭션 백업으로 이동됩니다. 이전 설치 복원을 통해 다른 버전을 복구할 수 있습니다. 끄면 여전히 .mpq.disabled가 사용됩니다. 기존 해시 접미사 아카이브는 그대로 유지됩니다.

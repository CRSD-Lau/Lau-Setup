<!-- LANGUAGES:START -->
[English](../../../../README.md) · [Deutsch](../../de/README.md) · [Español (España)](../../es-ES/README.md) · [Español (México)](../../es-MX/README.md) · [Français](../../fr/README.md) · [한국어](../README.md) · [Русский](../../ru/README.md) · [简体中文](../../zh-CN/README.md) · [繁體中文](../../zh-TW/README.md) · [Português (Brasil)](../../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — 하나의 ZIP에 이제 Windows 설치 관리자와 Linux/Wine 실행기가 함께 들어 있습니다. 인터페이스는 열 가지 옵션 중 운영 체제 언어를 자동으로 따르며, 수동 선택은 저장됩니다. 게임 버전 3.0.8과 게임 파일은 변경되지 않습니다. DBC 변경도 없습니다.
>
> Google HTTP 429로 전체 안내서 갱신은 아직 보류 중입니다. 아래 본문은 오래되었을 수 있으므로 현재 영어 원문과 1.3.0 릴리스 노트를 확인하세요. [English](../../../../wine/README.txt) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
>
> **현재 다운로드:** Windows와 Linux/Wine용 [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)입니다. 다섯 파일이 있는 `LauSetup/` 폴더를 추출하세요. Windows에서는 `LauSetup.exe`를 열고 Linux/Wine에서는 `LauSetup.sh`를 실행합니다. 아래의 별도 EXE 또는 Wine ZIP 관련 이전 안내는 1.3.0에 적용되지 않습니다.
>
> **1.3.0:** 인식된 추가 업그레이드 파일은 자동으로 백업되고 설치가 계속됩니다. 복원하면 파일이 원래 위치로 돌아갑니다. 직접 옮길 필요가 없습니다.


<!-- BEGINNER-120-STEPS -->
## 처음 시작하기

1. WoW를 완전히 종료하세요.
2. `LauSetup.zip`만 내려받으세요. Windows에서는 마우스 오른쪽 버튼을 눌러 **모두 추출**을 선택하고 `LauSetup`을 연 뒤 `LauSetup.exe`를 두 번 클릭합니다.
3. `LauSetup.zip`을 추출하세요. `LauSetup/`의 다섯 파일을 함께 보관하세요: `LauSetup.exe`, `LauSetup.sh`, `lau_wine.py`, `lau-languages.json`, `README.txt`.
4. **인터페이스 언어**는 Setup 텍스트만 바꿉니다. 자동은 시스템 언어를 따르고 선택은 저장되며, 게임의 9개 로케일은 바뀌지 않습니다.
5. **강화된 신성화**은 기본으로 켜져 있습니다. 새 주문 효과에는 감지된 호환 HD 모델이 필요하며 지도/미니맵은 선택 다운로드입니다.
6. **업그레이드 설치**을 선택하고 Setup을 닫지 말고 끝날 때까지 기다리세요. WoW를 시작한 뒤 `/pyversion`을 입력합니다. 복원하려면 WoW를 닫고 같은 폴더를 선택한 뒤 **이전 설치 복원**을 선택하세요.

### Linux/Wine

동일한 ZIP은 기존 64-bit Wine 접두사, Wine 11.0, Wine Mono 10.4.1, Python 3.9+, 문서화된 글꼴 및 로컬 Linux 저장소가 준비된 경우에만 사용하세요. 압축을 풀고 `WINEPREFIX="/path/to/prefix" sh LauSetup.sh`를 실행하세요. Wine에서 EXE를 직접 실행하지 마세요.
<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 자동 번역. [영어 출처](../../../../wine/README.txt). 표현이 다를 경우 영어 출처가 권위가 있습니다.

Linux의 Wine에 대한 Lau Setup
Author / Creator / Last Modified By: Neil Mitchell

1. 로컬 Linux 파일 시스템에서 기존 WoW 3.3.5a 빌드 12340 클라이언트를 사용합니다.
2. 다른 Wine 접두사의 게임을 포함하여 모든 WoW 인스턴스를 닫습니다.
3. `LauSetup.zip`을 추출하세요. `LauSetup/`의 다섯 파일을 함께 보관하세요: `LauSetup.exe`, `LauSetup.sh`, `lau_wine.py`, `lau-languages.json`, `README.txt`.
4. 추출된 폴더에서 터미널을 열고 다음을 실행합니다.

```sh
WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh
```

5. 기존 게임 폴더를 선택하고 설치하세요. 일반적인 자동 백업
   및 이전 설치 복원 버튼을 사용할 수 있습니다.

이 릴리스의 요구 사항:
- Wine 11.0, 64-bit 접두사 및 Wine Mono 10.4.1가 이미 설치되어 있습니다.
- 호스트 안전 도우미용 Python 3.9 이상(표준 라이브러리에만 해당)
- Liberation Sans 또는 DejaVu Sans 글꼴; 완전한 Wine 글꼴 패키지는 다음을 충족해야 합니다.
  또한 Wine Mono의 자체 기본 컨트롤이 렌더링될 수 있도록 설치됩니다.
- 로컬 Linux 스토리지. 네트워크 공유 및 Windows 장착 드라이브는 제외됩니다.
- 일반적인 호스트 프로세스 가시성. 샌드박스를 통해 이 런처를 실행하지 마세요
  다른 Wine 프로세스를 숨깁니다. sudo/root가 아닌 일반 사용자로 실행하세요.

64-bit 접두사는 32-bit WoW 클라이언트를 포함할 수 있습니다. 이 설치 프로그램은 그렇지 않습니다.
Wine 접두사 생성, 변환 또는 업그레이드, Wine/Mono 설치, 구성
DXVK를 사용하거나 게임 런처를 변경하세요. 배포판의 Wine 설정을 사용하세요.
런타임이 누락된 경우 먼저 지침을 따르세요.

이 테스트된 런타임에 대한 공식 Wine Mono 패키지:
https://github.com/wine-mono/wine-mono/releases/tag/wine-mono-10.4.1

Wine와 함께 Wine Mono 런타임을 사용하세요. Windows .NET Framework 설치 프로그램은 다음과 같습니다.
이 테스트된 Wine Mono 구성에서는 번들로 제공되지 않으며 필요하지 않습니다.

항상 LauSetup.sh를 통해 실행하세요. Wine에서 직접 LauSetup.exe 실행
Linux 도우미 없이는 클라이언트 작업을 거부합니다. 호스트 경로를 확인합니다.
Wine 접두사에서 공유되는 호스트 잠금을 처리하고 보유합니다. 멈추면,
다시 시도하기 전에 런처를 다시 열고 보류 중인 설치를 복원하세요.

설정이 완료될 때까지 WoW를 닫아 두세요. 프로세스 점검으로 경합이 줄어듭니다. 그들은 할 수 없다
다른 프로그램이 게임을 시작하거나 나중에 파일을 변경하는 것을 중지합니다.
심볼릭 링크된 경로, 하드링크 및 모호한 파일 이름 대소문자는 거부됩니다. 데이터
백업 디렉터리는 클라이언트와 동일한 파일 시스템에 남아 있어야 합니다.

검증 범위: 격리된 Wine 11.0 / Wine Mono 10.4.1 클라이언트, 고정 장치 및
실제 페이로드 설치/복원 테스트, 접두사 2개 안전 테스트 및 샘플 GUI
수표. 이는 모든 Linux 배포판, 파일 시스템,
디스플레이 규모, Wine 버전 또는 게임 만남. Lutris, Proton 또는 macOS 없음
이번 릴리스에는 통합이 포함되어 있습니다.

설치 프로그램 인터페이스는 열 가지 옵션 중 운영 체제 언어를 자동으로 따르며 수동 선택은 저장됩니다. 클라이언트 게임 데이터는 계속 9개 로케일을 지원하며 감지된 게임 로케일을 따릅니다.

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

1.1.7 정리 다시 활성화: 일치 비활성화된 Patch-S는 로컬에서 재사용됩니다. 일반 비활성화된 복사본은 LauSetupBackups의 확인된 트랜잭션 백업으로 이동되어 하나의 활성 S가 남습니다. 다른 복사본은 이전 설치 복원을 통해 복구 가능한 상태로 유지됩니다. 기존 해시 접미사 아카이브는 정리되지 않습니다.

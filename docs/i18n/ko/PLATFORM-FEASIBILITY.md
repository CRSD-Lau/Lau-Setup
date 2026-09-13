<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — 하나의 ZIP에 이제 Windows 설치 관리자와 Linux/Wine 실행기가 함께 들어 있습니다. 인터페이스는 열 가지 옵션 중 운영 체제 언어를 자동으로 따르며, 수동 선택은 저장됩니다. 게임 버전 3.0.8과 게임 파일은 변경되지 않습니다. DBC 변경도 없습니다.
>
> Google HTTP 429로 전체 안내서 갱신은 아직 보류 중입니다. 아래 본문은 오래되었을 수 있으므로 현재 영어 원문과 1.3.0 릴리스 노트를 확인하세요. [English](../../../PLATFORM-FEASIBILITY.md) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
>
> **현재 다운로드:** Windows와 Linux/Wine용 [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)입니다. 다섯 파일이 있는 `LauSetup/` 폴더를 추출하세요. Windows에서는 `LauSetup.exe`를 열고 Linux/Wine에서는 `LauSetup.sh`를 실행합니다. 아래의 별도 EXE 또는 Wine ZIP 관련 이전 안내는 1.3.0에 적용되지 않습니다.
>
> **1.3.0:** 인식된 추가 업그레이드 파일은 자동으로 백업되고 설치가 계속됩니다. 복원하면 파일이 원래 위치로 돌아갑니다. 직접 옮길 필요가 없습니다.

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 자동 번역. [영어 출처](../../../PLATFORM-FEASIBILITY.md). 표현이 다를 경우 영어 출처가 권위가 있습니다.

<a id="lau-setup-platform-feasibility"></a>

# Lau Setup 플랫폼 타당성

작성자: Neil Mitchell  
제작자:Neil Mitchell  
최종 수정자: Neil Mitchell  
평가 날짜: 2026-09-11

> **아래는 과거 평가입니다:** 다음 1.0.1/1.1.0 섹션은 당시의 평가 상태를 설명합니다. 하나의 공유 ZIP을 사용하는 현재 설치는 위의 Setup 1.2.0 안내를 따르세요.
업데이트: 사용자가 Wine만 선택했습니다. 설치 프로그램 1.1.0는 이제 테스트된
Wine 11 / Wine Mono 10.4.1 런처는 [Wine 가이드](wine/README.md)에 설명되어 있습니다.
아래의 Wine 8 프로브 및 권장 사항은 기록 평가로 보존됩니다.
Lutris, Proton 및 macOS 통합은 범위를 벗어납니다.

Lau Setup 1.0.1는 Windows 설치 프로그램으로 유지됩니다. Linux부터 Wine까지가 권장되는 다음 호환성 대상입니다. 이 평가는 Linux 또는 macOS에서의 설치를 인증하지 않습니다. 이전 63 Docker/Wine 사례에서는 이 설치 프로그램이 아닌 게임 데이터를 실행했습니다.

| 옵션 | 추천 | Lau Setup의 의미 |
| --- | --- | --- |
| Linux의 Wine | 첫 번째 목표; 원칙적으로 가능하지만 현재 검증되지 않음 | 명시적으로 선택된 Wine 접두사 내에서 Windows 설치 프로그램을 재사용합니다. 지원을 게시하기 전에 런타임, 폴더 선택, 다운로드, 파일 안전 및 복구를 입증하십시오. |
| 루트리스 | 다음으로 직접 Wine를 통과한 후 | 소규모 통합 레시피는 기존 게임의 접두사에서 설정을 시작할 수 있습니다. 별도의 페이로드 형식이 필요하지 않습니다. |
| 증기/양성자 | 나중에 조건부 | 올바른 기존 게임의 접두사를 사용하세요. Steam이 아닌 다른 게임으로 설정을 추가하면 다른 환경이 제공될 수 있습니다. Steam Deck 사용성을 위해서는 별도의 화면과 컨트롤러 확인이 필요합니다. |
| macOS의 CrossOver | 그럴듯한 별도의 테스트 트랙 | 게임의 병 안에서 달려보세요. 실제 macOS 하드웨어 및 지원되는 CrossOver 버전을 검증합니다. Linux 테스트에서는 이를 설정할 수 없습니다. |
| Wine + DXVK | 선택적 게임 구성 | DXVK는 게임의 Direct3D를 변환합니다. 설치 프로그램의 .NET, 글꼴 또는 파일 안전 요구 사항은 해결되지 않습니다. |
| 위스키 | 새로운 지원 대상으로 채택하지 않음 | 해당 업스트림 프로젝트는 더 이상 적극적으로 유지 관리되지 않습니다. |

위의 분류는 [Wine Mono](https://github.com/wine-mono/wine-mono), [Lutris](https://lutris.net/about/), [Proton](https://github.com/ValveSoftware/Proton), [DXVK](https://github.com/doitsujin/dxvk), [CrossOver의 Mac 가이드](https://support.codeweavers.com/en_US/crossover-mac-user-guide) 및 [위스키](https://github.com/Whisky-App/Whisky). 권장사항은 Lau Setup의 업스트림 인증이 아닌 당사의 평가입니다. CrossOver는 64-bit 병에서 32-bit Windows 애플리케이션을 실행할 수 있습니다. 기본 macOS 32-bit 지원 손실만으로는 이를 배제할 수 없습니다.

<a id="bounded-probe-results"></a>

## 제한된 프로브 결과

로컬 프로브는 격리된 win32 접두사인 Wine 8.0(Debian 8.0~repack-4)와 Xvfb를 사용했습니다. 로컬에서 사용 가능한 이 오래된 런타임은 현재 Wine 릴리스에 대한 테스트가 아닙니다. 개인 게임 클라이언트가 탑재되거나 수정되지 않았습니다.

1. 상속된 게임 테스트 이미지가 mscoree를 비활성화했습니다. 이를 활성화하면 Wine Mono가 누락된 것으로 나타났습니다. 이는 테스트 환경 문제였습니다.
2. [Wine 8.0 소스](https://raw.githubusercontent.com/wine-mirror/wine/wine-8.0/dlls/appwiz.cpl/addons.c)에 의해 고정된 SHA-256 `6413ff328ebbf7ec7689c648feb3546d8102ded865079d1fbf0331b14b3ab0ec`를 확인한 후 일회용 접두사에 공식 Wine Mono 7.4.0 MSI를 설치했습니다.
3. 진단 하네스가 WinForms를 초기화하고 포함된 카탈로그를 로드한 후 `System.ArgumentException: The requested FontFamily could not be found [GDI+ status: FontFamilyNotFound]`를 사용하여 양식을 구성하는 데 실패했습니다. 사용 가능한 Liberation 글꼴을 해당 접두사에 복사해도 문제가 해결되지 않았습니다. 성공적인 설치 프로그램 스크린샷이나 설치 결과가 없습니다.
4. 지역 증거는 `reports/wine-feasibility/`에 따라 유지됩니다. 프로브 컨테이너가 중지되었습니다. 진단 하네스는 분산 설치 프로그램이나 공개 소스 번들에 포함되어 있지 않습니다.

이는 Wine가 불가능하다는 증거가 아니라 런타임/글꼴 프로비저닝 작업을 식별합니다. 이 프로브의 Wine에서 설치/복원 트랜잭션이 시도되지 않았습니다.

<a id="acceptance-work-before-wine-support"></a>

## Wine 지원 전 승인 작업

1. Linux 데스크탑에서 재현 가능한 현재 Wine/런타임/글꼴 조합을 설정합니다. 일반적인 디스플레이 규모로 초기, 준비, 다운로드, 복구 및 오류 상태를 표시합니다. 키보드 액세스 및 폴더 선택을 확인합니다.
2. 대소문자만 다른 중복 이름을 포함하여 대소문자 구분 파일 시스템에서 정확한 호스트 폴더 매핑 및 대소문자 처리를 확인합니다. 관련 없는 패치와 개인 설정을 보존합니다.
3. 링크, 배타적 잠금, 여유 공간, 저널 및 원자 대체 동작을 증명합니다. 설치 프로그램은 현재 Windows 파일 정보 API를 호출합니다. 해당 의미는 가정하기보다는 Wine에서 테스트되어야 합니다.
4. 접두사 전반에 걸쳐 실행중인 게임 가드를 입증하십시오. 현재 코드는 Windows 프로세스를 열거하고 실행 가능한 디렉터리를 비교합니다. Wine 접두사 표시 여부에 따라 동일한 클라이언트를 실행하는 다른 접두사가 감지되지 않을 수 있습니다. 안전한 설치 지원을 제공하기 전에 이 문제를 해결하십시오. 성공적인 동일 접두사 테스트만으로는 충분하지 않습니다.
5. 고정 장치 설치/복원 및 중단된 복구 매트릭스를 실행한 다음 정확한 릴리스 자산을 사용하여 하나의 깨끗한 익명 GitHub 다운로드/설치/롤백을 실행합니다. TLS, 리디렉션, 재개, 취소 및 오프라인 복구를 테스트합니다.
6. 동일한 지원 환경에서 게임 내 검사를 진행하세요. 그런 다음에만 Wine 지침과 Lutris 통합을 게시하세요. Proton과 macOS는 자체 검사가 통과될 때까지 명시적으로 확인되지 않은 상태로 유지됩니다.

GitHub 릴리스에 불변의 게임 자산 세트 하나를 유지하세요. 다른 실행 프로그램을 활성화하기 위해 전체 클라이언트, 개인 UI 또는 모든 페이로드의 복사본을 Git 저장소에 추가하지 마세요. Wine가 안전 검사를 안정적으로 충족할 수 없는 경우 별도의 구현으로 동일한 매니페스트 및 트랜잭션 규칙을 중심으로 기본 Linux 설치 프로그램을 평가합니다.

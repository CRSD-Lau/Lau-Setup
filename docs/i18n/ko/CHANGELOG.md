<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

<!-- STABLE-140-CURRENT-GUIDE -->
> **현재 버전: Setup 1.4.0 / 게임 3.0.9 Lau.** WoW를 종료하고 LauSetup.zip 전체를 압축 해제한 뒤 Windows에서 LauSetup.exe를 여세요. Browse...로 WoW.exe가 있는 폴더를 선택하세요. 다음 → 시각 효과 → 다음 → 검토 → 설치 → 완료 순서입니다. 추가 옵션은 처음에 모두 꺼져 있습니다. WoW.exe와 로딩 화면은 하나의 옵션이며, 지도는 독립적이고 WDM 지원 파일을 포함합니다. 이미 설치된 지도는 유지됩니다. 이름을 바꾼 중복 패치는 그대로 남고, 빈 Patch-V만 자동 백업됩니다. 교체된 파일은 LauSetupBackups에 보관됩니다. Patch-Y의 DBC는 바뀌지 않았지만 선택 지도에는 문서화된 원본 프로젝트의 테이블이 추가됩니다. 동굴 지도는 베타입니다. Linux/Wine에서는 안내된 환경에서 LauSetup.sh를 사용하세요. Google HTTP 429로 전체 번역 갱신이 막혀 있습니다. 아래 예전 내용은 과거 참고용이며 현재 지침은 영어 원문을 확인하세요.
>
> [English](../../../CHANGELOG.md) · [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 자동 번역. [영어 출처](../../../CHANGELOG.md). 표현이 다를 경우 영어 출처가 권위가 있습니다.

<a id="lau-setup-116-hotfix---switch-options-with-existing-disabled-patch-s"></a>

# Lau Setup 1.1.6 핫픽스 - 기존 비활성화된 스위치 옵션 Patch-S

이전 설치 후 새 주문 시각 효과를 끌 때 "다른 비활성화된 Patch-S가 이미 존재합니다"라는 1.1.5 메시지를 수정합니다.

설치 프로그램에서는 두 파일을 모두 자동으로 유지합니다. 현재 S 파일은 항상 `.mpq.disabled`가 됩니다. 비활성화된 다른 이전 복사본이 이미 있는 경우 설치 프로그램에서는 먼저 해당 이전 복사본을 `.mpq.disabled.<12-character hash>`로 유지합니다. 동일한 저장된 사본이 재사용됩니다. 두 버전 모두 유지됩니다. 보존 중인 이전 파일과 내용이 일치하지 않는 해시 이름의 복사본은 여전히 ​​검사 작업을 중지합니다.

이는 **세 개의 플래그 모두 켜기 -> 새 주문 시각적 표시 끄기**, 반복되는 스위치 및 롤백 시퀀스를 포함하여 루트 및 활성 로케일 S 파일에 적용됩니다. 지도 선택이 유지됩니다.

새 EXE 또는 Wine ZIP을 다운로드하고 선택을 다시 시도하세요. 1.1.5에 표시된 일반적인 충돌을 해결하기 위해 기존 비활성화된 복사본을 삭제하거나 이름을 바꿀 필요가 없습니다.

전체 설치를 취소하려면 **이전 설치 복원**을 사용하세요. 저장된 S 파일을 수동으로 다시 활성화하려면 WoW를 닫고 `.disabled` 및 다음 해시를 제거하여 원래 `.mpq` 파일 이름을 복원합니다. 다른 활성 파일을 덮어쓰지 마십시오. 수동 변경으로 인해 파일 드리프트 시 관리되는 롤백이 중지될 수 있습니다. 백업을 유지하세요. 1.1.5 이전에 설치 프로그램이 제거한 파일은 여전히 ​​백업을 통해 복구해야 합니다.

게임 출시는 **3.0.8 Lau**로 유지되며 모든 게임 페이로드는 변경되지 않습니다. 모든 90급 원뿔, 유성 발사 반경 및 Coldflame이 보존됩니다.

Windows 및 Wine 검사에는 46 회귀 그룹, 9개 로케일 모두, 기존 비활성화된 파일, 반복되는 켜기/끄기 스위치, 변조된 복사 방지, 중단 복구 및 정확한 롤백이 포함됩니다. 새로운 공개 다운로드는 실제 On/Off 릴리스 파일과 이전의 비활성화된 복사본을 사용하여 테스트되었습니다. 이는 새로운 게임 내 확인이 아닌 설치 프로그램 확인입니다.

[Raw 6판 Patch-Y ZIP](https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.1.4/Lau-Patch-Y-3.0.8-All-Editions.zip)

[설치 도움말 및 변경 로그](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-115-hotfix---keep-disabled-patch-s-files"></a>

# Lau Setup 1.1.5 핫픽스 - 비활성화된 Patch-S 파일 유지

**새 주문 시각적 요소**를 끄면 이제 루트 및 활성 로케일 Patch-S 파일이 설치 프로그램 백업에만 남아 있는 것이 아니라 원래 위치인 `.mpq.disabled` 옆에 보존됩니다. 해당 바이트는 변경 전후에 확인됩니다. WoW는 비활성화된 파일 이름을 로드하지 않습니다.

- 다른 기존 `.disabled` 복사본으로 인해 설치가 차단됩니다. 절대 덮어쓰지 않습니다.
- 동일한 비활성화된 복사본이 재사용되고 보존됩니다.
- 옵션을 켜면 선택한 릴리스의 활성 S 파일이 설치되고 비활성화된 복사본이 유지됩니다.
- 반복 설치, 롤백 및 중단 복구에는 활성 경로와 비활성화된 경로가 모두 포함됩니다.

비활성화된 파일을 수동으로 다시 활성화하려면 WoW를 닫고 `.disabled` 접미사만 제거하세요. 다른 활성 파일을 덮어쓰지 마십시오. 전체 Lau 설치를 실행 취소하려면 **이전 설치 복원**을 사용하세요. Patch-Y만 삭제해도 Q/M/실행 파일 또는 기타 변경 사항이 실행 취소되지 않습니다. 수동으로 파일을 변경하면 드리프트 시 관리형 롤백이 중지될 수 있으므로 백업을 보관하세요.

**이전 설치 프로그램의 영향을 이미 받았습니까?** 이 업데이트는 이전 백업을 자동으로 추출하지 않습니다. 새 설정으로 다시 설치하기 전에 이전 설치 복원을 사용하여 해당 파일을 복구하고 누적 설치를 통해 역방향으로 작업하세요. LauSetupBackups를 유지하세요.

게임 출시는 **3.0.8 Lau**로 유지됩니다. 모든 MPQ는 변경되지 않았습니다. 90급 호흡/슬라임 스프레이, 승인된 +50% Halion 유성불 반경 및 Coldflame이 보존됩니다. 설치 프로그램 수정을 위해 새 EXE 또는 Wine ZIP을 다운로드하세요.

Windows 및 Wine 검증은 VALIDATION.json에 포함되어 있습니다. 테스트는 9개 로케일, 복사 비활성화 충돌, 켜기/끄기 전환, 반복 설치, 모든 이동/복원 단계의 중단, 파일 드리프트 및 정확한 롤백을 모두 포함합니다. 수정 사항은 새로운 게임 내 만남 확인을 요구하지 않습니다.

[원시 6판 Patch-Y ZIP(변경되지 않은 3.0.8)](https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.1.4/Lau-Patch-Y-3.0.8-All-Editions.zip)

[설치 도움말 및 변경 로그](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-114--game-release-308-lau"></a>

# Lau Setup 1.1.4 · 게임 출시 3.0.8 Lau

<a id="117-hotfix---patch-s-re-enable-cleanup"></a>

## 1.1.7 핫픽스 - Patch-S 정리를 다시 활성화

- 새로운 주문 시각적 요소를 다시 활성화하면 SHA-256 및 크기가 선택한 릴리스와 일치할 때 비활성화된 Patch-S를 재사용하여 다운로드를 방지합니다.
- 활성 Patch-S가 이미 일치하더라도 일반 비활성화된 복사본은 데이터 외부의 확인된 트랜잭션 백업으로 이동합니다. 비활성화된 다른 파일은 이전 설치 복원을 통해 복구 가능한 상태로 유지됩니다.
- 루트 및 활성 로케일 Patch-S에 적용됩니다. Off에서는 여전히 일반 `.mpq.disabled` 파일 이름을 사용합니다. 기존 해시 접미사 아카이브는 그대로 유지됩니다.
- 게임 페이로드는 3.0.8 Lau로 유지됩니다. Windows 및 Wine는 각각 50 회귀 그룹, 실제 파일 켜기/끄기/켜기 전환 및 정확한 롤백을 통과했습니다.

<a id="all-breath-and-slime-spray-warnings-are-now-90"></a>

## 모든 호흡 및 슬라임 스프레이 경고는 이제 90°입니다.

Warmane 테스터 확인에 따라 Halion(두 영역 모두), Saviana Ragefire, Sartharion, ICC Rimefang 및 Rotface Slime 스프레이는 이제 Sindragosa의 기존 90° 경고와 일치하는 **90° 총 원뿔**을 사용합니다. 이는 기존 일반/영웅 주문 매핑을 포함하여 6개 에디션과 9개 클라이언트 언어 모두에 적용됩니다.

원뿔 너비만 변경됩니다. 범위, 애니메이션 타이밍, 기본 주문 효과 및 주문 테이블이 보존됩니다. 승인된 50% 더 큰 Halion 유성불 반경, 하늘색 Coldflame, 색상 및 축성은 변경되지 않았습니다. 이는 시각적 경고 버퍼입니다. 서버 손상 및 메커니즘은 변경되지 않았습니다. 고르지 않은 지형은 여전히 ​​평평한 원뿔을자를 수 있습니다.

<a id="updating"></a>

## 업데이트 중

먼저 이 릴리스에서 **LauSetup.exe** 또는 **LauSetup-Wine.zip**를 다운로드하세요. WoW를 닫고 동일한 클라이언트와 시각적 개체를 선택한 다음 **업그레이드 설치**를 클릭합니다. 이전 설치 프로그램은 이전 카탈로그를 유지합니다. **3.0.8 Lau**에 대해서는 `/pyversion`를 확인하세요.

설치 프로그램은 실제 SHA-256 해시를 확인하므로 이전 릴리스와 크기 및 타임스탬프가 변경되지 않은 1바이트 변경 사항도 감지됩니다. 정확한 현재 파일만 이미 설치된 것으로 간주됩니다. 이전 설치의 백업 및 복원은 계속 사용할 수 있습니다.

Windows에는 .NET Framework 4.8가 필요합니다. Wine 사용자는 4개의 파일을 모두 추출하고 지원되는 기존 Wine/Mono 접두사를 사용하여 일반 사용자로 `LauSetup.sh`를 실행합니다. 런타임 설치 프로그램은 번들로 제공되지 않습니다.

<a id="validation"></a>

## 검증

Windows 및 Wine 회귀, 3.0.7의 6개 버전 업그레이드, 반복 감지, 1바이트 검사, 롤백 및 공개 다운로드 검사에 대해서는 VALIDATION.json를 참조하세요. 형상 검사를 통해 모든 에디션에서 90° 원뿔, 보존된 범위, 유효한 경계 및 삼각형 굴곡을 확인합니다. 정확히 11개의 기존 아카이브 멤버가 변경됩니다. 즉, 5개의 모델, 5개의 스킨 및 버전 TOC가 변경됩니다. 다른 모든 멤버는 3.0.7와 바이트 동일합니다.

너비 결정은 보고된 Warmane 테스트를 따릅니다. 이 릴리스는 모든 경우 또는 정확한 서버 경계 인증이 아닙니다.

[웹사이트 변경 로그 및 설치 도움말](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-113--game-release-307-lau"></a>

# Lau Setup 1.1.3 · 게임 출시 3.0.7 Lau

<a id="larger-halion-meteor-fire-warnings"></a>

## 더 큰 Halion 유성 화재 경고

테스터 승인 **테스트 v2** 촉진: Halion의 빨간색 지상 표시 반경은 트레일 및 착륙 사격 주변에서 릴리스 3.0.6보다 **50% 더 큽니다. 테스트 v3은 포함되지 않습니다. Coldflame, 색상, 애니메이션 트랙, 기본 불꽃, Consecration 및 Sindragosa/Rotface 원뿔은 변경되지 않았습니다. 6개 버전과 9개 클라이언트 언어가 모두 지원됩니다.

테스터는 업데이트되지 않은 패치를 수정한 후 v2를 확인했습니다. 이는 시각적 경고 버퍼이지 서버 손상에 대한 변경이나 모든 위치 또는 조우에 대한 인증이 아닙니다.

<a id="update-with-the-new-installer"></a>

## 새 설치 프로그램으로 업데이트

먼저 이 릴리스에서 **LauSetup.exe** 또는 **LauSetup-Wine.zip**를 다운로드하세요. WoW를 닫고 동일한 클라이언트와 시각적 개체를 선택한 다음 **업그레이드 설치**를 클릭합니다. 이전 설치 프로그램은 이전 카탈로그를 유지합니다. `/pyversion`는 **3.0.7 Lau**를 보고합니다.

기존 3.0.6 및 테스트 v2 사용자는 업데이트를 받습니다. 설치 프로그램에서는 크기와 타임스탬프가 변경되지 않은 1바이트 변경 사항을 포함하여 실제 파일 해시를 비교합니다. 정확한 현재 파일만 이미 설치된 것으로 간주됩니다. 이전 설치의 백업 및 복원은 계속 사용할 수 있습니다.

Windows에는 .NET Framework 4.8가 필요합니다. Wine 사용자는 4개의 파일을 모두 추출하고 지원되는 기존 Wine/Mono 접두사를 사용하여 일반 사용자로 `LauSetup.sh`를 실행합니다. 런타임 설치 프로그램은 번들로 제공되지 않습니다.

<a id="validation-1"></a>

## 검증

Windows 및 Wine 설치 프로그램 회귀, 6개 버전 업그레이드, 반복 감지, 1바이트 확인, 롤백 및 공개 다운로드 확인은 VALIDATION.json에 기록됩니다. Halion 모델과 스킨은 v2를 테스트하는 것과 바이트 동일합니다. 형상/경계 및 TOC 버전만 3.0.6와 다릅니다. Coldflame 및 기타 아카이브 구성원은 변경되지 않습니다.

[웹사이트 변경 로그 및 설치 도움말](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-112--game-release-306-lau"></a>

# Lau Setup 1.1.2 · 게임 출시 3.0.6 Lau

<a id="blue-coldflame-red-meteor-fire"></a>

## 블루 콜드플레임, 레드 유성불

- **Marrowgar Coldflame:** 영웅을 포함하여 기존 내부 빛과 시계 방향 애니메이션이 포함된 연한 파란색 원입니다.
- **할리온 유성 발사:** 기존 시계 방향 애니메이션으로 산책로 주변에 빨간색 원을 발사하고 착지 발사합니다.
- 6개의 HD/비HD 버전과 9개의 클라이언트 언어가 모두 제공됩니다. 기본 불꽃, 지속 시간, 신성화 선택 사항 및 90° Sindragosa / 60° Rotface 원뿔은 변경되지 않았습니다.

[애니메이션 색상 미리보기 및 전체 변경 로그](https://wrath-multilingual-hd.vercel.app/#changelog). 미리보기는 게임 내 녹화가 아닌 예시용 모형입니다. 서버 손상 및 메커니즘은 변경되지 않았습니다. 경고 가장자리는 시각적 버퍼로 유지됩니다.

<a id="already-installed-download-the-new-installer-first"></a>

## 이미 설치되어 있나요? 먼저 새 설치 프로그램을 다운로드하세요.

이번 릴리스에서 **LauSetup.exe** 또는 **LauSetup-Wine.zip**를 다운로드하세요. WoW를 닫고 동일한 폴더와 시각적 설정을 선택한 다음 **업그레이드 설치**를 클릭합니다. 이전에 다운로드한 설치 프로그램은 이전에 포함된 카탈로그를 유지합니다.

설치 프로그램은 실제 파일을 해시합니다. 이전 3.0.5 파일이 교체되었습니다. 파일 크기와 타임스탬프가 동일한 1바이트 변경도 감지됩니다. 완전히 새로운 파일만 이미 설치된 것으로 간주됩니다. `/pyversion`는 **3.0.6 Lau**를 보고합니다. 이전 설치의 백업 및 복원은 계속 사용할 수 있습니다.

Wine 사용자: 4개의 파일을 모두 함께 추출하고 기존 64-bit Wine 11.0 / Mono 10.4.1 접두사를 사용하여 일반 사용자로 `LauSetup.sh`를 실행합니다. Python 3.9+ 및 로컬 Linux 스토리지가 필요합니다. Windows에는 .NET Framework 4.8가 필요합니다. 런타임은 번들로 제공되지 않습니다.

<a id="fresh-verification-on-windows-and-wine"></a>

## Windows 및 Wine에 대한 새로운 검증

- 108 로케일/에디션/맵 계획을 각각 포함하여 플랫폼당 38 회귀 그룹.
- 실제 3.0.5에서 3.0.6로의 업그레이드 6개 모두, 두 플랫폼 모두에서 무작동 설치 및 정확한 롤백을 반복합니다.
- 두 플랫폼의 루트 및 로케일 Y에서 독립적으로 1바이트 동일 크기/동일 타임스탬프 변경 사항이 감지되고 복구됩니다.
- 익명의 GitHub 페이로드 다운로드, 실제 코어 설치 및 Windows 및 Wine에 대한 롤백.
- 15 Linux 호스트 안전성 테스트 및 일반 사용자의 정확한 4개 파일 Wine 실행기; Windows 양식 렌더링이 확인되었습니다.
- 세 개의 마커 M2 텍스처 참조 및 버전 TOC가 에디션별로 변경되었습니다. 두 가지 색상 텍스처가 추가되었습니다. 다른 모든 멤버는 바이트 단위로 보존됩니다.

이러한 설치 프로그램 검사는 모든 Linux 배포 또는 모든 게임 내 발생을 인증하지 않습니다. 실행 파일에는 디지털 서명이 없습니다. 자세한 증거, 체크섬 및 소스가 첨부되어 있습니다.

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-111--game-release-305-lau"></a>

# Lau Setup 1.1.1 · 게임 출시 3.0.5 Lau

<a id="wider-raid-warnings"></a>

## 더 폭넓은 공격 경고

- 신드라고사 프로스트 브레스: **75° → 90° 총계** (측면당 7.5° 추가).
- 로트페이스 슬라임 스프레이: **25° → 60° 총계** (측면당 17.5° 추가).
- 6개 HD/비HD 에디션 모두에 적용되며 9개 클라이언트 로케일 모두에서 사용 가능합니다. 기타 표시기, 축성 설정, 현지화된 표 및 삽화는 변경되지 않습니다.

이는 Warmane 습격 영상과 주문 적중 기록을 통해 알려주는 버퍼링된 시각적 경고입니다. 서버 손상이나 메커니즘을 변경하거나 정확한 손상 경계를 주장하지 않습니다.

<a id="updating-an-existing-installation"></a>

## 기존 설치 업데이트

새로운 **LauSetup.exe** 또는 **LauSetup-Wine.zip**를 먼저 다운로드하세요. WoW를 닫고 동일한 폴더와 시각적 선택 항목을 선택한 다음 **업그레이드 설치**를 클릭합니다. 설치 프로그램은 실제 파일 해시를 비교합니다. 이전 3.0.4 패치는 교체되고 정확한 3.0.5 설치는 이미 설치된 것으로 보고됩니다. `/pyversion`는 업데이트 후 **3.0.5 Lau**를 보고합니다. 이전에 다운로드한 설치 프로그램은 이전 카탈로그를 유지합니다.

Windows 및 Wine 다운로드에는 동일한 재구축된 설정 실행 파일이 포함되어 있습니다. Wine의 경우 4개의 파일을 모두 함께 추출하고 포함된 README에 설명된 대로 `LauSetup.sh`를 사용합니다. 기존 런타임 요구 사항은 변경되지 않습니다.

<a id="verification"></a>

## 확인

108 로캘/에디션/맵 계획을 포함하여 모든 38 Windows 회귀 그룹이 통과되었습니다. 6개 에디션 모두 실제 3.0.4에서 3.0.5로의 업그레이드, 반복 설치 및 정확한 롤백 검사를 통과했습니다. 새로운 페이로드는 익명 다운로드/해시 검사를 통과했습니다. GitHub에서 격리된 코어 설치 및 롤백이 통과되었습니다. 각 버전은 4개의 모델/형상 파일과 버전 TOC를 제외한 모든 멤버를 유지합니다.

Wine 실행기 코드는 변경되지 않았으며 ZIP에는 정확하게 재구축된 EXE가 포함되어 있습니다. 이전 Wine 11.0 / Mono 10.4.1 런타임 증거가 유지됩니다. Docker 엔진이 시작되지 않아 새로운 Wine 실행을 사용할 수 없습니다. 새로운 원뿔 형상은 게임 내에서 새로 인증되지 않고 정적으로 검증되었습니다.

다운로드 체크섬, 소스 및 자세한 검증 보고서가 첨부되어 있습니다. 복구를 위해 `LauSetupBackups`를 유지하세요.

Author / Creator / Last Modified By: Neil Mitchell

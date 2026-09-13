<!-- LANGUAGES:START -->
[English](../../../../../../README.md) · [Deutsch](../../../../de/README.md) · [Español (España)](../../../../es-ES/README.md) · [Español (México)](../../../../es-MX/README.md) · [Français](../../../../fr/README.md) · [한국어](../../../README.md) · [Русский](../../../../ru/README.md) · [简体中文](../../../../zh-CN/README.md) · [繁體中文](../../../../zh-TW/README.md) · [Português (Brasil)](../../../../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.2.0** — 하나의 ZIP에 이제 Windows 설치 관리자와 Linux/Wine 실행기가 함께 들어 있습니다. 인터페이스는 열 가지 옵션 중 운영 체제 언어를 자동으로 따르며, 수동 선택은 저장됩니다. 게임 버전 3.0.8과 게임 파일은 변경되지 않습니다. DBC 변경도 없습니다.
>
> Google HTTP 429로 전체 안내서 갱신은 아직 보류 중입니다. 아래 본문은 오래되었을 수 있으므로 현재 영어 원문과 1.2.0 릴리스 노트를 확인하세요. [English](../../../../../dbc/history/INDIVIDUAL-EDITS.md) · [1.2.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.2.0)
>
> **현재 다운로드:** Windows와 Linux/Wine용 [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)입니다. 다섯 파일이 있는 `LauSetup/` 폴더를 추출하세요. Windows에서는 `LauSetup.exe`를 열고 Linux/Wine에서는 `LauSetup.sh`를 실행합니다. 아래의 별도 EXE 또는 Wine ZIP 관련 이전 안내는 1.2.0에 적용되지 않습니다.

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 자동 번역. [영어 출처](../../../../../dbc/history/INDIVIDUAL-EDITS.md). 표현이 다를 경우 영어 출처가 권위가 있습니다.

<a id="individual-patch-y-dbc-edits-andre-baseline-to-retained-multilingual-lau-build"></a>

# 개별 Patch-Y DBC 편집: 다국어 Lau 빌드를 유지하기 위한 Andre 기준선



<a id="read-the-chronology-first"></a>

## 연표를 먼저 읽어보세요

Andre는 Lau에 따르면 지역화 충돌로 인해 의도적으로 **Spell.dbc**를 생략했습니다. 보관된 Andre 3.0.3 아카이브에는 6개의 시각적/모델 DBC가 포함되어 있습니다. Spell.dbc가 포함되어 있지 않습니다. 초기 Lau 추가로 인해 언어 종속성이 도입되었습니다. Lau 및 Andre는 ​​문제를 함께 디버깅했으며 다국어 재구축을 통해 문제를 해결했습니다.

Lau는 이러한 개발 이정표를 3.0.4(초기 추가) 및 3.0.5(다국어 수정)로 식별하며, 3.0.6–3.0.8는 버전 번호가 추가된 핫픽스입니다. 보유된 아티팩트는 해당 기억에 명확하게 매핑되지 않습니다. 3.0.4라는 레이블이 붙은 게시된 기준선에는 이미 다국어 수정 사항이 포함되어 있습니다. 이 보고서는 게시된 레이블에 초기에 손상된 빌드를 자동으로 할당하는 대신 아티팩트와 해시의 이름을 명시적으로 지정합니다.

[현지화 단계 증명](../../../../../dbc/history/localization-stage.json)은 보관된 현지화 전 v35 아카이브 4개를 다국어 버전과 비교합니다. Spell.dbc 변경 사항만 있고 모든 숫자 필드는 동일하게 유지되며 기존 시각적 링크는 보존됩니다. HD New Spells Off는 스톡 숫자 데이터를 사용하여 별도로 수집되었습니다.

<a id="format-and-scope"></a>

## 형식 및 범위

이것은 Patch-Y 핸드오프 비교이며, 모든 개별 Q/S/맵 현지화 파이프라인에 대한 감사가 아닙니다. 6개 버전의 CSV에는 개별 테이블/레코드/필드 편집 내용과 추가된 모든 레코드 값이 나열됩니다. 두 개의 공유 JSON gzip 파일에는 신성화 변형에 대한 텍스트를 복제하지 않고 디코딩된 주문 텍스트 변경 사항이 포함되어 있습니다. 각 텍스트 셀은 `[record_id, zero_based_field, old_string_index, new_string_index]`입니다. 해당 파일의 `strings` 배열을 통해 마지막 두 개를 해결합니다.

숫자 값은 부동 비트 패턴을 포함하여 부호 없는 원시 32-bit 단어입니다. 알 수 없는 스키마 이름은 추측되지 않습니다. Spell.dbc 필드 131는 빌드 스크립트에서 사용되는 시각적 링크입니다. 문자열 오프셋은 비교 전에 디코딩됩니다. 추가된 Spell.dbc는 HD New Spells On에 대해 보존된 HD Patch-S 데이터를 사용하고, HD New Spells Off 및 Non-HD에 대해 스톡 서버에서 추출된 데이터를 사용합니다. 상속된 행은 새로 작성된 레코드로 인정되지 않습니다.

<a id="what-the-edit-groups-mean"></a>

### 편집 그룹의 의미

- 주문 필드 131: 모든 에디션에서 허용되는 15개의 공격대 표시 시각적 링크.
- 철자 텍스트 셀: 다국어/대체 슬롯 채우기; 이 개수는 새로 작성된 번역의 개수가 아닙니다.
- SpellVisual, SpellVisualKit 및 부착 행: 표시기 라우팅, 키트 및 모델 부착 설정.
- SpellVisualEffectName: 모델 참조 및 신성화 외관 차이를 추가했습니다.
- CreatureDisplayInfo 및 CreatureModelData: 해당 Andre 기준선에서 변경되지 않았습니다.
- HD New Spells Off: 개인 Rimefang 키트는 90059를 사용하여 업스트림 90046 키트를 보존합니다.

<a id="y-hd-newspells-off-consecration-on"></a>

## Y-HD-NewSpells-꺼짐-축성-켜짐

| 테이블 | 변경/추가된 기록 | 필드 값 차이 | 추가된 ID | 삭제된 ID |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | 없음 | 없음 |
| creaturemodeldata.dbc | 0 | 0 | 없음 | 없음 |
| spell.dbc | 49839 | 824619 | 없음 | 없음 |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | 없음 |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | 없음 |
| spellvisualkit.dbc | 14 | 495 | 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058, 90059 | 없음 |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | 없음 |

| 테이블 | 레코드 ID | 필드 [0-기반을 둔] | 오래된 | 새로운 |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualeffectname.dbc | 2542 | 2 | 주문\consecration_impact_base.mdx | 주문\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[모든 기록/필드 편집 및 추가된 기록](../../../../../dbc/history/Y-HD-NewSpells-Off-Consecration-On.csv) · [디코딩된 텍스트 변경](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-hd-newspells-off-consecration-off"></a>

## Y-HD-NewSpells-꺼짐-축성-꺼짐

| 테이블 | 변경/추가된 기록 | 필드 값 차이 | 추가된 ID | 삭제된 ID |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | 없음 | 없음 |
| creaturemodeldata.dbc | 0 | 0 | 없음 | 없음 |
| spell.dbc | 49839 | 824619 | 없음 | 없음 |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | 없음 |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | 없음 |
| spellvisualkit.dbc | 14 | 495 | 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058, 90059 | 없음 |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | 없음 |

| 테이블 | 레코드 ID | 필드 [0-기반을 둔] | 오래된 | 새로운 |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[모든 기록/필드 편집 및 추가된 기록](../../../../../dbc/history/Y-HD-NewSpells-Off-Consecration-Off.csv) · [디코딩된 텍스트 변경](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-hd-newspells-on-consecration-on"></a>

## Y-HD-NewSpells-온-축성-온

| 테이블 | 변경/추가된 기록 | 필드 값 차이 | 추가된 ID | 삭제된 ID |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | 없음 | 없음 |
| creaturemodeldata.dbc | 0 | 0 | 없음 | 없음 |
| spell.dbc | 33950 | 227113 | 없음 | 없음 |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | 없음 |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | 없음 |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | 없음 |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | 없음 |

| 테이블 | 레코드 ID | 필드 [0-기반을 둔] | 오래된 | 새로운 |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualeffectname.dbc | 2542 | 2 | 주문\consecration_impact_base.mdx | 주문\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[모든 기록/필드 편집 및 추가된 기록](../../../../../dbc/history/Y-HD-NewSpells-On-Consecration-On.csv) · [디코딩된 텍스트 변경](../../../../../dbc/history/spell-text-hd.json.gz)

<a id="y-hd-newspells-on-consecration-off"></a>

## Y-HD-NewSpells-온-축성-해제

| 테이블 | 변경/추가된 기록 | 필드 값 차이 | 추가된 ID | 삭제된 ID |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | 없음 | 없음 |
| creaturemodeldata.dbc | 0 | 0 | 없음 | 없음 |
| spell.dbc | 33950 | 227113 | 없음 | 없음 |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | 없음 |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | 없음 |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | 없음 |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | 없음 |

| 테이블 | 레코드 ID | 필드 [0-기반을 둔] | 오래된 | 새로운 |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[모든 기록/필드 편집 및 추가된 기록](../../../../../dbc/history/Y-HD-NewSpells-On-Consecration-Off.csv) · [디코딩된 텍스트 변경](../../../../../dbc/history/spell-text-hd.json.gz)

<a id="y-non-hd-consecration-on"></a>

## Y-Non-HD-성결-On

| 테이블 | 변경/추가된 기록 | 필드 값 차이 | 추가된 ID | 삭제된 ID |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | 없음 | 없음 |
| creaturemodeldata.dbc | 0 | 0 | 없음 | 없음 |
| spell.dbc | 49839 | 824619 | 없음 | 없음 |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | 없음 |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | 없음 |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | 없음 |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | 없음 |

| 테이블 | 레코드 ID | 필드 [0-기반을 둔] | 오래된 | 새로운 |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualeffectname.dbc | 2542 | 2 | 주문\consecration_impact_base.mdx | 주문\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[모든 기록/필드 편집 및 추가된 기록](../../../../../dbc/history/Y-Non-HD-Consecration-On.csv) · [디코딩된 텍스트 변경](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-non-hd-consecration-off"></a>

## Y-Non-HD-성결-꺼짐

| 테이블 | 변경/추가된 기록 | 필드 값 차이 | 추가된 ID | 삭제된 ID |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | 없음 | 없음 |
| creaturemodeldata.dbc | 0 | 0 | 없음 | 없음 |
| spell.dbc | 49839 | 824619 | 없음 | 없음 |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | 없음 |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | 없음 |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | 없음 |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | 없음 |

| 테이블 | 레코드 ID | 필드 [0-기반을 둔] | 오래된 | 새로운 |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[모든 기록/필드 편집 및 추가된 기록](../../../../../dbc/history/Y-Non-HD-Consecration-Off.csv) · [디코딩된 텍스트 변경](../../../../../dbc/history/spell-text-nonhd.json.gz)

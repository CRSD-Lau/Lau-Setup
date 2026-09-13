<!-- LANGUAGES:START -->
[English](../../../../../../README.md) · [Deutsch](../../../../de/README.md) · [Español (España)](../../../../es-ES/README.md) · [Español (México)](../../../../es-MX/README.md) · [Français](../../../../fr/README.md) · [한국어](../../../../ko/README.md) · [Русский](../../../../ru/README.md) · [简体中文](../../../../zh-CN/README.md) · [繁體中文](../../../README.md) · [Português (Brasil)](../../../../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自動翻譯。 [英文來源](../../../../../dbc/history/INDIVIDUAL-EDITS.md)。若措詞不同，則以英文來源為準。

<a id="individual-patch-y-dbc-edits-andre-baseline-to-retained-multilingual-lau-build"></a>

# 單獨的 Patch-Y DBC 編輯：Andre 基線到保留的多語言 Lau 構建



<a id="read-the-chronology-first"></a>

## 首先閱讀年表

根據 Lau 的說法，由於本地化衝突，Andre 故意省略了 **Spell.dbc**。保留的 Andre 3.0.3 檔案確實包含六個視覺/模型 DBC；它們不包含 Spell.dbc。最初的 Lau 添加引入了語言依賴性。 Lau和Andre一起除錯問題，多語言重建解決了問題。

Lau 將這些開發里程碑標識為 3.0.4（初始新增）和 3.0.5（多語言修復），其中 3.0.6–3.0.8 是版本號已增加的補修程式。保留的工件無法清晰地映射到該回憶：標記為 3.0.4 的已發布基準已包含多語言修復。該報告明確命名工件和雜湊值，而不是默默地將早期損壞的建置分配給該已發布的標籤。

[本地化階段證明](../../../../../dbc/history/localization-stage.json) 將四個保留的預本地化 v35 存檔與多語言版本進行比較：僅 Spell.dbc 發生變化，所有數字字段保持相同，並且保留現有的可視鏈接。 HD New Spells Off 是使用庫存數位資料單獨組裝的。

<a id="format-and-scope"></a>

## 格式和範圍

這是 Patch-Y 切換比較，而不是每個單獨的 Q/S/地圖本地化管道的審核。六個版本的 CSV 列出了各個表/記錄/欄位編輯以及所有新增的記錄值。兩個共享的 JSON gzip 檔案保存解碼的拼字文字更改，而無需複製奉獻變體的文字。每個文字單元格為`[record_id, zero_based_field, old_string_index, new_string_index]`；透過該檔案的 `strings` 陣列解析最後兩個。

數值是原始無符號 32-bit 字，包括浮點位模式；不會猜測未知的模式名稱。 Spell.dbc 欄位 131 是建置腳本使用的視覺連結。字串偏移量在比較之前被解碼。新增的 Spell.dbc 使用保留的 HD Patch-S 資料進行 HD New Spells On，並使用庫存伺服器擷取的資料進行 HD New Spells Off 和非 HD。繼承的行不會記作新建立的記錄。

<a id="what-the-edit-groups-mean"></a>

### 編輯群組的意義

- 法術字段 131：每個版本中十五個接受的團隊指示器視覺連結。
- 拼字文字儲存格：多語言/後備插槽位；這些計數並不是新創作翻譯的計數。
- SpellVisual、SpellVisualKit 和附件行：指示器佈線、套件和模型附件設定。
- SpellVisualEffectName：增加了模型參考和奉獻外觀差異。
- CreatureDisplayInfo 和 CreatureModelData：與相應的 Andre 基線相比沒有變化。
- HD 新技能：私人 Rimefang 套件使用 90059 來保留上游 90046 套件。

<a id="y-hd-newspells-off-consecration-on"></a>

## Y-HD-NewSpells-關-開光-開

|表|更改/新增記錄 |欄位值差異 |新增 ID |已刪除 ID |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 |無 |無 |
| creaturemodeldata.dbc | 0 | 0 |無 |無 |
| spell.dbc | 49839 | 824619 |無 |無 |
| spellvisual.dbc | 9 | 165 | 20016、20017、20018、20019、20020 |无 |
| spellvisualeffectname.dbc | 12 | 79 | 9165、9166、9167、9168、9169、9170、9171、9172、 9173、9174、9175 |無 |
| spellvisualkit.dbc | 14 | 495 | 90047、90048、90049、90050、90051、90052、90053、90054、 90055、90056、90057、90058、90059 |無 |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073，8074 |無 |

| 桌子 | 記錄ID | 場地 [0-基於] | 老的 | 新的 |
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
| spellvisualeffectname.dbc | 2542 | 2 | 法術\consecration_impact_base.mdx | 法術\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[所有記錄/欄位編輯和新增的記錄](../../../../../dbc/history/Y-HD-NewSpells-Off-Consecration-On.csv) · [解碼文字變更](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-hd-newspells-off-consecration-off"></a>

## Y-HD-NewSpells-關-開光-關

| 桌子 | 更改/新增記錄 | 欄位值差異 | 新增的 ID | 刪除的 ID |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | 沒有任何 | 沒有任何 |
| creaturemodeldata.dbc | 0 | 0 | 沒有任何 | 沒有任何 |
| spell.dbc | 49839 | 824619 | 沒有任何 | 沒有任何 |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | 沒有任何 |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | 沒有任何 |
| spellvisualkit.dbc | 14 | 495 | 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058, 90059 | 沒有任何 |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | 沒有任何 |

| 桌子 | 記錄ID | 場地 [0-基於] | 老的 | 新的 |
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

[所有記錄/欄位編輯與新增記錄](../../../../../dbc/history/Y-HD-NewSpells-Off-Consecration-Off.csv) · [解碼文字變更](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-hd-newspells-on-consecration-on"></a>

## Y-HD-NewSpells-開光-開

| 桌子 | 更改/新增記錄 | 欄位值差異 | 新增的 ID | 刪除的 ID |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | 沒有任何 | 沒有任何 |
| creaturemodeldata.dbc | 0 | 0 | 沒有任何 | 沒有任何 |
| spell.dbc | 33950 | 227113 | 沒有任何 | 沒有任何 |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | 沒有任何 |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | 沒有任何 |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | 沒有任何 |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | 沒有任何 |

| 桌子 | 記錄ID | 場地 [0-基於] | 老的 | 新的 |
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
| spellvisualeffectname.dbc | 2542 | 2 | 法術\consecration_impact_base.mdx | 法術\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[所有記錄/欄位編輯與新增記錄](../../../../../dbc/history/Y-HD-NewSpells-On-Consecration-On.csv) · [解碼文字變更](../../../../../dbc/history/spell-text-hd.json.gz)

<a id="y-hd-newspells-on-consecration-off"></a>

## Y-HD-NewSpells-開光-關

| 桌子 | 更改/新增記錄 | 欄位值差異 | 新增的 ID | 刪除的 ID |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | 沒有任何 | 沒有任何 |
| creaturemodeldata.dbc | 0 | 0 | 沒有任何 | 沒有任何 |
| spell.dbc | 33950 | 227113 | 沒有任何 | 沒有任何 |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | 沒有任何 |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | 沒有任何 |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | 沒有任何 |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | 沒有任何 |

| 桌子 | 記錄ID | 場地 [0-基於] | 老的 | 新的 |
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

[所有記錄/欄位編輯與新增記錄](../../../../../dbc/history/Y-HD-NewSpells-On-Consecration-Off.csv) · [解碼文字變更](../../../../../dbc/history/spell-text-hd.json.gz)

<a id="y-non-hd-consecration-on"></a>

## Y-非 HD-奉獻-開啟

| 桌子 | 更改/新增記錄 | 欄位值差異 | 新增的 ID | 刪除的 ID |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | 沒有任何 | 沒有任何 |
| creaturemodeldata.dbc | 0 | 0 | 沒有任何 | 沒有任何 |
| spell.dbc | 49839 | 824619 | 沒有任何 | 沒有任何 |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | 沒有任何 |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | 沒有任何 |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | 沒有任何 |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | 沒有任何 |

| 桌子 | 記錄ID | 場地 [0-基於] | 老的 | 新的 |
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
| spellvisualeffectname.dbc | 2542 | 2 | 法術\consecration_impact_base.mdx | 法術\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[所有記錄/欄位編輯和新增記錄](../../../../../dbc/history/Y-Non-HD-Consecration-On.csv) · [解碼文字變更](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-non-hd-consecration-off"></a>

## Y-非高清-奉獻-關閉

| 桌子 | 更改/新增記錄 | 欄位值差異 | 新增的 ID | 刪除的 ID |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | 沒有任何 | 沒有任何 |
| creaturemodeldata.dbc | 0 | 0 | 沒有任何 | 沒有任何 |
| spell.dbc | 49839 | 824619 | 沒有任何 | 沒有任何 |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | 沒有任何 |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | 沒有任何 |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | 沒有任何 |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | 沒有任何 |

| 桌子 | 記錄ID | 場地 [0-基於] | 老的 | 新的 |
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

[所有記錄/欄位編輯和新增記錄](../../../../../dbc/history/Y-Non-HD-Consecration-Off.csv) · [解碼文字變更](../../../../../dbc/history/spell-text-nonhd.json.gz)

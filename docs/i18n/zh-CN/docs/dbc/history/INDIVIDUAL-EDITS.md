<!-- LANGUAGES:START -->
[English](../../../../../../README.md) · [Deutsch](../../../../de/README.md) · [Español (España)](../../../../es-ES/README.md) · [Español (México)](../../../../es-MX/README.md) · [Français](../../../../fr/README.md) · [한국어](../../../../ko/README.md) · [Русский](../../../../ru/README.md) · [简体中文](../../../README.md) · [繁體中文](../../../../zh-TW/README.md) · [Português (Brasil)](../../../../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.4.0** — 一个 ZIP 现在同时包含 Windows 安装程序和 Linux/Wine 启动器。界面会在十种选项中自动跟随操作系统语言，手动选择会被保存。游戏版本 3.0.8 和游戏文件没有变化，也没有 DBC 修改。
>
> 由于 Google HTTP 429，完整指南刷新仍在等待中。下方正文可能已过时；请以当前英文来源和 1.4.0 发布说明为准。 [English](../../../../../dbc/history/INDIVIDUAL-EDITS.md) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)
>
> **当前下载：** Windows 和 Linux/Wine 都使用 [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)。解压含五个文件的 `LauSetup/` 文件夹：Windows 打开 `LauSetup.exe`；Linux/Wine 运行 `LauSetup.sh`。下方关于单独 EXE 或 Wine ZIP 的旧说明不适用于 1.4.0。
>
> **1.4.0:** 已识别的额外升级文件会自动备份，然后继续安装。恢复操作会将文件放回原位。无需手动移动。 安装程序在替换或移动现有文件之前会自动保留原文件。无关文件保持不变。


> **1.4.0:** 选择游戏文件夹 → 下一步 → 选择视觉效果 → 下一步 → 确认 → 安装升级 → 完成。根据检测到的客户端固定选择 Patch-Y HD 或 Patch-Y Non-HD。额外选项默认关闭；已安装的地图升级会保留。确认页列出 Patch-Y（Lau 版本）及所选额外内容、WoW.exe、Patch-Q、语言文件、下载大小和备份。下一步不会更改游戏文件。每一步都可手动选择界面语言并保存；自动会重新使用系统语言。仍可使用恢复上次安装。

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自动翻译。 [英文来源](../../../../../dbc/history/INDIVIDUAL-EDITS.md)。如果措辞不同，则以英文来源为准。

<a id="individual-patch-y-dbc-edits-andre-baseline-to-retained-multilingual-lau-build"></a>

# 单独的 Patch-Y DBC 编辑：Andre 基线到保留的多语言 Lau 构建



<a id="read-the-chronology-first"></a>

## 首先阅读年表

根据 Lau 的说法，由于本地化冲突，Andre 故意省略了 **Spell.dbc**。保留的 Andre 3.0.3 档案确实包含六个视觉/模型 DBC；它们不包含 Spell.dbc。最初的 Lau 添加引入了语言依赖性。 Lau和Andre一起调试问题，多语言重建解决了问题。

Lau 将这些开发里程碑标识为 3.0.4（初始添加）和 3.0.5（多语言修复），其中 3.0.6–3.0.8 是版本号已增加的修补程序。保留的工件无法清晰地映射到该回忆：标记为 3.0.4 的已发布基线已包含多语言修复。该报告明确命名工件和哈希值，而不是默默地将早期损坏的构建分配给该已发布的标签。

[本地化阶段证明](../../../../../dbc/history/localization-stage.json) 将四个保留的预本地化 v35 存档与多语言版本进行比较：仅 Spell.dbc 发生变化，所有数字字段保持相同，并且保留现有的可视链接。 HD New Spells Off 是使用库存数字数据单独组装的。

<a id="format-and-scope"></a>

## 格式和范围

这是 Patch-Y 切换比较，而不是对每个单独的 Q/S/地图本地化管道的审核。六个版本的 CSV 列出了各个表/记录/字段编辑以及所有添加的记录值。两个共享的 JSON gzip 文件保存解码的拼写文本更改，而无需复制奉献变体的文本。每个文本单元格为`[record_id, zero_based_field, old_string_index, new_string_index]`；通过该文件的 `strings` 数组解析最后两个。

数值是原始无符号 32-bit 字，包括浮点位模式；不会猜测未知的模式名称。 Spell.dbc 字段 131 是构建脚本使用的可视链接。字符串偏移量在比较之前被解码。添加的 Spell.dbc 使用保留的 HD Patch-S 数据进行 HD New Spells On，并使用库存服务器提取的数据进行 HD New Spells Off 和非 HD。继承的行不会记作新创建的记录。

<a id="what-the-edit-groups-mean"></a>

### 编辑组的含义

- 法术字段 131：每个版本中十五个接受的团队指示器视觉链接。
- 拼写文本单元格：多语言/后备槽位；这些计数并不是新创作翻译的计数。
- SpellVisual、SpellVisualKit 和附件行：指示器布线、套件和模型附件设置。
- SpellVisualEffectName：添加了模型参考和奉献外观差异。
- CreatureDisplayInfo 和 CreatureModelData：与相应的 Andre 基线相比没有变化。
- HD 新技能：私人 Rimefang 套件使用 90059 来保留上游 90046 套件。

<a id="y-hd-newspells-off-consecration-on"></a>

## Y-HD-NewSpells-关-开光-开

|表|更改/添加记录 |字段值差异 |添加 ID |已删除 ID |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 |无 |无 |
| creaturemodeldata.dbc | 0 | 0 |无 |无 |
| spell.dbc | 49839 | 824619 |无 |无 |
| spellvisual.dbc | 9 | 165 | 20016、20017、20018、20019、20020 |无 |
| spellvisualeffectname.dbc | 12 | 79 | 9165、9166、9167、9168、9169、9170、9171、9172、 9173、9174、9175 |无 |
| spellvisualkit.dbc | 14 | 495 | 90047、90048、90049、90050、90051、90052、90053、90054、 90055、90056、90057、90058、90059 |无 |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073，8074 |无 |

| 桌子 | 记录ID | 场地 [0-基于] | 老的 | 新的 |
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
| spellvisualeffectname.dbc | 2542 | 2 | 法术\consecration_impact_base.mdx | 法术\F​​lamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[所有记录/字段编辑和添加的记录](../../../../../dbc/history/Y-HD-NewSpells-Off-Consecration-On.csv) · [解码文本更改](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-hd-newspells-off-consecration-off"></a>

## Y-HD-NewSpells-关-开光-关

|表|更改/添加记录 |字段值差异 |添加 ID |已删除 ID |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 |无 |无 |
| creaturemodeldata.dbc | 0 | 0 |无 |无 |
| spell.dbc | 49839 | 824619 |无 |无 |
| spellvisual.dbc | 9 | 165 | 20016、20017、20018、20019、20020 |无 |
| spellvisualeffectname.dbc | 11 | 77 | 9165、9166、9167、9168、9169、9170、9171、9172、 9173、9174、9175 |无 |
| spellvisualkit.dbc | 14 | 495 | 90047、90048、90049、90050、90051、90052、90053、90054、 90055、90056、90057、90058、90059 |无 |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073，8074 |无 |

| 桌子 | 记录ID | 场地 [0-基于] | 老的 | 新的 |
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

[所有记录/字段编辑和添加记录](../../../../../dbc/history/Y-HD-NewSpells-Off-Consecration-Off.csv) · [解码文本更改](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-hd-newspells-on-consecration-on"></a>

## Y-HD-NewSpells-开光-开

|表|更改/添加记录 |字段值差异 |添加 ID |已删除 ID |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 |无 |无 |
| creaturemodeldata.dbc | 0 | 0 |无 |无 |
| spell.dbc | 33950 | 227113 |无 |无 |
| spellvisual.dbc | 9 | 165 | 20016、20017、20018、20019、20020 |无 |
| spellvisualeffectname.dbc | 12 | 79 | 9165、9166、9167、9168、9169、9170、9171、9172、 9173、9174、9175 |无 |
| spellvisualkit.dbc | 14 | 495 | 90046、90047、90048、90049、90050、90051、90052、90053、 90054、90055、90056、90057、90058 |无 |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073，8074 |无 |

| 桌子 | 记录ID | 场地 [0-基于] | 老的 | 新的 |
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
| spellvisualeffectname.dbc | 2542 | 2 | 法术\consecration_impact_base.mdx | 法术\F​​lamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[所有记录/字段编辑和添加记录](../../../../../dbc/history/Y-HD-NewSpells-On-Consecration-On.csv) · [解码文本更改](../../../../../dbc/history/spell-text-hd.json.gz)

<a id="y-hd-newspells-on-consecration-off"></a>

## Y-HD-NewSpells-开光-关

|表|更改/添加记录 |字段值差异 |添加 ID |已删除 ID |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 |无 |无 |
| creaturemodeldata.dbc | 0 | 0 |无 |无 |
| spell.dbc | 33950 | 227113 |无 |无 |
| spellvisual.dbc | 9 | 165 | 20016、20017、20018、20019、20020 |无 |
| spellvisualeffectname.dbc | 11 | 77 | 9165、9166、9167、9168、9169、9170、9171、9172、 9173、9174、9175 |无 |
| spellvisualkit.dbc | 14 | 495 | 90046、90047、90048、90049、90050、90051、90052、90053、 90054、90055、90056、90057、90058 |无 |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073、8074 |无 |

| 桌子 | 记录ID | 场地 [0-基于] | 老的 | 新的 |
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

[所有记录/字段编辑和添加记录](../../../../../dbc/history/Y-HD-NewSpells-On-Consecration-Off.csv) · [解码文本更改](../../../../../dbc/history/spell-text-hd.json.gz)

<a id="y-non-hd-consecration-on"></a>

## Y-非 HD-奉献-开启

|表|更改/添加记录 |字段值差异 |添加 ID |已删除 ID |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 |无 |无 |
| creaturemodeldata.dbc | 0 | 0 |无 |无 |
| spell.dbc | 49839 | 824619 |无 |无 |
| spellvisual.dbc | 9 | 165 | 20016、20017、20018、20019、20020 |无 |
| spellvisualeffectname.dbc | 12 | 79 | 9165、9166、9167、9168、9169、9170、9171、9172、 9173、9174、9175 |无 |
| spellvisualkit.dbc | 14 | 495 | 90046、90047、90048、90049、90050、90051、90052、90053、 90054、90055、90056、90057、90058 |无 |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073，8074 |无 |

| 桌子 | 记录ID | 场地 [0-基于] | 老的 | 新的 |
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
| spellvisualeffectname.dbc | 2542 | 2 | 法术\consecration_impact_base.mdx | 法术\F​​lamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[所有记录/字段编辑和添加记录](../../../../../dbc/history/Y-Non-HD-Consecration-On.csv) · [解码文本更改](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-non-hd-consecration-off"></a>

## Y-非高清-奉献-关闭

|表|更改/添加记录 |字段值差异 |添加 ID |已删除 ID |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 |无 |无 |
| creaturemodeldata.dbc | 0 | 0 |无 |无 |
| spell.dbc | 49839 | 824619 |无 |无 |
| spellvisual.dbc | 9 | 165 | 20016、20017、20018、20019、20020 |无 |
| spellvisualeffectname.dbc | 11 | 77 | 9165、9166、9167、9168、9169、9170、9171、9172、 9173、9174、9175 |无 |
| spellvisualkit.dbc | 14 | 495 | 90046、90047、90048、90049、90050、90051、90052、90053、 90054、90055、90056、90057、90058 |无 |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073，8074 |无 |

| 桌子 | 记录ID | 场地 [0-基于] | 老的 | 新的 |
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

[所有记录/字段编辑和添加记录](../../../../../dbc/history/Y-Non-HD-Consecration-Off.csv) · [解码文本更改](../../../../../dbc/history/spell-text-nonhd.json.gz)

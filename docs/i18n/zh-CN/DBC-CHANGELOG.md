<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- HOTFIX-118-NOTICE -->
> **热修复 1.1.8** — Setup 会检查 Data 和当前语言文件夹中的 MPQ，识别已知的改名 Patch-Y 和与目录文件完全相同的副本。发现可能的冲突、无法读取或不支持的存档时，会停止安装并显示文件名，不会自动删除该文件。仅重命名文件不会改变内容哈希。游戏文件仍为 3.0.8。
>
> 由于 Google 请求限额，完整翻译尚未更新。下方原有正文描述的是较早版本的情况。请以最新英文原文为准。 [English](../../../DBC-CHANGELOG.md) · [1.1.8](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.1.8)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自动翻译。 [英文来源](../../../DBC-CHANGELOG.md)。如果措辞不同，则以英文来源为准。

<a id="dbc-changelog"></a>

# DBC 变更日志



跟踪客户端 DBC 编辑与模型、纹理和安装程序更改分开。游戏版本和安装程序版本是分开的：`/pyversion` 报告游戏版本。

<a id="handoff-history-andre-303-onward"></a>

## 切换历史记录：Andre 3.0.3 向前

[个人DBC编辑和开发历史](docs/dbc/history/INDIVIDUAL-EDITS.md) · [六版比较和基线哈希](../../dbc/history/andre-to-3.0.4.json)

Andre 故意省略 **Spell.dbc** 以避免本地化冲突。最初的 Lau 覆盖暴露了该依赖关系； **Lau和Andre一起调试**，多语言重建解决了拼写文本兼容性问题。保留的 Andre 档案包含其他六个视觉/模型 DBC，因此不应将其描述为缺少每个 DBC。

Lau 将里程碑描述为**3.0.4：初始表添加**、**3.0.5：多语言解决方案**和**3.0.6–3.0.8：版本升级的修补程序**。早期版本标签重叠：标记为 3.0.4 的存档发布版本已包含多语言修复。下面的工件比较使用精确的哈希值，并且不会删除该开发历史。

最初的 Patch-Y 比较包括每个版本十五个法术视觉链接编辑、新的指示器视觉/套件/附件记录、奉献差异和解码的本地化编辑。添加的表与其基础股票或 HD Spell 基础进行比较，因此继承的记录不会作为新创作的作品呈现。 [本地化阶段验证](../../dbc/history/localization-stage.json) 确认四个保留的预本地化高清/非高清版本中文本重建保留的数字数据。

<a id="archived-releases-304--308"></a>

## 存档版本 3.0.4 → 3.0.8

|存档过渡 | DBC 结果 |其他变化|
| --- | --- | --- |
| 3.0.4 → 3.0.5 |没有 DBC 编辑； 42 相同表| Sindragosa 和 Rotface 圆锥体几何形状，版本标签 |
| 3.0.5 → 3.0.6 |没有 DBC 编辑； 42 相同表| Coldflame/Halion 标记颜色资源和参考、版本标签 |
| 3.0.6 → 3.0.7 |没有 DBC 编辑； 42 相同表|批准的 Halion 流星火几何形状，版本标签 |
| 3.0.7 → 3.0.8 |没有 DBC 编辑； 42 相同表|剩余呼吸/史莱姆喷雾锥体几何形状，版本标签 |

[所有 168 表比较和存档哈希](../../dbc/history/3.0.4-through-3.0.8.json)。这些是保留版本工件的比较，而不是声称早期的本地化事件没有发生。

<a id="307--308--no-dbc-edits"></a>

## 3.0.7 → 3.0.8 — 无 DBC 编辑

随 [安装程序 1.1.4](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.1.4) 一起发布。所有 **42 DBC 比较都逐字节传递**：六个 Patch-Y 版本中的每个版本都有七个表。没有添加/删除表、更改记录、更改字段或更改字符串块。

|表|记录编辑|现场编辑|结果 |
| --- | ---: | ---: | --- |
| CreatureDisplayInfo.dbc | 0 | 0 |相同|
| CreatureModelData.dbc | 0 | 0 |相同|
| Spell.dbc | 0 | 0 |相同|
| SpellVisual.dbc | 0 | 0 |相同|
| SpellVisualEffectName.dbc | 0 | 0 |相同|
| SpellVisualKit.dbc | 0 | 0 |相同|
| SpellVisualKitModelAttach.dbc | 0 | 0 |相同|

[完整对比证据](../../dbc/3.0.7-to-3.0.8.json)记录了每个版本的源/目标MPQ SHA-256、每个DBC的SHA-256之前/之后、大小、行数和字段数。根据发布目录检查 MPQ 哈希值。其他 22 目录资产（包括区域设置 Q 和共享 S 资产）保持不变。

<a id="what-actually-changed-in-308"></a>

### 3.0.8 中实际发生了什么变化

通过编辑 `.m2` 几何形状和相应的 `00.skin` 边界，将五个现有锥体模型拓宽至 **90° 总计**。保留现有的 DBC 绑定。

| 模型杆 | 上一个角度 | 新角度 |
| --- | ---: | ---: |
| PW_Rotface_SlimeSpray_Fan25_Room | 60° | 90° |
| PW_White_Fan60_60yd_Glowing | 60° | 90° |
| PW_White_Fan60_30yd_Glowing | 60° | 90° |
| PW_White_Fan60_100y_Glowing | 60° | 90° |
| PW_White_Fan82_60yd_发光 | 82° | 90° |

文件名保留历史角度标签；几何形状决定显示角度。辛达苟萨已经是 90° 并且在此转变中没有改变。这将所有受支持的呼吸和史莱姆喷雾指示器带到了 90°。范围和动画时间没有变化。 Halion 流星火半径、冷焰颜色和奉献度保持不变。

每个版本都完全更改了**11存档成员**：五个`.m2`文件、五个`.skin`文件和`!pyandre.toc`游戏版本标签从3.0.7到3.0.8。每个其他列出的内容成员都是相同的。 MPQ 容器簿记不在内容成员比较范围内。

这验证了客户端文件更改，而不是 Warmane 的服务器机制或确切的损坏边界。

<a id="setup-115-116-and-117--no-dbc-edits"></a>

## 设置 1.1.5、1.1.6 和 1.1.7 — 无 DBC 编辑

这些是安装程序修补程序。他们的游戏有效负载仍为 3.0.8，DBC 数据未更改。最新的修补程序更改了Patch-S的安装、保存和重用，而不是其内部DBC内容。

<a id="required-entry-for-future-releases"></a>

## 未来版本所需的条目

每个版本都必须在此处添加一个条目，并在其 GitHub 发行说明中添加 **DBC 更改** 部分，包括仅限安装程序的版本。适用时明确声明**无 DBC 编辑**。与之前的稳定游戏版本进行比较，而不是与未发布的测试版本进行比较。不要将模型/纹理编辑描述为 DBC 编辑。

对于每个实际的 DBC 编辑，每个字段记录一行（或用于大型本地化更改的链接的机器可读行级差异）：

|游戏过渡 |表|记录ID |字段名称/从零开始的索引 |旧值 |新价值|版本/语言环境 |原因 |
| --- | --- | --- | --- | --- | --- | --- | --- |
|版本 → 版本 | TABLE.dbc |身份证 |命名字段[索引] |先前值|新价值|受影响的变体 |目的|

还记录添加/删除的记录和表、架构更改以及字符串值编辑。当内容发生变化时，解码字符串值而不是报告字符串块偏移量变动。指定字段索引约定和模式源；标记未知字段而不是猜测。附加归档前/后和表哈希、比较方法和验证限制。切勿在没有证据的情况下声称比较已通过。

移交审计涵盖从保留的 Andre 3.0.3 基线开始的 Patch-Y。单独的 Q/S/地图本地化管道和不相关的实验构建不在此初始回顾范围内。如果没有匹配的来源，则不会为早期损坏的工件分配版本号。

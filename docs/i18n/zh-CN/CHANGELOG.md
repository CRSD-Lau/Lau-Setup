<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- HOTFIX-118-NOTICE -->
> **热修复 1.1.8** — Setup 会检查 Data 和当前语言文件夹中的 MPQ，识别已知的改名 Patch-Y 和与目录文件完全相同的副本。发现可能的冲突、无法读取或不支持的存档时，会停止安装并显示文件名，不会自动删除该文件。仅重命名文件不会改变内容哈希。游戏文件仍为 3.0.8。
>
> 由于 Google 请求限额，完整翻译尚未更新。下方原有正文描述的是较早版本的情况。请以最新英文原文为准。 [English](../../../CHANGELOG.md) · [1.1.8](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.1.8)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自动翻译。 [英文来源](../../../CHANGELOG.md)。如果措辞不同，则以英文来源为准。

<a id="lau-setup-116-hotfix---switch-options-with-existing-disabled-patch-s"></a>

# Lau Setup 1.1.6 修补程序 - 切换现有禁用的选项 Patch-S

修复了在早期安装后关闭新拼写视觉效果时出现的 1.1.5 消息“已存在不同的已禁用的 Patch-S”。

安装程序会自动保留这两个文件。当前的S文件始终变为`.mpq.disabled`。如果已存在不同的旧禁用副本，安装程序首先将该旧副本保留为 `.mpq.disabled.<12-character hash>`。重复使用相同的已保存副本。两个版本均被保留。其内容与保留的旧文件不匹配的哈希命名副本仍会停止操作以进行检查。

这适用于根和活动区域设置 S 文件，包括序列**所有三个标志打开 -> 新拼写视觉效果关闭**、重复切换和回滚。地图选择被保留。

下载新的 EXE 或 Wine ZIP 并重试您的选择。您无需删除或重命名现有的禁用副本即可解决 1.1.5 显示的普通冲突。

要撤消完整安装，请使用 **恢复以前的安装**。要手动重新启用已保存的 S 文件，请关闭 WoW 并删除 `.disabled` 和任何后续哈希，恢复其原始 `.mpq` 文件名。切勿覆盖不同的活动文件。手动更改可以阻止文件漂移的托管回滚；保留您的备份。在 1.1.5 之前安装程序删除的文件仍然需要通过备份进行恢复。

游戏版本保持**3.0.8 Lau**，并且每个游戏有效负载均保持不变。所有 90 度锥体、流星火半径和冷焰均被保留。

Windows 和 Wine 检查包括 46 回归组、所有九个区域设置、现有禁用文件、重复开关、篡改复制保护、中断恢复和精确回滚。新的公开下载使用真实的开/关发布文件和旧的禁用副本进行测试。这是安装程序验证，而不是新的游戏内遭遇验证。

[原始六版 Patch-Y 拉链](https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.1.4/Lau-Patch-Y-3.0.8-All-Editions.zip)

[安装帮助和变更日志](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-115-hotfix---keep-disabled-patch-s-files"></a>

# Lau Setup 1.1.5 修补程序 - 保留禁用的 Patch-S 文件

关闭**新拼写视觉效果**现在会将根和活动区域设置 Patch-S 文件保留在其原始位置旁边作为 `.mpq.disabled`，而不是仅将它们保留在安装程序备份中。它们的字节在更改之前和之后都会得到验证。 WoW 不加载禁用的文件名。

- 不同的现有 `.disabled` 副本会阻止安装；它永远不会被覆盖。
- 重复使用并保留相同的禁用副本。
- 打开该选项会安装所选版本的活动 S 文件并保留禁用的副本。
- 重复安装、回滚和中断恢复涵盖活动路径和禁用路径。

要手动重新启用已禁用的文件，请关闭 WoW 并仅删除 `.disabled` 后缀。不要覆盖不同的活动文件。要撤消完整的 Lau 安装，请使用 **恢复以前的安装**；仅删除 Patch-Y 不会撤消 Q/M/可执行文件或其他更改。手动文件更改可能会导致托管回滚因漂移而停止，因此请保留备份。

**已受到旧安装程序的影响？** 此更新不会自动提取旧备份。使用“恢复以前的安装”来恢复这些文件，在使用新设置重新安装之前，向后执行任何堆叠的安装。保留LauSetupBackups。

游戏版本仍然是**3.0.8 Lau**。所有 MPQ 均保持不变：90 度呼吸/史莱姆喷雾，已批准 +50% Halion 流星火半径和冷焰均保留。下载新的 EXE 或 Wine ZIP 以进行安装程序修复。

Windows 和 Wine 验证包含在 VALIDATION.json 中。测试涵盖所有九个区域设置、禁用复制冲突、开/关转换、重复安装、每个移动/恢复步骤的中断、文件漂移和精确回滚。该修复不会要求新的游戏内遭遇验证。

[原始六版 Patch-Y 拉链 (不变 3.0.8)](https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.1.4/Lau-Patch-Y-3.0.8-All-Editions.zip)

[安装帮助和变更日志](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-114--game-release-308-lau"></a>

# Lau Setup 1.1.4 · 游戏发布 3.0.8 Lau

<a id="117-hotfix---patch-s-re-enable-cleanup"></a>

## 1.1.7 修补程序 - Patch-S 重新启用清理

- 当 SHA-256 和大小与所选版本匹配时，重新启用新咒语视觉效果会重复使用已禁用的 Patch-S，从而避免下载。
- 普通禁用副本移至数据外部的已验证事务备份中，即使活动 Patch-S 已匹配。通过恢复以前的安装，不同的禁用文件仍然可以恢复。
- 适用于根和活动区域设置 Patch-S。 Off 仍使用普通的 `.mpq.disabled` 文件名。现有的哈希后缀存档保持不变。
- 游戏有效负载仍为 3.0.8 Lau。 Windows 和 Wine 均通过了 50 回归组、真实文件开/关/开切换和精确回滚。

<a id="all-breath-and-slime-spray-warnings-are-now-90"></a>

## 所有呼吸和粘液喷雾警告现在为 90°

在 Warmane 测试人员确认后，Halion（两个领域）、Saviana Ragefire、Sartharion、ICC Rimefang 和 Rotface Slime Spray 现在使用 **90° 总锥**，与 Sindragosa 现有的 90° 警告相匹配。这适用于所有六个版本和九种客户端语言，包括现有的普通/英雄法术映射。

仅锥体宽度发生变化。范围、动画时间、原生法术效果和法术表都被保留。批准的50%更大的Halion流星火半径，浅蓝色冷焰，颜色和奉献度不变。这些是视觉警告缓冲区；服务器损坏和机制保持不变。不平坦的地形仍然会夹住扁平锥体。

<a id="updating"></a>

## 更新中

首先从该版本下载 **LauSetup.exe** 或 **LauSetup-Wine.zip**。关闭WoW，选择相同的客户端和视觉效果，然后单击**安装升级**。旧安装程序保留其旧目录。检查 `/pyversion` 的 **3.0.8 Lau**。

安装程序会验证实际的 SHA-256 哈希值，因此可以检测到以前的版本，甚至是大小和时间戳未更改的一字节更改。只有确切的当前文件才算作已安装。备份和恢复以前的安装仍然可用。

Windows 需要.NET框架 4.8. Wine 用户提取所有四个文件并运行 `LauSetup.sh` 作为普通用户，具有受支持的现有 Wine/单声道前缀。运行时安装程序未捆绑。

<a id="validation"></a>

## 验证

请参阅 VALIDATION.json 了解 Windows 和 Wine 回归、3.0.7 的六版升级、重复检测、一字节检查、回滚和公共下载检查。几何检查验证每个版本中的 90° 锥体、保留范围、有效边界和三角形缠绕。恰好有 11 个现有档案成员发生了变化：五个模型、他们的五个皮肤和版本目录。所有其他成员与 3.0.7 的字节相同。

宽度决定遵循报告的 Warmane 测试。此版本不是每次遇到或精确的服务器边界认证。

[网站变更日志和安装帮助](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-113--game-release-307-lau"></a>

# Lau Setup 1.1.3 · 游戏发布 3.0.7 Lau

<a id="larger-halion-meteor-fire-warnings"></a>

## 更大的 Halion 流星火警告

促进测试人员批准的 **测试 v2**：Halion 的红色地面标记半径 **50% 大于发布版 3.0.6**，围绕小径和着陆火力。不包括测试 v3。冷焰、颜色、动画轨迹、原生火焰、奉献和 Sindragosa/Rotface 锥体均保持不变。支持所有六个版本和九种客户端语言。

测试人员在修正未更新的补丁后确认了 v2。这是一个视觉警告缓冲区，而不是对服务器损坏的更改或对每个位置或遭遇的认证。

<a id="update-with-the-new-installer"></a>

## 使用新安装程序进行更新

首先从该版本下载 **LauSetup.exe** 或 **LauSetup-Wine.zip**。关闭WoW，选择相同的客户端和视觉效果，然后单击**安装升级**。旧的安装程序保留旧的目录。 `/pyversion` 报告 **3.0.7 Lau**。

现有 3.0.6 和测试 v2 用户将收到更新。安装程序会比较实际的文件哈希值，包括大小和时间戳不变的一字节更改；只有确切的当前文件才算作已安装。备份和恢复以前的安装仍然可用。

Windows 需要 .NET Framework 4.8。 Wine 用户提取所有四个文件，并以普通用户身份运行 `LauSetup.sh`，并使用受支持的现有 Wine/Mono 前缀。没有捆绑运行时安装程序。

<a id="validation-1"></a>

## 验证

Windows和Wine安装程序回归、六版升级、重复检测、一字节检查、回滚和公共下载检查都记录在VALIDATION.json中。 Halion 模型和皮肤与测试 v2 的字节相同。仅其几何/边界和版本 TOC 与 3.0.6 不同； Coldflame 和其他存档成员没有变化。

[网站变更日志和安装帮助](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-112--game-release-306-lau"></a>

# Lau Setup 1.1.2 · 游戏发布 3.0.6 Lau

<a id="blue-coldflame-red-meteor-fire"></a>

## 蓝色冷焰、红色流星火

- **Marrowgar Coldflame：** 浅蓝色圆圈，具有现有的向内发光和顺时针动画，包括英雄。
- **Halion 流星火：** 使用现有的顺时针动画在轨迹周围发射红色圆圈并着陆火力。
- 所有六种高清/非高清版本和九种客户端语言。原生火焰、持续时间、奉献选择和 90° Sindragosa / 60° Rotface 锥体保持不变。

[动画颜色预览和完整变更日志](https://wrath-multilingual-hd.vercel.app/#changelog)。预览是说明性的模型，而不是游戏中的录音。服务器损坏和机制不变；警告边缘仍然是视觉缓冲区。

<a id="already-installed-download-the-new-installer-first"></a>

## 已经安装了吗？首先下载新的安装程序

从此版本下载 **LauSetup.exe** 或 **LauSetup-Wine.zip**。关闭WoW，选择相同的文件夹和视觉设置，然后单击**安装升级**。旧的下载安装程序保留旧的嵌入式目录。

安装程序对实际文件进行哈希处理。旧的 3.0.5 文件被替换；即使文件大小和时间戳相同的一字节更改也会被检测到。只有全新的文件才会被视为已安装。 `/pyversion` 报告 **3.0.6 Lau**。备份和恢复以前的安装仍然可用。

Wine 用户：将所有四个文件一起提取并以普通用户身份运行 `LauSetup.sh`，并使用现有的 64-bit Wine 11.0 / Mono 10.4.1 前缀。需要Python 3.9+ 和本地Linux 存储。 Windows 需要 .NET Framework 4.8。运行时不捆绑。

<a id="fresh-verification-on-windows-and-wine"></a>

## Windows 和 Wine 的最新验证

- 每个平台的 38 回归组，包括每个 108 区域设置/版本/地图计划。
- 所有六个实际的 3.0.5 到 3.0.6 升级，在两个平台上重复无操作安装和精确回滚。
- 在两个平台上的根和语言环境 Y 中独立检测和修复一字节相同大小/相同时间戳更改。
- 匿名 GitHub 有效负载下载、实际核心安装以及 Windows 和 Wine 上的回滚。
- 15 Linux 主机安全测试和普通用户下的精确四文件 Wine 启动器； Windows 表单渲染已检查。
- 三个标记 M2 纹理参考和每个版本更改的版本目录；添加了两种颜色纹理。所有其他成员都逐字节保存。

这些安装程序检查并不验证每个 Linux 发行版或每个游戏内遭遇。 可执行文件没有数字签名。附有详细的证据、校验和和来源。

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-111--game-release-305-lau"></a>

# Lau Setup 1.1.1 · 游戏发布 3.0.5 Lau

<a id="wider-raid-warnings"></a>

## 更广泛的袭击警告

- 辛达苟萨冰霜吐息：**75° → 90° 总计**（7.5° 每侧额外）。
- 腐脸粘液喷雾：**25° → 60° 总计**（17.5° 每侧额外）。
- 适用于所有六个高清/非高清版本，并适用于所有九个客户端区域设置。其他指标、奉献设置、本地化表格和艺术品均保持不变。

这些是由 Warmane 突袭镜头和法术命中日志通知的缓冲视觉警告。他们不会改变服务器的损坏或机制，也不会要求精确的损坏边界。

<a id="updating-an-existing-installation"></a>

## 更新现有安装

首先下载新的 **LauSetup.exe** 或 **LauSetup-Wine.zip**。关闭WoW，选择相同的文件夹和视觉选择，然后单击**安装升级**。安装程序会比较实际的文件哈希值：旧的 3.0.4 补丁被替换，而确切的 3.0.5 安装报告为已安装。 `/pyversion` 更新后报告 **3.0.5 Lau**。旧下载的安装程序保留其旧目录。

Windows 和 Wine 下载包含相同的重建安装可执行文件。对于 Wine，将所有四个文件一起提取并使用 `LauSetup.sh`，如随附的自述文件中所述。现有的运行时要求保持不变。

<a id="verification"></a>

＃＃ 确认

所有 38 Windows 回归组均已通过，包括 108 语言环境/版本/地图计划。所有六个版本都通过了实际的 3.0.4 到 3.0.5 升级、重复安装和精确回滚检查。新的有效负载通过了匿名下载/哈希检查；与 GitHub 的隔离核心安装并已通过回滚。每个版本都保留除四个模型/几何文件和版本目录之外的所有成员。

Wine 启动器代码未更改，ZIP 包含准确的重建 EXE。保留早期的 Wine 11.0 / Mono 10.4.1 运行时证据；由于 Docker 引擎未启动，新的 Wine 执行不可用。新的锥体几何形状是静态验证的，而不是在游戏中新认证的。

随附下载校验和、源代码和详细验证报告。保留 `LauSetupBackups` 以供恢复。

Author / Creator / Last Modified By: Neil Mitchell

<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

<!-- STABLE-140-CURRENT-GUIDE -->
> **当前版本：Setup 1.4.0 / 游戏 3.0.9 Lau。** 关闭 WoW，完整解压 LauSetup.zip，在 Windows 中打开 LauSetup.exe，用 Browse... 选择包含 WoW.exe 的文件夹。下一步 → 视觉选项 → 下一步 → 检查 → 安装 → 完成。所有额外选项默认关闭。WoW.exe 和加载画面是同一个选项；地图独立，并包含 WDM 支持文件。已安装的地图会保留。重命名的重复补丁保持原样；只有空的 Patch-V 会自动备份。被替换的文件保存在 LauSetupBackups 中。Patch-Y 没有 DBC 修改；可选地图添加了已记录来源的上游表。洞穴地图仍为测试版。Linux/Wine 请在文档要求的环境中使用 LauSetup.sh。Google HTTP 429 阻止了完整翻译更新。下面的旧内容仅供历史参考，当前操作请以英文原文为准。
>
> [English](../../../KNOWN-LIMITATIONS.md) · [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自动翻译。 [英文来源](../../../KNOWN-LIMITATIONS.md)。如果措辞不同，则以英文来源为准。

<a id="known-limitations-and-assumptions"></a>

# 已知的限制和假设



[返回 Lau Setup](README.md) · [建议和功能请求](https://github.com/CRSD-Lau/Lau-Setup/discussions/1) · [DBC 更改历史记录](DBC-CHANGELOG.md)

在提出功能之前请阅读本文。 Lau Setup 为 **WoW 3.3.5a 版本 12340** 安装客户端可视化升级。它不是一个服务器修改框架。下面的边界描述了当前项目；超出范围并不一定意味着技术上不可能。

<a id="what-we-can-and-cannot-change"></a>

## 我们可以改变什么，不能改变什么

|请求 |当前边界|
| --- | --- |
|改进支持的地面指示器、纹理、模型或本地化客户端表 |在范围内，受文件依赖性和测试的约束。视觉改进不得被描述为服务器损坏或机制的改变。 |
|改进安装、备份、可访问性或文档 |范围内。保留不相关的文件并验证安装和恢复。 |
|更改 Warmane 伤害、命中检测、能力持续时间、目标或遭遇脚本 |在我们的控制范围之外。 Warmane运行自己的服务器代码；该项目无权更改或部署该代码。 MPQ 或插件不能使服务器采用不同的机制。 |
|将自定义C++代码添加到Warmane的核心 |此版本无法提供任何功能。对单独控制的测试服务器的更改不会更改 Warmane。 |
|注入 DLL、挂钩客户端或添加新的本机引擎行为 |在支持的补丁/插件工作流程之外。这需要单独的工程和兼容性调查，而不仅仅是 DBC 编辑。不提供 DLL 注入框架或一般客户端挂钩支持。 |
|解锁受保护的 Lua 操作或缺失的游戏 API |不受支持的功能。可编辑插件 Lua 和受保护的客户端操作是不同的事情。重写 Lua 本身并不授予权限或创建客户端不公开的 API。在假设存在解决方法之前报告确切的操作/API。 |
|提供完整的客户端、另一个语言包或高清模型库 |不包括在内。带来现有的兼容客户端以及所需的语言文件、字体和模型配置。 |

安装程序提供的兼容 `WoW.exe` 在批准的加载渲染器、存档容量和大地址支持方面具有特定作用。它的包含**不**承诺任意可执行文件或 DLL 修改。同样，并非每个 Lua 文件都受到保护或不可编辑：普通插件和 UI 更改在客户端支持的行为内是可行的。

<a id="indicators-are-visual-guidance"></a>

## 指标是视觉引导

- **Warmane 是 Warmane 报告的运行时参考。** AzerothCore 和隔离客户端有助于检查这些环境中的文件完整性和行为。他们无法证明 Warmane 的自定义命中检测、计时或遭遇行为。
- **绘制的边缘不能保证安全边界。** 支持的呼吸和粘液喷雾根据测试仪反馈使用 90° 总锥体。 Halion 流星火使用公认的 test-v2 放大。这些是基于观察的视觉警告，而不是来自 Warmane 服务器源的测量。
- **地形可能会夹住平坦的指示器。**平坦的地面网格可以与斜坡、台阶和不平坦的表面相交。放大或升高它并不能保证随处投影。
- **效果终生需要遇到证据。** 追踪/幽灵反馈包括一两秒后消失的效果。单独更改纹理、形状或循环动画并不能证明客户端将保持效果实例处于活动状态以进行完整的追求。时间修复需要该特定能力的镜头和事件证据；不要将模型或实验版本视为已确认的修复。
- **模型具有说明性。** 网站/聊天动画演示外观。它们不是游戏内渲染、持续时间或覆盖范围的录音或证明。

对于边界或时间报告，包括遭遇、能力、难度、客户端版本、`/pyversion`，以及显示引导和损坏或效果结束的剪辑。屏幕截图很有用，但透视和重叠效果限制了精确的半径测量。

<a id="dbc-and-patch-compatibility"></a>

## DBC 和补丁兼容性

DBC表是连接的数据，而不是独立的开关。添加视觉效果可能需要匹配的咒语、视觉效果、套件、效果和模型参考。替换完整的表还可能替换其本地化文本并与提供同一表的另一个补丁发生冲突。

本地化依赖性是该项目开发过程中的一个真正问题。 Andre 和 Lau 一起完成了它。 [历史 DBC 审计](DBC-CHANGELOG.md) 将报告的开发时间表与保留的档案证据分开：Andre 的基线省略了 `Spell.dbc`，并非每个 DBC。不要认为将英文表复制到另一个语言环境是安全的。

- 使用与您当前的高清/原始型号配置相匹配的版本。新的法术视觉效果需要兼容的高清依赖；检测并不验证每个第三方模型包。
- 如果您在安装后删除或禁用 HD 型号补丁，请重新运行最新的设置以获取最终的配置。安装的高清版本不会动态转换自身。不匹配的资产可能会产生缺失或不正确的视觉效果，并可能需要对崩溃进行调查；无法保证崩溃或无崩溃行为。
- 根位置和活动区域设置具有不同的作用。特别是，两个S档案是不同的。请遵循[放置指南](docs/TECHNICAL.md#file-placement)，而不是复制每个 MPQ 的通用说明。
- 保留不相关的补丁，但保留并不能保证兼容性。覆盖相同数据的另一个存档可能会改变结果。
- 安装程序界面会在十种选项中自动跟随操作系统语言，手动选择会被保存。游戏内容仍支持九种语言环境。仅更改 `Config.wtf` 不会安装其他语言的文件或字体。

<a id="installer-and-recovery-assumptions"></a>

## 安装程序和恢复假设

在安装或恢复之前完全关闭 WoW。使用确切的预期客户端文件夹并保持 `LauSetupBackups` 完好无损。

安装程序将实际文件哈希值与其**嵌入目录**进行比较。即使大小和时间戳匹配，也可以检测到一字节的更改，但旧的安装程序仍然只知道其旧目录。升级时下载最新的安装程序。安装程序不会在客户端退出后持续监视客户端，也不会自动协调以后的手动补丁更改。

关闭新法术视觉效果会将范围 S 文件保留为 `.mpq.disabled`。重新启用使用匹配的禁用字节（如果可用），并将普通禁用副本移动到已验证的事务备份中。保留较旧的哈希后缀副本。请参阅[当前恢复实现](docs/TECHNICAL.md#setup-117-re-enable-cleanup)。

恢复依赖于备份和恢复记录。当以后的更改使自动恢复变得不安全时，它就会停止。它不能承诺恢复唯一备份被删除的文件。单独删除 Patch-Y 并不能完全回滚安装程序安装的可执行文件和其他补丁。对托管事务使用**恢复以前的安装**。

<a id="platform-and-validation-limits"></a>

## 平台和验证限制

记录的 Windows 目标是带有 .NET Framework 4.8 的 Windows 10/11。测试的 Linux 配置使用 Wine 11.0、Wine Mono 10.4.1、现有的 64-bit 前缀和 Python 3.9+。运行时安装程序未捆绑。遵循 [Wine 先决条件](wine/README.md)；使用本地 Linux 存储。链接的文件夹、网络共享和 Windows 安装的驱动器不在支持的 Wine 路径配置范围内。

此版本不支持 Lutris、Proton、Steam Deck 特定集成和 macOS 集成目标。这并不是断言其他所有环境都是不可能的；这意味着我们还没有建立对其的支持。 Windows 软件包没有数字签名。

构建、哈希检查、安装程序回归测试、Wine 测试和游戏内测试回答了不同的问题。通过一项并不能取代其他项。目视检查是抽样的，并非对每个区域、遭遇、显示比例、Linux 分布或第三方客户端修改的认证。请参阅每个版本的验证报告以了解实际检查的内容。

<a id="before-requesting-a-feature"></a>

## 在请求功能之前

描述玩家可见的问题、你的设置和证据。欢迎在支持范围内提出建议 [想法](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas);可重现的缺陷属于 [问题](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose).

对于 DLL、本机代码、受保护操作或依赖于服务器的建议，明确标识依赖关系。在承诺实施之前，他们需要进行可行性工作并对受影响的系统进行适当的控制。请不要将它们归档为简单的缺失 DBC 选项。

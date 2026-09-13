<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- RELEASE-120-NOTICE -->
> **Setup 1.2.0** — 一个 ZIP 现在同时包含 Windows 安装程序和 Linux/Wine 启动器。界面会在十种选项中自动跟随操作系统语言，手动选择会被保存。游戏版本 3.0.8 和游戏文件没有变化，也没有 DBC 修改。
>
> 由于 Google HTTP 429，完整指南刷新仍在等待中。下方正文可能已过时；请以当前英文来源和 1.2.0 发布说明为准。 [English](../../../START-HERE.txt) · [1.2.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.2.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自动翻译。 [英文来源](../../../START-HERE.txt)。如果措辞不同，则以英文来源为准。

LAU 设置 — 释放 3.0.8

Windows：下载LauSetup.exe。
Linux/Wine：下载LauSetup-Wine.zip并关注其README.txt。
Wine 需要提供的 Linux 启动器；不要直接运行 EXE。

1。关闭World of Warcraft。
2。打开 LauSetup.exe 并选择您的 WoW 文件夹。
3。选择您的视觉效果并单击安装升级。

从旧版本或测试 v2 更新？首先下载新的安装程序；旧副本嵌入旧目录。
选择相同的客户端和视觉效果。文件哈希检查检测更改的补丁。
启动WoW并输入/pyversion；它应该报告 3.0.8 Lau。

安装程序会检测您的客户端语言和 HD 型号配置。
默认情况下选择增强奉献。取消选中库存
外观；咒语本身仍然有效。新的法术视觉效果需要
现有兼容高清型号客户端。升级地图/小地图是可选的。

您需要现有的 WoW 3.3.5a 客户端，在 Windows 10 或 11 上构建 12340。
此下载是升级，而不是完整的客户端或语言包。
所需的兼容 WoW.exe 会自动安装。

无需手动复制或重命名补丁。请勿下载整个
共享数据发布。该应用程序仅下载您选择所需的文件。

备份和可恢复下载保留在 WoW 内的 LauSetupBackups 中
文件夹，数据之外。要撤消更新，请关闭 WoW，重新打开 LauSetup.exe，
选择同一文件夹，然后单击恢复以前的安装。恢复也
如果更新中断导致 WoW.exe 暂时丢失，则可以使用。

您的插件、SavedVariables、字体、登录插图、领域设置和
不相关的补丁被保留。没有披萨勇士品牌，个人
捆绑 ElvUI 设置、LoginUI、帐户数据或完整游戏客户端。

下载来自GitHub Releases；不需要 GitHub 帐户。
如果下载停止，请稍后重试。已验证的文件
被重用并恢复部分下载。游戏文件仅在之后更改
所有必需的下载均已通过验证。如果保留 LauSetupBackups
该应用程序报告需要恢复。

此安装程序没有数字签名，因此 Windows 可能会显示未知发布者
警告。使用提供的校验和来验证您的下载。它不
需要禁用 Windows 安全性或安装 Python/PowerShell 工具。
需要 .NET Framework 4.8 运行时。

一旦此安装程序添加了地图升级，它就会在安装过程中保留该升级
版本变更。使用恢复之前的安装来撤消地图安装。

学分：Andre（Patch-Y 基线）、Loriendal 和 Trimitor（HD 基础）、
Project Reforged 贡献者（高清艺术作品），Blizzard（原创艺术作品和
本地化文本），Lau（适配、兼容性、指标、测试）。

Author / Creator / Last Modified By: Neil Mitchell

设置 1.1.7：新的拼写视觉效果关闭，使 Patch-S 保持为 .mpq.disabled 旁边
它原来的路径。不同的禁用副本永远不会被覆盖。
要撤消整个安装，请使用恢复之前的安装。对于文件
已被旧安装版本删除，请从这些备份中恢复它们
重新安装之前使用恢复以前的安装。保留LauSetupBackups。

当前的S文件始终变为.mpq.disabled。如果年纪较大的残疾人
副本存在，安装程序首先将其保留为 `.mpq.disabled.<12-character hash>`。无需手动重命名
需要切换选项。手动重新启用需要删除
.disabled 和任何后续哈希，WoW 关闭并且没有不同的活动
文件被覆盖。使用恢复以前的安装进行托管回滚。

1.1.7 修补程序：启用新拼写视觉效果可重复使用匹配的已禁用 Patch-S，而无需再次下载。即使活动 Patch-S 已匹配，普通禁用副本也会移至 LauSetupBackups 中经过验证的事务备份中。不同版本仍然可以通过恢复以前的安装来恢复。关闭仍然使用.mpq.disabled。现有的哈希后缀存档保持不变。

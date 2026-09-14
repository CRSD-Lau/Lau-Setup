<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

<!-- STABLE-140-CURRENT-GUIDE -->
> **当前版本：Setup 1.4.0 / 游戏 3.0.9 Lau。** 关闭 WoW，完整解压 LauSetup.zip，在 Windows 中打开 LauSetup.exe，用 Browse... 选择包含 WoW.exe 的文件夹。下一步 → 视觉选项 → 下一步 → 检查 → 安装 → 完成。所有额外选项默认关闭。WoW.exe 和加载画面是同一个选项；地图独立，并包含 WDM 支持文件。已安装的地图会保留。重命名的重复补丁保持原样；只有空的 Patch-V 会自动备份。被替换的文件保存在 LauSetupBackups 中。Patch-Y 没有 DBC 修改；可选地图添加了已记录来源的上游表。洞穴地图仍为测试版。Linux/Wine 请在文档要求的环境中使用 LauSetup.sh。Google HTTP 429 阻止了完整翻译更新。下面的旧内容仅供历史参考，当前操作请以英文原文为准。
>
> [English](../../../CONTRIBUTING.md) · [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自动翻译。 [英文来源](../../../CONTRIBUTING.md)。如果措辞不同，则以英文来源为准。

<a id="contributing-to-lau-setup"></a>

# 贡献给Lau Setup



感谢您帮助改进 Wrath 社区的安装和恢复。

<a id="community-roadmap"></a>

## 社区路线图

按照[社区路线图](https://github.com/users/CRSD-Lau/projects/2) 将工作视为问题，并通过 **Backlog**、**Ready**、**Inprogress**、**Testing** 和 **Done** 自动向董事会提供拉取请求。 **测试**卡包括验收清单并收集完成验证所需的证据；在提交问题之前使用[想法](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas) 讨论提案。 [发行说明](https://github.com/CRSD-Lau/Lau-Setup/releases) 保留每个版本中发布的内容的权威。

<a id="report-a-problem"></a>

## 报告问题

使用[错误报告表](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose)。包括安装程序版本、平台、客户端区域设置、选定的视觉效果、预期行为和重现步骤。对于游戏中的问题，请包括 `/pyversion`、Boss 或能力、难度和屏幕截图。 Wine 报告应包括 Wine 和 Wine Mono 版本。

从屏幕截图或摘录中删除帐户名、密码、令牌和个人路径。不要上传您的客户端、WTF 文件夹、SavedVariables 或整个日志。如果恢复待处理，请保留本地备份。

<a id="propose-a-change"></a>

## 提出更改

开始于 [已知的限制和假设](KNOWN-LIMITATIONS.md)。使用 [想法](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas) 寻求建议；在提出实现之前确定任何服务器、本机代码或受保护操作的依赖关系。

保持拉取请求的重点。解释用户可见的问题、更改以及您运行的检查。仅在孤立的装置中测试文件操作，切勿在活动的个人游戏客户端中测试文件操作。

保留存档允许列表、哈希检查、备份日志、进程检查和跨前缀锁定。请勿将更改游戏负载记录作为文档或界面更新的一部分。

[技术参考](docs/TECHNICAL.md) 解释了公共构建和需要私有本地固定装置的测试。在 PR 中明确区分成功的构建、夹具测试和实际游戏内验证。

<a id="artwork-and-attribution"></a>

## 作品和归属

保持已建立的 W 和屏蔽品牌和上游信用完好无损。包括拟议艺术品的来源和适用的权限。不要将个人客户状态引入公共资产。

<a id="dbc-release-records"></a>

## DBC 发布记录

每个游戏或安装程序版本都必须更新 [DBC-CHANGELOG.md](DBC-CHANGELOG.md) 并在其 GitHub 发行说明中包含 **DBC 更改**部分。对于实际的 DBC 编辑，列出表、记录 ID、命名字段和从零开始的索引、旧/新值、受影响的版本/区域设置和原因，以及之前/之后的哈希值和比较证据。对于未更改的 DBC，明确记录**无 DBC 编辑**。将几何、纹理和安装程序编辑与 DBC 更改分开。请参阅变更日志以了解所需的格式和验证边界。

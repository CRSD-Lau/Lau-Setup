<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

<!-- STABLE-140-CURRENT-GUIDE -->
> **当前版本：Setup 1.4.0 / 游戏 3.0.9 Lau。** 关闭 WoW，完整解压 LauSetup.zip，在 Windows 中打开 LauSetup.exe，用 Browse... 选择包含 WoW.exe 的文件夹。下一步 → 视觉选项 → 下一步 → 检查 → 安装 → 完成。所有额外选项默认关闭。WoW.exe 和加载画面是同一个选项；地图独立，并包含 WDM 支持文件。已安装的地图会保留。重命名的重复补丁保持原样；只有空的 Patch-V 会自动备份。被替换的文件保存在 LauSetupBackups 中。Patch-Y 没有 DBC 修改；可选地图添加了已记录来源的上游表。洞穴地图仍为测试版。Linux/Wine 请在文档要求的环境中使用 LauSetup.sh。Google HTTP 429 阻止了完整翻译更新。下面的旧内容仅供历史参考，当前操作请以英文原文为准。
>
> [English](../../../README.md) · [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自动翻译。 [英文来源](../../../README.md)。如果措辞不同，则以英文来源为准。

<p align="center">
  <a href="https://wrath-multilingual-hd.vercel.app/"><img src="../../assets/social-preview.png" alt="Wrath HD — gold W shield on an icy blue background" width="100%" /></a>
</p>

<h1 align="center">Lau Setup</h1>
<p align="center"><strong>你的客户。你的语言。你的Wrath。</strong><br />用于 Lau 可视化升级的 Windows 和 Linux/Wine 安装程序。</p>
<p align="center">
  <a href="https://github.com/CRSD-Lau/Lau-Setup/releases/latest">最新发布</a> ·
  <a href="https://wrath-multilingual-hd.vercel.app/">网站和画廊</a> ·
  <a href="https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose">报告问题</a> ·
  <a href="https://github.com/users/CRSD-Lau/projects/2">社区路线图</a>
</p>

---

多语言拼写文本、宽屏加载图稿、自定义地面指示器和可选的高清地图，用于 **WoW 3.3.5a，构建 12340**。选择您现有的客户和视觉效果； Lau Setup下载所需的文件，验证它们，放置补丁并备份原始文件。

**安装程序 1.1.7 · 游戏发行 3.0.8 Lau · 九种客户端语言**

<a id="patch-s-stays-recoverable"></a>

## Patch-S 保持可恢复

**设置 1.1.7 修补程序：**重新启用新拼写视觉效果重复使用匹配的禁用 Patch-S 并将普通禁用副本移至 `LauSetupBackups`，因此数据不会保留活动/禁用副本。事务备份中保留不同的副本。关闭仍然使用`.mpq.disabled`。使用 **恢复以前的安装** 进行恢复。

<a id="90-breath-and-slime-spray-warnings"></a>

## 90° 呼吸和粘液喷雾警告

**3.0.8 Lau：** 所有受支持的呼吸指示器和 Rotface Slime Spray 均为 **90° 总计**，经 Warmane 测试仪确认。涵盖两个领域的哈莱恩：萨维娜·怒火、萨萨里奥、ICC Rimefang 和辛达苟萨。范围和动画时间被保留。批准的较大哈利恩流星火半径和浅蓝色冷焰保持不变。

**已经安装？** 首先下载 **Setup 1.1.7**，选择相同的文件夹和视觉效果，然后安装。安装程序检查实际的 SHA-256 哈希值：即使是具有相同大小和时间戳的一字节更改也会被检测到。只有匹配的新文件才算作已安装。 `/pyversion` 报告 **3.0.8 Lau**。旧的安装程序保留旧的嵌入式目录。

[动画颜色预览和变更日志](https://wrath-multilingual-hd.vercel.app/#changelog)

<a id="download"></a>

## 下载

| Windows | Linux / Wine |
| :--- | :--- |
| **[下载LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)** | **[下载LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)** |
| Windows 10 / 11 · .NET 框架 4.8 | Wine 11.0 · Wine Mono 10.4.1 · 64-bit 前缀 |
|关于**156 KB** |关于 **80 KB** · Python 3.9+ |
| [Windows 指南](START-HERE.md) | [Wine 指南和先决条件](wine/README.md) |

在安装过程中下载游戏文件。英文核心安装是关于 **472 MB** 的高清模型和新的拼写视觉效果，或 **259 MB** 的原始模型。可选地图增加了更大的下载量；安装程序会在安装前显示总数。

[SHA-256 校验和](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/SHA256SUMS.txt) · [发行说明](https://github.com/CRSD-Lau/Lau-Setup/releases/latest) · [验证报告](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/VALIDATION.json)

> **带上您现有的客户端。** 这是升级，而不是完整的游戏客户端、语言包或高清模型库。 安装程序界面会在十种选项中自动跟随操作系统语言，手动选择会被保存。客户端游戏数据仍支持九种语言环境，并遵循检测到的游戏语言环境。

<a id="one-setup-the-details-handled"></a>

## 一种设置。细节处理好了。

|选择您的视觉效果 |控制您的安装 |
| :--- | :--- |
|加强或普通奉献|客户端语言和模型检测 |
|兼容高清客户端的新咒语视觉效果仅下载所需的文件 |
|可选的高清地图和小地图纹理| SHA-256 安装前验证 |
|区域宽屏加载图稿|自动备份和可断点下载 |
|本地化的法术名称、排名和工具提示 |恢复和中断操作恢复|

<p align="center"><img src="../../assets/installer-windows.png" alt="Lau Setup on Windows: choose a WoW folder, select visuals, install or restore" width="836" /></p>

您的插件、SavedVariables、字体、登录插图、领域设置和不相关的补丁保持不变。不包含个人用户界面、凭据或分析。

<a id="get-started"></a>

## 开始吧

1。 **完全关闭 WoW。** 在 Wine 上，关闭所有前缀上的每个 WoW 实例。
2。 **启动安装程序并选择您的客户端文件夹。** 将 `LauSetup.zip` 解压到 `LauSetup/` 文件夹。Windows 打开 `LauSetup.exe`；Linux/Wine 运行 `LauSetup.sh`。
3。 **选择您的视觉效果并安装。** 增强奉献开始选中；取消选中它以查看库存外观。新的法术视觉效果需要兼容的高清模型基础。地图是可选的。
4。 **启动 WoW 并运行 `/pyversion`。** 在进入游戏之前确认已安装的版本。

在 Linux 上，使用现有前缀从提取的文件夹中运行此命令：

```sh
WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh
```

作为普通用户使用启动器。它检查 Linux 路径、正在运行的游戏、可用空间和跨前缀的安装程序锁定。使用本地Linux存储；不支持链接文件夹、网络共享和 Windows 安装的驱动器。 [Wine 指南](wine/README.md) 列出了字体和所有先决条件。

在 Windows 上，如果缺少运行时，安装程​​序会提供 Microsoft 的官方 .NET Framework 4.8 下载页面。测试的 Wine 配置使用 **Wine Mono**，而不是 Windows .NET 安装程序。

<a id="nine-client-languages"></a>

## 九种客户端语言

英语 · 法语 · 德语 · 한국어 · Русский · 简体中文 · 繁体中文 · 西班牙语 (España) · 西班牙语 (México)

`enUS` · `frFR` · `deDE` · `koKR` · `ruRU` · `zhCN` · `zhTW` · `esES` · `esMX`

设置遵循客户端的活动区域设置。在更改配置之前安装适当的语言文件和字体。单独更改配置值不会安装语言包。

<a id="restore-with-your-backups"></a>

## 使用备份进行恢复

关闭 WoW，通过同一启动器重新打开安装程序，选择同一客户端并选择 **恢复以前的安装**。将 `LauSetupBackups` 保存在客户端文件夹内：它包含原始记录和恢复记录。

即使 `WoW.exe` 暂时丢失，也可以恢复中断的安装或恢复。如果另一个更新更改了已安装的文件，恢复将停止并保留备份以供解决。一旦此安装程序添加了地图升级，它就会在版本更改期间保留它；恢复以前的安装以撤消该升级。

<a id="tested-with-clear-limits"></a>

## 经过测试，有明确的限制

版本 1.1.7 通过了 Windows 和 Wine 上的 **50 回归组**，包括每个平台的 108 语言环境/版本/地图计划。游戏发布3.0.8此前在两个平台均通过了六版升级和一字节检测；它的有效负载没有改变。设置 1.1.7 还涵盖了从所有标志到新法术关闭序列，以及旧的禁用副本、重复切换和精确回滚。公共有效负载是匿名下载并经过哈希验证的；测试了实际的核心安装和回滚。

Wine 在本地 Linux 存储上使用 **Wine 11.0 / Wine Mono 10.4.1** 进行了测试，包括作为普通用户提供的启动器。 Halion 流星火几何形状与测试人员批准的 v2 完全匹配。 Coldflame、动画轨迹、原生火焰和法术表与 3.0.7 的字节保持相同。网站动画是说明性的模型。这些测试并不能证明每个 Linux 发行版或游戏中的遭遇。

此版本不包含 Lutris、Proton 和 macOS 集成。 可执行文件没有数字签名。

<a id="known-limitations-and-feature-requests"></a>

## 已知限制和功能请求

在建议功能之前，请阅读[已知限制和假设](KNOWN-LIMITATIONS.md)：Warmane 服务器控制、DLL/本机代码范围、受保护的 Lua 操作、指示器准确性和计时、DBC 依赖性以及平台/恢复限制。

<a id="for-contributors"></a>

## 对于贡献者

- [构建、存档放置和恢复设计](docs/TECHNICAL.md)
- [贡献和错误报告指导](CONTRIBUTING.md)
- [实施审查](REVIEW.md)
- [平台范围及可行性](PLATFORM-FEASIBILITY.md)

游戏有效负载通过 GitHub 版本进行分发。该存储库包含安装程序源、目录、启动器和文档；您不需要克隆它来安装升级。

<a id="built-on-community-work"></a>

## 以社区工作为基础

**Andre** — Patch-Y 基线 · **Loriendal 和 Trimitor** — 高清客户端基础 · **Project Reforged 贡献者** — 高清艺术作品 · **Blizzard** — 原创游戏、艺术作品和本地化文本 · **Lau** — 地面指示器、兼容性、适配、测试和发布工具。

[完整制作人员](https://wrath-multilingual-hd.vercel.app/credits) · [屏幕截图和安装帮助](https://wrath-multilingual-hd.vercel.app/)

<sub>非官方社区项目。不隶属于 Blizzard Entertainment，也不受其认可。原创游戏和第三方艺术品仍然是其各自所有者的财产。</sub>

<a id="dbc-change-tracking"></a>

## DBC 变更跟踪

请参阅 [DBC 变更日志](DBC-CHANGELOG.md) 了解各个表/记录/字段编辑和比较证据。 **3.0.7 → 3.0.8 没有 DBC 编辑**：90° 指标更新更改的模型几何形状。设置 1.1.5–1.1.7 也保持 DBC 数据不变。

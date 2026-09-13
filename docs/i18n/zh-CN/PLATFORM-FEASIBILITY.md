<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- RELEASE-120-NOTICE -->
> **Setup 1.2.0** — 一个 ZIP 现在同时包含 Windows 安装程序和 Linux/Wine 启动器。界面会在十种选项中自动跟随操作系统语言，手动选择会被保存。游戏版本 3.0.8 和游戏文件没有变化，也没有 DBC 修改。
>
> 由于 Google HTTP 429，完整指南刷新仍在等待中。下方正文可能已过时；请以当前英文来源和 1.2.0 发布说明为准。 [English](../../../PLATFORM-FEASIBILITY.md) · [1.2.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.2.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自动翻译。 [英文来源](../../../PLATFORM-FEASIBILITY.md)。如果措辞不同，则以英文来源为准。

<a id="lau-setup-platform-feasibility"></a>

# Lau Setup 平台可行性

作者：Neil Mitchell  
创建者： Neil Mitchell  
最后修改者：Neil Mitchell  
评估日期：2026-09-11

更新：用户仅选择了Wine。安装程序 1.1.0 现在提供经过测试的
Wine 11 / Wine Mono 10.4.1 启动器在 [Wine 指南](wine/README.md) 中描述。
下面的 Wine 8 探测和建议被保留为历史评估。
Lutris、Proton 和 macOS 集成仍然超出范围。

Lau Setup 1.0.1 仍然是 Windows 安装程序。 Linux 到 Wine 是推荐的下一个兼容性目标。此评估不证明在 Linux 或 macOS 上的安装。早期的 63 Docker/Wine 案例使用了游戏数据，而不是此安装程序。

|选项|推荐| Lau Setup 意味着什么 |
| --- | --- | --- |
| Wine 关于 Linux |第一个目标；原则上可行，目前未经验证|在明确选择的 Wine 前缀内重复使用 Windows 安装程序。在发布支持之前证明其运行时间、文件夹选择、下载、文件安全性和恢复。 |
|卢特里斯 |接下来直接Wine通过后|一个小的集成配方可以在现有游戏的前缀中启动设置。不需要单独的有效负载格式。 |
|蒸汽/质子 |以后有条件|使用正确的现有游戏前缀。添加设置作为另一个非 Steam 游戏可以给它一个不同的环境。 Steam Deck 可用性需要单独的屏幕和控制器检查。 |
| macOS 上的 CrossOver |看似合理的独立测试跑道|在游戏的瓶子里跑。在实际 macOS 硬件和支持的 CrossOver 版本上进行验证； Linux 测试无法证实这一点。 |
| Wine + DXVK |可选游戏配置| DXVK 为游戏翻译了 Direct3D。它不能解决安装程序的 .NET、字体或文件安全要求。 |
|威士忌|不采纳作为新的支持对象 |其上游项目不再积极维护。 |

上述分类遵循 [Wine Mono](https://github.com/wine-mono/wine-mono)、[Lutris](https://lutris.net/about/)、[Proton](https://github.com/ValveSoftware/Proton)、[DXVK](https://github.com/doitsujin/dxvk)、[CrossOver's 描述的角色Mac指南](https://support.codeweavers.com/en_US/crossover-mac-user-guide)和[威士忌](https://github.com/Whisky-App/Whisky)。建议是我们的评估，而不是 Lau Setup 的上游认证。 CrossOver 可以在 64-bit 瓶子中运行 32-bit Windows 应用程序；仅失去原生 macOS 32-bit 支持并不能排除这种情况。

<a id="bounded-probe-results"></a>

## 有界探测结果

本地探针使用Wine 8.0（Debian 8.0~repack-4），一个隔离的win32前缀和Xvfb。这个较旧的本地可用运行时不是对当前 Wine 版本的测试。未安装或修改个人游戏客户端。

1。继承的游戏测试图像禁用了 mscoree。启用它暴露了这一点 Wine Mono 失踪了。这是一个测试环境问题。
2。安装了官方的 Wine Mono 7.4.0 验证后一次性前缀中的 MSI SHA-256 `6413ff328ebbf7ec7689c648feb3546d8102ded865079d1fbf0331b14b3ab0ec`，固定于 [Wine 8.0的来源](https://raw.githubusercontent.com/wine-mirror/wine/wine-8.0/dlls/appwiz.cpl/addons.c).
3。诊断工具已初始化 WinForms 并加载嵌入的目录，然后无法构建表单 `System.ArgumentException: The requested FontFamily could not be found [GDI+ status: FontFamilyNotFound]`。将可用的 Liberation 字体复制到该前缀并不能解决问题。没有成功的安装程序屏幕截图或安装结果。
4。当地证据保留在 `reports/wine-feasibility/`。探针容器已停止。诊断工具不包含在分布式安装程序或公共源包中。

这标识了运行时/字体配置工作，而不是证明 Wine 是不可能的。在此探测器中的 Wine 下未尝试安装/恢复事务。

<a id="acceptance-work-before-wine-support"></a>

## Wine 支持前的验收工作

1。建立可重现的电流 Wine/运行时/字体组合 Linux 桌面。以常见的显示比例显示初始、就绪、下载、恢复和错误状态；验证键盘访问和文件夹选择。
2。验证区分大小写的文件系统上的准确主机文件夹映射和大小写处理，包括仅大小写不同的重复名称。保留不相关的补丁和个人设置。
3。证明链接、独占锁、可用空间、日志和原子替换行为。安装程序当前调用 Windows 文件信息 API；它们的语义必须在以下条件下进行测试 Wine 而不是假设的。
4。证明跨前缀的运行游戏守卫。当前代码枚举 Windows 处理并比较可执行目录。 Wine 前缀可见性可能会使运行同一客户端的另一个前缀未被检测到。在提供安全安装支持之前解决此问题；仅成功的相同前缀测试是不够的。
5。运行夹具安装/恢复和中断恢复矩阵，然后运行一个干净的匿名 GitHub 使用确切的发布资产下载/安装/回滚。测试 TLS、重定向、恢复、取消和离线恢复。
6。随后在同一受支持的环境中进行游戏内检查。然后才发布 Wine 说明和 Lutris 集成。保持 Proton 和 macOS 明确未经验证，直到它们自己的检查通过。

在 GitHub 版本上保留一组不可变的游戏资产。不要将完整的客户端、个人 UI 或每个有效负载的副本添加到 Git 存储库以启用另一个启动器。如果 Wine 无法可靠地满足安全检查，请围绕相同的清单和事务规则评估本机 Linux 安装程序作为单独的实现。

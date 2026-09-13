<!-- LANGUAGES:START -->
[English](../../../../README.md) · [Deutsch](../../de/README.md) · [Español (España)](../../es-ES/README.md) · [Español (México)](../../es-MX/README.md) · [Français](../../fr/README.md) · [한국어](../../ko/README.md) · [Русский](../../ru/README.md) · [简体中文](../README.md) · [繁體中文](../../zh-TW/README.md) · [Português (Brasil)](../../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.4.0** — 一个 ZIP 现在同时包含 Windows 安装程序和 Linux/Wine 启动器。界面会在十种选项中自动跟随操作系统语言，手动选择会被保存。游戏版本 3.0.8 和游戏文件没有变化，也没有 DBC 修改。
>
> 由于 Google HTTP 429，完整指南刷新仍在等待中。下方正文可能已过时；请以当前英文来源和 1.4.0 发布说明为准。 [English](../../../../wine/README.txt) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)
>
> **当前下载：** Windows 和 Linux/Wine 都使用 [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)。解压含五个文件的 `LauSetup/` 文件夹：Windows 打开 `LauSetup.exe`；Linux/Wine 运行 `LauSetup.sh`。下方关于单独 EXE 或 Wine ZIP 的旧说明不适用于 1.4.0。
>
> **1.4.0:** 已识别的额外升级文件会自动备份，然后继续安装。恢复操作会将文件放回原位。无需手动移动。 安装程序在替换或移动现有文件之前会自动保留原文件。无关文件保持不变。



> **1.4.0:** 选择游戏文件夹 → 下一步 → 选择视觉效果 → 下一步 → 确认 → 安装升级 → 完成。根据检测到的客户端固定选择 Patch-Y HD 或 Patch-Y Non-HD。额外选项默认关闭；已安装的地图升级会保留。确认页列出 Patch-Y（Lau 版本）及所选额外内容、WoW.exe、Patch-Q、语言文件、下载大小和备份。下一步不会更改游戏文件。每一步都可手动选择界面语言并保存；自动会重新使用系统语言。仍可使用恢复上次安装。

<!-- BEGINNER-140-STEPS -->


选择游戏文件夹 → 下一步 → 选择视觉效果 → 下一步 → 确认 → 安装升级 → 完成。根据检测到的客户端固定选择 Patch-Y HD 或 Patch-Y Non-HD。额外选项默认关闭；已安装的地图升级会保留。确认页列出 Patch-Y（Lau 版本）及所选额外内容、WoW.exe、Patch-Q、语言文件、下载大小和备份。下一步不会更改游戏文件。每一步都可手动选择界面语言并保存；自动会重新使用系统语言。仍可使用恢复上次安装。

Linux/Wine: Wine 11.0, Wine Mono 10.4.1, Python 3.9+, 64-bit WINEPREFIX. `WINEPREFIX="/path/to/prefix" sh LauSetup.sh`. [Guide](https://github.com/CRSD-Lau/Lau-Setup/blob/main/wine/README.txt).

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自动翻译。 [英文来源](../../../../wine/README.txt)。如果措辞不同，则以英文来源为准。

Lau Setup 用于 Linux 上的 Wine
Author / Creator / Last Modified By: Neil Mitchell

1。在本地 Linux 文件系统上使用现有的 WoW 3.3.5a 构建 12340 客户端。
2。关闭每个 WoW 实例，包括其他 Wine 前缀的游戏。
3。解压 `LauSetup.zip`。将 `LauSetup/` 中的五个文件放在一起：`LauSetup.exe`、`LauSetup.sh`、`lau_wine.py`、`lau-languages.json` 和 `README.txt`。
4。在提取的文件夹中打开终端并运行：

```sh
WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh
```

5。选择您现有的游戏文件夹并安装。常见的自动备份
   和恢复以前的安装按钮可用。

此版本的要求：
- Wine 11.0、64-bit 前缀和 Wine Mono 10.4.1 已安装在那里。
- 用于主机安全助手的 Python 3.9 或更新版本（仅限标准库）。
- Liberation Sans 或 DejaVu Sans 字体；完整的Wine字体包必须
  也可以安装Wine Mono自己的默认控件来渲染。
- 本地 Linux 存储。网络共享和 Windows 安装的驱动器不包括在内。
- 正常主机进程可见性。不要通过沙箱运行此启动器
  隐藏其他 Wine 进程。以普通用户身份运行，切勿使用 sudo/root。

64-bit 前缀可以包含 32-bit WoW 客户端。该安装程序不
创建、转换或升级您的 Wine 前缀，安装 Wine/Mono，配置
DXVK，或更改您的游戏启动器。使用您的发行版的 Wine 设置
如果缺少运行时，请先执行指令。

此测试运行时的官方 Wine Mono 包：
https://github.com/wine-mono/wine-mono/releases/tag/wine-mono-10.4.1

将 Wine Mono 运行时与 Wine 结合使用。 Windows .NET Framework 安装程序是
未捆绑，且此测试 Wine Mono 配置不需要。

始终通过 LauSetup.sh 启动。直接在Wine下运行LauSetup.exe
如果没有 Linux 帮助程序，将拒绝客户端操作。它检查主机路径
并处理并持有跨 Wine 前缀共享的主机锁。如果它停止了，
重新打开启动器并恢复挂起的安装，然后重试。

保持 WoW 关闭，直到安装完成。流程检查减少竞争；他们不能
阻止其他程序启动游戏或随后更改文件。
符号链接路径、硬链接和不明确的文件名大小写都会被拒绝。数据
备份目录必须与客户端保留在同一文件系统上。

验证范围：隔离 Wine 11.0 / Wine Mono 10.4.1 客户端、夹具和
真实有效负载安装/恢复测试、双前缀安全测试和采样 GUI
检查。这并不是每个 Linux 发行版、文件系统的认证，
显示比例，Wine版本，或者游戏遭遇。没有 Lutris、Proton 或 macOS
此版本中包含集成。

安装程序界面会在十种选项中自动跟随操作系统语言，手动选择会被保存。客户端游戏数据仍支持九种语言环境，并遵循检测到的游戏语言环境。

设置 1.1.7：新的拼写视觉效果关闭，使 Patch-S 保持为 .mpq.disabled 旁边
它原来的路径。不同的禁用副本永远不会被覆盖。
要撤消整个安装，请使用恢复之前的安装。对于文件
已被旧安装版本删除，请从这些备份中恢复它们
重新安装之前使用恢复以前的安装。保留 LauSetupBackups。

当前的S文件始终变为.mpq.disabled。如果年纪较大的残疾人
副本存在，安装程序首先将其保留为 `.mpq.disabled.<12-character hash>`。无需手动重命名
需要切换选项。手动重新启用需要删除
.disabled 和任何后续哈希，WoW 关闭并且没有不同的活动
文件被覆盖。使用恢复以前的安装进行托管回滚。

1.1.7 重新启用清理：匹配禁用的 Patch-S 在本地重用。普通禁用副本将移动到 LauSetupBackups 中经过验证的事务备份，留下一个活动 S。不同的副本仍然可以通过恢复之前的安装进行恢复。现有的哈希后缀存档不会被清除。

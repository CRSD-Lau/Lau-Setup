<!-- LANGUAGES:START -->
[English](../../../../README.md) · [Deutsch](../../de/README.md) · [Español (España)](../../es-ES/README.md) · [Español (México)](../../es-MX/README.md) · [Français](../../fr/README.md) · [한국어](../../ko/README.md) · [Русский](../../ru/README.md) · [简体中文](../README.md) · [繁體中文](../../zh-TW/README.md) · [Português (Brasil)](../../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- RELEASE-120-NOTICE -->
> **Setup 1.2.0** — 一个 ZIP 现在同时包含 Windows 安装程序和 Linux/Wine 启动器。界面会在十种选项中自动跟随操作系统语言，手动选择会被保存。游戏版本 3.0.8 和游戏文件没有变化，也没有 DBC 修改。
>
> 由于 Google HTTP 429，完整指南刷新仍在等待中。下方正文可能已过时；请以当前英文来源和 1.2.0 发布说明为准。 [English](../../../TECHNICAL.md) · [1.2.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.2.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自动翻译。 [英文来源](../../../TECHNICAL.md)。如果措辞不同，则以英文来源为准。

<a id="technical-reference"></a>

# 技术参考



[返回Lau Setup](../README.md)

<a id="build-and-verification"></a>

## 构建和验证

在安装了 .NET Framework 编译器的 Windows 上运行 `tools/build.ps1`。公共源包包含应用程序、嵌入式目录、构建脚本和文档。完整的开发检查还包含 `tools/test.ps1`，用于事务、下载、路径、进程、恢复和 GUI 回归测试；这些测试使用隔离的装置和本地参考可执行文件。 `tools/build.ps1 -Release` 拒绝未通过出版门的目录。测试工具、有效负载生成和本机游戏测试依赖于私有本地源路径，而不是公共源包的一部分。

`build/catalog.json` 按大小和 SHA-256 命名每个资产和下载段，以及观察到的 GitHub 发布 URL。该目录固定存储库、发布标签和散列命名的文件。安装程序会匿名下载并在遵循每个重定向之前检查它。安装程序不需要 GitHub 帐户、登录浏览器或 API 凭据。在完整的开发检查中，`tools/refresh_github_catalog.py` 在不更改哈希值的情况下关联上传的资产，并且 `tools/verify-public.ps1` 通过应用程序使用的同一下载器验证每个分段和重建的资产。

<a id="file-placement"></a>

## 文件放置

|组件|目的地 |
|---|---|
|兼容的可执行文件 | `WoW.exe` |
|选定区域Q |根 `Data/patch-q.mpq` 和活动区域设置 `Data/<locale>/patch-<locale>-Q.MPQ` 中的相同副本 |
|选定版本 Y |根 `Data/patch-y.mpq` 和活动区域设置 `Data/<locale>/patch-<locale>-Y.MPQ` 中的相同副本 |
|新法术资源（选择时）|根 `Data/patch-s.mpq` |
|匹配本地化拼写表（选择时）|活动区域设置 `Data/<locale>/patch-<locale>-S.MPQ` |
|可选地图/小地图 |根`Data/patch-m.mpq`；已备份被取代的活动区域设置 M |

Core Q 保留了该版本的 LoadingScreens.dbc、本地化的 Map.dbc 和逐字节加载图像。它省略了添加的世界地图定义和世界地图图稿。全地图模式使用原有的区域Q和共享M，无需重新打包。两个 S 位置包含不同的档案。关闭新拼写会将作用域根/区域设置 S 对保留为 .mpq.disabled；重新启用会将普通禁用的副本移至经过验证的事务备份中，如下面的设置 1.1.7 部分所述。 HD 检测需要匹配现有的根和区域设置 F 补丁。

<a id="recovery-design"></a>

## 恢复设计

一款客户端锁涵盖下载、暂存和安装。文件在暂存前进行验证，并在放置后再次进行验证。现有文件移至 `LauSetupBackups/transactions/<id>/before/`，保留其字节和时间戳；日志在提交之前持久写入。失败的提交会在安全时恢复原始版本。重新打开应用程序时，即使没有 WoW.exe，中断的提交和中断的恢复仍然可以发现。

恢复拒绝由其他更新更改的文件并保留备份以供手动解决。仅接受精确的 root/active-locale Q/M/S/Y 路径和 WoW.exe。遍历、替代流和重分析点被拒绝；可写恢复文件必须有一个硬链接。日志和程序集临时文件使用独特的名称和独家创建。应用程序永远不会将存档枚举到客户端文件系统中。

<a id="release-boundaries"></a>

## 释放边界

此安装程序没有数字签名。 Windows 和 Wine 安装程序测试、采样 GUI 检查和保留的游戏数据基线分别记录在 VALIDATION.json 中。 Wine 1.1.0 检查使用 Wine 11.0 / Wine Mono 10.4.1 和本地 Docker 覆盖存储；嵌套安装测试模拟设备身份，因为该容器无法创建安装。这些检查并不验证每个 Linux 发行版/文件系统、显示比例、遭遇或第三方客户端修改。原始 Patch-Y 版本 ZIP 可在 GitHub 版本上获取。有关当前范围和假设，请参阅[已知限制](../KNOWN-LIMITATIONS.md)。


<a id="306-color-update--setup-112"></a>

## 3.0.6 颜色更新/设置 1.1.2

六个 Y 档案中的每一个都会更改三个 M2 成员和 !PYAndre TOC，并添加两个 BLP 纹理。 `Spells/PW_Coldflame_Ground.m2` 现在引用 `Spells/PW_Coldflame_Blue.blp`； `Spells/PW_HalionMeteor_Ground.m2` 和 `Spells/PW_HalionMeteor_Ring.m2` 参考 `Spells/PW_Halion_Red.blp`。每个原始模型中只有纹理描述符 4 的文件名长度/偏移量发生变化；新路径已附加。原生粒子纹理（索引 0–3）、皮肤、几何体、全局动画轨迹、边界和 DBC 字节保持不变。其他指标的共享白色纹理保持不变。

新纹理保留了现有的不透明 8×8 DXT1 BLP2 格式和所有四个 mip 级别。仅 RGB565 端点发生变化：浅蓝色解码为 (120,216,248,255)，红色解码为 (248,68,40,255)。量化是现有纹理格式所固有的。两种 Halion 型号均使用相同的红色纹理。奉献和模型版本的选择保持独立。

更新决策会比较实际的 SHA-256 和大小，而不是发布标签或时间戳。回归测试在每个 Y 放置中修改一个字节而不更改文件大小或时间戳，只需要一次修复操作，验证修复的哈希，然后恢复以前的版本。旧的 EXE 嵌入旧目录，因此升级需要先下载新的 EXE/ZIP。

<a id="307-halion-radius--setup-113"></a>

## 3.0.7 Halion 半径/设置 1.1.3

提升 `Spells/PW_HalionMeteor_Ground.m2`、`Spells/PW_HalionMeteor_Ring.m2` 及其 `00.skin` 文件的精确 test-v2 字节。网格 X/Y 坐标为 1.5 乘以 3.0.6。 Z/UV/法线和动画/粒子轨迹被保留。模型边界（偏移 160）、序列边界（序列 +32）和皮肤子网格边界（子网格 +20）反映放大的几何体。 TOC版本从3.0.6更改为3.0.7。每个版本恰好有五个现有成员发生变化；没有添加或删除成员。测试 v3 几何体被排除。 Coldflame 和所有其他成员均匹配 3.0.6。用户转发测试人员对 v2 的接受；不主张广泛遭遇认证。

<a id="308-all-cones--setup-114"></a>

## 3.0.8 所有锥体/设置 1.1.4

所有六个版本均使用 90 度总风扇几何形状。旧模型文件名和所有 DBC 行保持不变，以保留拼写路由。更改：PW_White_Fan60_60yd_Glowing（Halion 两个领域）、PW_White_Fan60_30yd_Glowing（Saviana）、PW_White_Fan60_100y_Glowing（ICC Rimefang）和 PW_Rotface_SlimeSpray_Fan25_Room（Rotface）从60 至 90； PW_White_Fan82_60yd_Glowing (Sartharion) 从 82 扩大到 90。 PW_White_Fan75_60yd_Glowing (Sindragosa) 已经是 90 并且字节相同。

对于每个修改后的模型，仅顶点 XY（48 字节顶点步幅）和边界发生变化。关于+X刻度的角度由90/old-angle;每个顶点半径和 Z 都被保留。更新偏移量 160 处的模型边界、序列+32 处的序列边界以及子网格+20 处的皮肤子网格边界。 UV、法线、动画和粒子轨迹保持不变。每个版本的 TOC 中有 10 个模型/皮肤成员和两个版本字符串发生变化；不添加或删除任何成员。所有其他成员，包括 Halion Meteor-Fire Test-v2 Geometry 和 Coldflame，都逐字节匹配 3.0.7。

<a id="setup-115-disabled-patch-s-preservation"></a>

##设置1.1.5禁用Patch-S保存

只有根路径和活动区域设置 S 路径才会获得 .disabled 后缀。每次禁用都会在停用 S 之前创建一个哈希固定的本地暂存副本；两条路径都会被记录，最多有十一个目的地。回滚可恢复原始活动文件并仅删除新创建的禁用副本。先前存在的相同禁用副本保留在事务之外并被保留。冲突的文件或目录会阻碍规划。重新启用会安装目录 S 资产，并且不会消耗已禁用的副本。现有期刊仍然可读。不接受任意本地源路径：每个本地副本必须与其配对的 S 停用操作相匹配。

<a id="setup-116-disabled-copy-collisions"></a>

## 设置 1.1.6 禁用复制冲突

当前活动的 S 文件始终采用纯 .mpq.disabled 名称。在替换不同的现有禁用文件之前，安装程序将其字节放入以其 SHA-256 的第一个 12 字符结尾的同级文件中；在重新使用之前会检查完整的 SHA-256 和长度。这会将名称保留在现有的 Windows 路径限制内。冲突的存档内容无法关闭。活动 S、普通禁用文件和新创建的存档副本独立记录，最多有 13 个条目；回滚恢复所有原始数据。本地源仅限于配对 S 停用或禁用文件替换操作。旧期刊仍然可读。

<a id="setup-117-re-enable-cleanup"></a>

## 设置 1.1.7 重新启用清理

启用新拼写日志删除普通根和活动区域设置禁用的 S 文件。事务将其经过验证的原始字节移动到数据之外的备份之前。如果禁用的文件与目录 SHA-256 和大小匹配，则会在本地暂存以匹配 S 目标并从下载中排除。本地源必须与确切的禁用文件删除和目录资源配对。已匹配的 Active S 仍会产生清理事务。现有的哈希后缀存档不会被清除。以前的期刊仍然可读。开/关/开、源漂移、每个新提交/恢复步骤的中断、所有区域设置和堆叠恢复都涵盖在内。

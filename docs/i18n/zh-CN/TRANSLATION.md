<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — 一个 ZIP 现在同时包含 Windows 安装程序和 Linux/Wine 启动器。界面会在十种选项中自动跟随操作系统语言，手动选择会被保存。游戏版本 3.0.8 和游戏文件没有变化，也没有 DBC 修改。
>
> 由于 Google HTTP 429，完整指南刷新仍在等待中。下方正文可能已过时；请以当前英文来源和 1.3.0 发布说明为准。 [English](../../../TRANSLATION.md) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
>
> **当前下载：** Windows 和 Linux/Wine 都使用 [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)。解压含五个文件的 `LauSetup/` 文件夹：Windows 打开 `LauSetup.exe`；Linux/Wine 运行 `LauSetup.sh`。下方关于单独 EXE 或 Wine ZIP 的旧说明不适用于 1.3.0。
>
> **1.3.0:** 已识别的额外升级文件会自动备份，然后继续安装。恢复操作会将文件放回原位。无需手动移动。 安装程序在替换或移动现有文件之前会自动保留原文件。无关文件保持不变。

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自动翻译。 [英文来源](../../../TRANSLATION.md)。如果措辞不同，则以英文来源为准。

<a id="repository-translations"></a>

# 存储库翻译

**翻译文档** GitHub Action 使用 **Google Translate 的免费网站** 来保存每种受支持游戏语言以及 **巴西葡萄牙语** 的存储库文档。无需 API 密钥、付费云翻译帐户、订阅或模型下载。

使用自述文件顶部的语言链接。 GitHub 默认显示根README；访问者使用这些链接选择他们的语言。此工作流程翻译文档，包括安装指南和技术参考。它不会翻译 GitHub 的界面、问题、发布说明、单独的网站或安装程序界面，并且不会添加葡萄牙语游戏区域设置。

<a id="languages"></a>

## 语言

根据 `build/catalog.json` 检查覆盖范围，并添加 `ptBR` 作为文档。阅读选项包括英语、德语、西班牙语（西班牙和墨西哥）、法语、韩语、俄语、简体中文、繁体中文和巴西葡萄牙语。

Google 的网络语言选择器将 `pt` 识别为葡萄牙语（巴西）；葡萄牙语（葡萄牙）是一个不同的目标。 Google 提供了一个 `es` 目标，因此西班牙和墨西哥页面使用相同的通用西班牙语翻译。中国的目标是不同的。 Google 目标代码和本地语言名称位于 `tools/translation-locales.json` 中。添加游戏语言环境需要添加其文档映射；缺少覆盖范围无法验证。

<a id="automatic-updates"></a>

## 自动更新

推送更改的英文文档、目录或翻译工具触发操作。维护人员还可以选择 **操作 → 翻译文档 → 运行工作流程 → 主要**。它会在存储库根目录和 `docs/` 以及 `wine/README.txt` 中发现跟踪的 Markdown 和文本文件。生成的翻译和 `AGENTS.md` 被排除在外。文本指南在 `docs/i18n/<language>/` 下呈现为 Markdown。

只有更改的文件才需要翻译。源和输出哈希以及段缓存可避免重复请求。更改翻译约定时碰撞 `TRANSLATION_REVISION`。最多同时运行三种语言作业，每个作业的请求之间有一个暂停。速率限制会停止受影响的作业；稍后重试。免费的网络界面对于自动化来说是非官方的，可以更改或阻止请求。没有付费后备方案。当生成失败时，现有的已发布页面仍然可用。

标准 GitHub 托管的运行器执行对于此公共存储库是免费的。如果存储库变为私有，作业将被禁用。小型中间工件一天后就会过期；不存储模型或大的依赖关系。

<a id="integrity-and-publication"></a>

## 完整性和发布

代码、命令、URL、版本号、产品名称、信用和签名状态声明均受到保护。相关文档链接指向相同语言，而图像和代码链接则指向原文。稳定的英文标题锚保留部分链接。每个页面都将自己标识为自动翻译，链接到其英文源，并保留 **Neil Mitchell** 的作者、创建者和最后修改者元数据。

所有九个翻译阅读选项在发布到 `main` 之前必须通过源/输出完整性检查。出版物拒绝更改源修订版，并且从不强制推送。拉取请求运行单元检查和具有只读访问权限的真正的巴西葡萄牙语自述文件烟雾翻译。如果分支保护稍后阻止提交，请调整发布以适应批准的 PR 流程。

机器翻译仍然需要流利的读者审查。英语依然具有权威性。对于持久的更正，更新英文源或翻译工具；对生成文件的直接编辑将重新生成。失败或部分批次不会替换现有文档。

<a id="local-use"></a>

## 本地使用

Python 3.11 或更新版本就足够了；不需要额外的包。在没有网络访问的情况下检查结构：

```sh
python -m unittest discover -s tests -p test_translate_docs.py -v
python tools/translate_docs.py --check
```

使用免费的 Google 网站翻译公共文档：

```sh
python tools/translate_docs.py --locale ptBR
python tools/translate_docs.py --navigation
```

参考文献：[Google 翻译](https://translate.google.com/)、[GitHub 操作计费](https://docs.github.com/en/billing/concepts/product-billing/github-actions)。单独的 [Google Cloud Translation API](https://cloud.google.com/translate/pricing) 是一项收费服务，此处不使用。

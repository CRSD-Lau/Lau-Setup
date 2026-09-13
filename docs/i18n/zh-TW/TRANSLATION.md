<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — 一個 ZIP 現在同時包含 Windows 安裝程式和 Linux/Wine 啟動器。介面會在十種選項中自動跟隨作業系統語言，手動選擇會被儲存。遊戲版本 3.0.8 和遊戲檔案均未變更，也沒有 DBC 修改。
>
> 由於 Google HTTP 429，完整指南更新仍在等待中。下方正文可能已過時；請以目前英文來源和 1.3.0 發行說明為準。 [English](../../../TRANSLATION.md) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
>
> **目前下載：** Windows 和 Linux/Wine 都使用 [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)。解壓含五個檔案的 `LauSetup/` 資料夾：Windows 開啟 `LauSetup.exe`；Linux/Wine 執行 `LauSetup.sh`。下方關於個別 EXE 或 Wine ZIP 的舊說明不適用於 1.3.0。
>
> **1.3.0:** 已識別的額外升級檔案會自動備份，然後繼續安裝。還原操作會將檔案放回原位。無需手動移動。 安裝程式在替換或移動現有檔案之前會自動保留原檔案。無關檔案保持不變。

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自動翻譯。 [英文來源](../../../TRANSLATION.md)。若措詞不同，則以英文來源為準。

<a id="repository-translations"></a>

# 儲存庫翻譯

**翻譯文件** GitHub Action 使用 **Google Translate 的免費網站** 來保存每種受支援遊戲語言以及 **巴西葡萄牙語** 的儲存庫文件。無需 API 金鑰、付費雲端翻譯帳戶、訂閱或模型下載。

使用自述文件頂部的語言連結。 GitHub 預設顯示根README；訪客使用這些連結選擇他們的語言。此工作流程翻譯文檔，包括安裝指南和技術參考。它不會翻譯 GitHub 的介面、問題、發布說明、單獨的網站或安裝程式介面，並且不會添加葡萄牙語遊戲區域設定。

<a id="languages"></a>

## 語言

根據 `build/catalog.json` 檢查覆蓋範圍，並新增 `ptBR` 作為文件。閱讀選項包括英語、德語、西班牙語（西班牙和墨西哥）、法語、韓語、俄語、簡體中文、繁體中文和巴西葡萄牙語。

Google 的網路語言選擇器將 `pt` 識別為葡萄牙語（巴西）；葡萄牙語（葡萄牙）是一個不同的目標。 Google 提供了一個 `es` 目標，因此西班牙和墨西哥頁面使用相同的通用西班牙語翻譯。中國的目標是不同的。 Google 目標程式碼和本地語言名稱位於 `tools/translation-locales.json` 中。新增遊戲語言環境需要新增其文件映射；缺少覆蓋範圍無法驗證。

<a id="automatic-updates"></a>

## 自動更新

推送更改的英文文件、目錄或翻譯工具觸發操作。維護人員也可以選擇 **操作 → 翻譯文件 → 運行工作流程 → 主要**。它會在儲存庫根目錄和 `docs/` 以及 `wine/README.txt` 中發現追蹤的 Markdown 和文字檔案。產生的翻譯和 `AGENTS.md` 被排除在外。文本指南在 `docs/i18n/<language>/` 下呈現為 Markdown。

只有更改的檔案才需要翻譯。來源和輸出哈希以及段快取可避免重複請求。更改翻譯約定時碰撞 `TRANSLATION_REVISION`。最多同時執行三種語言作業，每個作業的請求之間有一個暫停。速率限制會停止受影響的作業；稍後重試。免費的網頁介面對於自動化來說是非官方的，可以更改或阻止請求。沒有付費後備方案。當產生失敗時，現有的已發布頁面仍然可用。

標準 GitHub 託管的運行器執行對於此公共儲存庫是免費的。如果儲存庫變成私有，作業將會被停用。小型中間工件一天後就會過期；不儲存模型或大的依賴關係。

<a id="integrity-and-publication"></a>

## 完整性和發布

代碼、命令、URL、版本號、產品名稱、信用和簽名狀態聲明均受到保護。相關文檔連結指向相同語言，而圖像和程式碼連結則指向原文。穩定的英文標題錨保留部分連結。每個頁面都將自己標識為自動翻譯，連結到其英文來源，並保留 **Neil Mitchell** 的作者、創建者和最後修改者元資料。

所有九個翻譯閱讀選項在發佈到 `main` 之前必須通過來源/輸出完整性檢查。出版物拒絕更改來源修訂版，並且從不強制推送。拉取請求運行單元檢查和具有唯讀存取權限的真正的巴西葡萄牙語自述文件煙霧翻譯。如果分支保護稍後阻止提交，請調整發布以適應已批准的 PR 流程。

機器翻譯仍然需要流利的讀者審查。英語依然具有權威性。對於持久的更正，更新英文來源或翻譯工具；對生成文件的直接編輯將重新生成。失敗或部分批次不會取代現有文件。

<a id="local-use"></a>

## 本機使用

Python 3.11 或更新版本就足夠了；不需要額外的套件。在沒有網路存取的情況下檢查結構：

```sh
python -m unittest discover -s tests -p test_translate_docs.py -v
python tools/translate_docs.py --check
```

使用免費的 Google 網站翻譯公共文件：

```sh
python tools/translate_docs.py --locale ptBR
python tools/translate_docs.py --navigation
```

參考文獻：[Google 翻譯](https://translate.google.com/)、[GitHub 操作計費](https://docs.github.com/en/billing/concepts/product-billing/github-actions)。單獨的 [Google Cloud Translation API](https://cloud.google.com/translate/pricing) 是一項收費服務，此處不使用。

<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自動翻譯。 [英文來源](../../../CONTRIBUTING.md)。若措詞不同，則以英文來源為準。

<a id="contributing-to-lau-setup"></a>

# 貢獻給Lau Setup



感謝您協助改進 Wrath 社群的安裝和恢復。

<a id="report-a-problem"></a>

## 回報問題

使用[錯誤報告表](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose)。包括安裝程式版本、平台、用戶端區域設定、選定的視覺效果、預期行為和重現步驟。對於遊戲中的問題，請包括 `/pyversion`、Boss 或能力、難度和螢幕截圖。 Wine 報告應包括 Wine 和 Wine Mono 版本。

從螢幕截圖或摘錄中刪除帳戶名稱、密碼、令牌和個人路徑。不要上傳您的客戶端、WTF 資料夾、SavedVariables 或整個日誌。如果恢復待處理，請保留本機備份。

<a id="propose-a-change"></a>

## 提出更改

開始於 [已知的限制和假設](KNOWN-LIMITATIONS.md)。使用 [想法](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas) 尋求建議；在提出實作之前確定任何伺服器、本機程式碼或受保護操作的依賴關係。

保持拉取請求的重點。解釋使用者可見的問題、變更以及您正在執行的檢查。僅在孤立的裝置中測試檔案操作，切勿在活動的個人遊戲用戶端中測試檔案操作。

保留存檔允許清單、雜湊檢查、備份日誌、進程檢查和跨前綴鎖定。請勿將更改遊戲負載記錄作為文件或介面更新的一部分。

[技術參考](docs/TECHNICAL.md) 解釋了公共建置和需要私有本地固定裝置的測試。在 PR 中明確區分成功的建置、夾具測試和實際遊戲內驗證。

<a id="artwork-and-attribution"></a>

## 作品和归属

保持已建立的 W 和屏蔽品牌和上游信用完好無損。包括擬議藝術品的來源和適用的權限。不要將個人客戶狀態引入公共資產。

<a id="dbc-release-records"></a>

## DBC 發布記錄

每個遊戲或安裝程式版本都必須更新 [DBC-CHANGELOG.md](DBC-CHANGELOG.md) 並在其 GitHub 發行說明中包含 **DBC 變更**部分。對於實際的 DBC 編輯，列出表格、記錄 ID、命名欄位和從零開始的索引、舊/新值、受影響的版本/區域設定和原因，以及之前/之後的雜湊值和比較證據。對於未更改的 DBC，明確記錄**無 DBC 編輯**。將幾何、紋理和安裝程式編輯與 DBC 變更分開。請參閱變更日誌以了解所需的格式和驗證邊界。

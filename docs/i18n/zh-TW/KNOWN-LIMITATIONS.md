<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

<!-- STABLE-140-CURRENT-GUIDE -->
> **目前版本：Setup 1.4.0 / 遊戲 3.0.9 Lau。** 關閉 WoW，完整解壓縮 LauSetup.zip，在 Windows 開啟 LauSetup.exe，用 Browse... 選擇包含 WoW.exe 的資料夾。下一步 → 視覺選項 → 下一步 → 檢查 → 安裝 → 完成。所有額外選項預設關閉。WoW.exe 和載入畫面是同一個選項；地圖獨立，並包含 WDM 支援檔案。已安裝的地圖會保留。重新命名的重複修補檔保持原樣；只有空的 Patch-V 會自動備份。被取代的檔案保存在 LauSetupBackups。Patch-Y 沒有 DBC 修改；可選地圖新增了已記錄來源的上游資料表。洞穴地圖仍為測試版。Linux/Wine 請在文件要求的環境中使用 LauSetup.sh。Google HTTP 429 阻止了完整翻譯更新。下方舊內容僅供歷史參考，目前操作請以英文原文為準。
>
> [English](../../../KNOWN-LIMITATIONS.md) · [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自動翻譯。 [英文來源](../../../KNOWN-LIMITATIONS.md)。若措詞不同，則以英文來源為準。

<a id="known-limitations-and-assumptions"></a>

# 已知的限制和假設



[返回 Lau Setup](README.md) · [建議與功能請求](https://github.com/CRSD-Lau/Lau-Setup/discussions/1) · [DBC 更改歷史記錄](DBC-CHANGELOG.md)

在提出功能之前請先閱讀本文。 Lau Setup 為 **WoW 3.3.5a 版本 12340** 安裝客戶端視覺化升級。它不是一個伺服器修改框架。下面的邊界描述了當前項目；超出範圍並不一定意味著技術上不可能。

<a id="what-we-can-and-cannot-change"></a>

## 我們可以改變什麼，不能改變什麼

|請求 |當前邊界|
| --- | --- |
|改進支援的地面指示器、紋理、模型或本地化用戶端表 |在範圍內，受檔案依賴性和測試的約束。視覺改進不得被描述為伺服器損壞或機制的改變。 |
|改進安裝、備份、可訪問性或文件 |範圍內。保留不相關的文件並驗證安裝和恢復。 |
|更改 Warmane 傷害、命中偵測、能力持續時間、目標或遭遇腳本 |在我們的控制範圍之外。 Warmane運行自己的伺服器程式碼；該專案無權更改或部署該程式碼。 MPQ 或外掛程式無法讓伺服器採用不同的機制。 |
|將自訂C++程式碼新增至Warmane的核心 |此版本無法提供任何功能。對單獨控制的測試伺服器的變更不會更改 Warmane。 |
|注入 DLL、掛鉤客戶端或添加新的本機引擎行為 |在支援的補丁/插件工作流程之外。這需要單獨的工程和相容性調查，而不僅僅是 DBC 編輯。不提供 DLL 注入框架或一般客戶端掛鉤支援。 |
|解鎖受保護的 Lua 操作或缺少的遊戲 API |不受支援的功能。可編輯插件 Lua 和受保護的客戶端操作是不同的事情。重寫 Lua 本身並不會授予權限或建立客戶端不公開的 API。在假設存在解決方法之前報告確切的操作/API。 |
|提供完整的客戶端、另一個語言包或高清模型庫 |不包括在內。帶來現有的兼容客戶端以及所需的語言檔案、字體和模型配置。 |

安裝程式提供的相容 `WoW.exe` 在核准的載入渲染器、存檔容量和大位址支援方面具有特定作用。它的包含**不**承諾任意可執行檔或 DLL 修改。同樣，並非每個 Lua 檔案都受到保護或不可編輯：普通插件和 UI 變更在客戶端支援的行為內是可行的。

<a id="indicators-are-visual-guidance"></a>

## 指標是視覺引導

- **Warmane 是 Warmane 報告的運行時參考。 ** AzerothCore 和隔離客戶端有助於檢查這些環境中的檔案完整性和行為。他們無法證明 Warmane 的自訂命中偵測、計時或遭遇行為。
- **绘制的边缘不能保证安全边界。 ** 支援的呼吸和黏液噴霧根據測試儀回饋使用 90° 總錐體。 Halion 流星火使用公認的 test-v2 放大。這些是基於觀察的視覺警告，而不是來自 Warmane 伺服器來源的測量。
- **地形可能会夹住平坦的指示器。 **平坦的地面網格可以與斜坡、階梯和不平坦的表面相交。放大或升高它并不能保证随处投影。
- **效果终生需要遇到证据。 ** 追蹤/幽靈回饋包括一兩秒後消失的效果。單獨更改紋理、形狀或循環動畫並不能證明客戶端將保持效果實例處於活動狀態以進行完整的追求。時間修復需要該特定能力的鏡頭和事件證據；不要將模型或實驗版本視為已確認的修復。
- **模型具有说明性。 ** 网站/聊天动画演示外观。它們不是遊戲內渲染、持續時間或覆蓋範圍的錄音或證明。

對於邊界或時間報告，包括遭遇、能力、難度、客戶端版本、`/pyversion`，以及顯示引導和損壞或效果結束的剪輯。螢幕截圖很有用，但透視和重疊效果限制了精確的半徑測量。

<a id="dbc-and-patch-compatibility"></a>

## DBC 和補丁兼容性

DBC表是連接的數據，而不是獨立的開關。添加視覺效果可能需要匹配的咒語、視覺效果、套件、效果和模型參考。替換完整的表還可能替換其本地化文字並與提供相同表的另一個補丁發生衝突。

在地化依賴性是該專案開發過程中的一個真正問題。 Andre 和 Lau 一起完成了它。 [歷史 DBC 審計](DBC-CHANGELOG.md) 將報告的開發時間表與保留的檔案證據分開：Andre 的基線省略了 `Spell.dbc`，並非每個 DBC。不要認為將英文表複製到另一個語言環境是安全的。

- 使用與您目前的高清/原始型號配置相符的版本。新的法術視覺效果需要相容的高清依賴；檢測並不驗證每個第三方模型包。
- 如果您在安裝後刪除或停用 HD 型號補丁，請重新執行最新的設定以取得最終的配置。安裝的高清版本不會動態轉換自身。不匹配的資產可能會產生缺失或不正確的視覺效果，並可能需要對崩潰進行調查；無法保證崩潰或無崩潰行為。
- 根位置和活動區域設定有不同的作用。特別是，兩個S檔案是不同的。請遵循[放置指南](docs/TECHNICAL.md#file-placement)，而不是複製每個 MPQ 的通用說明。
- 保留不相關的補丁，但保留並不能保證相容性。覆蓋相同資料的另一個存檔可能會改變結果。
- 安裝程式介面會在十種選項中自動跟隨作業系統語言，手動選擇會被儲存。遊戲內容仍支援九種語言環境。僅變更 `Config.wtf` 不會安裝其他語言的檔案或字型。

<a id="installer-and-recovery-assumptions"></a>

## 安裝程式和復原假設

在安装或恢复之前完全关闭 WoW。使用确切的预期客户端文件夹并保持 `LauSetupBackups` 完好无损。

安装程序将实际文件哈希值与其**嵌入目录**进行比较。即使大小和时间戳匹配，也可以检测到一字节的更改，但旧的安装程序仍然只知道其旧目录。升級時下載最新的安裝程式。安装程序不会在客户端退出后持续监视客户端，也不会自动协调以后的手动补丁更改。

關閉新法術視覺效果會將範圍 S 檔案保留為 `.mpq.disabled`。重新啟用使用符合的停用位元組（如果可用），並將普通停用副本移至已驗證的交易備份。保留較舊的雜湊後綴副本。請參閱[目前恢復實作](docs/TECHNICAL.md#setup-117-re-enable-cleanup)。

復原依賴備份和復原記錄。當以後的更改使自動恢復變得不安全時，它就會停止。它不能承諾恢復唯一備份被刪除的檔案。單獨刪除 Patch-Y 並不能完全回溯安裝程式安裝的可執行檔和其他修補程式。對託管事務使用**恢復先前的安裝**。

<a id="platform-and-validation-limits"></a>

## 平台和驗證限制

已記錄的 Windows 目標是 Windows 10/11 使用.NET框架 4.8。經測試的 Linux 配置用途 Wine 11.0, Wine Mono 10.4.1，現有的 64-bit 前綴和Python 3.9+。運行時安裝程式未捆綁。遵循 [Wine 先決條件](wine/README.md);使用本地 Linux 貯存。連結的資料夾、網路共用和 Windows- 安裝的驅動器超出支援範圍 Wine 路徑配置。

此版本不支援 Lutris、Proton、Steam Deck 特定整合和 macOS 整合目標。這並不是斷言其他所有環境都是不可能的；這意味著我們還沒有建立對其的支援。 Windows 套件沒有數位簽章。

構建、哈希檢查、安裝程式回歸測試、Wine 測試和遊戲內測試回答了不同的問題。通過一項並不能取代其他項。目視檢查是抽樣的，並非每個區域、遭遇、顯示比例、Linux 分佈或第三方客戶端修改的認證。請參閱每個版本的驗證報告以了解實際檢查的內容。

<a id="before-requesting-a-feature"></a>

## 在請求功能之前

描述玩家可見的問題、你的設定和證據。歡迎在支持範圍內提出建議 [想法](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas);可重現的缺陷屬於 [問題](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose).

對於 DLL、本機程式碼、受保護操作或依賴伺服器的建議，明確標識依賴關係。在承諾實施之前，他們需要進行可行性工作並對受影響的系統進行適當的控制。請不要將它們歸檔為簡單的缺失 DBC 選項。

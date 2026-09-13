<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.4.0** — 一個 ZIP 現在同時包含 Windows 安裝程式和 Linux/Wine 啟動器。介面會在十種選項中自動跟隨作業系統語言，手動選擇會被儲存。遊戲版本 3.0.8 和遊戲檔案均未變更，也沒有 DBC 修改。
>
> 由於 Google HTTP 429，完整指南更新仍在等待中。下方正文可能已過時；請以目前英文來源和 1.4.0 發行說明為準。 [English](../../../PLATFORM-FEASIBILITY.md) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)
>
> **目前下載：** Windows 和 Linux/Wine 都使用 [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)。解壓含五個檔案的 `LauSetup/` 資料夾：Windows 開啟 `LauSetup.exe`；Linux/Wine 執行 `LauSetup.sh`。下方關於個別 EXE 或 Wine ZIP 的舊說明不適用於 1.4.0。
>
> **1.4.0:** 已識別的額外升級檔案會自動備份，然後繼續安裝。還原操作會將檔案放回原位。無需手動移動。 安裝程式在替換或移動現有檔案之前會自動保留原檔案。無關檔案保持不變。


> **1.4.0:** 選擇遊戲資料夾 → 下一步 → 選擇視覺效果 → 下一步 → 確認 → 安裝升級 → 完成。根據偵測到的用戶端固定選擇 Patch-Y HD 或 Patch-Y Non-HD。額外選項預設關閉；已安裝的地圖升級會保留。確認頁列出 Patch-Y（Lau 版本）及所選額外內容、WoW.exe、Patch-Q、語言檔案、下載大小和備份。下一步不會變更遊戲檔案。每一步都可手動選擇介面語言並儲存；自動會重新使用系統語言。仍可使用還原上次安裝。

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自動翻譯。 [英文來源](../../../PLATFORM-FEASIBILITY.md)。若措詞不同，則以英文來源為準。

<a id="lau-setup-platform-feasibility"></a>

# Lau Setup 平台可行性

作者：Neil Mitchell
創作者： Neil Mitchell
最後修改者：Neil Mitchell
評估日期：2026-09-11

> **以下為歷史評估：** 後續關於 1.0.1/1.1.0 的章節描述的是當時的評估狀態。目前使用單一共享 ZIP 的安裝請參閱上方 Setup 1.2.0 提示。
更新：用戶僅選擇了Wine。安裝程式 1.1.0 現在提供經過測試的
Wine 11 / Wine Mono 10.4.1 啟動器在 [Wine 指南](wine/README.md) 中描述。
以下的 Wine 8 探測和建議被保留為歷史評估。
Lutris、Proton 和 macOS 整合仍然超出範圍。

Lau Setup 1.0.1 仍然是 Windows 安裝程式。 Linux 到 Wine 是建議的下一個相容性目標。此評估不證明在 Linux 或 macOS 上的安裝。早期的 63 Docker/Wine 案例使用了遊戲數據，而不是此安裝程式。

|選項|推薦| Lau Setup 代表什麼 |
| --- | --- | --- |
| Wine 關於 Linux |第一個目標；原則上可行，目前未經驗證|在明確選擇的 Wine 前綴內重複使用 Windows 安裝程式。在發布支援之前證明其運行時間、資料夾選擇、下載、檔案安全性和復原。 |
|盧特里斯 |接下來直接Wine通過後|一個小的集成配方可以在現有遊戲的前綴中啟動設定。不需要單獨的有效負載格式。 |
|蒸氣/質子 |以後有條件|使用正確的現有遊戲前綴。添加設定作為另一個非 Steam 遊戲可以給它一個不同的環境。 Steam Deck 可用性需要單獨的螢幕和控制器檢查。 |
| macOS 上的 CrossOver |看似合理的獨立測試跑道|在遊戲的瓶子裡跑。在實際 macOS 硬體和支援的 CrossOver 版本上進行驗證； Linux 測試無法證實這一點。 |
| Wine + DXVK |可選遊戲配置| DXVK 為遊戲翻譯了 Direct3D。它不能解決安裝程式的 .NET、字型或檔案安全要求。 |
|威士忌|不採納作為新的支持對象 |其上游項目不再積極維護。 |

上述分類遵循以下描述的角色 [Wine Mono](https://github.com/wine-mono/wine-mono), [盧特里斯](https://lutris.net/about/), [普騰](https://github.com/ValveSoftware/Proton), [DXVK](https://github.com/doitsujin/dxvk), [CrossOver的 Mac 指南](https://support.codeweavers.com/en_US/crossover-mac-user-guide)， 和 [威士忌酒](https://github.com/Whisky-App/Whisky)。建議是我們的評估，而不是上游認證 Lau Setup. CrossOver 可以運行 32-bit Windows 應用在 64-bit 瓶；遺失本機 macOS 32-bit 僅支持並不能排除這種可能性。

<a id="bounded-probe-results"></a>

## 有界探測結果

本地探針使用Wine 8.0（Debian 8.0~repack-4），一個隔離的win32前綴和Xvfb。這個較舊的本地可用運行時不是對當前 Wine 版本的測試。未安裝或修改個人遊戲用戶端。

1。繼承的遊戲測試圖像禁用了 mscoree。啟用它暴露了這一點 Wine Mono 失踪了。這是一個測試環境問題。
2。安裝了官方的 Wine Mono 7.4.0 驗證後一次性前綴中的 MSI SHA-256 `6413ff328ebbf7ec7689c648feb3546d8102ded865079d1fbf0331b14b3ab0ec`，固定於 [Wine 8.0的來源](https://raw.githubusercontent.com/wine-mirror/wine/wine-8.0/dlls/appwiz.cpl/addons.c).
3。診斷工具已初始化 WinForms 並載入嵌入的目錄，然後無法建立表單 `System.ArgumentException: The requested FontFamily could not be found [GDI+ status: FontFamilyNotFound]`。將可用的 Liberation 字型複製到該前綴並不能解決問題。沒有成功的安裝程式螢幕截圖或安裝結果。
4。當地證據保留在 `reports/wine-feasibility/`。探針容器已停止。診斷工具不包含在分散式安裝程式或公共來源套件中。

這標識了運行時/字體配置工作，而不是證明 Wine 是不可能的。在此偵測器中的 Wine 下未嘗試安裝/復原事務。

<a id="acceptance-work-before-wine-support"></a>

## Wine 支援前的驗收工作

1。建立可重現的電流 Wine/運行時/字體組合 Linux 桌面。以常見的顯示比例顯示初始、就緒、下載、復原和錯誤狀態；驗證鍵盤存取和資料夾選擇。
2。驗證區分大小寫的檔案系統上的準確主機資料夾對應和大小寫處理，包括僅大小寫不同的重複名稱。保留不相關的補丁和個人設定。
3。證明連結、獨佔鎖、可用空間、日誌和原子替換行為。安裝程式目前調用 Windows 文件資訊 API；它們的語意必須在以下條件下進行測試 Wine 而不是假設的。
4。證明跨前綴的運行遊戲守衛。目前程式碼枚舉 Windows 處理並比較可執行目錄。 Wine 前綴可見性可能會使執行相同客戶端的另一個前綴未被偵測到。在提供安全安裝支援之前解決此問題；僅成功的相同前綴測試是不夠的。
5。運行夾具安裝/恢復和中斷恢復矩陣，然後運行乾淨的匿名 GitHub 使用確切的發布資產下載/安裝/回滾。測試 TLS、重定向、復原、取消和離線復原。
6。隨後在同一受支援的環境中進行遊戲內檢查。然后才发布 Wine 說明和 Lutris 整合。保持 Proton 和 macOS 明確未經驗證，直到它們自己的檢查通過。

在 GitHub 版本上保留一組不可變的遊戲資產。不要將完整的用戶端、個人 UI 或每個有效負載的副本新增至 Git 儲存庫以啟用另一個啟動器。如果 Wine 無法可靠地滿足安全檢查，請圍繞相同的清單和事務規則評估本機 Linux 安裝程式作為單獨的實作。

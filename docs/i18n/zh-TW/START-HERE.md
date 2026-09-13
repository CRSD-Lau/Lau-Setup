<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.4.0** — 一個 ZIP 現在同時包含 Windows 安裝程式和 Linux/Wine 啟動器。介面會在十種選項中自動跟隨作業系統語言，手動選擇會被儲存。遊戲版本 3.0.8 和遊戲檔案均未變更，也沒有 DBC 修改。
>
> 由於 Google HTTP 429，完整指南更新仍在等待中。下方正文可能已過時；請以目前英文來源和 1.4.0 發行說明為準。 [English](../../../START-HERE.txt) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)
>
> **目前下載：** Windows 和 Linux/Wine 都使用 [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)。解壓含五個檔案的 `LauSetup/` 資料夾：Windows 開啟 `LauSetup.exe`；Linux/Wine 執行 `LauSetup.sh`。下方關於個別 EXE 或 Wine ZIP 的舊說明不適用於 1.4.0。
>
> **1.4.0:** 已識別的額外升級檔案會自動備份，然後繼續安裝。還原操作會將檔案放回原位。無需手動移動。 安裝程式在替換或移動現有檔案之前會自動保留原檔案。無關檔案保持不變。



> **1.4.0:** 選擇遊戲資料夾 → 下一步 → 選擇視覺效果 → 下一步 → 確認 → 安裝升級 → 完成。根據偵測到的用戶端固定選擇 Patch-Y HD 或 Patch-Y Non-HD。額外選項預設關閉；已安裝的地圖升級會保留。確認頁列出 Patch-Y（Lau 版本）及所選額外內容、WoW.exe、Patch-Q、語言檔案、下載大小和備份。下一步不會變更遊戲檔案。每一步都可手動選擇介面語言並儲存；自動會重新使用系統語言。仍可使用還原上次安裝。

<!-- BEGINNER-140-STEPS -->


選擇遊戲資料夾 → 下一步 → 選擇視覺效果 → 下一步 → 確認 → 安裝升級 → 完成。根據偵測到的用戶端固定選擇 Patch-Y HD 或 Patch-Y Non-HD。額外選項預設關閉；已安裝的地圖升級會保留。確認頁列出 Patch-Y（Lau 版本）及所選額外內容、WoW.exe、Patch-Q、語言檔案、下載大小和備份。下一步不會變更遊戲檔案。每一步都可手動選擇介面語言並儲存；自動會重新使用系統語言。仍可使用還原上次安裝。

Linux/Wine: Wine 11.0, Wine Mono 10.4.1, Python 3.9+, 64-bit WINEPREFIX. `WINEPREFIX="/path/to/prefix" sh LauSetup.sh`. [Guide](https://github.com/CRSD-Lau/Lau-Setup/blob/main/wine/README.txt).

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自動翻譯。 [英文來源](../../../START-HERE.txt)。若措詞不同，則以英文來源為準。

LAU 設定 — 釋放 3.0.8

Windows 和 Linux/Wine：下載 `LauSetup.zip` 並解壓 `LauSetup/`。Windows 開啟 `LauSetup/LauSetup.exe`；Linux/Wine 執行 `LauSetup/LauSetup.sh`。
Wine 請使用隨附的 Linux 啟動器，不要直接執行 EXE。

1。關閉World of Warcraft。
2。打开 LauSetup.exe 并选择您的 WoW 文件夹。
3。選擇您的視覺效果並點擊安裝升級。

从旧版本或测试 v2 更新？首先下载新的安装程序；旧副本嵌入旧目录。
选择相同的客户端和视觉效果。文件哈希檢查檢測更改的補丁。
启动WoW并输入/pyversion；它应该报告 3.0.8 Lau。

安装程序会检测您的客户端语言和 HD 型号配置。
預設選擇增強奉獻。取消選取庫存
外觀；咒語本身仍然有效。新的法术视觉效果需要
現有相容高清型號客戶端。升級地圖/小地圖是可選的。

您需要现有的 WoW 3.3.5a 客户端，在 Windows 10 或 11 上构建 12340。
此下载是升级，而不是完整的客户端或语言包。
所需的兼容 WoW.exe 会自动安装。

无需手动复制或重命名补丁。請勿下載整個
共享數據發布。该应用程序仅下载您选择所需的文件。

備份和可恢復下載保留在 WoW 內的 LauSetupBackups 中
資料夾，資料之外。若要撤銷更新，請關閉 WoW，重新開啟 LauSetup.exe，
選擇相同資料夾，然後按一下復原先前的安裝。恢復也
如果更新中斷導致 WoW.exe 暫時遺失，則可以使用。

您的插件、SavedVariables、字體、登入插圖、領域設定和
不相關的補丁被保留。沒有披薩勇士品牌，個人
捆綁 ElvUI 設定、LoginUI、帳戶資料或完整遊戲用戶端。

下載來自GitHub Releases；不需要 GitHub 帳戶。
如果下載停止，請稍後重試。已驗證的文件
被重複使用並恢復部分下載。遊戲檔案僅在之後更改
所有必要的下載均已通過驗證。如果保留 LauSetupBackups
該應用程式報告需要恢復。

此安裝程式沒有數位簽章，因此 Windows 可能會顯示未知發布者
警告。使用提供的校驗和來驗證您的下載。它不
需要停用 Windows 安全性或安裝 Python/PowerShell 工具。
需要 .NET Framework 4.8 運行時。

一旦此安裝程式添加了地圖升級，它就會在安裝過程中保留該升級
版本變更。使用恢復之前的安裝來撤銷地圖安裝。

學分：Andre（Patch-Y 基線）、Loriendal 和 Trimitor（HD 基礎）、
Project Reforged 貢獻者（高清藝術作品），Blizzard（原創藝術作品和
在地化文字），Lau（適配、相容性、指標、測試）。

Author / Creator / Last Modified By: Neil Mitchell

設定 1.1.7：新的拼字視覺效果關閉，使 Patch-S 保持為 .mpq.disabled 旁邊
它原來的路徑。不同的禁用副本永遠不會被覆蓋。
若要撤銷整個安裝，請使用恢復先前的安裝。對於文件
已被舊安裝版本刪除，請從這些備份中還原它們
重新安裝之前使用恢復先前的安裝。保留LauSetupBackups。

目前的S檔案始終變為.mpq.disabled。如果年紀較大的殘障人士
副本存在，安裝程式首先將其保留為 `.mpq.disabled.<12-character hash>`。無需手動重新命名
需要切換選項。手動重新啟用需要刪除
.disabled 和任何後續哈希，WoW 關閉並且沒有不同的活動
文件被覆蓋。使用恢復先前的安裝進行託管回滾。

1.1.7 修補程式：啟用新拼字視覺效果可重複使用相符的已停用 Patch-S，而無需再次下載。即使活動 Patch-S 已匹配，普通禁用副本也會移至 LauSetupBackups 中經過驗證的交易備份中。不同版本仍然可以透過恢復先前的安裝來恢復。關閉仍然使用.mpq.disabled。現有的雜湊後綴存檔保持不變。

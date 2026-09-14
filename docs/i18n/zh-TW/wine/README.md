<!-- LANGUAGES:START -->
[English](../../../../README.md) · [Deutsch](../../de/README.md) · [Español (España)](../../es-ES/README.md) · [Español (México)](../../es-MX/README.md) · [Français](../../fr/README.md) · [한국어](../../ko/README.md) · [Русский](../../ru/README.md) · [简体中文](../../zh-CN/README.md) · [繁體中文](../README.md) · [Português (Brasil)](../../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

<!-- STABLE-140-CURRENT-GUIDE -->
> **目前版本：Setup 1.4.0 / 遊戲 3.0.9 Lau。** 關閉 WoW，完整解壓縮 LauSetup.zip，在 Windows 開啟 LauSetup.exe，用 Browse... 選擇包含 WoW.exe 的資料夾。下一步 → 視覺選項 → 下一步 → 檢查 → 安裝 → 完成。所有額外選項預設關閉。WoW.exe 和載入畫面是同一個選項；地圖獨立，並包含 WDM 支援檔案。已安裝的地圖會保留。重新命名的重複修補檔保持原樣；只有空的 Patch-V 會自動備份。被取代的檔案保存在 LauSetupBackups。Patch-Y 沒有 DBC 修改；可選地圖新增了已記錄來源的上游資料表。洞穴地圖仍為測試版。Linux/Wine 請在文件要求的環境中使用 LauSetup.sh。Google HTTP 429 阻止了完整翻譯更新。下方舊內容僅供歷史參考，目前操作請以英文原文為準。
>
> [English](../../../../wine/README.txt) · [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自動翻譯。 [英文來源](../../../../wine/README.txt)。若措詞不同，則以英文來源為準。

Lau Setup 用於 Linux 上的 Wine
Author / Creator / Last Modified By: Neil Mitchell

1。在本機 Linux 檔案系統上使用現有的 WoW 3.3.5a 建置 12340 用戶端。
2。關閉每個 WoW 實例，包括其他 Wine 前綴的遊戲。
3。解壓 `LauSetup.zip`。將 `LauSetup/` 中的五個檔案放在一起：`LauSetup.exe`、`LauSetup.sh`、`lau_wine.py`、`lau-languages.json` 和 `README.txt`。
4。在提取的資料夾中打開終端機並運行：

```sh
WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh
```

5。選擇您現有的遊戲資料夾並安裝。常見的自動備份
   和恢復先前的安裝按鈕可用。

此版本的要求：
- Wine 11.0、64-bit 前綴和 Wine Mono 10.4.1 已安裝在那裡。
- 用於主機安全性助理的 Python 3.9 或更新版本（僅限標準函式庫）。
- Liberation Sans 或 DejaVu Sans 字型；完整的Wine字型包必須
  也可以安裝Wine Mono自己的預設控制來渲染。
- 本地 Linux 儲存。網路共用和 Windows 安裝的磁碟機不包括在內。
- 正常主機進程可見性。請勿透過沙箱運行此啟動器
  隱藏其他 Wine 進程。以一般使用者身分執行，切勿使用 sudo/root。

64-bit 前綴可以包含 32-bit WoW 用戶端。該安裝程式不
建立、轉換或升級您的 Wine 前綴，安裝 Wine/Mono，配置
DXVK，或更改您的遊戲啟動器。使用您的發行版的 Wine 設置
如果缺少運行時，請先執行指令。

此測試運行時的官方 Wine Mono 套件：
https://github.com/wine-mono/wine-mono/releases/tag/wine-mono-10.4.1

將 Wine Mono 運作時與 Wine 結合使用。 Windows .NET Framework 安裝程式是
未捆綁，且此測試 Wine Mono 配置不需要。

始終透過 LauSetup.sh 啟動。直接在Wine下運行LauSetup.exe
如果沒有 Linux 幫助程序，將拒絕客戶端操作。它檢查主機路徑
並處理並持有跨 Wine 前綴共享的主機鎖定。如果它停止了，
重新開啟啟動器並恢復掛起的安裝，然後重試。

保持 WoW 關閉，直到安裝完成。流程檢查減少競爭；他們不能
阻止其他程式啟動遊戲或隨後更改檔案。
符號連結路徑、硬連結和不明確的檔案名稱大小寫都會被拒絕。數據
備份目錄必須與客戶端保留在同一檔案系統上。

驗證範圍：隔離 Wine 11.0 / Wine Mono 10.4.1 客戶端、夾具和
真實有效負載安裝/復原測試、雙前綴安全測試和取樣 GUI
檢查。這並不是每個 Linux 發行版、檔案系統的認證，
顯示比例，Wine版本，或遊戲遭遇。沒有 Lutris、Proton 或 macOS
此版本中包含整合。

安裝程式介面會在十種選項中自動跟隨作業系統語言，手動選擇會被儲存。用戶端遊戲資料仍支援九種語言環境，並遵循偵測到的遊戲語言環境。

設定 1.1.7：新的拼字視覺效果關閉，使 Patch-S 保持為 .mpq.disabled 旁邊
它原來的路徑。不同的禁用副本永遠不會被覆蓋。
若要撤銷整個安裝，請使用恢復先前的安裝。對於文件
已被舊安裝版本刪除，請從這些備份中還原它們
重新安裝之前使用恢復先前的安裝。保留 LauSetupBackups。

目前的S檔案始終變為.mpq.disabled。如果年紀較大的殘障人士
副本存在，安裝程式首先將其保留為 `.mpq.disabled.<12-character hash>`。無需手動重新命名
需要切換選項。手動重新啟用需要刪除
.disabled 和任何後續哈希，WoW 關閉並且沒有不同的活動
文件被覆蓋。使用恢復先前的安裝進行託管回滾。

1.1.7 重新啟用清理：符合停用的 Patch-S 在本地重複使用。普通禁用副本將移至 LauSetupBackups 中經過驗證的交易備份，留下一個活動 S。不同的副本仍然可以透過恢復先前的安裝進行恢復。現有的雜湊後綴存檔不會被清除。

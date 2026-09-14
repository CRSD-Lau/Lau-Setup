<!-- LANGUAGES:START -->
[English](../../../../README.md) · [Deutsch](../../de/README.md) · [Español (España)](../../es-ES/README.md) · [Español (México)](../../es-MX/README.md) · [Français](../../fr/README.md) · [한국어](../../ko/README.md) · [Русский](../../ru/README.md) · [简体中文](../../zh-CN/README.md) · [繁體中文](../README.md) · [Português (Brasil)](../../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

<!-- STABLE-140-CURRENT-GUIDE -->
> **目前版本：Setup 1.4.0 / 遊戲 3.0.9 Lau。** 關閉 WoW，完整解壓縮 LauSetup.zip，在 Windows 開啟 LauSetup.exe，用 Browse... 選擇包含 WoW.exe 的資料夾。下一步 → 視覺選項 → 下一步 → 檢查 → 安裝 → 完成。所有額外選項預設關閉。WoW.exe 和載入畫面是同一個選項；地圖獨立，並包含 WDM 支援檔案。已安裝的地圖會保留。重新命名的重複修補檔保持原樣；只有空的 Patch-V 會自動備份。被取代的檔案保存在 LauSetupBackups。Patch-Y 沒有 DBC 修改；可選地圖新增了已記錄來源的上游資料表。洞穴地圖仍為測試版。Linux/Wine 請在文件要求的環境中使用 LauSetup.sh。Google HTTP 429 阻止了完整翻譯更新。下方舊內容僅供歷史參考，目前操作請以英文原文為準。
>
> [English](../../../TECHNICAL.md) · [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自動翻譯。 [英文來源](../../../TECHNICAL.md)。若措詞不同，則以英文來源為準。

<a id="technical-reference"></a>

# 技術參考



[返回Lau Setup](../README.md)

<a id="build-and-verification"></a>

## 建置和驗證

在安裝了 .NET Framework 編譯器的 Windows 上執行 `tools/build.ps1`。公共來源包包含應用程式、嵌入式目錄、建置腳本和文件。完整的開發檢查還包含 `tools/test.ps1`，用於事務、下載、路徑、進程、復原和 GUI 回歸測試；這些測試使用隔離的裝置和本機參考可執行檔。 `tools/build.ps1 -Release` 拒絕未通過出版門的目錄。測試工具、有效負載產生和本機遊戲測試依賴私有本機來源路徑，而不是公用來源套件的一部分。

`build/catalog.json` 按大小和 SHA-256 命名每個資產和下載段，以及觀察到的 GitHub 發布 URL。此目錄固定儲存庫、發布標籤和雜湊命名的檔案。安裝程式會匿名下載並在遵循每個重定向之前檢查它。安裝程式不需要 GitHub 帳戶、登入瀏覽器或 API 憑證。在完整的開發檢查中，`tools/refresh_github_catalog.py` 在不更改哈希值的情況下關聯上傳的資產，並且 `tools/verify-public.ps1` 透過應用程式使用的相同下載器驗證每個分段和重建的資產。

<a id="file-placement"></a>

## 檔案放置

|組件|目的地 |
|---|---|
|兼容的可执行文件 | `WoW.exe` |
|选定区域Q |根 `Data/patch-q.mpq` 和活动区域设置 `Data/<locale>/patch-<locale>-Q.MPQ` 中的相同副本 |
|选定版本 Y |根 `Data/patch-y.mpq` 和活动区域设置 `Data/<locale>/patch-<locale>-Y.MPQ` 中的相同副本 |
|新法术资源（选择时）|根 `Data/patch-s.mpq` |
|匹配本地化拼写表（选择时）|活动区域设置 `Data/<locale>/patch-<locale>-S.MPQ` |
|可选地图/小地图 |根`Data/patch-m.mpq`；已备份被取代的活动区域设置 M |

Core Q 保留了该版本的 LoadingScreens.dbc、本地化的 Map.dbc 和逐字节加载图像。它省略了添加的世界地图定义和世界地图图稿。全地图模式使用原有的区域Q和共享M，无需重新打包。两个 S 位置包含不同的档案。關閉新拼字會將作用域根/區域設定 S 對保留為 .mpq.disabled；重新啟用會將普通停用的副本移至經過驗證的交易備份中，如下面的設定 1.1.7 部分所述。 HD 检测需要匹配现有的根和区域设置 F 补丁。

<a id="recovery-design"></a>

## 復原設計

一款客戶端鎖涵蓋下載、暫存和安裝。文件在暫存前進行驗證，並在放置後再次進行驗證。現有文件移至 `LauSetupBackups/transactions/<id>/before/`，保留其位元組和時間戳記；日誌在提交之前持久寫入。失敗的提交會在安全性時恢復原始版本。重新開啟應用程式時，即使沒有 WoW.exe，中斷的提交和中斷的復原仍然可以發現。

恢復拒絕由其他更新更改的檔案並保留備份以供手動解決。僅接受精確的 root/active-locale Q/M/S/Y 路徑和 WoW.exe。遍歷、替代流和重分析點被拒絕；可寫入恢復檔案必須有一個硬連結。日誌和程序集臨時檔案使用獨特的名稱和獨家建立。應用程式永遠不會將存檔枚舉到客戶端檔案系統。

<a id="release-boundaries"></a>

## 釋放邊界

此安裝程式沒有數位簽章。 Windows 和 Wine 安裝程式測試、取樣 GUI 檢查和保留的遊戲資料基準分別記錄在 VALIDATION.json 中。 Wine 1.1.0 檢查使用 Wine 11.0 / Wine Mono 10.4.1 和本地 Docker 覆蓋裝置；這些檢查並不驗證每個 Linux 發行版/檔案系統、顯示比例、遭遇或第三方用戶端修改。原始 Patch-Y 版本 ZIP 可在 GitHub 版本上取得。有關當前範圍和假設，請參閱[已知限制](../KNOWN-LIMITATIONS.md)。


<a id="306-color-update--setup-112"></a>

## 3.0.6 色彩更新/設定 1.1.2

六個 Y 檔案中的每一個都會更改三個 M2 成員和 !PYAndre TOC，並添加兩個 BLP 紋理。 `Spells/PW_Coldflame_Ground.m2` 現在引用 `Spells/PW_Coldflame_Blue.blp`； `Spells/PW_HalionMeteor_Ground.m2` 和 `Spells/PW_HalionMeteor_Ring.m2` 參考 `Spells/PW_Halion_Red.blp`。每個原始模型中只有紋理描述符 4 的檔案名稱長度/偏移量發生變化；新路徑已附加。原生粒子紋理（索引 0–3）、皮膚、幾何體、全域動畫軌跡、邊界和 DBC 位元組保持不變。其他指標的共享白色紋理保持不變。

新紋理保留了現有的不透明 8×8 DXT1 BLP2 格式和所有四個 mip 等級。僅 RGB565 端點變更：淺藍色解碼為 (120,216,248,255)，紅色解碼為 (248,68,40,255)。量化是現有紋理格式所固有的。兩款 Halion 型號均使用相同的紅色紋理。奉獻和模型版本的選擇保持獨立。

更新決策會比較實際的 SHA-256 和大小，而不是發布標籤或時間戳記。回歸測試在每個 Y 放置中修改一個位元組而不更改檔案大小或時間戳，只需要一次修復操作，驗證修復的哈希，然後恢復先前的版本。舊的 EXE 嵌入舊目錄，因此升級需要先下載新的 EXE/ZIP。

<a id="307-halion-radius--setup-113"></a>

## 3.0.7 Halion 半徑/設定 1.1.3

提升 `Spells/PW_HalionMeteor_Ground.m2`、`Spells/PW_HalionMeteor_Ring.m2` 及其 `00.skin` 檔案的精確 test-v2 位元組。網格 X/Y 座標為 1.5 乘以 3.0.6。 Z/UV/法線和動畫/粒子軌跡保留。模型邊界（偏移 160）、序列邊界（序列 +32）和皮膚子網格邊界（子網格 +20）反映放大的幾何體。 TOC版本從3.0.6改為3.0.7。每個版本恰好有五個現有成員發生變化；沒有新增或刪除成員。測試 v3 幾何體被排除。 Coldflame 和所有其他成員均符合 3.0.6。使用者轉發測試人員對 v2 的接受度；不主張廣泛遭遇認證。

<a id="308-all-cones--setup-114"></a>

## 3.0.8 所有錐體/設定 1.1.4

所有六個版本均使用 90 度總扇形幾何形狀。舊模型檔案名稱和所有 DBC 行保持不變，以保留拼字路由。更改：PW_White_Fan60_60yd_Glowing (Halion 兩個領域), PW_White_Fan60_30yd_Glowing (薩維亞娜), PW_White_Fan60_100y_Glowing (ICC 霧牙)和 PW_Rotface_SlimeSpray_Fan25_Room (腐臉) 擴大自 60 到 90; PW_White_Fan82_60yd_發光 (薩薩里昂) 擴大自 82 到 90。 PW_White_Fan75_60yd_發光 (辛達戈薩) 已經是 90 且位元組相同。

對於每個修改後的模型，僅頂點 XY（48 位元組頂點步幅）和邊界發生變化。關於+X刻度的角度由90/old-angle;每個頂點半徑和 Z 都被保留。更新偏移量 160 處的模型邊界、序列+32 處的序列邊界以及子網格+20 處的皮膚子網格邊界。 UV、法線、動畫和粒子軌跡保持不變。每個版本的 TOC 中有 10 個模型/皮膚成員和兩個版本字串發生變化；不添加或刪除任何成員。所有其他成員，包括 Halion Meteor-Fire Test-v2 Geometry 和 Coldflame，都逐字節匹配 3.0.7。

<a id="setup-115-disabled-patch-s-preservation"></a>

##設定1.1.5禁用Patch-S儲存

只有根路徑和活動區域設定 S 路徑才會獲得 .disabled 字尾。每次停用都會在停用 S 之前建立一個雜湊固定的本機暫存副本；兩條路徑都會被記錄，最多有十一個目的地。回滾可還原原始活動檔案並僅刪除新建立的停用副本。先前存在的相同禁用副本保留在事務之外並被保留。衝突的文件或目錄會阻礙規劃。重新啟用會安裝目錄 S 資產，且不會消耗已停用的副本。現有期刊仍然可讀。不接受任意本機來源路徑：每個本機副本必須與其配對的 S 停用操作相符。

<a id="setup-116-disabled-copy-collisions"></a>

## 設定 1.1.6 停用複製衝突

目前活動的 S 檔案始終採用純 .mpq.disabled 名稱。在取代不同的現有停用檔案之前，安裝程式將其位元組放入以其 SHA-256 的第一個 12 字元結尾的同級檔案中；在重新使用之前會檢查完整的 SHA-256 和長度。這會將名稱保留在現有的 Windows 路徑限制內。衝突的存檔內容無法關閉。活動 S、普通停用檔案和新建立的存檔副本獨立記錄，最多有 13 個條目；回滾恢復所有原始資料。本機來源僅限於配對 S 停用或停用檔案取代操作。舊期刊仍然可讀。

<a id="setup-117-re-enable-cleanup"></a>

## 設定 1.1.7 重新啟用清理

啟用新拼字日誌刪除普通根和活動區域設定已停用的 S 檔案。交易將其經過驗證的原始位元組移至資料之外的備份之前。如果停用的檔案與目錄 SHA-256 和大小相符，則會在本機暫存以符合 S 目標並從下載中排除。本機來源必須與確切的停用檔案刪除和目錄資源配對。已配對的 Active S 仍會產生清理交易。現有的雜湊後綴存檔不會被清除。以前的期刊仍然可讀。開/關/開、來源漂移、每個新提交/恢復步驟的中斷、所有區域設定和堆疊恢復都涵蓋在內。

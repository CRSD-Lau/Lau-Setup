<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自動翻譯。 [英文來源](../../../CHANGELOG.md)。若措詞不同，則以英文來源為準。

<a id="lau-setup-116-hotfix---switch-options-with-existing-disabled-patch-s"></a>

# Lau Setup 1.1.6 修補程式 - 切換現有停用的選項 Patch-S

修正了在早期安裝後關閉新拼字視覺效果時出現的 1.1.5 訊息「已存在不同的已停用的 Patch-S」。

安裝程式會自動保留這兩個檔案。目前的S檔案始終變為`.mpq.disabled`。如果已存在不同的舊停用副本，安裝程式首先將該舊副本保留為 `.mpq.disabled.<12-character hash>`。重複使用相同的已儲存副本。兩個版本均被保留。其內容與保留的舊文件不符的哈希命名副本仍會停止操作以進行檢查。

這適用於根和活動區域設定 S 文件，包括序列**所有三個標誌開啟 -> 新拼字視覺效果關閉**、重複切換和回滾。地圖選擇被保留。

下載新的 EXE 或 Wine ZIP 並重試您的選擇。您無需刪除或重新命名現有的停用副本即可解決 1.1.5 顯示的普通衝突。

若要撤銷完整安裝，請使用 **恢復先前的安裝**。若要手動重新啟用已儲存的 S 文件，請關閉 WoW 並刪除 `.disabled` 和任何後續哈希，恢復其原始 `.mpq` 檔案名稱。切勿覆蓋不同的活動文件。手動更改可以阻止文件漂移的託管回滾；保留您的備份。在 1.1.5 之前安裝程式刪除的檔案仍然需要透過備份進行還原。

遊戲版本保持**3.0.8 Lau**，並且每個遊戲有效負載均保持不變。所有 90 度錐體、流星火半徑和冷焰都被保留。

Windows 和 Wine 檢查包括 46 回歸群組、所有九個區域設定、現有停用檔案、重複開關、篡改複製保護、中斷復原和精確回滾。新的公開下載使用真實的開/關發布文件和舊的禁用副本進行測試。這是安裝程式驗證，而不是新的遊戲內遭遇驗證。

[原始六版 Patch-Y 拉鍊](https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.1.4/Lau-Patch-Y-3.0.8-All-Editions.zip)

[安裝幫助和變更日誌](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-115-hotfix---keep-disabled-patch-s-files"></a>

# Lau Setup 1.1.5 修補程式 - 保留停用的 Patch-S 文件

關閉**新拼字視覺效果**現在會將根和活動區域設定 Patch-S 檔案保留在其原始位置旁邊作為 `.mpq.disabled`，而不是僅將它們保留在安裝程式備份中。它們的位元組在更改之前和之後都會得到驗證。 WoW 不載入已停用的檔案名稱。

- 不同的現有 `.disabled` 副本會阻止安裝；它永遠不會被覆蓋。
- 重複使用並保留相同的停用副本。
- 開啟該選項會安裝所選版本的活動 S 檔案並保留已停用的副本。
- 重複安裝、回滾和中斷復原涵蓋活動路徑和停用路徑。

若要手動重新啟用已停用的文件，請關閉 WoW 並僅刪除 `.disabled` 後綴。不要覆蓋不同的活動文件。若要撤銷完整的 Lau 安裝，請使用 **還原先前的安裝**；僅刪除 Patch-Y 不會撤銷 Q/M/執行檔或其他變更。手動檔案變更可能會導致託管回滾因漂移而停止，因此請保留備份。

**已受到舊安裝程式的影響？ ** 此更新不會自動提取舊備份。使用「恢復先前的安裝」來恢復這些文件，在使用新設置重新安裝之前，請向後執行任何堆疊的安裝。保留LauSetupBackups。

遊戲版本仍然是**3.0.8 Lau**。所有 MPQ 保持不變：90 度呼吸/史萊姆噴霧，已批准 +50% Halion 流星火半徑和冷焰均保留。下載新的 EXE 或 Wine ZIP 以進行安裝程式修復。

Windows 和 Wine 驗證包含在 VALIDATION.json 中。測試涵蓋所有九個區域設定、停用複製衝突、開/關轉換、重複安裝、每個移動/恢復步驟的中斷、檔案漂移和精確回滾。該修復不會要求新的遊戲內遭遇驗證。

[原始六版 Patch-Y 拉鍊 (不變 3.0.8)](https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.1.4/Lau-Patch-Y-3.0.8-All-Editions.zip)

[安裝幫助和變更日誌](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-114--game-release-308-lau"></a>

# Lau Setup 1.1.4 · 遊戲發行 3.0.8 Lau

<a id="117-hotfix---patch-s-re-enable-cleanup"></a>

## 1.1.7 修補程式 - Patch-S 重新啟用清理

- 當 SHA-256 和大小與所選版本相符時，重新啟用新咒語視覺效果會重複使用已停用的 Patch-S，從而避免下載。
- 普通停用副本移至資料外部的已驗證交易備份中，即使活動 Patch-S 已匹配。透過恢復先前的安裝，不同的停用檔案仍然可以恢復。
- 適用於根和活動區域設定 Patch-S。 Off 仍使用普通的 `.mpq.disabled` 檔案名稱。現有的雜湊後綴存檔保持不變。
- 遊戲有效負載仍為 3.0.8 Lau。 Windows 和 Wine 都通過了 50 回歸組、真實文件開/關/開切換和精確回滾。

<a id="all-breath-and-slime-spray-warnings-are-now-90"></a>

## 所有呼吸和黏液噴霧警告現在為 90°

下列的 Warmane 測試員確認，Halion (兩個領域)、Saviana Ragefire、Sartharion、ICC Rimefang 和 Rotface Slime Spray 現已使用 **90° 總視錐細胞**，匹配辛達苟薩現有的 90° 警告。這適用於所有六個版本和九種客戶語言，包括現有的普通/英雄法術映射。

僅錐體寬度發生變化。範圍、動畫時間、原生法術效果和法術表都被保留。經批准的50%更大的Halion流星火半徑，淺藍色冷焰，顏色和奉獻度不變。這些是視覺警告緩衝區；伺服器損壞和機制保持不變。不平坦的地形仍會夾住扁平錐體。

<a id="updating"></a>

## 更新中

首先從該版本下載 **LauSetup.exe** 或 **LauSetup-Wine.zip**。關閉WoW，選擇相同的客戶端和視覺效果，然後按一下**安裝升級**。舊安裝程式保留其舊目錄。檢查 `/pyversion` 的 **3.0.8 Lau**。

安裝程式會驗證實際的 SHA-256 雜湊值，因此可以偵測到先前的版本，甚至是大小和時間戳記未更改的一位元組變更。只有確切的當前檔案才算作已安裝。備份和還原先前的安裝仍然可用。

Windows 需要.NET框架 4.8. Wine 用戶提取所有四個文件並運行 `LauSetup.sh` 作為普通用戶，具有受支援的現有 Wine/單聲道前綴。運行時安裝程式未捆綁。

<a id="validation"></a>

## 驗證

請參閱 VALIDATION.json 以了解 Windows 和 Wine 回歸、3.0.7 的六版升級、重複檢測、一位元組檢查、回滾和公共下載檢查。幾何檢查驗證每個版本中的 90° 錐體、保留範圍、有效邊界和三角形纏繞。恰好有 11 個現有檔案成員發生了變化：五個模型、他們的五個皮膚和版本目錄。所有其他成員與 3.0.7 的位元組相同。

寬度決定遵循報告的 Warmane 測試。此版本不是每次遇到或精確的伺服器邊界認證。

[網站變更日誌和安裝幫助](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-113--game-release-307-lau"></a>

# Lau Setup 1.1.3 · 遊戲發行 3.0.7 Lau

<a id="larger-halion-meteor-fire-warnings"></a>

## 更大的 Halion 流星火警告

促進測試人員批准的 **測試 v2**：Halion 的紅色地面標記半徑 **50% 大於發布版 3.0.6**，圍繞小徑和著陸火力。不包括測試 v3。冷焰、顏色、動畫軌跡、原生火焰、奉獻和 Sindragosa/Rotface 錐體均保持不變。支援所有六個版本和九種客戶端語言。

測試人員在修正未更新的補丁後確認了 v2。這是一個視覺警告緩衝區，而不​​是對伺服器損壞的更改或對每個位置或遭遇的認證。

<a id="update-with-the-new-installer"></a>

## 使用新安裝程式進行更新

首先從該版本下載 **LauSetup.exe** 或 **LauSetup-Wine.zip**。關閉WoW，選擇相同的客戶端和視覺效果，然後按一下**安裝升級**。舊的安裝程式保留舊的目錄。 `/pyversion` 報告 **3.0.7 Lau**。

現有 3.0.6 和測試 v2 用戶將收到更新。安裝程式會比較實際的檔案雜湊值，包括大小和時間戳記不變的一位元組變更；只有確切的目前檔案才算已安裝。備份和還原先前的安裝仍然可用。

Windows 需要 .NET Framework 4.8。 Wine 使用者擷取所有四個文件，並以一般使用者身分執行 `LauSetup.sh`，並使用受支援的現有 Wine/Mono 前綴。沒有捆綁運行時安裝程式。

<a id="validation-1"></a>

## 驗證

Windows和Wine安裝程式回歸、六版升級、重複偵測、一位元組檢查、回溯和公共下載檢查都記錄在VALIDATION.json中。 Halion 模型和皮膚與測試 v2 的位元組相同。僅其幾何/邊界和版本 TOC 與 3.0.6 不同； Coldflame 和其他存檔成員沒有變化。

[网站变更日志和安装帮助](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-112--game-release-306-lau"></a>

# Lau Setup 1.1.2 · 遊戲發行 3.0.6 Lau

<a id="blue-coldflame-red-meteor-fire"></a>

## 藍色冷焰、紅色流星火

- **Marrowgar Coldflame：** 淺藍色圓圈，具有現有的向內發光和順時針動畫，包括英雄。
- **Halion 流星火：** 使用現有的順時針動畫在軌跡周圍發射紅色圓圈並著陸火力。
- 所有六種高清/非高清版本和九種客戶語言。原生火焰、持續時間、奉獻選擇和 90° Sindragosa / 60° Rotface 錐體保持不變。

[動畫色彩預覽和完整變更日誌](https://wrath-multilingual-hd.vercel.app/#changelog)。預覽是說明性的模型，而不是遊戲中的錄音。伺服器損壞和機制不變；警告邊緣仍然是視覺緩衝區。

<a id="already-installed-download-the-new-installer-first"></a>

## 已經安裝了嗎？首先下載新的安裝程序

從此版本下載 **LauSetup.exe** 或 **LauSetup-Wine.zip**。關閉WoW，選擇相同的資料夾和視覺設置，然後點擊**安裝升級**。舊的下載安裝程式保留舊的嵌入式目錄。

安裝程式對實際檔案進行哈希處理。舊的 3.0.5 檔案被取代；即使檔案大小和時間戳記相同的一位元組變更也會被偵測到。只有全新的檔案才會被視為已安裝。 `/pyversion` 報告 **3.0.6 Lau**。備份和還原先前的安裝仍然可用。

Wine 使用者：將所有四個檔案一起提取並運行 `LauSetup.sh` 作為您現有的一般用戶 64-bit Wine 11.0 / 單核白血球增多症 10.4.1 前綴。 Python 3.9+ 和當地的 Linux 需要存儲。 Windows 需要.NET框架 4.8。運轉時不捆綁。

<a id="fresh-verification-on-windows-and-wine"></a>

## Windows 和 Wine 的最新驗證

- 每個平台的 38 回歸組，包括每個 108 區域設定/版本/地圖計畫。
- 所有六個實際的 3.0.5 到 3.0.6 升級，在兩個平台上重複無操作安裝和精確回滾。
- 在兩個平台上的根和語言環境 Y 中獨立檢測和修復一位元組相同大小/相同時間戳更改。
- 匿名 GitHub 有效負載下載、實際核心安裝以及 Windows 和 Wine 上的回滾。
- 15 Linux 主機安全測試和一般使用者下的精確四檔案 Wine 啟動器；Windows 表單渲染已檢查。
- 三個標記 M2 紋理參考和每個版本更改的版本目錄；添加了兩種顏色紋理。所有其他成員都逐字節保存。

這些安裝程式檢查並不驗證每個 Linux 發行版或每個遊戲內遭遇。 執行檔沒有數位簽章。附有詳細的證據、校驗和和來源。

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-111--game-release-305-lau"></a>

# Lau Setup 1.1.1 · 遊戲發行 3.0.5 Lau

<a id="wider-raid-warnings"></a>

## 更廣泛的襲擊警告

- 辛達苟薩冰霜吐息：**75° → 90° 總計**（7.5° 每側額外）。
- 腐臉黏液噴霧：**25° → 60° 總計**（17.5° 每側額外）。
- 適用於所有六個高清/非高清版本，並適用於所有九個客戶端區域設定。其他指標、奉獻設定、在地化表格和藝術品均保持不變。

這些是由 Warmane 突襲鏡頭和法術命中日誌通知的緩衝視覺警告。他們不會改變伺服器的損壞或機制，也不會要求精確的損壞邊界。

<a id="updating-an-existing-installation"></a>

## 更新現有安裝

首先下載新的 **LauSetup.exe** 或 **LauSetup-Wine.zip**。關閉WoW，選擇相同的資料夾和視覺選擇，然後按一下**安裝升級**。安裝程式會比較實際的檔案雜湊值：舊的 3.0.4 補丁被替換，而確切的 3.0.5 安裝報告為已安裝。 `/pyversion` 更新後報告 **3.0.5 Lau**。舊下載的安裝程式保留其舊目錄。

Windows 和 Wine 下載包含相同的重建安裝執行檔。對於 Wine，將所有四個文件一起提取並使用 `LauSetup.sh`，如隨附的自述文件中所述。現有的運行時要求保持不變。

<a id="verification"></a>

＃＃ 確認

所有 38 Windows 回歸組均已通過，包括 108 語言環境/版本/地圖計畫。所有六個版本都通過了實際的 3.0.4 到 3.0.5 升級、重複安裝和精確回滾檢查。新的有效負載通過了匿名下載/哈希檢查；與 GitHub 的隔離核心安裝並已通過回滾。每個版本都保留除四個模型/幾何檔案和版本目錄之外的所有成員。

Wine 啟動器程式碼未更改，ZIP 包含準確的重建 EXE。保留早期的 Wine 11.0 / Mono 10.4.1 運行時證據；由於 Docker 引擎未啟動，新的 Wine 執行不可用。新的錐體幾何形狀是靜態驗證的，而不是在遊戲中新認證的。

隨附下載校驗和、原始碼和詳細驗證報告。保留 `LauSetupBackups` 以供恢復。

Author / Creator / Last Modified By: Neil Mitchell

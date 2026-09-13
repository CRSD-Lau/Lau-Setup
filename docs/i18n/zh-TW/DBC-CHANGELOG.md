<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.4.0** — 一個 ZIP 現在同時包含 Windows 安裝程式和 Linux/Wine 啟動器。介面會在十種選項中自動跟隨作業系統語言，手動選擇會被儲存。遊戲版本 3.0.8 和遊戲檔案均未變更，也沒有 DBC 修改。
>
> 由於 Google HTTP 429，完整指南更新仍在等待中。下方正文可能已過時；請以目前英文來源和 1.4.0 發行說明為準。 [English](../../../DBC-CHANGELOG.md) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)
>
> **目前下載：** Windows 和 Linux/Wine 都使用 [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)。解壓含五個檔案的 `LauSetup/` 資料夾：Windows 開啟 `LauSetup.exe`；Linux/Wine 執行 `LauSetup.sh`。下方關於個別 EXE 或 Wine ZIP 的舊說明不適用於 1.4.0。
>
> **1.4.0:** 已識別的額外升級檔案會自動備份，然後繼續安裝。還原操作會將檔案放回原位。無需手動移動。 安裝程式在替換或移動現有檔案之前會自動保留原檔案。無關檔案保持不變。


> **1.4.0:** 選擇遊戲資料夾 → 下一步 → 選擇視覺效果 → 下一步 → 確認 → 安裝升級 → 完成。根據偵測到的用戶端固定選擇 Patch-Y HD 或 Patch-Y Non-HD。額外選項預設關閉；已安裝的地圖升級會保留。確認頁列出 Patch-Y（Lau 版本）及所選額外內容、WoW.exe、Patch-Q、語言檔案、下載大小和備份。下一步不會變更遊戲檔案。每一步都可手動選擇介面語言並儲存；自動會重新使用系統語言。仍可使用還原上次安裝。

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> 自動翻譯。 [英文來源](../../../DBC-CHANGELOG.md)。若措詞不同，則以英文來源為準。

<a id="dbc-changelog"></a>

# DBC 變更日誌



追蹤客戶端 DBC 編輯與模型、紋理和安裝程式變更分開。遊戲版本和安裝程式版本是分開的：`/pyversion` 報告遊戲版本。

<a id="handoff-history-andre-303-onward"></a>

## 切換歷史記錄：Andre 3.0.3 向前

[個人DBC編輯與開發歷史](docs/dbc/history/INDIVIDUAL-EDITS.md) · [六版比較與基準雜湊](../../dbc/history/andre-to-3.0.4.json)

Andre 故意省略 **Spell.dbc** 以避免局部化衝突。最初的 Lau 覆蓋暴露了該依賴關係； **Lau和Andre一起調試**，多語言重建解決了拼字文字相容性問題。保留的 Andre 檔案包含其他六個視覺/模型 DBC，因此不應將其描述為缺少每個 DBC。

Lau 將里程碑描述為 **3.0.4：初始表格添加**, **3.0.5：多語言分辨率**， 和 **3.0.6–3.0.8：版本更新的修補程序**。早期版本標籤重疊：已歸檔的已發佈版本已標記 3.0.4 已經包含多語言修復。下面的工件比較使用精確的雜湊值，並且不會刪除該開發歷史。

最初的 Patch-Y 比較包括每個版本十五個法術視覺連結編輯、新的指示器視覺/套件/附件記錄、奉獻差異和解碼的在地化編輯。新增的表格與其基礎股票或 HD Spell 基礎進行比較，因此繼承的記錄不會作為新創作的作品呈現。 [本地化階段驗證](../../dbc/history/localization-stage.json) 確認四個保留的預先本地化高清/非高清版本中文字重建保留的數位資料。

<a id="archived-releases-304--308"></a>

## 檔案版本 3.0.4 → 3.0.8

|存檔過渡 | DBC 結果 |其他變化|
| --- | --- | --- |
| 3.0.4 → 3.0.5 |沒有 DBC 編輯；42 相同表| Sindragosa 和 Rotface 圓錐幾何形狀，版本標籤 |
| 3.0.5 → 3.0.6 |沒有 DBC 編輯；42 相同表| Coldflame/Halion 標記顏色資源和參考、版本標籤 |
| 3.0.6 → 3.0.7 |沒有 DBC 編輯；42 相同表| 批准的 Halion 流星火幾何形狀，版本標籤 |
| 3.0.7 → 3.0.8 |沒有 DBC 編輯；42 相同表|剩餘呼吸/史萊姆噴霧錐體幾何形狀，版本標籤 |

[所有 168 表比較和存檔雜湊](../../dbc/history/3.0.4-through-3.0.8.json)。這些是保留版本工件的比較，而不是聲稱早期的本地化事件沒有發生。

<a id="307--308--no-dbc-edits"></a>

## 3.0.7 → 3.0.8 — 無 DBC 編輯

隨 [安裝程式 1.1.4](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.1.4) 一起發布。所有 **42 DBC 比較都逐字節傳遞**：六個 Patch-Y 版本中的每個版本都有七個表。沒有新增/刪除表、更改記錄、更改欄位或更改字串區塊。

|表|記錄編輯|現場編輯|結果 |
| --- | ---: | ---: | --- |
| CreatureDisplayInfo.dbc | 0 | 0 |相同|
| CreatureModelData.dbc | 0 | 0 |相同|
| Spell.dbc | 0 | 0 |相同|
| SpellVisual.dbc | 0 | 0 |相同|
| SpellVisualEffectName.dbc | 0 | 0 |相同|
| SpellVisualKit.dbc | 0 | 0 |相同|
| SpellVisualKitModelAttach.dbc | 0 | 0 |相同|

[完整對比證據](../../dbc/3.0.7-to-3.0.8.json)記錄了每個版本的來源/目標MPQ SHA-256、每個DBC的SHA-256之前/之後、大小、行數和字段數。根據發布目錄檢查 MPQ 哈希值。其他 22 目錄資產（包括區域設定 Q 和共享 S 資產）保持不變。

<a id="what-actually-changed-in-308"></a>

### 3.0.8 中實際發生了什麼變化

透過編輯 `.m2` 幾何形狀和對應的 `00.skin` 邊界，將五個現有錐體模型拓寬至 **90° 總計**。保留現有的 DBC 綁定。

|模型莖|上一個角度 |新角度|
| --- | ---: | ---: |
| PW_Rotface_SlimeSpray_Fan25_Room | PW_Rotface_SlimeSpray_Fan25_Room | 60° | 90° |
| PW_White_Fan60_60yd_發光 | 60° | 90° |
| PW_White_Fan60_30yd_發光 | 60° | 90° |
| PW_White_Fan60_100y_發光| 60° | 90° |
| PW_White_Fan82_60yd_發光| 82° | 90° |

檔案名稱保留歷史角度標籤；幾何形狀決定顯示角度。辛達苟薩已經是 90° 並且在此轉變中沒有改變。這將所有受支持的呼吸和史萊姆噴霧指示器帶到了 90°。範圍和動畫時間沒有變化。 Halion 流星火半徑、冷焰顏色和奉獻度保持不變。

每個版本都有完全相同的變化 **11 檔案成員**： 五 `.m2` 文件，五個 `.skin` 文件和 `!pyandre.toc` 遊戲版本標籤來自 3.0.7 到 3.0.8。每個其他列出的內容成員都是相同的。 MPQ 容器記帳不在內容成員比較範圍內。

這驗證了客戶端檔案更改，而不是 Warmane 的伺服器機製或確切的損壞邊界。

<a id="setup-115-116-and-117--no-dbc-edits"></a>

## 設定 1.1.5、1.1.6 和 1.1.7 — 無 DBC 編輯

這些是安裝程式修補程式。他們的遊戲有效負載仍為 3.0.8，DBC 資料未更改。最新的修補程式更改了Patch-S的安裝、儲存和重複使用，而不是其內部DBC內容。

<a id="required-entry-for-future-releases"></a>

## 未來版本所需的條目

每個版本都必須在此處新增一個條目，並在其 GitHub 發行說明中新增 **DBC 變更** 部分，包括僅限安裝程式的版本。適用時明確聲明**無 DBC 編輯**。與先前的穩定遊戲版本進行比較，而不是與未發布的測試版本進行比較。不要將模型/紋理編輯描述為 DBC 編輯。

對於每個實際的 DBC 編輯，每個欄位記錄一行（或用於大型本地化變更的連結的機器可讀行級差異）：

|遊戲過渡 |表格|記錄ID |欄位名稱/從零開始的索引 |舊值 |新價值|版本/語言環境 |原因 |
| --- | --- | --- | --- | --- | --- | --- | --- |
|版本 → 版本 | TABLE.dbc |身分證 |命名欄位[索引] |先前值|新價值|受影響的變體 |目的|

也記錄新增/刪除的記錄和表、架構變更以及字串值編輯。當內容發生變化時，解碼字串值而不是報告字串塊偏移量變動。指定欄位索引約定和模式來源；標記未知欄位而不是猜測。附加歸檔前/後和表雜湊、比較方法和驗證限制。切勿在沒有證據的情況下聲稱比較已通過。

移交審計涵蓋從保留的 Andre 3.0.3 基線開始的 Patch-Y。單獨的 Q/S/地圖本地化管道和不相關的實驗構建不在此初步回顧範圍內。如果沒有符合的來源，則不會為早期損壞的工件指派版本號。

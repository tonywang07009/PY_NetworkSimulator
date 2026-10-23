# Ambient IoT DES：模組原型與工具規劃草案

> **2026-10-23 優先順序／時間範圍更新**：使用者指定首模組改為 IAB 網路拓撲，先完成[拓撲範圍盤點](iab-topology-scope.md)，不以本文件舊模組排序或全套 Config 定稿阻擋開工。首版一輪全部服務於全域 0 開始，輪長取最晚 Deadline（R-01 第 31 節）；舊多期需求更新與自行填週期長度不屬於首版必需範圍。逐模組原型、情境測試、人類理解後抽離流程維持。

更新：2026-10-20。狀態：架構討論草案；未建立模擬器、Notebook 或 OpenSpec change，未執行模擬器測試。使用者已確認逐模組的交付流程，模組切分及工具選擇仍為本次建議。

首版採逐模組 Notebook 原型，每個模組先完成對應情境測試，再由使用者逐段閱讀程式、確認理解與行為；接受後才抽離為 `.py`。這項最新決策取代先前「整體 Notebook 完成五類驗收後才能開始任何 `.py` 抽離」的順序；五類整合驗收仍保留，不能以單模組通過代替。

## 決策來源與邊界

- [交接規格](../../ReferDoc/Plan/Codex_Handoff_Specification_Ambient_IoT_DES.md) 與 [R-01](../../ReferDoc/Plan/R-01_System_Model_and_Baseline_Decision_Record.md) 是既有產品決策來源；新增決策見 R-01 第 25–27 節。
- [系統模型決策](../../ReferDoc/Plan/R-01_System_Model_and_Baseline_Decision_Record.md) 保留本次明確答案。此文件及[互動模組圖](system.html)是衍生設計，後續核准的行為及驗收歸入 OpenSpec，避免多份競爭規格。
- 沒有阻擋架構討論的未決問題。正式 TBS/payload、CFA、PHY/EH、情境分布與時間取整等設定，需在依賴它們的模組實作前明示來源或確認測試替代值。
- Q-TRADEOFFS-01 的 synthetic／正式參數順序仍未回答，暫緩到相關模組；本輪不代選、不採用數值、不安裝環境。
- 預告下一窗 CW 功率不代表預知下一窗時間或 SNR；引擎真實狀態不得直接傳給 Policy。保持既定的最多 8 Tag、固定 CFA、整數 ns、同時間批次結算及 Deadline 排他規則。

## 模組責任、輸入輸出及情境驗收

以下是邏輯模組，不要求一模組一 class。原型檔名為規劃，尚未建立。

| 順序／原型 | 輸入 → 輸出與所有權 | 對應最小情境 |
|---|---|---|
| 01 `contracts.ipynb`：Config／DTO | 明示配置、快照值 → 不含可變別名的 Observation、Action、事件資料；不推進時間 | 不合法型別／單位、負時間、重複 ID；修改輸入容器不影響快照；序列化前後一致 |
| 02 `energy.ipynb`：Tag／Energy | 舊能量、模式、已流逝區間、EH/功耗 → 能量增量／可行性；Tag 持有電池，Engine 決定提交時點 | 啟動不足、中途耗盡、容量飽和、非排程 Tag EH、Guard 無 CW EH、跨 cycle 不重置 |
| 03 `services.ipynb`：ServiceManager | 同時間合格新 payload 集合、期限、結算前需求 → 各服務認列增量／達標；持有服務帳及去重身分 | 8/8 缺 10 → 5/5；3/4 缺 5 → 2/3；同分 ID 排序、共享、重傳去重、完成凍結、期限前 1 ns／期限當下 |
| 04 `environment.ipynb`：Timeline／Channel | Scenario/config、分開的隨機來源 → 依時間揭露的本窗資源、SNR、EH rate／PHY 結果 | UE/DU 不衝突、同 seed 重現、同窗 SNR 不變、未來不可見、首窗功率初始化；物理模型參數待確認 |
| 05 `validation.ipynb`：ActionValidator | 原 Action、當前快照及固定配置 → 拒絕原因／不可變執行計畫；不提交真實狀態 | 0/1/8/9 Tag、重複 ID、非法 TBS、CFA 衝突、時間不足、能量不足；空集合走合法 NO_OP 分支 |
| 06 `engine.ipynb`：SimulationEngine | 已驗證計畫、外生事件及模組 → 時間推進、唯一狀態提交與 Trace | 同時間事件入隊順序置換、區間只積分一次、CW_OFF 一次、Guard end 等於窗末、NO_OP／非法動作停排與下窗恢復 |
| 07 `scheduling.ipynb`：Node／最小 Policy | 引擎允許的當前資料 → 新 Observation → Tag/TBS Action；Node 組合資料，Policy 提議 | 每次 Guard 後快照更新、不可修改真值、不可讀未來；最小測試 Policy 驅動兩批，不冒充正式 Baseline |
| 08 `integration.ipynb`：整合驗收 | 已接受的 `.py` 模組、完整 run 配置 → ACPT-01～05 結果與 Trace | 多批／跨窗、能量、同時事件期限、服務共享、非法 Action／DTO 隔離；固定 seed 重跑一致 |

Trace 是第一個有狀態模組起就使用的共同輸出契約，不等到最後才補。01 只做資料契約；02–05 的情境透過顯式輸入驅動，不另造一套模擬時鐘。06 接回全域事件時鐘，07 才接入實際決策循環。

Engine 收到事件後依序：結算舊能量區間 → 批次收集接收結果 → 服務認列與截止／CW 關閉 → Guard/Window 狀態更新 → 合法時建立 Observation → Policy Action → Validator → Engine 執行或停排。具體函式名稱在實作時依已接受的 Interface 定義，不提前假裝已有程式呼叫證據。

## 每個模組如何完成

1. 先寫目的、Interface、狀態所有者、必需配置及輸入／預期輸出的情境表；依賴的未決值先確認。
2. 在 Notebook 先寫對應情境斷言，再做最小實作；展示具名輸入、預期值、實際結果與必要 Trace。測試覆蓋該模組相關的空值、零值、負值、上下界、重複及時間交界，避免只驗證正常路徑。
3. 重新啟動 kernel 後從頭執行；不得靠亂序執行或隱藏全域變數通過。失敗輸出相關時間、Window/Batch、Tag/Service 與原因。
4. 提供完整原型及 tree 式 `code-trace.md`，按資料流逐段說明每段程式、狀態變更與對應測試。使用者閱讀、提問及接受；未接受前保留在 Notebook。
5. 接受後只抽離核心到 `.py`，不更改模型；同一組情境測試在抽離前後比較認列、能量、錯誤碼及規範化 Trace。若行為改動，修正並重新確認受影響部分。
6. 保留 Notebook 作導讀與示範，改為 import 已接受的 `.py`；移除已搬出的重複核心定義。後續 Notebook 只 import 已接受模組，不 import 或 `%run` 尚未接受的其他 Notebook。

單模組人類接受是本地程式導讀關卡，不等同整合通過或 PR 已合併。OpenSpec change／Issue／PR 的實際拆分在開發範圍確定後安排；不默認每個 Notebook 都是一個 change，亦不因本地 `.py` 抽離就宣稱 workflow 完成。

## 工具建議與本機觀察

下列為本機 `python`（3.12.12）於 2026-10-20 的 metadata 探測，不代表其他虛擬環境、kernel 或使用者 IDE 的狀態，也不代表套件已通過執行測試。尚未安裝或更改任何依賴。

| 用途 | 建議選擇 | 理由／目前狀態 |
|---|---|---|
| 核心資料與事件 | Python 標準庫 `dataclasses`、`enum`、`heapq` | 小介面可直接表達資料與最早事件；同時間語意仍由 Engine 明確實作。`frozen=True` 不能單獨保證深層唯讀，需使用 tuple／不可變巢狀值與複製 |
| 情境與 Trace | 標準庫 `json`、`pathlib`，分開的 RNG 實例 | 明示單位／版本／seed；JSONL 便於逐事件查看。固定 seed 仍需固定配置、演算法版本與抽樣規則 |
| Notebook 編輯／執行 | 使用者既有 Notebook 編輯器；`ipykernel`、`nbformat`、`nbclient` | 支援可讀原型與乾淨 kernel 自動執行；目前解譯器未找到這三個套件，實作前需對齊環境。未檢查使用者 IDE，不推定需裝 JupyterLab |
| 自動驗收 | Notebook 中的具名測試函式與 `assert`；抽離後使用 `pytest` | 同一案例跨格式複驗，失敗訊息附情境身分；pytest 9.1.1 已有 metadata |
| 數值與繪圖 | 有需要才用 NumPy／Matplotlib | metadata 為 2.3.5／3.10.8；可畫能量／事件圖，圖不能代替 assert；純計帳不強制用陣列 |
| DES 框架 | 首版建議標準庫最小 Engine | 目前需求重點在同時間批次提交與能量因果；先明示語意，無需先引入額外框架。SimPy 此解譯器未找到；此為設計取捨，非效能優劣證據 |
| 架構／需求 | 既有 Archify、OpenSpec | 使用本專案已有路由；本輪是規劃草案，沒有模擬器 runtime 證據 |

官方技術資料：[heapq](https://docs.python.org/3.12/library/heapq.html)、[nbclient 執行 Notebook](https://nbclient.readthedocs.io/en/latest/client.html)、[pytest assertions](https://docs.pytest.org/en/stable/how-to/assert.html)。這些資料支持工具能力，不證明本專案已整合通過。

## 待實作前確認

| 項目 | 何時需要 | 本輪處理 |
|---|---|---|
| synthetic 或正式參數與其來源 | 依賴具體時序／PHY／EH 的模組前 | 保留 Q-TRADEOFFS-01，不阻擋架構 |
| Python/kernel／依賴與專案環境 | 首個 Notebook 執行前 | 先回報目前缺口，不改使用者層級設定 |
| `.py` 抽離 | 各模組情境測試及人類閱讀後 | 使用者已指定流程；等待該模組的具體人類接受，毋須重問流程 |
| 正式 Baseline／公平性彙整與研究校準 | 演算法比較前 | 保留既有未決事項，不納入最小 Engine 自動補規則 |

下一個可討論的工作是 01 Config／DTO 的欄位、單位與讀寫權限，先檢查實際資料例子再寫原型；目前沒有啟動程式實作。

2026-10-20 更新：使用者已指定 Config／DTO／必要 Enum 定義集中於單一 `.py`，類似 C `.h`；內部 State 定義留各模組。詳見 [Config／DTO 討論](config-dto.md)。共用檔名及精確欄位仍待設計，尚未建立程式檔。

# Config／DTO 集中定義：討論草案

> **目前首版範圍（2026-10-23）**：依 R-01 第 31 節，本輪全部服務從全域 t=0 開始，輪長取最晚 Deadline；先前獨立指定週期長度／多期依序服務的候選設計已被取代。服務 Deadline 可等於輪末，認列仍為 `t<deadline`。目前優先 [IAB 拓撲模組](iab-topology-scope.md)，不以整份服務契約定稿阻擋拓撲盤點。

日期：2026-10-20。尚未實作。使用者已指定使用標準庫 dataclass，集中於單一 `.py` 管理，類似 C 的 `.h` 共用資料定義；檔名建議 `contracts.py`，實際路徑尚未決定。仍沿用 Notebook 原型、情境測試與人工理解接受後才抽離 `.py` 的順序，未先建立程式檔。

最新時間資訊（2026-10-23）：DU Window 固定 600 ms；單項服務的 10～15 s 起指完成 Deadline。本輪所有服務同時從 0 起算，`T_round=max(deadline_i)`；15／20 s 的例子輪長為 20 s，不再獨立選擇 Q-DECISION-03 的 A/B。

## 資料的生命週期

| 類別 | 目的／例子 | 誰建立與使用 |
|---|---|---|
| Config | 描述本次 run 的條件，例如 Tag 容量、服務需求、合法 TBS、固定 CFA 設定 | 情境入口建立，交給需要的模組；不向 Policy 傳遞含完整未來時序的整份 run 配置 |
| DTO | 模組當次交換的資料，例如當前 Tag 能量快照、服務缺口、Tag/TBS 動作、驗證結果 | 生產模組建立，消費模組依契約讀取；每次決策重新建立 Observation |
| State | 模擬中會變化的電池、模式、服務認列與事件佇列 | 各既定狀態所有者持有，型別定義留各模組；Engine 協調提交 |

容量 `capacity_j` 屬 Tag Config；當前真實 `energy_j` 屬 Tag State；Policy 當次看到的 `energy_j` 屬 TagObservationDTO。三者數值可能相關，但不是同一份可變物件。

## 共用檔涵蓋範圍（已確認 A）

2026-10-20 使用者回答 A：Config／DTO／必要 Enum 集中於單一共用檔，內部 State 定義留各模組。下列具體名稱與欄位仍為設計草案。

- Config dataclass：按時序／固定接入、Tag、Service、Channel／Scenario 分組，再以 SimulationConfig 聚合；不預先補齊未決研究參數或採用巨大平面參數表。
- DTO dataclass：Tag／Service／Scheduling Observation，TagTbs／PagingBatch Action，ValidationResult／ExecutionPlan，必要事件與 Trace 資料。名稱與精確欄位逐項討論，不要求一次建立全部。
- 共用 Enum：僅在已有明確取值集合且跨模組需要時加入，例如動作驗證狀態；NO_OP 必須與接受／拒絕有可區分的結果，不以單一 accepted 布林值隱藏其語意。
- 型別定義可以集中，實際模擬函式與狀態更新留在原模組；共用檔僅依賴標準庫與自身資料型別，避免回頭 import Engine／Tag 等實作。
- 設定的具體數值與情境實例不等於型別定義；已確認在 Notebook 情境設定 cell 建立，不建立全域可變 SimulationConfig 單例。

## dataclass 使用建議

Config／快照／Action 建議 `@dataclass(frozen=True, kw_only=True)`；以具名參數建立，集合欄位使用 tuple 與不可變巢狀 dataclass。frozen 不能凍結 list／dict 的內容，需避免可變別名。這是程式介面約束，不是 Python 不可信程式碼的安全沙箱。

時間用 `*_ns: int`，能量用 `*_j: float`，功率明示 W 或 dBm，資料用 `*_bits: int`；ID 型別與排序仍需明示。範例：

```python
# 形狀示意，非已實作／已核准欄位全集
@dataclass(frozen=True, kw_only=True)
class TagTbsActionDTO:
    tag_id: int
    tbs_bits: int

@dataclass(frozen=True, kw_only=True)
class PagingBatchActionDTO:
    items: tuple[TagTbsActionDTO, ...]
```

dataclass 型別註記不會自動做執行期型別或數值範圍檢查。配置入口負責拒絕無效設定；Policy Action 的重複 Tag、非法 TBS、時間／能量／資源可行性保留共用 Validator 原子拒絕並記錄。不可先在 DTO constructor 丟出例外而漏掉 Engine 應記錄的 INVALID_ACTION；具體錯誤接收契約後續在 Validator 設計時封閉。

官方依據：[Python 3.12 dataclasses](https://docs.python.org/3.12/library/dataclasses.html)。

## 第一項範圍問題（已回答）

Q-INFLUENCE-01：這個共用檔集中 Config／DTO，或連模組內部的 State dataclass 定義也一起集中？

- A（建議）：集中 Config／DTO／必要 Enum；內部 State 定義留各模組。方便跨模組查契約，內部結構修改較局部。
- B：連 TagState／ServiceState 等資料型別也集中；結構一處可查，但內部狀態與跨模組契約會放在同檔，需分段標示權限。

兩者都不集中狀態實例，不允許 Policy 持有可變 State 引用，亦不改變既有狀態所有權。使用者已選 A，不再重問。

## Config 分組建議與使用例子

同一個共用 `.py` 可包含多個小 dataclass；使用 SimulationConfig 組合本次 run 所需配置，模組只取得其需要的部分，Policy 只取得合法 Observation。

| 結構（建議名稱） | 內容／生命週期 |
|---|---|
| SimulationConfig | scenario_id、seed、本輪服務及以下配置的組合；在 run 前建立，執行中不改動；輪末取各服務 Deadline 最大值，不另填週期數／獨立輪長 |
| AccessConfig | Paging／Guard 時長、合法 TBS 與 payload 映射、固定 BD/SFS/CFA 配置；最多 8 Tag 是既定限制，不任意開放調高 |
| TagConfig 的集合 | 每 Tag 的 ID、容量、模式功耗、啟動成本及 EH 參數；初始滿電由已定模型初始化，不提供任意初始能量開關 |
| ServiceConfig 的集合 | Notebook 明列本輪全部服務、指定 Tag、最低 payload 與排他期限；2026-10-23 改為全部服務同時在全域 0 啟動，多期更新不屬於首版 |
| EnvironmentConfig | UE/DU 情境生成、通道／CW 的外生配置；具體分布與數值仍待來源確認，不含 Policy 可直接預覽的完整未來 Trace |

例如換一組 Tag 的電池容量，只改該組 TagConfig；執行過程扣耗只更新 TagState，不改 TagConfig。DTO 在後續再分別列出每次交換的當前資訊。

### Q-TRADEOFFS-02｜原型階段在哪裡填入配置值（已回答 A）

目的：區分集中定義資料結構與每個測試情境採用哪些數值。例：兩個情境可共用 TagConfig 定義，但使用不同容量；不需修改共用檔或其他模組。

- A（建議）：先在 Notebook 的「情境設定」cell 用具名參數建立 dataclass 實例，方便人類閱讀及修改；每次執行仍保存完整配置快照。批次實驗需要時再加外部配置載入。
- B：一開始就從外部 JSON 載入並轉成 dataclass；方便批次情境，但需先設計檔案格式、轉換與輸入驗證。

使用者於 2026-10-20 選 A：Notebook 情境設定 cell 以具名參數建立 Config 實例，執行時保存完整配置快照。此答案不影響仍未回答的 synthetic／正式參數來源題；目前不需先增加外部 JSON 載入器。

## SimulationConfig：run 的識別與停止條件

先確定 run 範圍，再逐項定義各組 Config 欄位。`scenario_id` 用於識別情境；`seed` 是重現輸入之一，仍須與完整配置及程式版本一起保存。初期模擬從 0 ns 開始是設計建議，未提供任意起始時刻功能。

### Q-DECISION-02｜一次 run 何時結束（已回答 A）

目的：避免驗收統計涵蓋到未完成的服務週期，或到達停止時間時仍不清楚哪些資料應結算。例：3 個服務週期各 100 ms，跑完 3 個週期與固定跑 250 ms，最後統計的服務集合不同。此處數值僅示意。

- A（建議）：以指定服務週期數停止；完整跑完 N 個 cycle。適合逐週期檢查服務結果與電量持續性，總時間由各週期長度推得。
- B：以固定模擬時間停止；可能落在 cycle 中間，需另定尚未到期限服務的統計與已開始傳輸的終止處理。

使用者於 2026-10-20 回答 A：以完整服務週期數停止；總時間由各週期長度推得，不另設可獨立矛盾的固定時間停止欄位。最後週期結束後不建立下一期服務，精確邊界的物理事件結算仍需與 Engine／Window 語意核對。服務統計逐期重設，Tag 電量持續保留，不能用重啟 N 次模擬代替連續 N 個週期。

## 服務週期配置草案

每個服務週期需要長度及當期服務集合；各 ServiceConfig 描述指定 Tag、最低 payload 需求與 Deadline。既有決策只要求服務在當期起點固定，不代表所有週期的服務需求相同。

建議欄位：`duration_ns: int`（週期長度，正整數）、`services: tuple[ServiceConfig, ...]`（本期服務定義）。週期 ID／起點可由引擎依序產生，避免與累積長度不一致；具體欄位尚未核准。服務 Deadline 需嚴格落在週期內，輸入格式與 slot 轉換另行明示，不擅自延長期限。

### Q-INFLUENCE-02｜各週期的服務需求從哪裡來（已回答 B）

目的：確定週期設定的資料形狀。例：第一期 S1 需要 A/B，第二期 S2 需要 B/C；這仍符合每期起點固定，不是期中動態到達。

- A：全部週期重複同一份服務模板；最少設定，但無法直接測不同週期需求。
- B（建議）：Notebook 明列每一期服務設定；可重複也可不同，便於人類核對情境與跨期行為，代價是逐期填寫。
- C：由服務生成參數與 Seed 決定每期需求；適合大量實驗，但需先確認需求分布、生成規則及重現性。

使用者於 2026-10-22 回答 B：Notebook 明列每一期服務設定，各期可相同或不同；首版不自行以 Seed 生成服務需求。週期長度是否相同及具體數值未在本題鎖定；此題只決定服務集合如何提供。

後續討論清單見 [剩餘設計與配置事項](remaining-discussion.md)，區分本階段資料契約、相關模組實作前配置與正式研究議題；不把每個欄位都轉為額外確認題。

2026-10-22：已整理 [三層 Config 欄位與兩週期範例](service-config-example.md)。相對 Deadline、週期長度表示、ID 型別及清單長度推得週期數為設計建議，尚未視為使用者已接受。

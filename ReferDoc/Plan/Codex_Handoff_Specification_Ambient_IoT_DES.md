# Codex Handoff Specification — Ambient IoT DES Simulator v1

> **用途**：Codex 的首版 `.ipynb` 模擬器實作交接規格；本文件不是實作完成證明，也不是 3GPP 規範符合性證明。  
> **交接日期**：2026-10-20  
> **階段**：Architecture Decisions CLOSED / Implementation NOT STARTED / Tests NOT RUN  
> **授權狀態**：**目前僅授權文件整理；Codex 實作前仍須獲使用者另行授權。**  
> **權威來源**：`R-01_System_Model_and_Baseline_Decision_Record.md`，**尤其第 14–25 節；遇歷史章節狀態衝突，以較後之正式 [DECIDED] 為準**。對應附件：`system_model.pdf`、`Baseline.pdf`、`模擬器設計.pdf`。不得將來源提案或候選值直接視為 3GPP 規範事實。

> **補充決策**：第 26 節已確認空 Action 為合法 `NO_OP`，停止本 Window 後續排程，下個 Window 再決策；本檔第 5 節已同步。

> **最新首版範圍（2026-10-23，R-01 第 31 節）**：一輪全部服務於全域 t=0 同時出現，輪長 `T_round=max_i deadline_i`；例：15 s／20 s → 輪長 20 s。取代下文首版多期依序啟動、獨立手填共同週期長度與全部 Deadline 嚴格早於期末的舊要求；允許最晚 Deadline 等於輪末，服務成功仍嚴格 `D2R_END<deadline_i`。優先模組為 IAB 拓撲 Notebook，先盤點拓撲直接依賴的決策。

> **拓撲配置更新（R-01 第 32 節）**：1 Donor 直連 5 IAB Nodes，各 1 UE 與多個隨機關聯／部署 Tags；CW／Reader 共址與 IAB split 支援列研究擴充。回傳無干擾，干擾僅考慮 Node–Tag 段。全場 30 Tags 的例子為好 10／中 13／差 7，不當每 Node 各 30 或均分。`main.pdf` 第 3／4 頁已閱讀；已選室外農場研究情境，僅沿用 T1／共址意圖、不套完整 D1 室內參數。戶外距離／干擾證據見 `docs/architecture/outdoor-literature-evidence.md`；分區幾何／品質定義及生成參數仍需對齊，未選定半徑或干擾值。

> **最新交付流程（R-01 第 27 節，2026-10-20）**：使用者改為「每模組 `.ipynb` 原型 → 對應情境測試 → 人類閱讀理解與接受 → 抽離該模組 `.py` → 等價複驗」。本規則優先於本檔下方整體 Notebook 通過後才開始 `.py` 的舊順序；五類整合驗收仍需完成。當前只進行架構／工具規劃，尚未啟動原型實作，亦未發生任何模組的人工接受。

## 0. Codex 任務邊界與建議順序

**最終任務（使用者未來另行授權後才開始）**：先在 `.ipynb` 建立具可重播 Event Trace 的最小 Discrete-Event Simulator；依固定 Scenario／Seed 執行自動化 Invariant Tests；全部通過後**才**可在另行授權下重構成 `.py`。首版用於驗證時間、資源、能量與服務計帳，而非預先宣稱某演算法效能優越。

**不得自行擴大範圍**：不建立 AI／DRL／其他演算法架構、不引入新的協定訊令（尤其不引入 1-bit energy report）、不加入 BD/SFS 最佳化器、不改動既有 GitHub／發布程式、不代替使用者決定未提供的 PHY 參數、不預設模型/方法的性能或標準合規性。

**建議工程順序（不是新增研究決策）**：
1. 閱讀本檔與決策紀錄第 14–25 節，列出配置缺口與來源對照。
2. 定義固定配置結構及 DTO 欄位契約；設定 deterministic Scenario fixtures。
3. 實作可觀測性隔離、事件排程／相同時間戳批次提交、Window／Guard 狀態機。
4. 接入 Tag 能量帳本、Channel 當前狀態、固定 CFA 映射及 Validator。
5. 接入 ServiceManager 計帳與最簡可替換 Policy；產生 Trace。
6. 驗證 ACPT-01～05 與各模組 invariant；失敗即停在 Notebook 階段，不急於轉 `.py`。

## 1. 系統範圍及研究目標 [DECIDED / MODEL]

- **拓樸**：具 IAB 無線回傳情境的 A-IoT Node；Node 整合 Reader，Tag D2R 直接回傳 Node，沒有 UE Reader relay。Node 的可用 DU Window 受外生 UE UL／TDD 資源占用影響。此為研究系統模型，不宣稱所有 3GPP 部署均如此。
- **服務（第 31 節更新）**：首版一輪全部服務於全域 t=0 啟動，需求、指定 Tag、最低有效 payload 與各自 Slot-level Deadline 在起點固定；不同服務 Tag 集合可重疊。相同服務成功資料可跨 Paging batch、跨 DU Window 累加；輪長取最晚 Deadline，各服務仍在其排他期限前認列。多輪服務更新不屬於當前首版必需範圍。
- **主要目標**：最大化每項服務在自身期限前達到最低需求的**服務數**。次要目標為服務內指定 Tag 集合的需求內貢獻 Max–Min Gap；多服務關注最差服務公平性。不可將「最大總 bits」偷偷取代主要目標，亦不可把未定的正規化分母偽裝為已決定的目標函式。
- **Baseline 審查定位**：`Baseline.pdf` 反映利用 CW 功率／鏈路分類、服務內貢獻差距及 TBS 對 Tag 進行排程的思路；尚無可直接視為經完整驗證之演算法實作。共享 Tag 是否在排序中額外加分與公平性正規化屬後續演算法／評估議題，不阻擋首版 Engine 建構。

## 2. 時間、Window、CFA、CW 行為 [DECIDED]

| 介面與不變量 | v1 生效要求 |
|---|---|
| 內部時鐘 | 所有事件、期限與排序使用**絕對整數奈秒 `int ns`**；顯示時間可轉 ms/μs，不得以浮點顯示值回寫時間戳 |
| Slot Grid | 15 kHz SCS、normal CP：1 ms NR slot = 1,000,000 ns；事件可在 slot 內發生 |
| Deadline | `deadline_exclusive_ns=(last_allowed_slot+1)*1_000_000`；有效認列嚴格 `D2R_END_ns < deadline_exclusive_ns` |
| DU Window | `window=[start_ns,end_ns)`；2026-10-23 使用者確認長度固定 `600_000_000 ns`（R-01 第 29 節）。Window 起點／間隔仍待配置，不代表連續每 600 ms 一窗；原先未來長度未知的敘述需按固定長度設定對齊，未來起點／完整 Trace 不揭露 |
| Window Channel | 對各 Tag，每個 DU Window 的 SNR 固定；下一 Window 更新；**跨窗是否獨立／相關未定**，不能自動宣稱獨立 |
| CW Power | Donor 每個 Window 指定一個固定 CW 功率，該 Window 所有 D2R 批次使用相同功率；Node 在**前一 Window**已得到下一 Window 功率預告（僅功率，非未來 SNR／時間） |
| Batch Limit | 每批 Paging 至多 **8 個 Tag**；固定合法 BD/SFS 組態與 CFA 資源池；Policy 不決定 BD／SFS／功率 |
| Batch Sequence | `Paging → CW_ON / D2R → last D2R_END → CW_OFF → Guard → GUARD_END`；若剩餘時間夠，允許同一 Window 的下一批 Paging |
| CW / EH | **只在 D2R 階段**開啟 energizing CW；在 UE UL、Paging、Guard 關閉。CW 覆蓋下，未排程 Tag 也可 EH；已排程 Tag 可同時 backscatter + EH，但能量分流參數不可憑空設定 |
| Guard | 每批最後的 D2R 結束立即 `CW_OFF`，Guard 全段 CW EH 為零；`last_D2R_END + guard <= window_end`；下一批只能在 `GUARD_END` 後開始 |
| Re-decision | `GUARD_END` 完成當前狀態提交後，重新生成 Observation 並呼叫 Policy；不在 Window 起點先規劃全部批次 |
| Failure Action | 非法 Action 拒絕**整批**；當前 Window 不再新 Paging；仍處理既有外生事件／Deadline；下一 Window 才恢復 |

**CFA 固定資源映射**：使用**每批**共享的固定合法資源池；以確定性映射規則指派至多 8 個被選 Tag 的專用 CFA 資源，禁止資源衝突。不將 Tag 永久綁死資源，也不引入動態 BD/SFS 適應或最佳化。**映射所需的具體資源池表、各 BD/SFS 固定值、TS/頻率映射與能力上限需從既有正式參數來源／配置明示提供；未提供時採配置缺失回報，不得捏造。**

## 3. DES Engine：同時間事件與狀態所有權 [H-01]

每次取出時間戳 `t`，先收集所有同時到期事件，按**邏輯階段**結算；不要讓 heap 插入順序改變物理或服務結果：

1. 對 `[previous_boundary,t)`，使用**舊 CW 狀態、舊 Tag mode** 結算能量與資源占用；同一段時間不得重算。
2. 收集所有 `D2R_END(t)`；每個唯一 `(window,batch,tag,transmission)` 接收結果只能決定／提交一次；使用同一個結算前 ServiceManager 快照批次認列合格新 payload。
3. 依 `t` 的截止邊界結算 `SERVICE_DEADLINE`、`DU_WINDOW_END`、批次最後 D2R 結束時的 `CW_OFF`；時間上相同的 Deadline 一律採 `< deadline_exclusive_ns`，不可偷改為 `<=`。
4. 完成 `GUARD_END` 與全部應生效的截止／狀態更新後，若 `t < window_end_ns` 且 Window 未被非法 Action 停排，建立**新** Observation；可行時允許下一批決策。`GUARD_END == WINDOW_END` 不可開始新批次。
5. 同時間衍生事件必須形成**有限的因果閉包**；禁止零時間無限排程迴圈。每個 Batch 只能有一次 `CW_OFF` 與一次服務認列提交。

**狀態主權**：`SimulationEngine` 推進事件與提交狀態；`Tag` 持有物理電量／模式；`Channel` 決定本 Window 通道狀態與接收／EH 模型；`ServiceManager` 對服務認列、期限與 payload 去重負責；`ResourceTimeline` 保有完整外生 UE/DU Trace，**Node 與 Policy 不可讀取**；`Node` 僅組裝當下合法可觀測快照；`Policy` 僅提議動作。這些是邏輯模組，不強制一模組一個 Python class。

## 4. Energy Ledger 與 Channel [MODEL / DECIDED]

- 每個 simulation run 開始：`energy_j = capacity_j`；**不是**每個 cycle 或第一次 Paging 重新滿電。自然流逝及 Idle/UE UL 功耗仍需結算。
- 採 **Event-Based Energy Update**：CW ON/OFF、模式切換、D2R START/END 或功率／能耗參數改變時分段積分 `ΔE=(P_EH−P_consume)Δt`，容量封頂但**不得利用負值裁切掩蓋不可行傳輸**。啟動成本要即時扣除；傳輸期間每個時點的 `energy_j >= 0`，必要時預先判斷耗盡時刻。
- CW 只在實際 ON 的時間提供本系統 energizing EH；所有受到 CW 覆蓋且具 EH 能力的 Tag 應被更新，包括未被排程的 Tag。正在 D2R 的 Tag 允許背散射及採能，但需合理反射／採能分流，不能把同一入射功率同時 100% 供兩種用途。
- 首版採 **Perfect Energy State Tracking / Perfect EH Information**：Node 已知當前各 Tag 的實際採能功率及效率／能耗參數，故理想估計 `Ehat_k(t)=E_k(t)`；加上**完美當前 CSI**。這些為資訊模型假設，**不是 3GPP 必然提供的能力**。不能提供未來 CSI、未來 Window 長度、完整外生 Trace。
- Channel 在同一 DU Window 內採 **Window-Level Block Fading**：即使同窗多次 Paging，各 Tag 的 SNR 不變；下窗更新 SNR。具體路損、衰落分布、跨窗相關性、EH/PHY 耦合及 BER/PER 參數須明示配置，不能依本交接檔推造。
- 尚未確定的實體參數應列出 TODO／配置缺口；可以使用**明顯標成 synthetic 的確定性測試 fixture**驗證 Engine invariants，但不可當作正式 PHY 驗證或研究實驗數值。

## 5. Policy Action 與 Validator [H-02 / H-02b / H-04]

**唯一可用的 Policy 動作**：`PagingBatchActionDTO(items=[(tag_id, tbs_bits), ...])`。`Policy(immutable SchedulingObservationDTO) -> PagingBatchActionDTO`；Policy 無法改寫真實 Tag/Service/Channel/Engine 狀態。

Validator 在執行前檢查（全數同時通過才可提交）：

- `1 <= count(tag_id) <= 8`；Tag ID 不重複且存在；Tag 本次可排程並符合尚有需求的服務資格；TBS 屬明示合法離散集合。
- 固定 BD、SFS 及 per-batch CFA 資源映射可用且無衝突；不另創優化器。
- 各 Tag 在 Paging／CW+D2R／Guard 預定時序中具有可行能量（含啟動成本、全部過程因果），且**完整一批**能在當前 Window 結束前完成；不能只確認 Paging 放得下。
- 額外可行性約束只能來自明示的本版本模型／配置，不能默默加上新的限制改變 Policy 比較條件。

**INVALID_ACTION**：原子拒絕、不縮批、不降 TBS、不修改原 Action、不執行本批 Paging／CW／D2R、記錄 `time_ns/window_id/policy_id/reason_code/original_action`；當前 DU Window 停止後續新 Paging，但事件時鐘和外生事件照常運行；下一 DU Window 再恢復。`INVALID_ACTION` ≠ `PHY_FAILURE` ≠ 合法 `NO_OP`。

**合法空 Action [DECIDED / R-01 第 26 節]**：`items=[]` 記錄為 `NO_OP`，停止本 DU Window 後續 Paging，不在同窗再呼叫 Policy；下一 DU Window 恢復合法決策。不建立本批 Paging／CW／D2R／Guard 或其能耗／服務認列。時間、既有外生事件、Deadline 及自然能量結算照常；不計為 INVALID_ACTION 或 PHY_FAILURE。此為零項動作的獨立分支，非違反非空批次的 `1–8 Tag` 限制。需測試同窗停排、下窗恢復、無重試迴圈及統計分類。

## 6. ServiceManager：服務、共享、同時結算及整數認列 [H-03 / H-03b]

- 各服務 `i` 有指定 Tag 集合 `T_i_req`、最低有效 payload bit `D_i_min`、排他截止 `deadline_exclusive_ns`。維護每 Tag 本服務需求內整數認列量 `C_i,k`、`G_i=sum_k C_i,k <= D_i_min`、`remaining_i=max(0,D_i_min-G_i)`。只在服務活躍、`tag in T_i_req`、新資料符合服務內容要求且 `t_D2R_END < deadline_exclusive_ns` 時認列。
- **TBS ≠ 有效 payload**：TBS 含 MAC header；Service 的 `D_i_min` 與公平性使用有效**新 payload bit**。必須有明確的 TBS→payload 與 PHY 成功／失敗資料契約；不能把 TBS 整包直接計成有效服務資料。
- 同一次成功的新 payload 可對多個需求重疊、尚未達標且未過期的服務分別認列，但全域物理 goodput **僅算一次**；對 `(tag_id,payload_id)` 或等價內容身分去重，重傳相同資料不得重覆認列。服務達標後凍結其認列向量；共享 Tag 仍可替其他活躍服務傳輸。
- 同時間戳完成的多 Tag 必須以**同一服務結算前快照**共同認列。設服務缺口 `R_i`、合格新 payload `b_i,k`、`B_i=sum_k b_i,k`：
  - `R_i=0`：全部認列 0；`B_i<=R_i`：`c_i,k=b_i,k`。
  - `B_i>R_i>0`：`q_i,k=R_i*b_i,k/B_i`；先取 `floor(q_i,k)`；餘下 bit 依**精確小數餘額降序**配置；餘額相同時按**Tag ID 升序**。使用整數比例比較以維持跨平台確定性；每 Tag `0<=c_i,k<=b_i,k` 且 `sum_k c_i,k=R_i`。
  - 例：`R=10`，A/B 新 payload 各 8 → 認列 `5/5`，物理 payload 16；`R=5`、A/B 新 payload `3/4` → 認列 `2/3`，物理 payload 7。
- 此為「**可按 bit 分割的服務需求內認列量**」模型，不表示 PHY TB 可以拆開傳送，也不能將超額有效資料當成 PHY 失敗。若應用 payload 不可分割，須另行確認計帳模型。
- 每個 cycle 初始化當期服務統計；Tag 實際能量不重置。已達標服務不因其公平性尚不均衡而單獨排程；服務公平性以其**完整指定 Tag 集合**（含零貢獻 Tag）計算。

## 7. DTO 設計待辦 [H-04 / IMPLEMENTATION TODO]

DTO 是**邏輯契約**，Codex 可使用 immutable dataclass、TypedDict＋只讀轉換或其他輕量結構；不可在未授權前實作。名稱可一致調整，**不得改變欄位的可觀測性與寫入權限**。

**工具選擇更新（R-01 第 28 節）**：使用者已指定 dataclass，Config／DTO／必要 Enum 定義集中於單一 `.py`，內部 State 定義留各模組；本節先前列舉的其他資料結構不再作為首版待選工具。檔名與具體欄位仍在討論；仍須先完成 Notebook 原型、情境測試及人工接受再抽離。

**Config 入口與 run 範圍（第 31 節取代舊多期安排）**：原型在 Notebook 設定 cell 明列本輪全部服務並建立 Config，保存完整 run 配置快照；本輪從 0 至最晚服務 Deadline，不另手填週期數或共同週期長度。Tag 電量一輪內持續，首版不自行生成或期中加入另一批需求。

**場景尺度修正（R-01 第 29／31 節）**：DU Window 固定 600 ms；單項服務的 10～15 s 起指完成 Deadline，非實際傳輸時間；共同輪長現在已定為最晚期限。100 ms 舊例不適用；15 s／20 s 為使用者的說明例，不作所有服務的預設值。

| DTO／內部計畫 | 最小建議欄位 | 權限／用途 |
|---|---|---|
| `TagObservationDTO` | `tag_id`, `snr_db`, `energy_j`, `is_schedulable` | 當前 CSI／理想能量快照；不能包含可變 Tag 引用或未來 channel |
| `ServiceObservationDTO` | `service_id`, `deadline_exclusive_ns`, `remaining_bits`, `required_tag_ids`, `credited_bits_by_tag` | 單服務當前合法狀態；對 Policy 唯讀 |
| `SchedulingObservationDTO` | `now_ns`, `window_id`, `window_end_ns`, `cw_power_current`, `cw_power_next_announced?`, `tag_observations`, `service_observations`, `legal_tbs_bits`, `fixed_config_id?` | 在 Window 起點及每個 `GUARD_END` 重新建立；僅已揭露當前資訊 |
| `TagTbsActionDTO` | `tag_id`, `tbs_bits` | Policy 可控制欄位；不含 BD、SFS、CW power |
| `PagingBatchActionDTO` | `items: TagTbsActionDTO[]` | 每批 1–8 Tag（另明確區分合法 no-op）；不含未驗證的執行計畫 |
| `ActionValidationResultDTO` | `accepted`, `reason_code?`, `execution_plan?` | Validator 統一產生結果；拒絕時不可篡改原 Action |
| `ExecutionPlan`（內部，非 Policy Action） | `window_id`, `batch_id`, `paging_interval`, `per_tag_cfa_resource`, `d2r_intervals`, `guard_interval`, `cw_power` | 僅已驗證後供 Engine 執行；固定映射、不能倒寫原 Action |
| `SimulationEventTraceDTO` | `time_ns`, `event_type`, `window_id?`, `batch_id?`, `tag_id?`, `service_id?`, `action_id?`, `outcome`, `reason_code?`, `energy_delta_j?`, `credited_delta_bits?` | Trace/replay；適當區分「Policy 看得到的 Observation」與「僅供評估的真實 Trace」 |

**Tag 真實狀態至少**：ID、容量、當前電量、模式、最後結算時刻、必要電路/EH 參數。**Channel 真實狀態至少**：本 Window／Tag 的通道樣本與 SNR、計算 PHY/EH 所需的模型參數。**ServiceManager 真實狀態至少**：活躍服務、截止、`C_i,k`、共享 payload 去重集合、達標凍結標記。**Engine 真實狀態至少**：全域事件佇列、`now_ns`、Window/Batch 狀態、CW ON/OFF 與當前停止排程旗標。這些**不是**應直接暴露給 Policy 的 DTO。

## 8. 事件 Trace、Scenario／Seed 與最小自動驗收 [H-05]

### 8.1 追蹤與可重現資料

每次 run 保存：`scenario_id`、情境參數／分布版本與其快照、`seed`（必要時分 RNG stream）、`policy_id`、合法 TBS/BD/SFS/CFA 配置、能量/PHY 參數、Tag 初始電量、所有 Window 外生 Trace（**僅保存於環境/離線 Trace，不傳入 Policy**）、Observation 摘要、原始 Action／Validation、事件 Trace、服務完成及公平性統計、Invalid Action 次數。相同完整配置＋Scenario＋Seed＋Policy 應得可重現結果。

`ResourceTimeline` 由事先定義的情境參數池與 Seed 產生完整 UE UL 占用及 DU Window 時序，**按時間揭露**。第一版 fixture 可以是硬編碼、顯示為 synthetic 的簡單情境；正式研究需要另行確認負載分布與多 Seed。即使 Simulator 私下已生成未來 Trace，Policy 也不得預覽。

### 8.2 五類 Acceptance Tests（全部需自動 assert）

| ID | 必測案例／不變量 |
|---|---|
| `ACPT-01` | **同 Window 多批**：完成 `Paging→CW/D2R→CW_OFF→Guard` 至少兩次；第二次在 `GUARD_END` 後重新讀取能量／服務狀態；同窗 SNR 及 CW 功率不變；Guard 不採 CW 能量；不能讓完整批次跨 Window |
| `ACPT-02` | **能量因果**：Run 起點滿電、跨 Window/Cycle 不重置；CW ON 時排程及未排程 Tag 正確 EH；Paging/Guard/UE UL 無該 CW EH；啟動成本與中途耗盡可行性；`0<=E<=Emax`，不重複積分 |
| `ACPT-03` | **Deadline＋同時間事件**：多 Tag `D2R_END`、`CW_OFF`、Deadline 同時；事件插入順序置換不影響結算；`d_exclusive-1 ns` 可有效、`d_exclusive` 不可；`GUARD_END==WINDOW_END` 不開新批；CW_OFF 一次 |
| `ACPT-04` | **服務共享＋比例認列**：同時 8/8 成功、缺 10 → 5/5；3/4 成功、缺 5 → 2/3；再測精確餘額同分的 Tag ID 規則、超額、去重、跨服務同 payload 可各自認列但物理 goodput 只算一次；已完成／過期服務不可新認列 |
| `ACPT-05` | **非法 Action＋DTO 隔離**：9 個 Tag、重複 Tag、非法 TBS、能量不足、批次跨 Window、無效資源映射均原子拒絕；不修正 Action、不產生被拒批次副作用；當前 Window 停止後續 Paging、下一 Window 恢復；Policy 無法修改 Observation 真值或讀未來 Timeline |

**必要 invariant／測試風格**：測試必須使用 assert（或等價機械檢查），失敗輸出絕對時間、Window/Batch ID、Tag/Service ID、原始 Action、原因碼與相關能量/認列增量；不可僅憑 Notebook 圖表或人工閱讀 Trace 宣稱通過。保留固定 Seed 重跑測試、同時事件入隊順序置換測試，以及零時間事件無限循環防護測試。

### 8.3 Notebook → `.py` 驗收 Gate

- [ ] `GATE-01`：五大 ACPT 類別 Scenario 與自動斷言**實際執行通過**；所有配置與 Seed 可重播。
- [ ] `GATE-02`：相同 Scenario／Seed／Policy 重跑統計及規範化 Trace 一致；同時間事件更換入隊次序的計帳結果一致。
- [ ] `GATE-03`：能量非負/容量上限、時間／Window/Guard、固定 CFA 映射、服務去重/Deadline、DTO 隔離與非法 Action 全部符合 invariant；無同時刻無限迴圈。
- [ ] `GATE-04`：缺失／未校準的 PHY/EH／通道／Scenario／公平性設定有明確 TODO／Config 標示，不宣稱為已驗證 3GPP 或論文結果。
- [ ] `GATE-05`：輸出可追蹤的測試結果表與失敗理由；只有通過驗收並取得後續授權才轉成 `.py`。

**當前所有 Gate 都是未執行／未通過；不得勾選。**

## 9. 參數來源、未決研究議題與實作前缺口

將未決事項分為兩類，以避免 Codex 自行發明資料：

**A. 在具體執行某個模組／測試前必須提供或明確鎖定的 Config（不可臆造）**：
- 合法 `TBS` 集合、`TBS→有效 payload`／header 規則、Tag/Service 合格 payload 識別規則；不能把 TBS 當有效 payload。
- 固定 `BD`／`SFS`、CFA 資源池實際項目與 deterministic 映射順序、同批傳輸起點／長度的合法計算、`Paging`／`Msg2`／`Guard` 時間值；未能取得時以 synthetic fixture 專門驗證 Engine，且標記非正式參數。
- Tag `E_max`、模式功耗、啟動成本、EH／反射分流係數、P_CW 到實際 EH 的轉換、PHY 成功／錯誤抽樣來源、初始條件；不要自行宣稱符合某版 3GPP。
- 情境參數池的生成分布／Seed 規則、跨 Window 通道更新方式、第一 Window 的功率通知初始化、原始期限需求到 `last_allowed_slot` 的轉換；需和 Source/Decision Record 對照。

**B. 可延至正式研究／演算法比較時處理（不阻擋先用 synthetic fixture 驗證 DES）**：
- Baseline 詳細排序與 tie-break、共享 Tag 是否額外加分（R-01.16）、公平性跨服務正規化分母／未達標服務集合（R-01.17）；不可讓首版 Engine 暗中選定研究演算法。
- 通道衰落及跨 Window 相關性、PHY/BER 預測校準、EH/背散射耦合可信度、理想 CSI/能量觀測敏感度、協定標準版次及規範符合性核驗。
- 正式研究負載分布、統計信賴區間、公平比較與消融實驗。

**Codex 處理原則**：對每項缺口標明 `REQUIRED_CONFIG`、`SYNTHETIC_TEST_FIXTURE` 或 `RESEARCH_VALIDATION_OPEN`。若缺少足以保證合法行為的輸入，應明示阻塞並向使用者要求決策，不得以「通常如此」補成正式參數或悄悄變更已定模型。

## 10. 最小交付清單與停止條件

**首版 Notebook 實作任務收到授權後，交付應包含**：

- [ ] `*.ipynb`：DES 執行流程與可讀的事件追蹤（此階段不建立 `.py` 重構成果）。
- [ ] 可重現 `scenario/config/seed` 快照；精簡的 DTO 契約與 Owner／Mutation Rules。
- [ ] 頻率／時間 CFA 映射配置的合法性檢查；Policy 輸出 Tag/TBS，Validator 原子拒絕。
- [ ] 五類自動化 Scenario/Invariant 測試與明確 pass/fail 結果；完整必要 Trace／Result Summary。
- [ ] 完成的決策／配置缺口清單；對 research-limited synthetic fixtures 清楚標示其適用範圍。
- [ ] 測試通過後提出 `.py` 重構計畫，**不得未經另行授權便動手轉檔**。

**停止條件**：遇到缺失的規範級參數、配置衝突、事件語意不明或自動化測試失敗，暫停相關正式功能，回報最小可重現案例、缺少的資訊與可能替代方案；不得擅自把缺口變成已核准決策。即使 Notebook 工作完成，也不代表研究假設與標準符合性已實證。

## 11. 可直接貼給 Codex 的啟動指令（需在使用者另行授權後使用）

> 請先閱讀 `Codex_Handoff_Specification_Ambient_IoT_DES.md` 以及 `R-01_System_Model_and_Baseline_Decision_Record.md` 第 14–25 節，並以這兩份檔案及原始 PDF 作為來源。先產生「配置缺口與資料契約核對表」，不要引用歷史 proposal 覆蓋最新 [DECIDED]。本任務的第一階段只建立精簡 DES `.ipynb` 原型、固定 Scenario/Seed、Event Trace、DTO／狀態權限、五大 ACPT 自動化測試；不實作 AI 方法、不更動 3GPP 參數假設、不修改 GitHub、不重構 `.py`。Baseline／AI 的 Policy Action 限 `(tag_id, tbs_bits)`；BD/SFS、CFA 映射及 CW Power 是共用固定配置。若必要 Config 缺失，可用明確標示的 synthetic fixture 測試 Engine，但不得把它當正式研究結果。執行後回報各 Gate 的真實 pass/fail 和未決配置，再請使用者決定是否准許 `.py` 重構。

---

**最終狀態（2026-10-20）**：H-01、H-02/H-02b、H-03/H-03b、H-04、H-05 的**選擇均 [DECIDED]**；軟體模組、DTO、Notebook、事件 Trace 及自動化測試均 **NOT IMPLEMENTED / NOT RUN**。此文件僅為交接規格，不構成 Codex 已接手或已獲實作授權。

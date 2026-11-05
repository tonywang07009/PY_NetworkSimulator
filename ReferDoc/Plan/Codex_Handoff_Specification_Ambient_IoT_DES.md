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

Latest resource contract (2026-10-31, R-01 §34.6–34.11): shared 600 ms outer windows with scenario-supplied starts/gaps. Each Node/window has one UE prefix: ceil(600*r) ms, r uniform over 0.60–0.75; UL/DL each 0.5. Duration/direction draws are separate across Nodes/windows and reproducible by scenario seed and stable identities. Tags use the remainder for Paging/D2R/Guard. Earlier one-time-only UE and unspecified timing-dependence passages are superseded. Numerical starts/gaps remain scenario inputs.


2026-10-31 clarification (R-01 §34): The 600 ms DU interval includes UE uplink occupancy. Paging, D2R and Guard use the remaining time within that interval. Window start/spacing and per-Node synchronization remain unresolved.


| 介面與不變量 | v1 生效要求 |
|---|---|
| 內部時鐘 | 所有事件、期限與排序使用**絕對整數奈秒 `int ns`**；顯示時間可轉 ms/μs，不得以浮點顯示值回寫時間戳 |
| Slot Grid | 15 kHz SCS、normal CP：1 ms NR slot = 1,000,000 ns；事件可在 slot 內發生 |
| Deadline | `deadline_exclusive_ns=(last_allowed_slot+1)*1_000_000`；有效認列嚴格 `D2R_END_ns < deadline_exclusive_ns` |
| DU Window | `window=[start_ns,end_ns)`；2026-10-23 使用者確認長度固定 `600_000_000 ns`（R-01 第 29 節）。Window 起點／間隔仍待配置，不代表連續每 600 ms 一窗；原先未來長度未知的敘述需按固定長度設定對齊，未來起點／完整 Trace 不揭露 |
| Window Channel | 對各 Tag，每個 DU Window 的 SNR 固定；下一 Window 更新；**跨窗是否獨立／相關未定**，不能自動宣稱獨立 |
| CW Power | Donor 每個 Window 指定一個固定 CW 功率，該 Window 所有 D2R 批次使用相同功率；Node 在**前一 Window**已得到下一 Window 功率預告（僅功率，非未來 SNR／時間） |
| Batch Limit | 每批 Paging 至多 **7 個 Tag**；固定合法 BD/SFS 組態與 CFA 資源池；Policy 不決定 BD／SFS／功率 |
| Batch Sequence | `Paging → CW_ON / D2R → last D2R_END → CW_OFF → Guard → GUARD_END`；若剩餘時間夠，允許同一 Window 的下一批 Paging |
| CW / EH | UE UL/DL is the harvesting phase. Q-INFLUENCE-22 A selects communication RF: Node-to-Tag DL and UE-to-Tag UL; dedicated CW stays off during UE traffic. D2R retains external CW for backscatter but contributes no harvested energy. Paging/Guard do not charge. See R-01 section 46; this supersedes simultaneous D2R EH. |
| Guard | 每批最後的 D2R 結束立即 `CW_OFF`，Guard 全段 CW EH 為零；`last_D2R_END + guard <= window_end`；下一批只能在 `GUARD_END` 後開始 |
| Re-decision | `GUARD_END` 完成當前狀態提交後，重新生成 Observation 並呼叫 Policy；不在 Window 起點先規劃全部批次 |
| Failure Action | 非法 Action 拒絕**整批**；當前 Window 不再新 Paging；仍處理既有外生事件／Deadline；下一 Window 才恢復 |

**CFA 固定資源映射**：使用**每批**共享的固定合法資源池；以確定性映射規則指派至多 7 個被選 Tag 的專用 CFA 資源，禁止資源衝突。不將 Tag 永久綁死資源，也不引入動態 BD/SFS 適應或最佳化。**映射所需的具體資源池表、各 BD/SFS 固定值、TS/頻率映射與能力上限需從既有正式參數來源／配置明示提供；未提供時採配置缺失回報，不得捏造。**

## 3. DES Engine：同時間事件與狀態所有權 [H-01]

每次取出時間戳 `t`，先收集所有同時到期事件，按**邏輯階段**結算；不要讓 heap 插入順序改變物理或服務結果：

1. 對 `[previous_boundary,t)`，使用**舊 CW 狀態、舊 Tag mode** 結算能量與資源占用；同一段時間不得重算。
2. 收集所有 `D2R_END(t)`；每個唯一 `(window,batch,tag,transmission)` 接收結果只能決定／提交一次；使用同一個結算前 ServiceManager 快照批次認列合格新 payload。
3. 依 `t` 的截止邊界結算 `SERVICE_DEADLINE`、`DU_WINDOW_END`、批次最後 D2R 結束時的 `CW_OFF`；時間上相同的 Deadline 一律採 `< deadline_exclusive_ns`，不可偷改為 `<=`。
4. 完成 `GUARD_END` 與全部應生效的截止／狀態更新後，若 `t < window_end_ns` 且 Window 未被非法 Action 停排，建立**新** Observation；可行時允許下一批決策。`GUARD_END == WINDOW_END` 不可開始新批次。
5. 同時間衍生事件必須形成**有限的因果閉包**；禁止零時間無限排程迴圈。每個 Batch 只能有一次 `CW_OFF` 與一次服務認列提交。

**狀態主權**：`SimulationEngine` 推進事件與提交狀態；`Tag` 持有物理電量／模式；`Channel` 決定本 Window 通道狀態與接收／EH 模型；`ServiceManager` 對服務認列、期限與 payload 去重負責；`ResourceTimeline` 保有完整外生 UE/DU Trace，**Node 與 Policy 不可讀取**；`Node` 僅組裝當下合法可觀測快照；`Policy` 僅提議動作。這些是邏輯模組，不強制一模組一個 Python class。

## 4. Energy Ledger 與 Channel [MODEL / DECIDED]

- At each simulation-run start, set energy_j = capacity_j. Preserve residual energy across slots, windows and cycles; do not refill at boundaries or first Paging. Account for applicable mode consumption. Q-INFLUENCE-24 A omits additional storage self-discharge/leakage; keep all applicable mode costs and losses already in the nonlinear RF-to-DC curve.
- 採 **Event-Based Energy Update**：CW ON/OFF、模式切換、D2R START/END 或功率／能耗參數改變時分段積分 `ΔE=(P_EH−P_consume)Δt`，容量封頂但**不得利用負值裁切掩蓋不可行傳輸**。啟動成本要即時扣除；傳輸期間每個時點的 `energy_j >= 0`，必要時預先判斷耗盡時刻。
- Use a hardware-supported nonlinear RF-to-DC curve (Q-INFLUENCE-23 B, R-01 section 48). Numerical fit, operating range and capacity remain open.
- Q-INFLUENCE-25 A assumes continuous RF during the UE prefix: Node DL or UE UL. Transmit power remains an unresolved profile input; continuous activity does not imply maximum power.
- UE-phase EH replaces simultaneous D2R EH (R-01 section 46). Deduct D2R consumption without charging, even while its backscatter CW is on. Communication RF is selected by Q-INFLUENCE-22 A; include actual activity, source-to-Tag geometry, compatible passband and receiver conversion. Keep stored-energy-only full-operation admission.
- 首版採 **Perfect Energy State Tracking / Perfect EH Information**：Node 已知當前各 Tag 的實際採能功率及效率／能耗參數，故理想估計 `Ehat_k(t)=E_k(t)`；加上**完美當前 CSI**。這些為資訊模型假設，**不是 3GPP 必然提供的能力**。不能提供未來 CSI、未來 Window 長度、完整外生 Trace。
- Channel 在同一 DU Window 內採 **Window-Level Block Fading**：即使同窗多次 Paging，各 Tag 的 SNR 不變；下窗更新 SNR。具體路損、衰落分布、跨窗相關性、EH/PHY 耦合及 BER/PER 參數須明示配置，不能依本交接檔推造。
- 尚未確定的實體參數應列出 TODO／配置缺口；可以使用**明顯標成 synthetic 的確定性測試 fixture**驗證 Engine invariants，但不可當作正式 PHY 驗證或研究實驗數值。

## 5. Policy Action 與 Validator [H-02 / H-02b / H-04]

The Policy returns `PagingBatchActionDTO(items=[(tag_id, tbs_bytes), ...])` from an immutable SchedulingObservationDTO.
Use complete-TB bytes from {8,16,32,64}; see R-01 section 42. Policy cannot modify Tag, Service, Channel or Engine state.

Validator 在執行前檢查（全數同時通過才可提交）：

- `1 <= count(tag_id) <= 7`；Tag ID 不重複且存在；Tag 本次可排程並符合尚有需求的服務資格；TBS 屬明示合法離散集合。
- 固定 BD、SFS 及 per-batch CFA 資源映射可用且無衝突；不另創優化器。
- 各 Tag 在 Paging／CW+D2R／Guard 預定時序中具有可行能量（含啟動成本、全部過程因果），且**完整一批**能在當前 Window 結束前完成；不能只確認 Paging 放得下。
- 額外可行性約束只能來自明示的本版本模型／配置，不能默默加上新的限制改變 Policy 比較條件。

**INVALID_ACTION**：原子拒絕、不縮批、不降 TBS、不修改原 Action、不執行本批 Paging／CW／D2R、記錄 `time_ns/window_id/policy_id/reason_code/original_action`；當前 DU Window 停止後續新 Paging，但事件時鐘和外生事件照常運行；下一 DU Window 再恢復。`INVALID_ACTION` ≠ `PHY_FAILURE` ≠ 合法 `NO_OP`。

**合法空 Action [DECIDED / R-01 第 26 節]**：`items=[]` 記錄為 `NO_OP`，停止本 DU Window 後續 Paging，不在同窗再呼叫 Policy；下一 DU Window 恢復合法決策。不建立本批 Paging／CW／D2R／Guard 或其能耗／服務認列。時間、既有外生事件、Deadline 及自然能量結算照常；不計為 INVALID_ACTION 或 PHY_FAILURE。此為零項動作的獨立分支，非違反非空批次的 `1–7 Tag` 限制。需測試同窗停排、下窗恢復、無重試迴圈及統計分類。

## 6. ServiceManager：服務、共享、同時結算及整數認列 [H-03 / H-03b]

- 各服務 `i` 有指定 Tag 集合 `T_i_req`、最低有效 payload bit `D_i_min`、排他截止 `deadline_exclusive_ns`。維護每 Tag 本服務需求內整數認列量 `C_i,k`、`G_i=sum_k C_i,k <= D_i_min`、`remaining_i=max(0,D_i_min-G_i)`。只在服務活躍、`tag in T_i_req`、新資料符合服務內容要求且 `t_D2R_END < deadline_exclusive_ns` 時認列。
- Use a selected-TBS transmission as the processing unit (R-01 section 52). Aggregate valid unique application payload across Tags to reduce each service's remaining demand, capped at zero. No fixed sensor-record/reassembly layer is required.
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
| `SchedulingObservationDTO` | `now_ns`, `window_id`, `window_end_ns`, `cw_power_current`, `cw_power_next_announced?`, `tag_observations`, `service_observations`, `legal_tbs_bytes`, `fixed_config_id?` | Rebuild at window start and each GUARD_END; include only current disclosed information |
| `TagTbsActionDTO` | `tag_id`, `tbs_bytes` | Select complete-TB bytes from {8,16,32,64}; no BD, SFS or CW power control |
| `PagingBatchActionDTO` | `items: TagTbsActionDTO[]` | 每批 1–7 Tag（另明確區分合法 no-op）；不含未驗證的執行計畫 |
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
| `ACPT-02` | Energy causality: start full and preserve energy across windows/cycles; harvest from the selected source during UE UL/DL only; no D2R/Paging/Guard EH; retain startup/full-operation feasibility, capacity saturation and no duplicate integration. Source and numerical powers remain open. |
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


## 2026-11-02 | Access/PHY source order (R-01 section 35)

The user selected Q-TRADEOFFS-01 option B: complete the source-backed Access/PHY configuration before implementation.
Keep legal message formats, useful payload and fixed resources distinct. Record missing parameters instead of choosing synthetic replacements.
This decision does not approve a numerical profile or change the earlier accepted channel prototype.
Source map: AgentDoc/openspec/discuss/2026-11-02-access-phy-source-map.md. Multi-Tag CFA signalling remains unresolved.


## 2026-11-02 | Individual CFA Paging (R-01 section 36)

The user confirmed individual Paging for each selected Tag: "B 我這邊就是逐個paging".
Use separate CFA Paging messages with each Tag's Scheduling Info. Do not introduce a multi-grant Paging extension.
Count every control message and its response offset. The Policy selected set does not imply one physical message.
Q-INFLUENCE-14 must resolve Paging/D2R sequencing and Guard placement before dependent implementation.
Do not infer concurrent D2R, serialized D2R or a one-Tag Action limit from the word "individual".


## 2026-11-02 | Eight orthogonal SFS resources (R-01 section 37)

The user clarified C: individual Paging, at most eight selected Tags, sufficient orthogonal SFS resources and permitted parallel D2R.
Keep one Guard after the last response. The explicit parallel-transmission clarification supersedes the earlier serial C wording.
Do not treat eight-Tag SFS capacity as unresolved or introduce intra-batch D2R interference under this ideal model.
Keep noise and external/inter-Node interference separate; no measured orthogonality or standard-conformance claim follows.
Q-INFLUENCE-15 must resolve whether all Paging ends before CW/D2R or whether the earlier CW-off-during-Paging rule changes.
Actual legal parameter values, response offsets, time/energy limits and payload mapping remain separate work.


## 2026-11-02 | Settled batch phase order (R-01 section 38)

The user selected Q-INFLUENCE-15 A. Use individual Paging messages, all completed while the dedicated CW is off.
Then enter the CW/D2R phase. The assumed eight orthogonal SFS resources permit parallel responses; common start times are not assumed.
At the last D2R completion, turn CW off, apply one full Guard and then call Policy with a new Observation.
This settles the phase alignment left open in the preceding section 37 note. Keep exact response timing and numerical profiles pending.


## 2026-11-02 | Application payload abstraction (R-01 section 39)

The user accepted Q-INFLUENCE-16 A: actual MAC SDU bytes are application data in the first simulator; abstract NAS/security encapsulation.
Exclude MAC fields, padding and PHY overhead from new application data. Count successful unique content before applying existing service-credit rules.
Actual SDU length need not fill TB capacity. Preserve the complete transmitted packet when calculating time and energy.
For a qualifying 112-bit new payload and 40-bit service gap, credit 40 and record 72 as service excess; physical new data remains 112 bits.
Data filling, payload identity, segmentation and numerical PHY values remain open. No implementation or runtime acceptance is implied.


## 2026-11-02 | Reduced TBS set and expansion (R-01 section 40)

The user selected a smaller fixed TBS subset with a 64-byte complete-TB cap, including mandatory MAC fields.
Permit later additions if experiments show insufficient resolution; retain the cap unless separately changed.
Keep one explicit candidate list per experiment and the same list for all compared policies. Preserve the existing bit-valued Action format.
The cap is 512 TB bits; maximum SDU capacity is 62 bytes under the accepted MAC format. Actual new data remains separately measured.
Q-INFLUENCE-18 asks for the exact initial list. {8,16,32,64} bytes is proposed, not yet accepted.


## 2026-11-02 | Initial TBS candidates (R-01 section 41)

The user accepted complete-TB candidates {8,16,32,64} bytes, including mandatory MAC fields.
Use existing Action values {64,128,256,512} bits. Maximum SDU capacities are {6,14,30,62} bytes; actual application data may be shorter.
Keep the set shared by compared policies and saved in each experiment. Retain the 64-byte cap and permitted later expansion.
This resolves the initial-members gap in the preceding section 40 note. Other PHY/data parameters and implementation remain pending.


## 2026-11-02 | Byte-valued TBS action (R-01 section 42)

The user requested actual byte-valued TBS choices: tbs_bytes in {8,16,32,64}, four choices per selected Tag.
Current Policy/Observation names are tbs_bytes and legal_tbs_bytes. This supersedes older bit-valued Action statements, including sections 40-41 above.
Convert to TB bits only when Access/PHY calculations need them: TB bits = 8*tbs_bytes. Keep service credit in bits.
Internal categorical encoding must resolve to the actual byte value before validation; the specific model and encoding remain future work.
The complete scheduler also chooses Tags. No measured overall training-cost reduction or implemented four-output model is claimed.


## 2026-11-02 | Finite Tag data (R-01 section 43)

The user selected finite available application data per Tag and cited charging performance as a concern.
Track available data separately from battery energy. Apply the accepted data and energy rules together; charging alone does not generate data.
Actual SDU can be shorter than capacity, with padding in the complete selected TB. Padding is not useful data and does not shorten TB airtime.
Q-INFLUENCE-20 asks whether the finite workload is present at t=0 or has later arrivals. Numerical amounts and record/retransmission rules remain open.


## 2026-11-02 | Complete-TBS energy gate (R-01 section 44)

The user clarified that selected TBS must be fully transmittable under the energy rule. Policy considers energy; Validator checks the full plan before execution.
Include required startup and packet overhead and check energy causality throughout the operation. Do not silently shorten a selected TB because energy is insufficient.
Keep {8,16,32,64} complete-TB byte choices and atomic rejection. Full-energy feasibility does not guarantee PHY decoding success.
Q-INFLUENCE-21 asks whether admission requires stored energy alone or permits causal same-operation CW harvesting; runtime harvesting stays allowed.
The data-arrival question Q-INFLUENCE-20 is unanswered and deferred, not a new prerequisite for the energy gate.


## 2026-11-02 | Stored-energy admission and runtime charging (R-01 section 45)

The user selected A: stored battery energy alone must cover the complete selected operation at admission.
Runtime charging remains allowed; actual energy updates deduct consumption and add only energy actually harvested, with causal timing and capacity saturation.
The user's question about battery decline does not disable the accepted simultaneous EH model. Net energy need not always decrease during CW-covered D2R.
Q-INFLUENCE-21 is resolved; Q-INFLUENCE-20 about data timing remains deferred. No numerical energy thresholds or runtime implementation are approved here.

## 2026-11-02 | UE-phase harvesting supersedes simultaneous D2R EH

R-01 section 46 is current. Q-INFLUENCE-21 remains A for stored-energy-only admission.
Q-INFLUENCE-22 asks which RF source supplies the UE harvesting phase; Q-INFLUENCE-20 stays deferred.
Do not infer a Type-1 prohibition, negligible total circuit power or improved efficiency from higher frequency.
The earlier simultaneous-EH notes below prior decisions are historical. No energy implementation or calibration is accepted.

## 2026-11-02 | Communication RF source selected; literature reviewed

R-01 section 47 closes Q-INFLUENCE-22 with A. UL energy originates at the UE, DL at the Node.
Read AgentDoc/openspec/discuss/2026-11-02-ue-rf-harvesting-literature.md for original papers and evidence limits.
Q-INFLUENCE-23 asks linear versus nonlinear conversion; numerical profiles remain open.
Older source-open notes are historical. No implementation or calibrated power budget is accepted.

## 2026-11-02 | Nonlinear conversion and cross-slot storage accepted

R-01 section 48 closes Q-INFLUENCE-23 with B and confirms persistent residual energy across slots/windows/cycles.
Only run initialization starts full. Capacity remains finite; preserve full-operation stored-energy admission and mode costs.
Q-INFLUENCE-24 asks about additional storage leakage. Curve, capacity and power parameters remain open.
Earlier conversion-open notes are historical. No hardware feasibility or runtime validation is claimed.

## 2026-11-02 | Additional storage leakage omitted

R-01 section 49 closes Q-INFLUENCE-24 with A. Keep finite persistent storage and all operating costs.
Q-INFLUENCE-25 asks about continuous versus intermittent RF activity within the UE prefix.
Earlier leakage-open notes are historical. No numerical source/hardware profile is accepted.

## 2026-11-02 | Continuous UE RF accepted; inventory requested

R-01 section 50 closes Q-INFLUENCE-25 with A. Keep prior energy and TBS decisions.
Plan/decision-inventory.md lists nine current packages and four later first-version packages; CLM is excluded.
The thirteen packages are not thirteen predetermined questions. Source/profile preparation remains agent-owned.
No new question is active for this status request. Influence remains 25; Q-INFLUENCE-20 stays deferred.
Earlier source-activity-open notes are historical. No numerical power or hardware calibration is accepted.

## 2026-11-02 | Data-supply discussion resumed

The user resumes AP-01 at Q-INFLUENCE-20. Finite available data remains accepted.
Ask whether data is all present at run start or also arrives during the run; do not select either without an answer.
Initial byte amounts, payload identity, retry and segmentation remain open. Influence remains 25; no new ID is created.
All energy decisions remain in force. This is discussion status, not a new implementation requirement.

## 2026-11-02 | Initial-only data supply closed

R-01 section 51 closes Q-INFLUENCE-20 with A. Each Tag's finite data is ready at t=0; no later arrivals.
The user recalls prior discussion; retain this as settled and do not ask again. Initial amounts remain scenario inputs.
AP-01 is closed: eight current plus four later packages remain. Q-INFLUENCE-26 asks about splitting application data.
Identity, eligibility and retry rules remain AP-02 work. Earlier pending/deferred labels are historical.

## 2026-11-02 | Packet-level service accounting clarified

R-01 section 52 accepts the user's custom Q-INFLUENCE-26 answer: selected-TBS transmission units and multi-Tag service-demand aggregation.
Retain actual SDU credit, full TB cost, uniqueness/eligibility/deadlines, simultaneous allocation and shared-service rules.
Q-INFLUENCE-27 asks failed-data retention vs discard at the Tag; failure never reduces service demand.
Finite initial-only data stays accepted. No fixed sensor-record/reassembly layer or automatic retry mechanism is selected.

## 2026-11-02 | Failed data retained

R-01 section 53 closes Q-INFLUENCE-27 with A. Retain undelivered data for later valid scheduling.
Failures consume actual time/energy and earn no service credit. Later attempts require full-TBS energy feasibility.
Preserve content identity and successful-new-data deduplication. No automatic retry, ACK exchange or fixed retry TBS is selected.
AP-02 identity/accounting contract preparation remains; no new question is active. Influence stays 27.

## 2026-11-02 | Fixed PHY profile comparison prepared

Q-INFLUENCE-28 compares two proposed complete CFA/BPSK profiles at BD=2*tau with eight permitted SFS values.
A uses no FEC; B uses FEC. Other fields and exact airtime table are in AgentDoc/openspec/discuss/2026-11-02-fixed-d2r-profile-candidates.md.
No profile is accepted yet. FEC 32/64-byte airtimes exceed the available window remainder under this candidate.
Full Paging/offset/Guard timing, energy and FBL mapping remain unresolved. AP-02 identity/accounting draft is included for later review.

## 2026-11-02 | Accepted no-FEC profile with user-adjusted BD

Q-INFLUENCE-28 is answered A with the user's explicit BD change: interpret 1/2tau as tau/2.
T_bit=200/3 microseconds. Keep CFA/BPSK, repetition 1, short seven-bit ambles and no additional midamble.
Preserve the proposed interval-field choice S*48. At this BD S=4, so I_bit=192, not 48.
The old 2*tau profile/table above remains historical candidate evidence, not the current selected BD.

| TB bytes | E bits | V bits | Exact pure D2R ms | Display ms |
|---|---:|---:|---|---:|
| 8 | 80 | 87 | 29/5 | 5.800000 |
| 16 | 144 | 151 | 151/15 | 10.066667 |
| 32 | 272 | 286 | 286/15 | 19.066667 |
| 64 | 528 | 549 | 183/5 | 36.600000 |

Derivation: E=8*N+16; V=E+(1+floor(E/192))*7; T=V*(200/3) microseconds.
No ns rounding policy is selected. Paging, response offsets and Guard are excluded.
These pure airtimes do not prove complete-batch timing, energy feasibility or receiver reliability.

At tau/2, MAC Table 6.2.1.6-1 permits SFS {1,2,4,8,16,32}: six values.
Do not retain 64/128 as valid values at this BD or invent two more factors.
Keep the accepted eight-resource ideal orthogonality and parallelism assumption; its concrete standards-backed mapping is unresolved.
An abstract resource ID is not a claim of eight different legal SFS values at tau/2.
Do not silently reduce the batch limit, serialize responses, change BD back, or introduce extra carriers.
AP-03 numerical mapping and full conformance remain open before implementation. No new resource-sufficiency question is asked.

## 2026-11-02 | FEC enabled at tau/2 [CURRENT]

The user explicitly replaces the previous no-FEC choice with FEC to improve reliability.
Keep tau/2 BD (200/3 microseconds), CFA/BPSK, repetition 1, short seven-bit ambles, interval 192 and no additional midamble.
Previous no-FEC selections/tables are historical. This update is current; R-01 section 55 records the decision.

| TB bytes | Coded E bits | V bits | Exact D2R ms | Display ms |
|---|---:|---:|---|---:|
| 8 | 240 | 254 | 254/15 | 16.933333 |
| 16 | 432 | 453 | 151/5 | 30.200000 |
| 32 | 816 | 851 | 851/15 | 56.733333 |
| 64 | 1584 | 1647 | 549/5 | 109.800000 |

E=3*(8*N+16); V=E+(1+floor(E/192))*7; T=V*(200/3) microseconds.
FEC changes transmitted redundancy and processing costs, not useful application bytes or complete-TB Action values.
Include encoded airtime and applicable circuit/decoder costs in the future energy model; no numerical power increase is assumed here.
Reliability improvement is the design intent, not guaranteed success or measured coding gain.
FBL mapping must represent the actual coding/receiver abstraction and must not count the same coding gain twice.
Paging, response offsets, Guard, integer-ns conversion and full-batch energy/time feasibility remain open.
The six legal SFS values at tau/2 still do not resolve the eight ideal orthogonal-resource mapping.
Keep the eight-Tag assumption without inventing SFS values or additional carriers. No new interview question is opened.

## 2026-11-02 | Accepted D2R airtime table

Use [the accepted timing configuration](D2R_Timing_Configuration.md), under R-01 section 56.
It fixes pure D2R airtime for FEC/tau/2 and {8,16,32,64} TB bytes, with exact rational values.
Paging/response/Guard, ns rounding, energy feasibility, eight-resource mapping and receiver reliability remain separate open work.
This acceptance does not implement a runtime configuration or close the full PHY review.

## 2026-11-02 | Remaining work audited after timing acceptance

Use Plan/decision-inventory.md, especially the audit after D2R table acceptance.
Eight current work packages plus four later packages remain. They are not twelve unanswered model questions.
AP-02 is identity/accounting contract preparation; AP-03 is eight-resource physical mapping, with nominal D2R airtime already accepted.
AP-04 full batch timing, AP-05 receiver/FBL mapping, AP-06 ns conversion and EN-01/02/03 energy work remain.
Later work is scenario/integration, baseline, fairness and experiment design. Implementation/tests/human acceptance/delivery are tracked separately.
No new question, implementation or publication authorization follows from this inventory. Influence stays 28.

## 2026-11-02 | Current bit duration changed to tau

The user changes BD from tau/2 to tau; retain FEC, BPSK, repetition 1, short ambles and no additional midamble.
Preserve the interval-field index S*48: S=2 at tau, so the actual interval is 96 bits.
Current exact pure D2R ms for {8,16,32,64} bytes: {174/5,934/15,586/5,3406/15}.
Use ReferDoc/Plan/D2R_Timing_Configuration.md as the canonical updated table (R-01 section 57).
At tau, legal SFS factors are {1,2,4,8,16,32,64}: seven, not eight.
Preserve the eight ideal orthogonal-resource assumption and keep its concrete mapping open. Do not add SFS=128 at tau.
Full Paging/offset/Guard, ns rounding, receiver reliability and energy feasibility remain unresolved.

## 2026-11-02 | Seven-Tag limit and resource mapping

R-01 section 58 reduces the batch limit to seven. Fixed tau SFS pool: {1,2,4,8,16,32,64}.
Assign stable Tag-ID order to ascending pool entries. Keep ideal orthogonality and parallel D2R.
Nonempty actions have 1-7 Tags; eight is atomically invalid. Empty remains NO_OP.
The D2R timing table is unchanged. AP-03 configuration mismatch is resolved; other PHY/time/energy evidence remains open.
Earlier eight-Tag/eight-resource notes are historical. No runtime Access/Validator enforcement is claimed.

## 2026-11-02 | Remaining decision view clarified

Plan/decision-inventory.md now separates six current model/profile discussion areas from AP-02 agent-owned contract review.
Current topics: full-batch timing, receiver/FBL, ns rounding, energy-source profile, Tag energy profile and depletion/wakeup.
Four later areas remain scenario/integration, baseline, fairness and experiments. Eleven is a work-package count, not an unanswered-question count.
Prepare evidence-backed profile candidates before consolidated discussion. No new question; Influence remains 28.

## 2026-11-02 | AP-04 response-time reference decision open

Q-INFLUENCE-29 compares a final-Paging batch reference (explicit research abstraction, A recommended) with per-Tag standard response timing (B, requiring phase redesign).
Source-derived lower bounds show the current seven sequential Paging messages cannot all finish before the first response with mandatory MAC fields retained.
Evidence and assumptions: AgentDoc/openspec/discuss/2026-11-02-batch-response-timing.md.
No phase revision, R2D profile, Guard or numerical batch schedule is accepted yet. Keep seven-SFS and tau/FEC decisions. Influence is 29.

## 2026-11-02 | Common batch-Paging reference accepted

R-01 section 59 accepts Q-INFLUENCE-29 A. Each Tag's delay is measured from the final batch-Paging end.
This is a simulator timing abstraction; it preserves all-Paging-first operation and need not align D2R starts.
Q-INFLUENCE-30 compares M=24/minimum-three-PRB and M=6/minimum-one-PRB R2D formats. Answer pending.
No actual Paging ID/TBS, Guard, reception gain or full-batch feasibility is selected.

## 2026-11-02 | R2D M=24 accepted

R-01 section 60 fixes M=24 and at least three PRBs for CAP/PRDCH/postamble/padding; SIP remains separate.
Q-INFLUENCE-31 compares complete permanent-ID/no-domain profiles with 32/96-bit identification content.
Derived Paging TBs are 27/35 bytes and total OFDM symbol counts 24/30; neither profile is accepted yet.
CP alignment, Guard and full batch feasibility remain open. Do not reuse the earlier 32-byte fixture as actual Paging size.

## 2026-11-02 | Compact Paging profile accepted

R-01 section 61 accepts Q-INFLUENCE-31 A: 32-bit content, no optional domain, 42-bit full Paging ID and 27-byte CFA Paging.
Use Paging_R2D_Timing_Configuration.md: M=24 gives 24 symbols; CP-dependent physical duration is about 1.714063-1.714583 ms.
Seven consecutive messages total 12 ms only with continuous CP phase/no gaps. CP alignment, Guard and response/batch verification remain open.
Influence stays 31; no new question, complete physical schedule or runtime implementation is accepted.

## 2026-11-02 | Fixed Paging design accepted

R-01 section 62 fixes sequential 27-byte/24-symbol Paging with continuous batch-local CP and zero inter-message gaps.
Use long CP at batch-local n modulo 7 = 0. The canonical Paging table has exact per-message and cumulative values; seven messages total 12 ms.
For fewer Tags use the actual prefix, not 12 ms or 12/7 ms per packet. No global NR frame-alignment proof or hidden wait is inferred.
Guard, response verification, ns conversion and full batch/energy remain open. Influence stays 31; no new question.

## 2026-11-03 | Guard candidate prepared

Q-INFLUENCE-32 is open. TS 38.191 clause 9.3 and current tau/SFS yield maximum device post-D2R interval 200 us.
A proposes fixed 200 us with explicit Reader/CW recovery-within-Guard assumption. B requires G=max(200 us,hardware recovery bound).
This device requirement does not by itself specify the complete simulator Guard. No value or hardware recovery evidence is accepted.
Keep one Guard after the last D2R, CW off/no EH and full-window validation. Evidence: 2026-11-03-guard-candidates.md in discuss/.

## 2026-11-03 | Fixed Guard accepted

R-01 section 63 closes Q-INFLUENCE-32 with A: G=200 us=200000 ns, once after the latest D2R end.
CW turns off at that end; no Guard harvesting. Next Policy/Paging waits for the complete Guard; require end+G<=window_end.
Assume Reader/CW recovery fits inside G; no hardware validation or universal normative batch-Guard claim.
Guard selection is closed. Response lookup/full batch verification, AP-06 rounding and receiver/energy profiles remain open. Influence stays 32.

## 2026-11-03 | First-version reception simplification accepted

R-01 section 64 supersedes the earlier first-version RANDOM/FBL mapping.
Retain CW/zone classes: RELIABLE succeeds, UNREACHABLE fails, RANDOM uses constant packet-success probability p_rx.
The user selected revised Q-INFLUENCE-33 A. No numerical p_rx is accepted yet.
CRC/FEC overhead remains in duration and energy; within-class TBS/SINR decoder reliability is excluded.
Q-INFLUENCE-34 is open: proposed p_rx=0.5 research baseline versus a user-specified constant.
The proposal is not empirical calibration. Existing source still uses FBL; implementation is pending.

## 2026-11-03 | Reception aligned with prior CW table

R-01 section 65 records the custom Q-INFLUENCE-34 answer. Preserve LOW near/middle/far=RELIABLE/RANDOM/UNREACHABLE,
MEDIUM=RELIABLE/RELIABLE/RANDOM, HIGH=RELIABLE/RELIABLE/RELIABLE. No independent 50-percent setting is accepted.
The prior table specifies RANDOM qualitatively; numerical entries remain open before sampler implementation.
One shared constant versus separate entries is not decided. Section 64's shared-constant requirement is superseded.
FBL stays disabled; preserve CRC/FEC overhead and stored-energy admission. No source/runtime change. Influence stays 34.

## 2026-11-03 | Original hybrid reception restored

R-01 section 66 supersedes the earlier no-FBL and fixed-RANDOM-value discussion.
Q-INFLUENCE-35 A: retain RELIABLE success 1, UNREACHABLE success 0 and RANDOM success 1-epsilon_FBL(rho,k,n).
CW/zone classes stay unchanged. No extra constant probability, second FBL factor or arbitrary coding gain.
Existing channel source already implements this classification. Selected-TBS k/n/rho mapping still needs preparation and verification.
CRC/FEC time/energy overhead and all admission/accounting rules remain. Influence stays 35; no new question or code change.

## Required Notebook explanation: stored-energy admission (2026-11-03)

The user requested this explanation in the future Jupyter Notebook; no Notebook implementation is started by this request.

- Explain that selecting a TBS requires enough stored energy for the complete planned operation, including applicable startup, waiting and mode costs.
- Show the D2R duration lookup and transmission-energy calculation with explicit units.
- The accepted D2R duration already includes CRC, FEC and ambles. Do not multiply the duration or energy by three again.
- Assume no energy harvesting during D2R. External CW enables reflection; it does not make Tag circuitry consume zero energy.
- Reject a TBS whose full operation exceeds stored energy. A smaller legal TBS or a later feasible opportunity can be used.
- A completed transmission consumes its full modeled energy even if reception fails; failed data earns no service credit and remains available.
- Separate illustrative power values from source-backed Tag parameters. Actual support for the longest packet remains [Needs Verification] until parameters are selected.

This documentation request does not resolve Q-INFLUENCE-36's CRC/FBL interpretation. Influence remains 36.

## 2026-11-03 | Remaining decisions audited

Current discussion scope: five model/profile groups (AP-05 FBL mapping, AP-06 ns conversion, EN-01 source profile,
EN-02 Tag hardware profile, EN-03 depletion/wakeup) plus four later study groups (SI-01, BL-01, FA-01, EX-01).
These are nine discussion groups, not a fixed question count. Eleven work packages include two agent-owned reviews: AP-02 and AP-04.
Q-INFLUENCE-36 remains open; the Notebook note request did not accept either CRC/FBL interpretation.
The power-table/FBL hybrid is settled; no independent RANDOM probability is needed.
Plan/decision-inventory.md contains the current ordered snapshot. Influence stays 36; no new question or implementation.

## 2026-11-03 | FBL and conversion selected; energy-source discussion begins

R-01 sections 67-68: Q-INFLUENCE-36 A selects k=8*N,n=3*(8*N+16). UE-style ceil-to-ms conversion is accepted.
Complete D2R occupancy is 35/63/118/228 ms. Preserve nominal tables, cumulative Paging prefixes, seven-message 12 ms and exact 200-us Guard.
Three current energy discussion groups remain, plus four later study groups. AP-05/AP-06 source calibration and implementation checks remain preparation.
Q-INFLUENCE-37 asks whether harvesting counts serving-cell communication sources only or all configured compatible active sources.
No source scope, carrier, transmit powers, UE geometry or hardware curve is selected by the question.

## 2026-11-03 | Serving-cell harvesting scope accepted

R-01 section 69: Q-INFLUENCE-37 A counts only the serving DU and its configured communicating UE sources.
Use DU-to-Tag for DL and UE-to-Tag for UL; exclude neighbor harvesting contributions without changing reception interference.
Carrier-profile Q-INFLUENCE-38 is open: equivalent 915-MHz research carrier vs explicit NR-band communication sources.
No carrier, UE count/position, transmit power or compatible nonlinear hardware curve is accepted yet. Influence 38.

## 2026-11-03 | Equivalent carrier accepted; dual-frequency coexistence explored

R-01 section 70: Q-INFLUENCE-38 A selects the equivalent 915-MHz research communication carrier.
The user also requests literature on concurrent 3.5-GHz and 915-MHz operation and frequency isolation.
This is exploration only: no simultaneous UE-phase CW, D2R harvesting or zero-interference assumption is accepted.
Evidence: AgentDoc/openspec/discuss/2026-11-03-dual-frequency-coexistence.md.
Source powers, UE geometry and compatible harvesting hardware remain open. Influence stays 38; no new question or implementation.

## 2026-11-03 | RF hardware evidence and transition clarification

R-01 section 71 records the user-confirmed UE-end -> RF transition -> Tag-band procedure.
The transition is inside the 600-ms window, before Tag-band operations, and separate from the 200-us final Guard.
No duration is selected; no source-free harvesting credit or extra payload is assumed during transition.
ReferDoc/Plan/RF_Hardware_and_Frequency_Switching_Evidence.md records TMTT/NSDI hardware evidence and X310/SBX/AD9361 official links.
The future Notebook must show the transition interval, remaining Tag budget and evidence limits.
No simultaneous dual-band requirement or change to the equivalent 915-MHz profile is introduced. Influence stays 38.

## 2026-11-03 | Source-power time dependence under discussion

Q-INFLUENCE-39: A separately configured fixed-per-run DU/UE communication powers vs B external per-Window powers; no answer or numerical value.
Preserve R-01 section 32's one logical UE per DU without coordinates. New UL harvesting needs independent traceable link-gain input, not an invented UE position.
Communication powers do not automatically equal D2R CW tiers. Policy actions stay Tag/TBS. Influence 39; no source changes.

## 2026-11-03 | DU per-Window power; UE fixed power

R-01 section 72: DU communication transmit power is configured per Window; each UE uses fixed configured transmit power.
DL harvesting uses DU power; UL uses UE power. No source-power Policy action or within-Window power-control algorithm is added.
Q-INFLUENCE-40 asks whether communication and CW share a common Window power state; exact dBm remain unselected.
Influence 40. Existing resource/source, RF transition and reception rules remain unchanged. No code change.

## 2026-11-03 | Shared Window state and proposed RedCap/SUL source

R-01 section 73: DU communication and CW share LOW/MEDIUM/HIGH state, with distinct configured numerical mappings allowed. UE power stays fixed.
The user proposes RedCap UE characteristics and possible SUL transmission. Its source role is open under Q-INFLUENCE-41.
SUL is a supplementary communication uplink, not inherently a high-power or energy-only carrier. Capability and supported band combinations must be declared.
Keep the accepted equivalent 915-MHz abstraction and continuous-prefix research assumption unless explicitly revised. Influence 41; no code change.

## 2026-11-03 | Ordinary SUL source accepted; remaining inventory reconciled

R-01 section 74 accepts Q-INFLUENCE-41 A: ordinary scheduled SUL UL traffic from a suitably capable RedCap UE profile supplies RF for Tag harvesting.
No dedicated UE energy waveform or actual NR carrier is selected. Equivalent 915 MHz and fixed configured UE power remain research assumptions.
Remaining current groups: source/RF numerical operating profile (including RF transition duration), Tag hardware/energy profile and depletion/wakeup.
Four later groups remain scenario/integration, baseline, fairness and experiments. Seven discussion groups are not seven fixed questions.
AP-02/04/05/06 source/contract/schedule/validation work is agent-owned preparation. Influence stays 41; no new question or implementation.

## 2026-11-03 | EN-01 source/RF candidate for consolidated review

Q-INFLUENCE-42 is open: adopt or adjust ReferDoc/Plan/EN01_Source_RF_Profile_Candidate.md.
The synthetic candidate proposes DU DL 18/24/30 dBm, UE 20 dBm, common -50-dB UL gain and 1-ms RF transition; retained CW values are -2/10/22 dBm.
No new numerical value is accepted or implemented. One-way DL gains retain the accepted prototype reference; incident RF examples are not battery increments.
The UL equal-gain assumption and switching budget are research settings, not literature measurements. EN-02 hardware/energy choices remain open.
Influence 42; no code/runtime tests or calibration.

## 2026-11-03 | Source/RF baseline accepted; Tag energy profile starts

R-01 section 75 records Q-INFLUENCE-42 A. EN01_Source_RF_Profile_Candidate.md now records accepted source-rf-synthetic-v0.1 values.
Two current groups remain: Tag hardware/energy profile and low-energy recovery, plus four later study groups.
Q-INFLUENCE-43 is open: use a hardware-data table with piecewise interpolation or fit a normalized logistic RF-to-DC curve.
Both are nonlinear; no curve data, capacity or mode-cost numbers are accepted yet. Influence 43; no runtime/default changes.

## 2026-11-03 | Named charging-model paper required

R-01 section 76 supersedes Q-INFLUENCE-43's generic A/B choice with the user's named reference:
Throughput Optimization for Ambient IoT Systems in Indoor Factory Environments, WCSP 2025, DOI 10.1109/WCSP68525.2025.1010215.
Publisher metadata/abstract is verified; exact charging equations and coefficients are unavailable. Request a PDF or the relevant equation pages.
Preserve UE-prefix-only harvesting, persistent finite storage and stored-energy admission; do not silently import the paper's factory scenario or all parameters.
Report any conflict with the previous nonlinear assumption after inspecting the original. Influence stays 43; no implementation.

## 2026-11-03 | WCSP original inspected; zero-input correction proposed

R-01 section 77 and WCSP2025_Charging_Model_Mapping.md verify the user-provided paper's unnormalized Sigmoid (equation 3) and finite-capacity energy update (equation 5).
The raw formula has nonzero DC output at zero RF input. Table I coefficients have incomplete individual unit labels and are not transferred to our low-power profile.
Q-INFLUENCE-44 proposes zero-input correction plus newly supported passive parameters; no answer or Tag numerical values yet. Influence 44.
Preserve UE-prefix-only harvesting, event-based mode/startup costs, stored-energy admission and accepted source/timing profile. No code changes.

## 2026-11-03 | Zero-input-corrected Sigmoid accepted

Original answer to Q-INFLUENCE-44:
> 採用

The user accepts the zero-input-corrected Sigmoid with newly selected passive parameters.
Use L(P)=M/(1+exp(-s*(P-z))), Omega=1/(1+exp(s*z)), and F(P)=(L(P)-M*Omega)/(1-Omega).
This adaptation gives F(0)=0. It does not adopt the WCSP table coefficients.
Use linear watts for P, M and z; s has units W^-1.
Require 0<=F(P)<=P throughout the declared input domain. Do not conceal unsuitable parameters through output clipping.
Preserve UE-prefix-only harvesting, finite persistent storage, mode/startup costs and full-operation stored-energy admission.
EN-02 numerical conversion, capacity and mode/startup costs remain open as one coherent profile.
EN-03 recovery remains open. Influence stays 44; other facet counts are unchanged.
No simulator implementation, fitted curve, hardware validation, commit, push or publication.

## 2026-11-03 | User requests capacity and mode-power alignment

Original instruction:
> 了解,那這邊的tag容量與各模式功耗可以請您對齊我剛剛提供的paper那篇嘛？或是是否有高品質文獻可以直接對齊？

Reviewed the selected WCSP original and three primary hardware/circuit papers.
WCSP Table I supplies E_max=E_0=1 mJ. Equation (4) supplies P_con=alpha*g_n*p_n(t).
No numerical alpha or separate sleep/Paging/wait/startup cost table was identified.
The paper therefore does not provide our complete event-mode consumption profile.
SIGCOMM 2013 analog-only TX/RX powers and ISCAS 2022 simulated wake-up power are not whole-Tag costs.
ISSCC 2023 supplies measured wake-up/calibration/backscatter powers, but its 25-uW active mode differs from our Device-1 scope.
The 1-mJ candidate also needs a time-scale check: at constant total 1 uW, without harvesting or extra startup, it lasts 1000 s.
Details and links are in ReferDoc/Plan/WCSP2025_Charging_Model_Mapping.md and the existing Tag energy discussion.
No numerical capacity or mode/startup cost is accepted yet. Influence stays 44; no new decision question.

## 2026-11-03 | Numerical Tag energy candidate proposed

Original instruction:
> 了解,還是您這邊有推薦可靠的數值,來進行 tag 電量的遞迴更新 , 像是比較論文那篇那樣

Prepared ReferDoc/Plan/EN02_Tag_Energy_Profile_Candidate.md, tag-energy-synthetic-v0.1.
Propose 1-uJ usable capacity, initial full, 10-nW quiescent power, 1-uW receive/D2R totals and 1-nJ activation energy.
Supply a complete synthetic corrected Sigmoid: M=10 uW, s=2e5 W^-1, z=10 uW.
These are explicit research assumptions, not measured or fitted Tag parameters.
The global derivative bound 0.5676676416 proves 0<=F(P)<=P without clipping.
UL input 1 uW produces 0.2571323571-uW DC; a 400-ms quiescent interval gains 0.09885294284 uJ before capacity saturation.
Q-INFLUENCE-45 proposes A complete 1-uJ research candidate versus B same candidate with WCSP 1-mJ capacity. No answer.
Both keep existing source, phase, timing and stored-energy admission rules. EN-03 recovery remains open.
Influence 45; other counts unchanged. Scalar checks only; no simulator or hardware validation.

## 2026-11-03 | Q-INFLUENCE-45 A accepted

Original answer:
> a

Adopt the complete tag-energy-synthetic-v0.1 profile from ReferDoc/Plan/EN02_Tag_Energy_Profile_Candidate.md.
E_max=E_0=1 uJ; quiescent power 10 nW; receive and D2R total powers 1 uW each; activation energy 1 nJ when needed.
Converter parameters are M=10 uW, s=2e5 W^-1 and z=10 uW in the accepted zero-input-corrected Sigmoid.
The 1-mJ capacity alternative is not selected. Preserve causal admission, phase permissions and persistent storage.
This acceptance selects research parameters, not measured hardware or a fitted curve. Existing calibration limits remain.
EN-02 numerical selection is closed for this version. EN-03 recovery remains open, followed by four later study groups.
No runtime source/default changes, simulator tests, hardware validation, commit, push or publication.

## Q-INFLUENCE-46 | Depleted-state charging abstraction [OPEN]

Facet: Influence, total 46; other facet counts unchanged.
Purpose: prevent negative energy while specifying what remains operational after stored usable energy reaches zero.
This applies outside previously admitted complete operations. It does not replace TBS energy admission.

A, recommended: use an ideal passive recovery state after depletion.
Disable reception, D2R and normal 10-nW quiescent operation in that state.
Assign zero separately modeled recovery-circuit draw and no additional harvester cold-start threshold.
Continue only phase-permitted charging through the accepted F(P); retain the capacity cap and simulator service state.
At a legal Policy decision, return to eligibility only if stored energy covers at least one complete currently legal operation.
Apply the accepted 1-nJ activation cost if an operation is selected; do not charge it merely for becoming eligible.
Do not create an asynchronous transmission, assume every TBS fits, spend future harvest or reset energy to full.
If no complete operation fits, remain in passive recovery even when some energy has accumulated.

B: require a hardware-based PMU/cold-start and recovery-cost model before specifying this state.
This needs additional circuit parameters and original evidence. It is not an instruction to invent a threshold or continue drawing from an empty store.

Example for A: at zero usable energy, 400-ms permitted UL harvesting would store about 0.102852943 uJ before activation.
The normal quiescent state's 400-ms net gain remains 0.098852943 uJ because it spends 10 nW.
The difference is the proposed recovery-mode overhead assumption, not a change to the converter or normal idle power.
Full-operation costs still decide which TBS options can be admitted later.

A makes the simulator's recovery abstraction explicit and keeps development small.
Its zero separate recovery overhead and ideal cold-start behavior are research assumptions, not hardware measurements.
B allows a calibrated recovery model but needs more evidence before numeric implementation.
Optional custom answers may specify a different recovery model. No answer is recorded.

## 2026-11-03 | Q-INFLUENCE-46 A accepted: ideal passive recovery

Original answer:
> A

When usable stored energy reaches zero outside an admitted operation, enter ideal passive recovery.
Disable receive, D2R and normal 10-nW quiescent operation. Recovery has zero separately modeled circuit draw and no additional cold-start threshold.
Keep only UE-prefix-permitted charging through the accepted F(P), with E_next=min(E_max,E+H*F(P)*Delta_t).
When H=0, recovery-state energy remains unchanged. Preserve accumulated energy and simulator service state; do not reset to full.
At legal Policy decisions, a recovered Tag is eligible only if stored energy covers a complete currently legal operation, including activation when needed.
Eligibility alone does not start reception, transmission or activation debit. A valid selected operation triggers the accepted activation and normal mode ledger.
If no complete legal operation fits, remain in recovery, even with positive accumulated energy.
Do not insert a new Policy call or autonomous transmission merely because a charging threshold is crossed.
Normal, non-recovery quiescent operation still costs 10 nW. The zero overhead applies only to the accepted ideal recovery state.
Split at actual depletion; do not conceal a negative-energy interval with lower-bound clipping.
Full-operation stored-energy admission still prevents mid-operation energy exhaustion under the accepted model.
Example: 400-ms allowed UL charging at 1-uW RF input stores 0.10285294284 uJ from zero before activation.
This differs from the normal quiescent net gain of 0.09885294284 uJ because recovery omits the separate 10-nW draw.
These are research assumptions, not measured cold-start or PMU behavior.
EN-03 first-version model selection is closed. Access/PHY/data/energy discussion choices are settled; implementation and calibration remain separate work.

## 2026-11-04 | Q-INFLUENCE-47 B accepted

Original answer:
> B 我們必須考量到對應實務性

Select 600-ms shared outer Windows every 1000 ms from t=0, with 400-ms gaps.
Window k is [k*1000000000,k*1000000000+600000000) ns for integer k>=0.
Keep independent local UE duration/direction draws and all accepted source/PHY/energy settings.
Gaps permit no harvesting, Paging or D2R. Charge normal quiescent power until depletion; then use accepted passive recovery.
Preserve absolute exclusive service deadlines and persistent stored energy. Do not extend deadlines or recharge at each Window.
The user's practicality motivation selects a research calendar, not measured deployment timing or a standard requirement.

## Q-INFLUENCE-48 | Final Guard at the round boundary [OPEN]

Date: 2026-11-04. Facet: Influence, total 48; other counts unchanged. No answer.
Purpose: specify cleanup when the final service deadline falls inside a Window.
Keep evaluation end T_end=max(service deadlines), strict D2R_END<service_deadline credit and full 200-us Guard.
Both options require the complete batch and Guard to fit in the actual outer Window.
Example only: T_end=15.5000 s, Window [15.0000,15.6000) s, final D2R_END=15.4999 s, Guard_END=15.5001 s.
The final D2R is before evaluation end; Guard extends 0.1 ms beyond it.
A: require Guard_END<=T_end as an extra admission constraint; reject the example batch.
B, recommended: permit this already-required Guard to finish after T_end, within the Window.
For B, stop service credit and new Policy/Paging at T_end. Complete only Guard and its normal mode-energy accounting.
Record evaluation end and physical cleanup end separately. No deadline extension or new service opportunity is created.
Preserve each scheduled D2R's applicable service deadline; this proposal does not authorize late D2R credit.
A keeps physical stop at evaluation end; B preserves a valid final reception while completing mandatory cleanup.
Optional custom answers may specify another consistent rule. No answer, implementation or publication is authorized.

## 2026-11-04 | Q-INFLUENCE-48 B accepted: final Guard cleanup

Original answer:
> B

Keep the service evaluation end T_end=max(configured service deadlines).
Permit already-required final Guard to finish after T_end, provided Guard_END<=outer_Window_END.
All batch D2R ends must precede T_end. Each service credit still requires D2R_END<that service's exclusive deadline.
At T_end, stop service credit and new Policy/Paging. Complete only the existing Guard and its reserved mode-energy accounting.
Do not harvest, extend deadlines, start new batches or expose a new service opportunity during cleanup.
Record evaluation end and physical cleanup end separately. The configured service round length remains unchanged.
Example: final D2R at 15.4999 s and Guard end at 15.5001 s are permitted for T_end=15.5000 s within Window [15,15.6) s.
Full-operation admission must reserve the complete Guard energy and time, including its permitted tail after T_end.
No code/default changes, simulator tests, commit, push or publication.

## Q-INFLUENCE-49 | Initial per-Tag application data for the reference scenario [OPEN]

Date: 2026-11-04. Facet: Influence, total 49; other counts unchanged. No answer.
Purpose: select the missing numerical data supply for a reproducible reference run.
Initial finite supply at t=0, no later arrivals, failed-data retention and multi-service shared credit are already settled.
This question selects initial valid application bytes per configured Tag, not a TBS, service demand or arrival process.

| Option | Initial valid bytes per Tag | Payload-only lower bound with 62 valid bytes per successful 64-byte TB |
|---|---|---|
| A, recommended | 64 | ceil(64/62)=2 successful transmissions |
| B | 256 | ceil(256/62)=5 successful transmissions |

Both are proposed synthetic reference inputs, not measured farm-sensor data volumes.
Use the same selected amount for all configured Tags in this first reference workload.
A provides a smaller case for checking partial payload, retention and repeated transmissions.
B provides more data per Tag and can expose longer energy/time competition, without guaranteeing completion.
The displayed lower bounds ignore calendar, energy, channel failures and service stops; they do not prove 64-byte scheduling feasibility.
Selected TBS remains in {8,16,32,64} bytes. Padding contributes no new application data or service credit.
Services still have separate demands, designated Tag sets and deadlines; this answer does not select those missing values.
Optional custom answers may supply another initial amount or an explicit per-Tag table.
No implementation or publication is authorized by this question.

## 2026-11-04 | Q-INFLUENCE-49 custom answer: ample initial data

Original answer:
> 這邊的話我們就假設初始的tag可以先回傳最多資料量

Interpret this in the current initial-supply discussion: each Tag starts with enough application data to fill the selected legal TBS.
Use ample initial supply for the reference run, rather than selecting the proposed 64/256-byte inventory limits.
Preserve the earlier finite t=0-only supply and no later arrivals. No periodic refill or infinite arrival process is introduced.
Choose a conservative finite initial count during scenario construction so the run cannot exhaust it through legal transmissions.
This is an input-preparation task; do not ask another preference question merely for its derived number.

The maximum valid application payloads for TBS {8,16,32,64} bytes remain {6,14,30,62} bytes.
Policy still selects a legal TBS based on actual energy, timing and service needs.
This data-supply answer does not force an initial 64-byte transmission or guarantee that a 64-byte operation fits a Window.
Preserve complete-TBS duration/energy, failed-data retention, unique successful payload and per-service demand caps.
A 62-byte successful payload can reduce a service's 20-byte remaining demand by only 20 bytes; the service cap is unchanged.

A conservative finite input construction is available after T_end is configured:
N_bound=ceil(T_end_ns/35000000), initial_bytes_per_Tag=62*N_bound.
A Tag cannot complete more nonoverlapping D2R attempts than this bound when the shortest accepted occupancy is 35 ms.
Every successful attempt consumes at most 62 new application bytes. Failed attempts retain their data.
This ignores UE occupancy, Paging, gaps, Guard, energy and failures, so it overestimates available transmission opportunities.
It is not a feasible-attempt count, calibrated hardware memory capacity or a mandatory materialized byte array.
For an illustrative 20-s horizon, N_bound=572 and initial count=35464 bytes. This selects no new service deadline.
A tighter proven bound may be used during input preparation without changing the ample-supply behavior.

Q-INFLUENCE-49 is answered with this custom supply choice. Influence remains 49; no new question is opened.
Service counts, designated Tag sets, service demands and deadlines remain scenario-workload inputs.
No runtime source/default change, simulator tests, commit, push or publication.

## 2026-11-04 | Remaining-study discussion resumed; service reference table open

- Scope: Continue the existing discussion. Four groups remain: SI-01 scenario/integration, BL-01 Baseline, FA-01 fairness and EX-01 experiments.
- Prepared: Complete two-service candidate in docs/architecture/service-config-example.md and existing scenario discussion; R-01 section 86 records proposal status.
- Values proposed: S1 Tag-001/002/003, 128 bytes, 15-s deadline; S2 Tag-003/004/005, 256 bytes, 20-s deadline. Require these actual IDs, retaining topology ownership and zones.
- Active: Q-INFLUENCE-50 A adopt small integration table versus B adjust to intended workload. No answer. Influence 50; other counts unchanged.
- Preserved: Explicit Notebook inputs, t=0 start, max-deadline horizon, ample initial data, shared credit and all accepted timing/energy rules.
- Limits: Synthetic integration example, not calibrated farm demand, representative full-network load or demonstrated feasible completion.
- Verification: Payload/bit/calendar arithmetic and document checks only. No code/default changes, simulator tests, commit, push or publication. OpenSpec remains channel 11/12 and timeline 8/9.

## 2026-11-04 | Q-INFLUENCE-50 A accepted; Tag energy preparation requested

Original instruction:
> A 這邊可以,這邊的目標是請先確定好目前的組態內容,則baseline的部份我等等會給您算法 因此先不用做,則這邊我確定下可以先實做tag 的電量改變跟我們剛剛討論內容的模組媽 這邊的模組輸出請遵照 $workflow

Accept the complete small reference table: S1 Tag-001/002/003, 128 valid bytes, exclusive deadline 15 s; S2 Tag-003/004/005, 256 valid bytes, deadline 20 s.
Both start at zero. Retain actual topology ownership, shared credit, ample finite initial data and the accepted max-deadline horizon.
The user will supply the Baseline algorithm later. Do not design or implement Baseline now.
Prepare Tag energy update, conversion, operation-energy checks and depletion recovery as an independent first module scope.
Module output must follow workflow: executable teaching Notebook, behavior checks, architecture and tree-form code trace, human acceptance before source extraction.
Accepted configuration is sufficient for isolated energy behavior checks using explicit event sequences; no Baseline algorithm is required.
Implementation scheduling remains subject to the existing merge rule. No local-first exception is inferred from this request.
ReferDoc/Plan/Tag_Energy_Implementation_Readiness.md records the complete configuration, scope, acceptance cases and the verified workflow gate.
Influence stays 50; no new model preference question. No new change/specification or implementation started.

## 2026-11-04 | Local-first scope authorized; charging trace first

Original answer:
> 可以,先trace 充電模組

The user confirms the scoped local-first Tag energy exception, then asks to trace charging first.
This overrides serial-merge scheduling only for the authorized local Tag energy prototype.
It does not mark Channel or ResourceTimeline merged, change their remote-delivery tasks, authorize publication or complete the workflow.
Baseline remains deferred to the user. The immediate output is design/source trace, not a completed charging implementation.

Delivered docs/architecture/tag-energy-trace/README.md and README.zh-TW.md, with code-trace.md, a Decimal calculator and its JSON evidence.
The Archify design diagram is .archify/dataflow-tag-charging-20261104-151852/tag-charging.html, stored through the existing agent-worktree navigation link.
The diagram explicitly marks the charging core/adapters as planned. Its schema, delivery, strict and automated-browser gates passed.
No separate human visual review or user acceptance of a runtime implementation is claimed.

Source inspection: build_timeline creates UL/DL direction, but CurrentResource/current_resource omit that field and source RF power.
The current link_budget applies reflection loss and twice one-way gain; its Reader receive power must not be used as harvesting input.
The planned environment adapter must supply only current phase/direction/one-way RF to energy accounting.
The worked normal example uses an in-run 0.8-uJ snapshot, 1-uW RF input and 400 ms: final energy 0.89885294284 uJ.
Capacity saturation, passive recovery and no-harvest gap examples are included; exact 200-ms depletion is a separate scalar case.
The arithmetic calculator passed with a rounding-only Decimal balance tolerance, not a runtime energy-clipping policy.

Influence stays 50; no new model question. No energy Notebook, src/energy, energy module tests or new OpenSpec change exists yet.
The next phase is the scoped specification/TDD contract and Notebook after this requested design trace.
No commit, push, remote Issue/PR, merge or publication.

## 2026-11-04 | Charging trace converted to executable Notebook

Original instruction:
> 這邊可以請您轉成jupyter notebook , 跟 ＠/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks 一樣

Created notebooks/04_tag_energy.ipynb in the established teaching style, with accepted settings, Traditional Chinese explanations, explicit calculations, tables, phase gates, depletion, PNG plot and assertions.
The Notebook implements the scalar conversion/trace only; full Tag state/operation admission, adapter, Engine and Baseline remain outside this conversion task.
OpenSpec change add-tag-charging-trace-notebook records scope and TDD acceptance. Core remains in the Notebook until human acceptance.
24 focused tests pass. A clean temporary RL kernel executes all 13 code cells without errors and shuts down; saved output includes one inspected PNG.
Spec review found no defects. Standards review found one integer-overflow rejection defect, repaired and rechecked. Scoped marked-debt scan found no markers.
The current Notebook dataflow passes Archify validate/deliver/strict/browser checks. Trace and paired guide/README links are updated.
Human acceptance, src extraction and remote delivery remain pending. Previous changes remain unmerged; no commit, push, Issue/PR, merge or archive.
Influence stays 50. No new model decision.

## 2026-11-04 | User-selected PScatter state-machine reference

Original instruction:
> 了解,那這邊tag狀態切換的模式我認為可以參考這篇paper 進行設計  @/home/tonywang/Downloads/Energy-Efficient_Paging_for_Duty-Cycled_LTE_Backscatter.pdf

Read the ten-page original; Fig. 5 and Table III visually checked. Source mapping: ReferDoc/Plan/PScatter_Tag_State_Mapping.md.
The paper distinguishes Static, Wakeup, Active and Sleep, with Timing and Modulate for backscatter preparation/execution.
Paging Active is not D2R modulation. The paper's UE forwarding/UE-ID protocol differs from our DU/Reader Tag Paging.
IC power values are Cadence/TSMC circuit simulation, not measured ASIC results. Do not replace accepted 1-uJ/1-uW profile silently.
Fig. 5(b)'s lower arrow/label conflicts with the section III-B prose and Fig. 5(a); record this ambiguity instead of copying it blindly.
Q-INFLUENCE-51 opens A state structure with existing activation abstraction versus B explicit new wake-up packet/synchronization stage. No answer.
Influence 51; other counts unchanged. State/power mapping is proposed, not a final accepted FSM.
Existing charging Notebook remains unchanged, human acceptance pending. Baseline remains deferred; no implementation or publication.

## 2026-11-04 | Q-INFLUENCE-51 A accepted

Original answer:
> A

Borrow PScatter's separation of control states while retaining our accepted scheduled-operation activation abstraction.
WAKING applies the existing 1-nJ activation debit when needed. It adds no wake-up packet, 80-us interval or separate synchronization duration.
Retain current DU/Reader CFA Paging, D2R offsets, Guard, source phases and numerical energy budgets.
Do not import PScatter's UE paging relay, UE-ID protocol, LTE PF/PO schedule, PSS synchronizer or IC power values.
The adapted state/control mapping is documented in docs/architecture/tag-state-design.md.
Full-operation stored-energy/time admission remains before activation; future harvesting cannot fund it.
Influence stays 51. No new preference question or runtime implementation is implied by this design update.

## 2026-11-04 | Assumption explanation criterion confirmed

Original answer:
> 行 這邊因為是假設組態,所以可以跟老闆解釋的出來即可

The user accepts the research-configuration framing and wants a clear supervisor explanation.
State sources, selection reasons and evidence limits for control states, power, capacity, activation, conversion and recovery.
The rationale table is in docs/architecture/tag-state-design.md. Retain all accepted numbers and scheduled-activation semantics.
Do not present explanatory rationale as measured hardware, standard conformance or demonstrated experimental robustness.
Future sensitivity evidence is not yet performed. Influence stays 51; no new model question or runtime change.

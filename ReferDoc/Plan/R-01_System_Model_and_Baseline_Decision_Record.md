# R-01 — Ambient IoT 碩論 System Model 與 Baseline 討論紀錄

> **文件性質**：GRILL 討論的設計決策／待驗證問題交接紀錄（非論文已驗證結果、非實作規格定稿）  
> **更新日期**：2026-10-19（臺灣時間）  
> **範圍**：R-01 系統模型、服務目標、公平性、Baseline 審查；R-02 模擬器架構與介面決策（持續更新）  
> **參考檔案**：`system_model.pdf`（11 頁）、`Baseline.pdf`（3 頁）、`模擬器設計.pdf`（2 頁）  
> **閱讀方式**：`[DECIDED]` 為設計選擇、`[ASSUMPTION]` 為模型假設、`[PROVISIONAL]` 為候選規則、`[OPEN]` 為待決定、`[TEST]` 為待證實的驗證工作。

> **最新修訂（2026-10-20）**：第 25 節已由使用者確認 H-03b 最大餘數法及 Tag ID 同分規則；第 21–24 節相關 PROVISIONAL／OPEN 是歷史狀態，由第 25 節取代。此確認不代表實作或測試已完成。

> **交付順序修訂**：最新第 27 節改採每模組 Notebook 原型、對應情境測試及人類理解驗收，接受後才抽離該模組為 `.py`；取代舊章節要求整體 Notebook 通過後才開始 `.py` 抽離的順序。整合驗收仍保留。

> **目前生效的時間／首模組範圍（2026-10-23）**：第 31 節取代首版多期依序啟動、手填共同週期長度及 Deadline 必須嚴格早於期末的舊規則。首版一輪服務全在 t=0 啟動，輪長為最晚 Deadline；最晚 Deadline 可以等於輪末，但服務認列仍採 `t < deadline`。當前優先工作為 IAB 拓撲 Notebook，先完成拓撲範圍盤點。

## 0. 研究問題與目前的論證界線

研究情境為具有 IAB 無線回傳的 Ambient IoT Node，Node 在 UE / TDD 資源占用下取得可使用的 DU 時間，對指定 Tag 進行 Paging、CW 供能及 D2R 回傳排程。Tags 具有不同位置／鏈路品質與能量狀態；服務具有異質的指定 Tag 集合、最低資料需求與期限。

**研究優先順序（已決定）**：在期限內**最大化達標服務數**；在不破壞首要目標的情況下，改善**服務內部 Tag 的資料貢獻公平性**。尚未證實任何 AI／Baseline 方法有較佳效能。所謂「服務達標優先」是整體評估的字典序優先，不代表已證實每次局部選擇最大服務缺口改善就是全域最優。

**證據性質提醒**：此文件的研究環境與目標多屬使用者決定的建模假設／研究設計。`system_model.pdf` 中的公式是現有提案，不應自動視為已通過 3GPP 規範確認。3GPP 規範、研究近似與演算法自訂規則須獨立標記。

## 1. 核心記號及定義

| 記號 | 含義 | 性質／注意事項 |
|---|---|---|
| `q`, `t_q`, `T_q^cycle` | 服務週期索引、起點、長度 | 週期起點確定本期需求 |
| `S_q` | 本週期的服務集合 | 各項服務可有不同期限 |
| `T_{i,q}^req` | 服務 `i` 的指定 Tag 集合 | 可與其他服務重疊；公平性計算的固定集合 |
| `D_{i,q}^min` | 服務 `i` 最低有效資料需求（payload bit） | 正值，不應與含 MAC header 的 TBS 混同 |
| `T_{i,q}^max`, `d_{i,q}` | 原研究模型的服務相對／絕對期限 | `0 < T_{i,q}^max < T_q^cycle`；`d_{i,q}=t_q+T_{i,q}^max`。R-02.1c 已決定以「最後可完成 Slot」表示模擬器的 Deadline；原始時間需求如何轉換到 Slot 尚須規格化，不可默默延長期限。 |
| `B_k^phy` | Tag `k` 實際成功傳回的 payload | 物理成功資料指標；每次新有效資料只計一次 |
| `C_{i,k,q}` | Tag `k` 對服務 `i` **需求內被認列**的有效資料 | 單服務上限、跨服務共享及計帳規則需明確 |
| `G_{i,q}(t)` | 服務 `i` 已認列資料量 | `sum_{k in T_{i,q}^req} C_{i,k,q}(t)` |
| `D_{i,q}^gap(t)` | 剩餘需求 | `max(0, D_{i,q}^min-G_{i,q}(t))` |
| `x_{k,w}`, `D_{k,w}^TBS` | DU Window `w` 選擇 Tag 與完整 TBS 的動作 | TBS 為**含 MAC header**的離散候選值 |
| `gamma_{k,w}` | Tag `k` 在 DU Window `w` 的即時 SNR | 各 Tag、各 Window 可變；排程器僅觀測目前值 |
| `F_{i,q}` | 服務 `i` 的 Max–Min 公平性差距 | 必須在服務指定 Tag 集合上計算 |

### 1.1 服務達標

原 R-01 使用連續時間期限 `d_{i,q}`；**R-02.1c 已正式決定 Slot-level Deadline**。模擬器以最後允許完成的 Slot `n_{i,q}^{last}` 判斷：若 `T_slot = 1 ms`，成功接收完成時刻須滿足 `t_D2R_END < (n_{i,q}^{last}+1)*T_slot`。此決策是「期限語意」，而非時鐘誤差或事後增加容忍時間。

```text
G_{i,q}(t) = sum_{k in T_{i,q}^req} C_{i,k,q}(t)
Satisfied_{i,q} = 1{ G_{i,q}(t < (n_{i,q}^{last}+1)*T_slot) >= D_{i,q}^min }
```

原始計量可大於需求，但**認列量**封頂 `0 <= G_{i,q} <= D_{i,q}^min`。未達標服務在其 Deadline 到達時即終止該週期服務的計量資格；服務期限不跨週期。

## 2. 已確認設計選擇（R-01）

| ID | 狀態 | 決策與範圍 |
|---|---|---|
| R-01.1 | [DECIDED] | **第一優先**：最大化各自 Deadline 前達標的服務數；公平性為次要軟性目標。 |
| R-01.2 | [DECIDED] | 同一服務的成功資料可在**多個 DU Window 累加**；不要求於單一 Window 完成。 |
| R-01.3 | [DECIDED] | 各服務需求在每個服務週期起點固定；本階段不處理週期中途動態到達。 |
| R-01.4 | [DECIDED] | 同一筆 Tag 成功新資料可同時被多個需要該 Tag 的**活躍服務**認列；物理 goodput 不重複計算。 |
| R-01.5 | [DECIDED] | 服務認列資料不沿用上一週期；但 **Tag 實際儲能不能隨週期重置**。 |
| R-01.6 | [DECIDED] | 各服務 Deadline 異質且嚴格落在共同服務週期內；完成時刻決定是否達標。 |
| R-01.7 | [DECIDED] | 當資源不足時，優先增加達標**服務數量**，不是單純最大化總 payload bits。 |
| R-01.8 | [DECIDED] | 公平性定義為**每項服務指定 Tag 集合**內的成功資料貢獻接近；不能只對本輪已選 Tag 評估。 |
| R-01.9 | [DECIDED] | Node 在每個 DU Window 使用當前資訊做 Tag 選擇及離散 TBS 配置。 |
| R-01.10 | [ASSUMPTION] | 排程器可完美觀察當前候選 Tag 的**即時 SNR/CSI**，但**無未來 SNR**；此為理想化假設，未表示標準保證。 |
| R-01.11 | [DECIDED] | **停止規則 A**：服務達標後，不再僅為提升其公平性而安排新傳輸；共享 Tag 仍可因其他未達標、未逾期服務而被選中。 |
| R-01.12 | [DECIDED] | **認列規則 A**：主要公平性僅用服務最低需求內的有效貢獻 `C_{i,k,q}`；超額成功資料另行記錄。 |
| R-01.14a | [DECIDED] | 以服務內 **Max–Min Gap** 為主要公平性方向；Jain 指標可作輔助，不強制取代。 |
| R-01.14b | [DECIDED] | 最大與最小貢獻 Tag **必須屬於同一項服務**的指定 Tag 集合。 |
| R-01.14c | [DECIDED] | 多服務層級採選項 **B：優先降低最差服務的公平性差距**，而非僅降低總差距；具體正規化與集合仍待定。 |
| R-01.16 | [OPEN] | 「共享 Tag 排程時是否額外加分」尚未定案，不得假定已採 A 或 B。 |

### 2.1 與最初投影片定義的差異

`system_model.pdf` 第 9 頁曾定義 `W[ℓ]` 為本輪選出的 Tag，並使用：

```text
F[ℓ] = max_{k in W[ℓ]} B_k[ℓ] - min_{k in W[ℓ]} B_k[ℓ]
```

**已識別的問題**：若只選 1 個 Tag，則 Gap 恆為 0，即使所有未被選 Tag 的貢獻為零；且不同服務要求可能被混合。此為**指標退化案例**，不能保留作主要服務公平性定義。修正為：

```text
F_{i,q} = max_{k in T_{i,q}^req} C_{i,k,q}
        - min_{k in T_{i,q}^req} C_{i,k,q}
```

對 `|T_{i,q}^req|=1`，Gap 自然為 0，**不能代表該服務已達標**；必須另外檢查滿足率。服務間需求大小不同，不能將所有 Tag 的 `C` 混成全域 Max–Min。

### 2.2 多服務最差公平性（B）的數學候選

當每個服務的 `D_i^min` 與 Tag 數量不同時，僅比較 raw bit Gap 缺乏可比性。曾提出但**尚未證實／確認分母與評估集合**的候選：

```text
Ftilde_{i,q} = F_{i,q} / (D_{i,q}^min / |T_{i,q}^req|)
Secondary objective candidate: minimize max_{i in S_q} Ftilde_{i,q}
```

評估時必須定義：(a) 未達標服務是否列入最差公平性；(b) 各服務的結果凍結於何時；(c) `D_i^min` 不同時是否採此正規化；(d) 若服務仍未達標、Tag 全為 0，原始 Gap 仍為 0 的語意陷阱。**正規化公式屬 [PROVISIONAL]，不是已證實的最終目標。**

## 3. 跨服務共享及停止排程的界線

每項服務 `i` 獨立維護需求內認列量 `C_{i,k,q}`；每個 Tag `k` 的同一次成功回傳，在物理資料指標中只計算一次，若內容滿足多個服務的要求且各服務未到期限，才可分別認列。**一次傳輸的共享資格與新資料去重必須有可實作的資料識別規則**，不能把純粹重傳失敗／成功的同一 payload 多次認列。

建議供設計檢查的候選活躍集合：

```text
A_k(t) = {i : k in T_{i,q}^req, D_{i,q}^gap(t)>0, t<d_{i,q}}
```

若 `A_k(t)` 為空，不因單一服務的公平性需求而新發起其 Paging。若 `A_k(t)` 非空，仍需通過 SNR、能量、協定與 DU 時間可行性檢查。**已開始的傳輸是否允許中止、是否計入完成後的服務及是否凍結完成服務的 `C`，都要用明確事件規則處理。**

## 4. TBS、同時事件與計帳風險

- **TBS 與 payload 不可混用**：`system_model.pdf` 第 8 頁的 `D_k^TBS` 含 MAC header；`D_i^min` 與主要公平性為有效 payload。須定義 overhead、成功判定、payload 對應。
- **超額例子**：某服務只缺 10 payload bit，而一次合法動作成功回傳 32 payload bit；認列量只能新增 10 bit，其餘 22 bit 記為超額，不得藉此美化主要公平性分數。
- **多 Tag 同時完成**：若同一時刻 Tag A 成功 24 bit、Tag B 成功 16 bit，服務只缺 10 bit，逐事件先到先得可能使 `C_{i,A}, C_{i,B}` 不同，導致相同物理結果因事件隊列順序而得到不同公平性。
- **候選修正 [PROVISIONAL]**：同一時間的 D2R 完成事件先批次收集，再依明示、可重現的規則認列。先前提過「按 payload 比例分攤」，但**尚未獲使用者確認**，且若 payload 不可分割，就不能任意按 bit 拆分。
- **跨服務共享凍結**：服務已滿足後，其他未達標服務使用共享 Tag 的新資料，不得反過來改寫已完成服務的主要公平性；需明文規定服務計量凍結時間及同時事件排序。

## 5. Baseline.pdf 的流程重建與審查結論

> 來源：`Baseline.pdf` 第 1–3 頁手寫流程。以下是**審查重建，不是逐字可靠轉錄、也不是已經可直接執行的偽碼**。

1. 根據 DU 開始／結束及 guard，估算剩餘可用 DU 時間。
2. 建立候選 Tag 清單，包括上一輪尚未被 Paging 的 Tag 等條件。
3. 根據 CW 發射功率、Tag 的鏈路／功率需求分級，形成不同功率情境下的候選優先順序。
4. 先以候選最大 TBS 估算 D2R 時間上限／初始配置；**最大 TBS 是估算起點，不代表最終配置**。
5. 參考服務內最大認列貢獻與低貢獻 Tag 的差距，調整候選 Tag/TBS，檢查剩餘 DU 時間及必要可行性；不足時考慮降低 TBS，再執行 Paging／回傳。

**已辨識的合理動機**：Max–Min Gap 可直觀地尋找貢獻不足的 Tag，且資料差距能作為離散 TBS 的配置參考。**並未證實**「每次選最少貢獻 Tag」保證降低最終 Gap，亦未證實該局部規則能最大化服務達標數。

**反例 1（離散 TBS 造成 Gap 反升）**：服務內目前貢獻 `(20,25,30)`，Gap 為 10 bit；若最低貢獻 Tag 一次成功增加 32 bit，變成 `(52,25,30)`，Gap 變成 27 bit。應比較傳輸後預期狀態，而非只比較傳輸前缺口。

**反例 2（Deadline vs. 公平性）**：服務 S1 的 Gap 較大但 Deadline 尚遠；S2 的 Gap 較小、期限將到，且本 DU 僅能排一次 D2R。無條件服務 S1 可能令 S2 無法達標，違反首要目標。最差公平性是**次要整體目標**，不是局部硬性優先順序。

**反例 3（混合不同服務造成虛假不公平）**：S1 Tag 成功貢獻 `(100,100)`，S2 `(20,20)`；兩服務各自 Gap 為 0，但若全域混合便得到 80 bit Gap，並不能說明服務內部不公平。此反例已由 R-01.14b 決策排除。

**跨服務共享案例**：S1 指定 `{A,B}`、S2 指定 `{B,C}`，Tag B 一筆成功新資料可同時降低兩項未達標服務的缺口，亦可能改善各自 Gap。尚未決定 Baseline 是否要將「共享服務數／邊際貢獻」額外加入排序，**不能將原 Baseline 悄悄改成另一個演算法**。

## 6. 可檢驗的研究貢獻與公平比較

### 6.1 評估層級

- **Primary**：各服務在其 Deadline 前達標的數量／比例；包含負載不可行時的情況。
- **Secondary（已選方向）**：最差服務的服務內 Max–Min Gap（跨服務可比較的正規化規則未定）。
- **Diagnostic**：每項服務的 Deadline 前有效資料、未滿足缺口、零貢獻 Tag 比率、實際 PHY goodput、超額 payload、Tag 能耗／能量不足事件、Paging 次數／失敗／重試、DU 利用率、時間與運算成本。
- **Limitations**：理想 CSI、理想化 PHY 偵測／干擾假設等；不能把環境簡化產生的益處誤認為演算法貢獻。

### 6.2 公平比較的最小要求 [TEST]

Baseline 與候選方法必須使用同一批服務請求／Deadline、Tag 初始能量、信道實現與當前 CSI、UE／DU 時間、合法 TBS／BD／SFS、PHY 成功與超額規則、跨服務共享與計帳規則。不得讓 AI 提前知道未來 SNR，也不得以較弱資訊限制 Baseline 造成不公平對照。需比較強但同樣低複雜度的替代 heuristic，不能只用刻意脆弱的 baseline；應評估多負載、多 SNR 分布、能量與 Deadline 壓力、隨機種子、信賴區間、敏感度與消融實驗。

## 7. 可追蹤議題樹（依依賴順序）

- [x] **R-01.1–1.10** 服務週期、期限、共享、觀測與首要目標的**設計選擇**完成；[ ] 其實證驗證未完成。
- [x] **R-01.11** 達標後停止為該服務新增排程；允許為其他服務使用共享 Tag。
- [x] **R-01.12** 服務最低需求內認列量作為主要公平性資料。
- [x] **R-01.14a / 14b** Max–Min Gap 主要方向；只比較**同服務** Tag。
- [x] **R-01.14c** 多服務採**最差服務優先 B**。
- [ ] **R-01.13** 同時事件認列、可分割 payload、凍結時點（依賴 1.12）。
- [ ] **R-01.15** Baseline 是否遵守 Primary > Secondary、是否能抗離散 TBS 超額（依賴 1.11–1.14）。
- [ ] **R-01.16** 共享 Tag 是否納入 Baseline 排序（依賴 1.4、1.14）。
- [ ] **R-01.17** 正規化分母、未達標服務公平性及最差服務集合（依賴 1.14c）。
- [x] **R-02.1c** 截止 Slot 是否包含邊界：包含整個最後 Slot，下一 Slot 起點排除（設計決定）；[ ] 原始服務時間需求轉換、能量因果、PHY 時間與實驗可信度仍待驗證（原 R-01.18 義務）。

> **GRILL 暫停點**：使用者明確希望先進入 R-02 模擬器架構；上述 R-01 未決事項**保留，並不等於已通過科學驗證**。只有當 R-02 的模組接口需要某一未決定規則時，才回頭處理對應前置問題。

## 8. 進入 R-02 的交接（非 R-01 正文決策）

- **R-02.1 [DECIDED]**：採用精簡 **Discrete-Event Simulation (DES)**，不採全程固定時間步進；在 `.ipynb` 原型加入 Event Trace，驗證後移至 `.py`。
- **R-02.1a 時間標尺 [DECIDED｜2026-10-19]**：採用 **15 kHz SCS（μ=0）、normal CP 的 1 ms NR slot** 作為排程索引／TDD 資源網格；**DES 內部事件時鐘須細於 1 ms**，允許 Paging、D2R 開始與結束、Guard Time、能量變化等發生於 Slot 內；不可強制取整至 Slot 邊界。這是模擬設計，非聲稱 Ambient IoT 各協定操作均必須 Slot 對齊。具體內部精度已於 R-02.1d 決定使用整數奈秒。
- **R-02.1b 同時間事件處理 [PROVISIONAL]**：採事件佇列，對相同時戳的完成事件先批次結算，再處理 Deadline／窗口狀態與新決策；具體 tie-break、資料認列及邊界規則需另驗證。事件插入序號只能保證執行可重現，不能代替物理因果。
- **R-02.1c Deadline 語意 [DECIDED｜2026-10-19]**：使用者選擇 **Slot-level Deadline，非 Clock Error 模型**。令 `n_last` 為服務最後允許完成的 Slot 索引（從模擬時間原點計，Slot n 為 `[n*T_slot,(n+1)*T_slot)`）；成功 D2R 有效當且僅當 `t_D2R_END < (n_last+1)*T_slot`，且 payload 在其他服務／物理限制下有效。若 `n_last=20`，`20.000 ms`、`20.999 ms` 為有效例，`21.000 ms` 無效。恰於 21 ms 的完成不能因 `D2R_END` 比 `SERVICE_DEADLINE` 先執行就算有效；服務認列資格取決於截止時戳，**不得以事件排序繞過 `<`**。最後 Slot 的終點為**排他**邊界。
  - **必要一致性檢查 [OPEN / TEST]**：原 R-01 模型以嚴格位於週期內的連續時間相對 Deadline 表示需求；轉成 `n_last` 不能無說明地向後放寬最多近 1 ms，也不能使最後 Slot 溢出該服務週期。應在服務生成與實驗設定時明確規定如何從原始期限映射、以及若原始期限非 Slot 對齊如何處理；所有 Baseline／AI 使用同一組轉換後期限。
  - **單元測試 [TEST]**：`n_last=20`，檢查 19.999、20.000、20.999、21.000 ms 四個案例；加入 D2R_END 與截止事件同在 21.000 ms 的案例，確保不因佇列順序而誤認成功。
- **R-02.1d 內部時間表示 [DECIDED｜2026-10-19]**：DES 事件時間、事件佇列排序及截止時間比較一律使用**整數奈秒 (`int ns`)**；`T_slot = 1_000_000 ns`。Notebook 中可將時間轉為 ms/μs 顯示，但不得以顯示後的浮點數回寫事件時鐘。為避免低估占用時間，候選實作規則為「先計算整段物理持續時間、再向上取整至整數 ns」，**此取整規則仍為 [PROVISIONAL]**，待核對 BD 原始精度、Guard Time、長時程誤差與零時長事件後確認。`133.33 μs` 可能為近似參數；納秒精度不表示輸入 PHY 參數無誤差。
- **R-02.1e DU Window／Service Cycle／Event Queue 生命週期 [PROVISIONAL]**：建議 Event Queue 為單次 simulation run 共用的全域佇列；Service Cycle 僅更新本週期需求／統計，Tag 能量與物理時間不得重置；DU Window 開閉為帶明確時間戳記的事件。Window 開始時提供本輪資源與當下觀測，已承諾的 D2R＋Guard 須在該 Window 內完成。不得因 Window 結束而抹除仍有因果影響的事件，也不得讓 Policy 讀取未來才會揭露的 DU/UE 隨機結果。上述為架構候選，尚未獲正式確認。
  - **[DECIDED｜R-02.1e-1]**：選擇預先定義情境參數池，再按 seed 選情境與產生完整 UE/DU 時序，依時間揭露；詳見下項。
  - **[TEST]**：在窗口／週期交界與同時 Deadline 情境驗證沒有跨窗口超時傳輸、沒有跨週期服務資料混算、沒有 Tag 能量憑空重置；Window end 同時 D2R end 必須遵循 Guard 與半開區間規則。
- **R-02.1e-1 UE/DU 情境池與隨機種子 [DECIDED｜2026-10-19]**：使用者正式選擇 **A：事先定義若干 UE UL 負載／時序生成的「情境參數組」**，而非僅從少數固定完整 Trace 隨機抽一條。每次 run 由 seed 選擇情境，並用該情境的生成參數產生**不同、可重現**的完整 UE 占用與 DU Window 時序；執行時僅依時間向排程器揭露可觀測部分。具體情境種類、分布及抽樣權重**尚未決定**，低／中／高／突發負載只是示例。
  - **配對公平性 [TEST]**：Baseline 與 AI 在相同 Scenario ID、Trace ID、環境 seed、服務需求與其他外生條件下比較；實驗報告須按情境分組分析，不能只有隨機混合後的整體平均，或事後篩選有利情境。
  - **生成一致性 [TEST]**：UE UL 占用與 DU Window 應由同一套相容的 TDD／資源時序生成，不可分別隨機抽樣後出現物理不可能的重疊或反因果。
  - **因果隔離 [TEST]**：完整 Trace 僅 Simulator／評估器可讀；Policy Observation 不包含未到達時間的 UE 占用或未知 DU 結果。需明確決定**在某 DU Window 開始決策時，其結束時刻／剩餘長度是否已知**；已知完整當前窗口與偷看未來窗口是不同假設。
  - **隨機性 [TEST]**：Scenario 選擇、環境生成、通道／PHY、Policy 隨機性採獨立 RNG stream 或等效的可重現方案；不能使 Policy RNG 呼叫次數改變 UE/DU 外生 Trace。
  - **實驗設計 [OPEN]**：情境分布與抽樣機率、每情境測試多個 seed、未知情境與敏感度分析、信賴區間；避免少數樣本造成偶然結論。固定 Trace 仍可作 Notebook Debug fixture，但不作唯一正式實驗分布。
- **R-02.1e-2 DU Window 觀測界線 [DECIDED｜2026-10-19]**：使用者選擇 **A：DU Window 開始時，Node 與 Policy 已知「本輪 Window」的完整實際可用長度／結束時刻**，用於檢查 Paging＋D2R＋Guard 是否能在本輪可用資源內完成。這表示該 Window 的資源區間在決策前已確定且不會在本模型中被未預告的 UE UL 中途截斷；屬於**明示的系統建模與可觀測性假設**，**不是 3GPP 強制提供的預知能力**。
  - **資訊邊界 [DECIDED]**：Observation 可包含 `now_ns`、`current_window_end_ns`（或 `remaining_ns`），但不可包含**下一個尚未開始 Window 的長度／結束時間**、未來 UE 占用或未來 SNR；預生成完整 Trace 僅供 Simulator/評估元件管理，Policy 不得直接讀取。
  - **一致性驗證 [TEST]**：同一 Window 的實際可用區間須與預生成 UE／DU Trace 一致；在 `DU_WINDOW_START` 揭露當前結束時刻，在開始之前不揭露；所有方法使用相同 Observation 欄位。若日後加入不可預期中途搶占，需重新開啟本決策並定義取消／失敗行為。
- **R-02.1e-3 UE／DU 時序模組責任 [DECIDED｜2026-10-19]**：使用者選擇 **A：由獨立 `TrafficScenario`／`ResourceTimeline` 負責 UE UL 占用及 DU Window 的外生時序生成與管理**，而非讓 UE 與 Node 各自產生互相矛盾的資源時序。`TrafficScenario` 保有情境參數與環境 seed；`ResourceTimeline` 保有完整時序；`SimulationEngine` 依事件揭露當前合法資源；Node／Policy 不得直接讀完整時序。這是**責任分配**而非強制建立多個 class。後續須測試同 seed 生成重現性、UE/DU 時序無衝突，以及不同 Policy 的 Observation 一致性。
- **R-02.1e-4 Donor→Node CW 功率通知與可觀測邊界 [DECIDED｜2026-10-19]**：使用者選擇 **B：在前一個 DU Window 期間，Node 已收到下一次 CW 發射功率的預告（one-step lookahead）**。Donor 為 Node 指定功率屬**研究建模假設／控制決策**，不宣稱是 3GPP 對所有 IAB 部署的必然保證。
  - **已確認的資訊界線**：當前已發佈的 CW 功率 `P_CW,current` 與**下一次** CW 的預告功率 `P_CW,next` 可供排程器使用；不得直接讀整個未來功率計畫。`P_CW,next` 不代表下一個 DU Window 的起迄時刻、未來 UE 負載或未來瞬時 SNR 已知；R-01.10 理想**當前** CSI 與 R-02.1e-2 **當前** Window 長度已知兩項決策不變。
  - **通知事件候選 [PROVISIONAL]**：Donor 設定功率計畫，`SimulationEngine` 在約定的揭露時點產生 `CW_POWER_ANNOUNCE(target_cw_id, power, effective_interval)`，更新 Node 持有的「已公佈配置」；Policy 從 Node Observation 讀取，**不可查詢完整 `DonorPowerPlan`**。可先假設通知發生於前一個 DU Window 的決策之前，以便 Trace 驗證，但此**精確通知時點尚未定案**。若不存在前一個 Window（首輪），須另設初始化通知事件。
  - **R-02.1e-4-1 [DECIDED｜2026-10-19]**：使用者選擇 **A：每個 DU Window 對應一個由 Donor 指定、在該 Window 的 CW 發射期間保持不變的功率 `P_CW,w`**；單一 DU Window 不容許 CW 功率切換。若連續多個 DU Window 的數值相同，仍分別以 Window ID 管理。前一個 DU Window 期間已預告 `P_CW,w+1`，**但未來 Window 的長度、實際 SNR 仍未知**。單一 Window 的「固定功率」**不蘊含** CW 於整個 Window 連續開啟；CW 發射起迄、Paging／D2R／Guard 交界與 EH 更新是下一個前置問題。
  - **R-02.1e-4-3 [DECIDED｜2026-10-19]**：使用者選擇 **A：Tag 自身進行 D2R 時允許同時 Backscatter 與 Energy Harvesting（EH）**。這是具備分流／等效耦合特性的 Tag 電路建模假設，**不是任何 Tag 天生必備的功能**；不得把同一份入射 RF 功率同時 100% 用於背散射與採能。具體反射／採能功率分配係數及其與 D2R SNR／BER 的耦合仍待參數化與敏感度驗證。
    - **[DECIDED：時間限制]**：UE UL、Paging 階段沒有本 Window 的專用 energizing CW，不能計入其 EH；`CW_ON` 發生後，所有處於 CW 覆蓋且允許 EH 的 Tag（包括正在 D2R 的 Tag）才可能採能。`CW_OFF` 後停止該來源 EH。Donor 預告未來功率只是觀測資訊，不是當前可用能量。
    - **[MODEL：候選能量帳本]**：對有效 CW 區間及 Tag mode，示意 `P_h,k(t) = η_k · (1-β_k) · P_rx,k(t)`（`β_k` 僅表示簡化的 RF 功率分配比例，不能不經校準即視為反射係數幅度）；`dE_k/dt = P_h,k(t) - P_c,k(mode,t)`，並考慮 `E_max,k` 上限及起動／切換的離散能量成本。對不反射的 Tag，可有不同採能模式；不應未經設定直接套同一 `β`。
    - **[TEST：全時刻能量因果]**：D2R 開始、狀態切換及每個功耗／EH 參數改變的時點前，先結算已流逝區間的實際能量；對兩事件間功率常數的區間，可利用端點與 `E=0` 交點檢查 `E_k(t)≥0`，不必設固定微小 time step。僅檢查 D2R 結束時 `E≥0` 不足以判斷中途是否已斷電。起動耗能須在開始時先扣除／驗證，後續 EH 不得倒灌到過去。總儲能上限 `E_max` 必須處理飽和而非允許提前儲存未來能量。
    - **[TEST：時間／資源可行]**：`D2R` 必須完全受 CW 覆蓋，並符合 `t_D2R,end + guard ≤ t_DU,end`；初始能量須先支持 Paging（依已決定的初始保證），及後續必要起動動作。多 Tag 並行時 CW 的供能及 PHY／SFS 可行性仍須獨立檢查；不能由「允許同時 EH」推論並行必然成功。
    - **[DECIDED：R-02.1e-4-4｜2026-10-19]**：採用 **A：Event-Based Energy Update（事件邊界積分／lazy update）**，不以固定頻率 `EH_TICK` 作為常態能量更新。每逢 CW ON/OFF、Tag 模式切換、D2R START/END 或 EH／功耗參數改變時，先結算上一段區間，再檢查啟動成本及新狀態的可行性。若在下一事件前會耗盡能量，須預先否決不可行排程或安排能量耗盡事件；不得只看終點能量。具體公式與最小驗證案例見第 10 節。
  - **R-02.1e-4-6 [DECIDED｜2026-10-19]**：同一 DU Window 可以有多批 Paging；每批在 `GUARD_END` 並結算前批傳輸成功／失敗、服務認列、Tag 能量與資源後，若仍可容納下一批完整 Paging、CW+D2R 與 Guard，**重新呼叫 Baseline／AI Policy**，不在 Window 開始時一次固定所有批次。見第 12 節。
  - **R-02.1e-4-5 [DECIDED｜2026-10-19]**：選擇 A：**每批最後一個 Tag 的 D2R 結束時立即 `CW_OFF`，Guard 期間不發射此 energizing CW，也不從此 CW 採能**。同一 DU Window 若時間足夠，可在該批 Guard 結束後再執行下一次 Paging（多批次）；各批共用同一 Window 的 Donor 指定 CW 功率。詳見第 11 節。
  - **R-02.1e-4-2 [DECIDED｜2026-10-19]**：使用者選擇 B，並明確補充「CW 就在 CW／D2R 端發射即可」；保留 `system_model.pdf` p.10 的階段安排：UE UL → Paging → CW+D2R。**不在 UE UL 或 Paging 階段啟動 A-IoT energizing CW**；CW 自 D2R 階段開始，於該階段連續發射，每個 DU Window 的 CW 發射功率由 Donor 指定且保持固定。CW 不等於 UE 的 NR 下行波形；UE 並不需要透過此專用 energizing CW 進行一般 NR 通訊。CW 停止與 Guard 的關係已於 R-02.1e-4-5 決定（Guard 期間 CW OFF）；不同 Tag 的 D2R 起訖／重疊安排仍為 [OPEN]，不得在未決定前假設整個 DU Window 都有 CW。
  - **能量因果 [DECIDED 的原則／TEST 的義務]**：預告功率是排程資訊，不是已採集能量。Tag 的實際儲能僅按**已經經過、且實際 CW 正在發射**的時間區間與所建模的接收功率／效率更新；例如 `E_k(t) = clip(E_k(t0) + ∫_{t0}^t P_EH,k(τ)·1_CW_on(τ)dτ − E_use,k([t0,t]), 0, E_max,k)` 為候選能量帳本形式，須補定 EH 函式、功耗與容量。未來預告可支援規劃，但不得在當前時刻提前增加 `E_k`、假定未來充電已完成，或預支尚未採集的能量。
  - **Action 邊界 [DECIDED／OPEN]**：Donor 指定的 `P_CW` 是 Node 排程的外生限制，**本階段不讓 Baseline／AI 自行任意調整 CW 功率**；Policy 可選擇 Tag、合法 TBS 等既有動作。是否允許基於預告功率而將 Tag 延到下一次 CW 排程，尚取決於下一次時窗的未知時間、服務期限與安全可行性，不能直接視為已確保可行。
  - **最小測試 [TEST]**：(1) 同一環境 Trace/seed 的 Baseline 與 AI 收到一致的功率預告；(2) 宣告前後 Observation 有且只有被允許的資訊變化；(3) 即使預告下一次高功率，若目前無實際 CW 發射則 Tag 能量不得增加；(4) 功率切換時 EH/SNR 影響以實際發射時間為準；(5) 下一窗口長度與未來 CSI 保持不可讀；(6) 首次 CW 的功率通知初始化、變更／撤回的處理需有可重現規則。
- **R-02.2+ [OPEN]**：Node/UE/Tag/Channel 邊界、事件優先級、Observation–Action、Trace／測試與 Policy 介面；尚未進入實作。

## 9. 原始材料索引

| 材料 | 相關頁面 | 用途 |
|---|---|---|
| `system_model.pdf` | p.3–4 | 農場 IAB／Tag 場景與拓樸示意 |
| `system_model.pdf` | p.7 | 服務最低資料、Deadline 與指定 Tag 集合 |
| `system_model.pdf` | p.8 | `x_k`、完整 TBS、需求缺口、Tag 能量等變數 |
| `system_model.pdf` | p.9 | 舊版 `W[ℓ]` 上的 Max–Min 目標（已指出退化問題） |
| `system_model.pdf` | p.10–11 | DU 與 D2R 時間示意及原始限制式；仍須獨立驗證 |
| `Baseline.pdf` | p.1–3 | 手寫 Baseline 排程步驟（本文件為邏輯重建） |
| `模擬器設計.pdf` | p.1–2 | 早期模擬器模組／MVC 設計草案，於 R-02 再審查 |
| 3GPP TS 38.211 | §4.2、§4.3.2 | 15 kHz SCS 的 numerology 與 slot 時間；非 Ambient IoT 完整時序驗證 |

---

**交接摘要**：R-01 的需求、共享、停止排程、公平性「服務內 Max–Min／多服務最差優先」均已有方向；但計帳與 Baseline 排序仍有明確待驗證義務。R-02 已選精簡 DES。**R-02.1a 已確認允許 Slot 內更細事件時間；R-02.1c 已確認最後允許完成的 Slot 包含整個 Slot（下一 Slot 起點排除）**。**R-02.1d 已確認以整數奈秒作為內部事件時鐘**。**R-02.1e-1 已決定「情境參數池＋seed 產生完整 Trace」**；**R-02.1e-2 已選擇本 DU Window 開始時可知其實際結束時刻（未來 Window 仍不可知）**；**R-02.1e-3 已確認獨立 `ResourceTimeline`／`TrafficScenario` 管理 UE／DU 外生時序**；**R-02.1e-4 已決定前一個 DU Window 期間可預告下一次 CW 功率（one-step lookahead）；R-02.1e-4-1 已確認每個 DU Window 對應一個固定 CW 功率，且該 Window 內不切換功率；CW 已決定僅在 D2R 階段發射；每批最後 D2R 結束即停止 CW，精確功率通知時點仍待決定**。**R-02.1e-4-3 已決定允許 Tag 在自身 D2R 期間同時採能與反射，但其 RF 分流與 EH 效率需驗證**。未來 CW 發射功率可知不代表未來即時 SNR 可知。**R-02.1e-4-4 已確認以事件邊界結算 Tag 能量，須檢查中途耗盡與初始啟動成本**。**R-02.1e-4-5 已確認每批最後 D2R 結束即 CW_OFF，Guard 無此 CW 採能；R-02.1e-4-6 已確認每批 GUARD_END 後可在資源可行時重新呼叫 Policy**。時間取整精確性仍待測試。實作方式維持 `.ipynb` Trace 驗證後再轉為 `.py`。

### R-02.1e-4-2｜CW 僅於 D2R 階段發射（2026-10-19）[DECIDED]

- **使用者決策**：明確選擇 B，並補充「CW 就在 CW／D2R 端發射即可」。保留 `system_model.pdf` 第 10 頁示意中的先後：**UE UL → Paging → CW ON + Tag D2R**。UE UL 與 Paging 時段不發射 A-IoT energizing CW。CW 在 D2R 階段連續提供激勵，功率為 Donor 給該 DU Window 指定的固定值。
- **實體層概念**：給 Tag 的 energizing CW 與一般 NR 下行 OFDM 訊號不同；不能再引用「UE 需要同一條 CW」作為設計理由。選 B 降低了 CW 與 UE UL 併行的額外 TX/RX 假設，但**不代表 D2R 期間的 CW 自干擾、頻譜／接收相容性自動通過 PHY 驗證**；原先理想 CW 隔離仍須明列為假設。
- **時間與資訊邊界**：`CW_ON` 必須不早於 D2R 階段起點；D2R 期間必須有 CW 覆蓋；已知下一次 Donor 功率仍不等於已知未來 SNR。`Paging` 所需 Tag 喚醒／回覆的能量應由之前已儲存的能量或先前已定義的初始電池支持，不得在 Paging 階段虛構本 Window 的 CW 採能。
- **能量因果 [TEST]**：在 UE UL／Paging 階段，若沒有其他明確定義的採能來源，應有 `P_EH,CW=0`；從真正 `CW_ON` 事件起才可按已流逝時間積分 EH，並同時記錄接收機／反射／電路耗能。**Tag 自身於 D2R 反射時可同時採能 [DECIDED R-02.1e-4-3]；採能比例、電路功耗與有效反射耦合仍待定案**，需確認功率分配／電路假設；其他被 CW 覆蓋且具 EH 能力的 Tag 是否採能亦需由一致模型決定。
- **DU Window 可行性 [TEST]**：滿足 UE UL → Paging → CW+D2R 的資源先後、D2R 位於 CW ON 內、`t_D2R_end + T_guard <= t_DU_end`，所有時刻 `0 <= E_k(t) <= E_max,k` 且不能預支未來能量。特別測試：Tag 在 Paging 結束時能量不足、但在 D2R 開始後可能採到能量時，能否執行須依時間逐段驗證，不能只檢查 D2R 結束時的淨能量。
- **[DECIDED：R-02.1e-4-3]**：允許 Tag 在自己的 D2R 期間同時 Backscatter 與 EH；**[DECIDED：R-02.1e-4-4]**：選用事件邊界積分（Event-Based Energy Update），詳見第 10 節。採能／反射分流參數、CW_OFF 與 Guard 已於 R-02.1e-4-5 決定；並行 Tag 共用 CW 的細節保留待驗證。

**交接狀態**：R-02.1e-4-2 已關閉為「B：CW 僅在 D2R 階段發射」。不得將先前僅提出的 A 全窗連續 CW 當作已採用系統模型，也不得認定 CW 在 UE UL／Paging 期間採能。


## 10. R-02.1e-4-4｜Tag 能量更新機制（2026-10-19）[DECIDED]

**使用者正式選擇 A：Event-Based Energy Update（事件驅動能量更新）。** 這是模擬器架構決策，並非對特定 Tag EH 電路的實證。**暫不實作程式**。

### 10.1 模型與事件處理

- **時間基準**：DES 事件時間仍使用已決定的整數 ns；能量／功率使用有單位的一致數值計算，Trace 可顯示 ms、μJ、mW。
- **需結算的事件**：`CW_ON`、`CW_OFF`、`D2R_START`、`D2R_END`、Tag 電路模式切換，以及接收 RF／EH／功耗參數發生改變的事件。其他 Tag 若在 CW 覆蓋內，即使未被排程 D2R，也需累積 EH。
- **結算順序**：在事件時間 `t`，先用 `[last_update_k,t)` 內**實際存在**的 CW、Tag 工作模式與功率參數結算能量；接著檢查與扣除當下離散啟動／切換成本；最後更新模式及 `last_update_k=t`，供下一段使用。事件同時發生時，應進行一次一致的時點結算，不能重複累計同一區間。
- **分段常數模型**：若區間內 `P_EH,k` 與 `P_consume,k` 為常數，`ΔE_k=(P_EH,k−P_consume,k)·Δt`，配合 `E_max,k` 容量上限與任一時刻能量非負限制。若區間內功率改變，必須另立事件切段，不能錯用固定功率解析式。
- **能量因果**：必須能支付當下啟動成本且整個預定傳輸期間維持 `E_k(t)≥0`。若淨耗電為常數且為負，應檢查耗盡時刻 `t_deplete=t_start+E_start/(P_consume−P_EH)`；若早於預定 D2R 結束，應在排程前否決，或依明確失敗規則觸發 `ENERGY_DEPLETED`。**不能用未來 CW 採能支付當下 Paging／電路啟動，也不能只檢查 D2R_END 能量。**
- **邊界限制**：只在 `CW_ON` 至 `CW_OFF` 期間計入本系統的 energizing CW EH；UE UL 與 Paging 階段沒有該 CW。Tag 自身 D2R 中同時 EH 為已決定的能力假設，但 EH／反射 RF 功率分配、D2R SNR 耦合及 Guard 是否有 CW 仍屬待驗證／待決事項。

### 10.2 Notebook Trace 教學案例（[ILLUSTRATIVE]，非 3GPP 參數）

假設某 DU Window 中 CW 在 **3–7 ms** 開啟；Tag A 在 **3–6 ms** 進行 D2R；Tag B 未 D2R 但受到 CW 覆蓋。**注意：這是 R-02.1e-4-5 決定前的能量算術教學案例，CW 在 6–7 ms 空轉與新決策不一致，不可直接作為目前正式事件 Trace。若無其他 Tag 在 6–7 ms 進行 D2R，正式模型必須於 6 ms `CW_OFF`，並將該段改為 Guard 或其他合法活動，該段不計 CW EH。**初始 `E_A=3 μJ`、`E_B=2 μJ`，CW ON 時兩者 `P_EH=0.6 mW`；A 的 D2R 電路功耗 `1.0 mW` 並在啟動時支付 `1 μJ`，兩者的 Idle 功耗皆 `0.1 mW`。假設容量足夠，其他階段能耗略去。

| 時間 | 事件／結算 | Tag A (`μJ`) | Tag B (`μJ`) |
|---|---|---:|---:|
| 3 ms | `CW_ON`、A `D2R_START` 扣除啟動 1 μJ | 2.0 | 2.0 |
| 6 ms | `D2R_END`；A `(0.6−1.0)×3=−1.2 μJ`；B `(0.6−0.1)×3=+1.5 μJ` | 0.8 | 3.5 |
| 7 ms | `CW_OFF`；兩者 Idle 採能淨額 `(0.6−0.1)×1=+0.5 μJ` | 1.3 | 4.0 |

單位換算：`1 mW × 1 ms = 1 μJ`。此例只需結算事件邊界，**但不能因此略去事件間的可行性檢查**。

**反例 [TEST]**：Tag C 在 D2R 起點有 `1.5 μJ`，啟動成本 `1 μJ`，剩 `0.5 μJ`；`P_EH=0.6 mW`、`P_consume=1.0 mW`，淨耗電 `0.4 mW`，因此 `T_available=0.5/0.4=1.25 ms`，不足以支撐預定 `3 ms` D2R。模擬器必須拒絕該配置或依事先定義的耗盡事件處理，不能讓 Tag 傳輸至 3 ms 再以負能量結算。

### 10.3 最小測試與未決依賴

- [ ] **TEST-EH-01**：事件邊界的分段積分與一個小時間步參考解（在相同分段常數條件下）一致，且對事件插入順序不敏感。
- [ ] **TEST-EH-02**：同時間 `CW_ON`、`D2R_START` 等事件只結算一次舊區間；啟動成本只扣一次。
- [ ] **TEST-EH-03**：非排程 Tag 在 CW ON 時正確採能；在 UE UL、Paging 及 CW OFF 時不從該 CW 採能。
- [ ] **TEST-EH-04**：啟動能量不足與中途耗盡均被阻止或按明定失敗事件處理；整段歷程 `0≤E≤E_max`。
- [ ] **TEST-EH-05**：跨 DU Window／Service Cycle 保留 Tag 物理儲能，不因服務統計重置而重設電池。
- [ ] **OPEN**：CW_OFF 與 Guard 時序、並行 Tag D2R／EH 的分流細節、PHY/SNR 耦合、容量飽和與能耗參數來源。

**狀態**：R-02.1e-4-4 的架構選擇已關閉；以上測試與物理參數的科學有效性**尚未完成驗證**。下一輪可處理 CW_OFF／Guard 的事件與資源關係，不應把候選細節當成已定案。


## 11. R-02.1e-4-5｜同一 DU Window 多批 Paging、CW_OFF 與 Guard（2026-10-19）[DECIDED]

### 11.1 使用者決策、理由與適用範圍

- **[DECIDED] 選擇 A**：每一批（batch）最後完成 D2R 的 Tag 結束時，立即 `CW_OFF`。**Guard Time 期間專用 energizing CW 為 OFF，不累積此 CW 的 EH**。`CW_OFF` 是按批次而非整個 DU Window 只發生一次。
- **[DECIDED] 同一 DU Window 可多次 Paging**：如果剩餘 DU 資源與時間足夠，可有 `Paging_1 → CW_ON/D2R_1 → CW_OFF → Guard_1 → Paging_2 → CW_ON/D2R_2 → CW_OFF → Guard_2 → …`。Guard 有防止相鄰批次時序過度緊貼的功能；**不得只預留 Window 末端的一次 Guard 而忽略批次間 Guard**。
- **[MODEL]**：每個 DU Window 對應一個 Donor 指定的固定 CW 功率；即使該 Window 有多個 CW ON/OFF 區間，**功率值仍相同**。UE UL／Paging 期間 CW OFF；D2R 必須有 CW 覆蓋。是否有同批多 Tag 部分重疊，須另依 SFS 與 PHY 可行性檢查，不因批次化而自動合法。
- **[NOT NORMATIVE]**：這是研究模型的時間／資源設計，未經獨立規範核對，不宣稱 3GPP 必然採用此 CW／Guard 配置。

### 11.2 最小時序與可行性不變量

對 Window `w=[s_w,e_w)`，同一批 `b` 設 Paging 區間、CW ON 起點 `c_b`、各 Tag D2R 末端 `f_{k,b}`，令 `f_b=max_k f_{k,b}`：

- `Paging_b` 結束在 `c_b` 前或當下，`CW_ON_b=c_b`，該批所有 D2R 皆被 CW 覆蓋。
- **[DECIDED]** `CW_OFF_b=f_b`；`Guard_b=[f_b,f_b+T_guard)`，期間沒有此專用 CW EH。
- **[CONSTRAINT]** `f_b+T_guard <= e_w`；若還有下一批，`Paging_{b+1}.start >= f_b+T_guard`。不得讓下一批 Paging 與上一批 Guard 重疊（首版保守設計）。
- **[CONSTRAINT]** 啟動下一批前，必須確認新 Paging、必要控制訊令、後續 D2R 及新一批 Guard 能在 Window 結束前完成；不能僅憑「Paging 放得下」就開始新批次。
- **[INVARIANT]** Service Cycle 的有效資料量可跨批／跨 DU Window 累積；Tag 能量持續跨批／跨週期保留。批次成功 D2R 仍按接收完成時戳與已決定的 Slot-level Deadline 檢查。

### 11.3 DES 事件與能量更新（供 Notebook Trace 驗證）

候選事件節點為 `PAGING_END_b → CW_ON_b / D2R_START → D2R_END_k（可能多 Tag）→ CW_OFF_b → GUARD_END_b → （可行時）SCHEDULING/PAGING_{b+1}`。這**不是完整協定訊令規範**，只表示模擬器責任與事件因果。

- 同時刻多個 `D2R_END` 要先以一致的批次結算方式處理資料與能量，再關閉 CW；不能依 heap 插入順序任意改變每個服務的公平性認列。
- 能量採用已決定的 Event-Based Update：各批 CW ON 時段積分 EH，`CW_OFF` 後的 Guard 不積分此 CW 的 EH；Tag 的基礎 Idle 耗能仍按其模式及經過時間計算。
- **[TEST-SEQ-01]** Window 內有足夠時間時可完成兩批 Paging＋D2R＋Guard；第二批開始時間不可早於第一批 `GUARD_END`。
- **[TEST-SEQ-02]** Window 剩餘時間不足以同時容納下一批的 Paging、D2R 和 Guard 時，拒絕該批且不能出現超過 `e_w` 的 D2R。
- **[TEST-SEQ-03]** 第一批最後 D2R 結束後 CW 立即關閉；Guard 全段 CW EH 為 0；下一批 CW_ON 才重新採能。非排程 Tag 亦遵循相同規則。
- **[TEST-SEQ-04]** 多個 D2R 同時結束時，`CW_OFF` 一次、資料批次結算一次，與事件插入順序無關。

### 11.4 下一個必要架構選擇 [OPEN｜R-02.1e-4-6]

**Window 內的第二次及後續 Paging 應在何時重新呼叫 Policy？** 候選：(A) 每批 `GUARD_END` 後，若資源足夠就以最新 Observation 再做決策；(B) 在 Window 開始時一次規劃全部批次，再由 DES 依序執行。兩者的資訊可見性、失敗後重排與比較公平性不同。**尚未替使用者定案**，下一輪 GRILL 只針對此項選擇。


## 12. R-02.1e-4-6｜每批 Guard 結束後重新決策（2026-10-19）[DECIDED]

- **決定**：在同一 DU Window 內，完成一批 D2R（所有已承諾的 Tag 傳輸結束）與 `CW_OFF` 後，保留完整 Guard。當 `GUARD_END` 發生，先完成該時點的能量／資料／資源結算，**再重新產生當下 Observation 並呼叫 Policy**，選擇下一批 Tag、TBS 等動作；不得於 Window 起始時一次決定所有後續批次。若沒有足夠剩餘資源，停止該 Window 的新 Paging。
- **事件順序／時序不變量**：`PAGING_b → CW_ON_b → D2R_{k,b} → (最後 D2R_END) → CW_OFF_b → Guard_b → GUARD_END_b → SCHEDULING_(b+1)`。只有符合下一批完整 Paging＋D2R＋Guard 可行性的動作才可承諾；`CW_OFF` 不必等 Window 結束。`GUARD_END` 不是保證一定再排程，僅是**允許重新考慮**的事件。
- **資料因果**：下一批 Observation 必須反映已發生 D2R 的成功／失敗、需求缺口、Tag 能量與本 Window 剩餘時間，不讀未來未揭露的 SNR／UE Trace。前批若無成功 Tag，也不能無故更新成功資料。跨服務認列及同時完成批次計帳仍屬 R-01 待驗證項目。
- **CW 功率**：本 Window 每批都採 Donor 指定的**同一功率值**；前一 Window 預告的是下一 Window 功率，不能誤解為下一個 Paging 批次可改功率。
- **多 Tag 同批**：若 Tag D2R 結束時刻不同，最後一個合法 D2R 結束才 `CW_OFF`；即使有 Tag 提早結束，它在其他 Tag 持續 CW 期間是否 EH，由自身模式／EH 條件決定。
- **比較公平性**：Baseline 與 AI 的決策觸發條件相同；環境／服務 Trace、Observation 欄位和動作合法性檢查相同，不保證兩個 Policy 將出現相同數目的批次，因為它們可能選不同的傳輸時間。
- **可重現測試（尚未執行）**：
  - [ ] `TEST-BATCH-01`：Window 夠長時同一 Window 能依序執行至少兩批；第二批決策恰在首批 `GUARD_END` 後，使用新狀態。
  - [ ] `TEST-BATCH-02`：剩餘時間不足下一完整批時不再 Paging，沒有超出 Window 的傳輸／Guard。
  - [ ] `TEST-BATCH-03`：前批成功、失敗、能量改變均正確影響下一批 Observation。
  - [ ] `TEST-BATCH-04`：相同時間多 Tag 完成先一致結算，再觸發一次 `CW_OFF` 與一次後續決策，不因事件佇列插入順序產生差異。
  - [ ] `TEST-BATCH-05`：單一 DU Window 內多批使用相同 Donor CW 功率，批次間 Guard 的此 CW EH 為 0。

### 12.1 下一階段：Node／Tag／Channel 最小模組責任（候選，未定案）

- **Node／Reader（系統實體／排程協調）**：持有已揭露的本輪 Window 資源與 Donor 功率配置，組合合法 Observation，提交 Policy 建議並承接執行結果；不直接更改 Simulator 的真實通道或憑空更新 Tag 電量。
- **Tag（物理個體狀態）**：Tag ID、電池容量與真實儲能、工作模式、上次能量結算時刻及必要的能耗／反射參數；負責提供可結算的狀態，**不應把每服務的認列量混入電池狀態**。
- **Channel／PHY（鏈路計算）**：依 Node 功率、Tag 位置／通道、噪聲／干擾及反射配置，產生當下 SNR 與傳輸成功模型所需參數；分開處理 Simulator 真實通道與 Policy 可觀測 CSI（目前理想**當前** CSI）。
- **SimulationEngine（事件與狀態提交）**：唯一驅動時間、事件佇列與合法的狀態轉移；處理 CW、Paging、D2R、Guard 與能量事件；不選擇研究 Policy。
- **ResourceTimeline（外生環境時序）**：保存完整 UE／DU Trace，但只依決策時點揭露本輪允許的資源資訊。
- **ServiceManager（服務計量）**：保有服務需求、Deadline、認列資料／完成狀態，與 Tag 物理儲能分離；跨服務共享細節保留 R-01 未決事項。
- **Policy（可替換決策）**：以同一格式 Observation 產生 Tag、TBS 等建議，由 Engine／Validator 檢查可行性；不能直接讀 Tag 真實隱藏量或未來資源 Trace。

**下個最重要的前置問題 [OPEN / R-02.2a]**：Node 在決策時可否取得所有候選 Tag 的**精確當前儲能**？過去已決定理想當前 CSI，但這不自動表示 Node 也知道每個 Tag 的真實電池能量。該資訊邊界會影響 Observation、Tag/Node 責任分工與公平比較，須先確認；目前未替使用者選擇。

**狀態**：R-02.1e-4-6 的設計已定案；其時間、能量、協定與可重現測試**尚未執行**。暫不實作模擬器。

## 13. R-02.2a｜Paging 後由 Tag 回報 1-bit 能量狀態（2026-10-19）[PROPOSED / OPEN]

- **使用者提議（尚未選定完整機制）**：Tag 在 Paging 完成後，回傳自身能量狀態的 1 bit，作為 Node 排程可觀測資訊；這**不等於精確電量回報**。保留 R-02.2a 原本精確能量／估計能量選擇為待修正，不得擅自標記精確電量可觀測。
- **位元語意候選**：`b_k(t)=1[E_k(t)>=E_th]`。`E_th` 需定義；單一固定門檻對不同 TBS、BD、耗能及當時 CW EH 不一定足夠，須測試 false feasible / false infeasible。可另考慮多位元量化，但目前不預設。
- **標準查核**：TS 38.391 Rel-19 §5.3.2、§5.4.2 的 CFA 由 Paging 提供資源並直接啟動 D2R；TS 38.300 §16.23.5.3 亦描述 CFA 直接利用 Paging 指定資源傳 D2R 資料。尚無證據顯示標準 CFA 本身具備獨立的 1-bit 電池回報欄位；若新增，此為研究模型／協定擴充假設，必須交代負載與時序成本，不能宣稱規範既有功能。
- **候選 A（較小修改、尚待選擇）**：1-bit 狀態封入已排程的 D2R 資料中；Tag 在 Paging 後取樣能量，於 D2R 成功完成後 Node 才得知，**僅供下一批／下一決策使用**，且須將回報佔用計入 TBS／payload/overhead，D2R 失敗不能憑空更新報告。CW 維持僅於 D2R ON。
- **候選 B（另增交握、尚待選擇）**：Paging 後新增先行能量回報 D2R 與後續 TBS 重配置程序，使回報可用於當批的主要資料傳輸配置；需額外 CW 時間、回報資源、能量耗用與可行性檢查，並明確標註為既有 CFA 以外的研究擴充。
- **核心因果規則**：在 `t_report_received` 前，Policy 不可使用該報告；Simulator 的真實 `E_k(t)` 僅供真實狀態演進與可行性驗證，不得直接混入 Observation。1-bit 回報的取樣時點與到達時點應分開，避免用過時資訊假裝精確即時狀態。
- **[TEST／未執行]**：第一次 Paging 尚無電量回報時如何選 Tag／TBS；報告遺失或傳輸失敗；離散 TBS 是否足夠承載報告；回報後到下批的 EH/耗能改變；Node 能量判斷與真實能量不一致；公平比較下兩種 Policy 是否拿到相同的回報資訊與開銷。
- **下一個單一決策問題 [OPEN]**：1 bit 應附在既有 D2R 資料內，只能供後續批次使用（候選 A），或需新增 Paging 與主要 D2R 之間的獨立回報步驟以影響本批 TBS（候選 B）？



## 14. R-02.2a｜理想精確能量追蹤取代 1-bit 回報（2026-10-19）[DECIDED / ASSUMPTIONS OPEN]

- **[DECIDED / 使用者修訂]**：撤回第 13 節「Paging 後 1-bit 能量回報」作為首版方案，不增加能量回報、回報位元負載或額外交握；第 13 節保留為歷史候選，不再視為待採用方案。
- **[DECIDED / 初始化]**：模擬 Run 起點令所有 Tag 的初始儲能為各自電池容量 `E_k(t0)=E_k,max`；之後依已決定的 Event-Based Energy Update 及能量因果性遞迴更新。**Service Cycle 更新只重置服務統計，絕對不得將 Tag 重新充滿電**。在第一輪 Paging 前如有已經過的 Idle/UE UL 時間及功耗，仍必須先結算，不能把「初始滿電」誤讀成「Paging 當下無條件滿電」。
- **[DECIDED / Observation 假設]**：首版採 *Perfect Energy State Tracking*，Node 的 `Ehat_k(t)` 理想上等於 Simulator 的真實 `E_k(t)`；這是一個理想資訊可得性／完美模型假設，**不是規範宣稱，也不是部署可實現性證明**。Simulator 真值與 Node 的估計應在概念與介面上區分，即使首版數值相等；Policy 不可讀取未揭露的未來環境資訊。
- **[MODEL / 必要條件]**：精確性只在能耗、EH 轉換、CW ON/OFF、實際採能 RF 功率、Tag 模式、起始能量與所有歷史事件可正確推得的前提下成立；若其中含未知隨機量、未觀測干擾／通道、測量或回報誤差，不能直接主張 `Ehat=E`。該前提須在後續 Channel/Tag 模組驗證。
- **[INVARIANT]**：每次模式／CW 事件結算 `E_k(t2)=clip(E_k(t1)+∫(P_EH,k−P_consume,k)dt−E_start,k,0,E_k,max)`，但 `clip` 只處理容量上限；能量因果性須**事前**判定，不能把負能量裁成零後假裝 D2R 成功。所有 Tag（包含未被 Paging 者）都必須依 CW 與模式演進；CW 僅在 D2R 階段，Guard/Paging/UE UL 沒有該 energizing CW 的 EH。
- **[TEST / 尚未執行]**：① 初始化滿電，經 Idle/UE UL/首批 Paging 扣耗後確認第一批可用儲能；② 多次 Paging、D2R、CW 間隔使 Node Ehat 與真值對齊；③ 非排程 Tag CW 採能與容量飽和；④ 跨 Service Cycle 不重設電池；⑤ 僅切換 Policy 不改變同一物理事件的能量結算；⑥ 突破能量不足時必須禁止傳輸或產生明確失敗事件。
- **[RESOLVED by R-02.2b]**：使用者已選擇理想精確採能資訊；完整決策及限制見第 15 節。


## 15. R-02.2b｜理想精確採能資訊與最小 Node／Tag／Channel 介面（2026-10-19）[DECIDED / INTERFACE PROVISIONAL]

### 15.1 使用者確認的決策

- **[DECIDED] 選擇 A：Perfect EH Information**。Node 在當下可取得每個候選 Tag 的實際 EH 入射功率（或足以計算採能功率的等效資訊）、能量轉換參數及電路能耗模型，因此首版可依事件歷史精確遞迴其剩餘能量：`Ehat_k(t) = E_k(t)`。
- **[DECIDED] 不增加獨立的能量回報機制**；模擬 Run 起始 `E_k(t0)=E_k,max`，服務週期切換只重置服務計量，不重置電池。這些決策與 R-02.2a 一致。
- **[ASSUMPTION]** 精確追蹤等式是理想資訊／完美模型假設，需已知每段實際 CW、模式、EH/耗能等條件；**不是**從「知道 Donor CW 功率」自動導出，也不是 3GPP 對能源資訊的規範保證。暫不證實真實硬體能達到。
- **[INVARIANT]** 未來 CW 功率預告可用於規劃，不能提前列入目前電池能量；Channel 未來未揭露的通道／SNR 不得進入 Policy 的 Observation。傳輸必須在開始前通過啟動能量及整段能量因果性檢查。

### 15.2 首版最小資料責任（建議介面，尚未變成程式設計定稿）

| 邊界 | 必要狀態或輸入 | 輸出／責任 | 不應處理的事 |
|---|---|---|---|
| `Tag`（真實物理狀態） | `tag_id`, `E_max`, `E_now`, `last_energy_update_ns`, `mode`, 消耗／採能／反射參數 | 保存並提供某一時間點的電池與工作模式狀態 | 不保管跨服務認列資料；不直接控制排程決策 |
| `Channel/PHY`（環境真值與計算） | 當前 CW 功率、Tag 幾何／通道、接收模型、噪聲及反射參數 | 當前 `SNR_k`、實際入射 RF／EH 功率或等效 EH rate、D2R 成功機率／結果的物理計算 | 不擅自修改電池或服務計量；不提供未來 SNR |
| `Node`（資訊整合） | 當前 Window 範圍、Donor 已預告 CW 功率、當前 Tag `SNR_k`、理想 `Ehat_k`、活躍服務與缺口 | 組成 Policy 可見的 `Observation`；發送 Policy 建議供合法性檢查 | 不直接讀未揭露的完整未來 Trace；不自行篡改真實能量 |
| `SimulationEngine`（唯一事件提交者） | Event Queue、資源有效性、Tag/Channel/Service 狀態 | 在事件邊界先結算能量、套用動作、提交 D2R 結果，再建構最新 Observation | 不自行選擇 Baseline／AI 排程策略 |
| `ServiceManager`（服務計量） | 各週期要求、Deadline、服務內 Tag 認列量 | 完成狀態、服務缺口、跨服務認列 | 不持有 Tag 電池真值 |

- `Observation` **候選必要欄位**：`now_ns`, `window_end_ns`, `cw_power_current`, `cw_power_next_announced`（若已通知）, 候選 `tag_id`, 當下 `SNR`, `Ehat`, 活躍服務需求／Deadline／各 Tag 認列量。欄位名稱非 API 定稿。
- `Action` **候選必要欄位**：本批 Tag 集合、各 Tag 的合法 TBS／BD／SFS（僅納入本模型允許決策的欄位）。Donor CW 功率不是 Policy 可任意改動的 Action。
- **[FAIR COMPARISON]** 同一 Trace、相同決策時刻的 Baseline／AI 對所有共同欄位須有相同可觀測性及合法動作限制；不將 Simulator 的真值物件引用直接傳入 Policy。

### 15.3 待驗證與下個單一架構問題

- [ ] **TEST-OBS-01**：在同一事件歷史、固定通道及 EH/耗能模型下，`Ehat=E_true`；非排程 Tag 在 CW ON 期間亦正確更新。
- [ ] **TEST-OBS-02**：Cycle 切換不使能量重設；尚未發生之 CW 或 D2R 不會增加目前能量。
- [ ] **TEST-OBS-03**：Policy Observation 不暴露下一個 Window 長度／未來即時 SNR；Donor 已公告的下一 Window CW 功率除外。
- [ ] **TEST-OBS-04**：Energy Check 對啟動不足或區間中途耗盡拒絕／產生明確失敗事件；不將負能量裁成零再認定傳輸成功。
- [ ] **TEST-OBS-05**：相同事件輸入且使用相同物理模型時，Baseline 與 AI 的物理狀態轉移和合法性驗證完全相同。
- **[OPEN / R-02.2c]**：既然同一 DU Window 可經多個 Paging 批次，**Channel 的瞬時 SNR 在同一 Window 內是否固定（Window-level block fading），還是每批重新抽樣／更新（Batch-level fading）？** 必須保持與已確認的「每次合法決策取得當前 CSI、不得預知未來 CSI」一致；目前尚未決定。

**實作狀態**：僅更新架構決策紀錄；未撰寫或修改任何模擬器程式。

## 16. R-02.2c 與下次 GRILL 議程（2026-10-19）

### 16.1 本次新確認決策

- **[DECIDED / R-02.2c]**：選擇 **A — Window-Level Block Fading**。各 Tag 的通道／瞬時 SNR 在**同一 DU Window 的所有 Paging 批次**保持固定；進入下一個 DU Window 才更新。已確認「同窗內不變」，不代表不同 Window 之間必然獨立；跨窗時間相關性與分布仍須以明確模型定義。
- **[INVARIANT]**：Node 在每個合法排程決策點可取得本 Window 的理想當前 CSI；不提供下一個 Window 的未來 SNR。Donor 設定的 CW 功率在同一 Window 內固定，且上一個 Window 即預告下一 Window 的功率。
- **[DISTINCTION]**：通道／SNR 固定不代表不同 TBS、BD、SFS 的成功機率相同；PHY 成功模型仍應以配置參數計算。是否將有效接收 SNR 直接等同於原始通道 SNR，需在 PHY 介面明確界定。
- **[SCOPE]**：此項為首版模擬簡化假設，不是所有 Ambient IoT 場景的通道實證結論；需保留跨 Window 衰落及敏感度測試義務。

### 16.2 下次討論順序（依前置依賴排列）

1. **R-02.2d — Observation / Action 契約 [MUST DECIDE]**：以單一 Paging 批次為決策單位，明確列出 `now_ns`、本 Window 結束時刻、當前／已預告 CW 功率、Tag 當前 SNR／理想能量、服務缺口／期限、現有認列量；Action 至少定義 Tag 集合與 TBS，並區分是否需由 Policy 選 BD／SFS／啟動時間。釐清 Policy 是提供 Batch 配置，而非直接操作真實狀態。
2. **R-02.3 — Event & Validator 最小規則 [MUST DECIDE]**：把已選的每批 `Paging → CW_ON/D2R → CW_OFF → Guard → 再決策` 實作責任落到事件引擎；同時事件批次結算、非法動作的拒絕行為、無可行批次時退出 Window 需有確定語意。已定的不再重問。
3. **R-02.4 — ServiceManager 計帳邊界 [MUST DECIDE]**：已完成服務凍結認列、跨服務共享成功 payload、同時完成多 Tag 與離散 TBS 超額時，需有**事件順序無關**的最小計帳規則；首版可以選一個透明、可重現的政策，不必現在最佳化公平性演算法。
4. **R-02.5 — Tag / Channel / PHY 最小資料責任 [MUST DECIDE]**：誰持有真實能量及工作模式、誰回傳當下 EH rate / SNR / D2R 成功機率、由誰結算能量／採樣成功事件。無需先決定 Class 數與資料夾結構。
5. **R-02.6 — Notebook Trace、測試與重構門檻 [MUST DECIDE]**：採 `.ipynb` 最小案例（單 Window 多批、跨 Window 累計、能量、服務 Deadline、共享 Tag），記錄 seed/scenario/事件與動作、執行 invariant tests，再轉 `.py`。界定驗證通過的最小條件。

### 16.3 可以延後，但不可偽稱已驗證

- **[DEFER]** EH 轉換效率／反射係數及其 D2R SNR 耦合、具體 BER/PER 參數校準、通道跨窗相關性、UE traffic 精確分布；可以先以參數化假設支援 Notebook 原型，之後必須核對證據與做敏感度分析。
- **[DEFER]** Baseline 的跨服務共享排序、最差服務 Max–Min 的彙整細節、AI 方法選型與訓練，不妨礙先定模組介面；但正式 Baseline 比較前必須封閉演算法規則。
- **[TEST]** 同時間 `D2R_END`／`CW_OFF`／Deadline 的一致性、整數 ns 取整邊界、跨服務計帳與服務完成後停止認列、空批次／無限事件循環、Window 截止可行性。

### 16.4 下一輪只問一題（GRILL）

**R-02.2d：Policy 的 Action 是由 Policy 一次輸出完整 Batch 配置（Tag + TBS + 選用的 BD／SFS／時序），還是 Policy 只選 Tag／TBS，其餘由固定可行配置器補齊？** 兩者影響可行動作空間與 Baseline/AI 公平比較；先確定此邊界，再定精確欄位。**暫不實作。**

## 17. R-02.2d｜Policy 僅選 Tag／TBS；BD、SFS 固定組態（2026-10-20）[DECIDED / RESOURCE MAPPING OPEN]

### 17.1 本輪已確認的設計

- **[DECIDED] 使用者選擇方案 B，並進一步限定為固定組態**：`BD`（Bit Duration）與 `SFS`（Subcarrier Frequency Shift）不是 Policy 動作，也不需要動態 BD／SFS 最佳化器。這比先前「由共用配置器自適應決定 BD／SFS」更嚴格；後者**不採用**。
- **[DECIDED] Policy Action**：每次合法批次決策僅提交 `a_b={(tag_id, TBS_k)}`（包含選取 Tag 集合及各自 TBS）。`CW power` 由 Donor 固定，`BD/SFS` 由事先指定的 PHY／接入配置提供；Policy 不得修改這些環境條件。
- **[MODEL] CFA（Contention-Free Access）**：Tag 使用 Paging 指定的 CFA 資源進行 D2R。此為研究模型的接入方式；固定 BD／SFS 與資源綁定／傳送時點的具體配置規則，仍須與適用版本的規範或明確的研究擴充假設區別，不能直接聲稱所有固定配置可任意同時使用。
- **[INVARIANT]** 同一 DU Window 可多批 Paging，Guard 結束後才以最新 Observation 重新決策；CW 只在當批 D2R 發射，Donor 功率在 Window 內不變；PHY／能量／時間及 SFS/TS 資源衝突由共用 Validator 檢查。Policy 不能直接修改物理真值與服務計量。
- **[FAIR COMPARISON]** Baseline 與 AI 使用同一 BD／SFS 固定設定、CFA 資源映射、候選 TBS、通道／能量資訊及相同 Validator；兩者的動作空間均只包含 Tag Selection 與 TBS Selection。

### 17.2 最小架構介面（候選欄位，不是程式實作）

| 模組 | 輸入 | 輸出／責任 |
|---|---|---|
| `Policy` | 當前 Window 剩餘時間、CW 功率、Tag 目前 SNR／精確估計儲能、服務缺口／Deadline／認列量、固定配置可用性 | 本批 `(Tag, TBS)` 集合 |
| `StaticAccessConfig`（邏輯設定，未必是 Class） | 固定 BD、SFS、CFA 專用資源與相關起始/映射規則 | 提供 Validator／Engine 可讀取的固定配置 |
| `ActionValidator` | Policy Action、固定組態、當前 Window／能量／資源 | 檢查候選 Tag、TBS、至多 8 Tag/批（若沿用現有研究限制）、SFS/TS 衝突、Paging+D2R+Guard 時間與能量可行性；回報是否可執行 |
| `SimulationEngine` | 合法配置與當前事件 | 實際發動 Paging/CW/D2R/Guard；更新能量與服務計量；在 Guard 結束後重新觸發決策 |

### 17.3 尚未封閉的單一必要設計 [OPEN / R-02.2e]

**固定 SFS／CFA 資源究竟如何對應 Tag？** 候選：

- **A. 每個 Tag 預先綁定固定 BD／SFS／CFA 資源**：Policy 選 Tag/TBS，Validator 只檢查所選 Tag 的固定資源是否相互衝突；若資源不足需選更小批或等待下一批。
- **B. 每批從事先定義的固定合法資源池分配**：BD／SFS 候選表固定，但每批可對選中的 Tag 配給不同合法 CFA 專用資源；分配由共用確定性規則完成，不讓 Policy 選 SFS。

兩者都可避免 BD／SFS 變成 Policy 動作，但行動可行集合、同批並行及比較實驗不同。**尚未替使用者選擇**。這屬於資源映射的最小架構設計，不要求展開新的 PHY 演算法。

### 17.4 待驗證（未執行）

- [ ] `TEST-ACTION-01`：Policy Action 只含 Tag/TBS，無法修改 BD／SFS／CW 功率。
- [ ] `TEST-ACTION-02`：當選中的兩個 Tag 會占用相同 CFA SFS/TS 資源時，不能憑「CFA」假定並行一定合法。
- [ ] `TEST-ACTION-03`：TBS 需區分總傳輸區塊位元與有效 payload；若超過服務缺口，使用已決定的需求內認列規則，不重複算實體 Goodput。
- [ ] `TEST-ACTION-04`：相同 Observation／靜態配置下，不同 Policy 的資源可行性檢查完全一致。

**實作狀態**：本節僅更新研究／架構決策；未實作或修改模擬器。

## 18. R-02.2e｜固定 CFA 資源池逐批映射（2026-10-20）[DECIDED]

- **[DECIDED]** 選擇方案 B：每批從預先定義的合法 CFA 資源池，依共用、確定性、可重現的規則指派專用資源給 Policy 所選 Tag；Policy Action 僅含 `(tag_id, TBS)`，不得選擇 BD、SFS 或 CW 功率。
- **[DECIDED]** BD 與 SFS 的合法組態預先固定；資源池映射不是動態 BD/SFS 最佳化。Baseline 與 AI 共用完全相同的映射及 Action Validator。
- **[CONSTRAINT]** 資源不足、SFS/TS 衝突、Tag 數量上限、Paging/D2R/Guard 時間或能量不合法時，不能將該批次視為成功執行。資源池容量、衝突規則及非法動作的處置仍須在 H-01/H-02 定義。
- **[EVIDENCE TASK]** 驗證固定資源映射符合所選 3GPP 版本或清楚標示為研究假設；不得因使用 CFA 就推論任意並行皆合法。

### 18.1 Codex 交接前收斂檢查（五項）[OPEN]

1. **H-01 DES Event Engine**：同時間事件的批次結算與優先序、DU Window/Batch 生命週期、無限重試防護。
2. **H-02 Action Validator**：非法動作拒絕/修復規則、資源池映射失敗、能量及時間可行性。
3. **H-03 ServiceManager**：成功 payload 去重、跨服務共享、服務達標凍結、Deadline 邊界、同時完成的計帳規則。
4. **H-04 最小資料契約**：Node/Tag/Channel/Policy 的狀態所有權、可觀測資訊、動作及 PHY/EH 更新責任。
5. **H-05 Notebook 驗收**：固定 seed/trace、逐事件日誌、invariant 測試與 `.ipynb` 轉 `.py` 的條件。

**交接停止條件**：五項皆具備明確可測的最小規則；未完成的 PHY 校準、AI 方法及正式實驗列為後續驗證義務。尚未授權模擬器實作。

## 19. H-01｜同時間事件批次結算及確定性事件處理（2026-10-20）[DECIDED / TESTS OPEN]

### 19.1 決策與既有前提

- **[DECIDED / 使用者選擇 A]**：DES 對相同整數奈秒時間戳 `t` 的事件採用**同時間批次結算**，不依 Event Queue 的插入順序決定資料是否有效。此為實作架構決策，尚非測試完成證明。
- **[EXISTING DECISION / R-02.1c]**：Deadline 以最後允許 Slot 的**排他上界** `d_exclusive_ns=(n_last+1)*1_000_000 ns` 表示；`D2R_END(t)` 僅在 `t < d_exclusive_ns` 時可認列該服務。因此，即使同時刻的 `D2R_END` 先於 `SERVICE_DEADLINE` 結算，**`t == d_exclusive_ns` 一律無效**；不可因 H-01 選 A 而默改成 `<=`。
- **[EXISTING DECISION]**：Window `[s_w,e_w)`；Guard 必須完整容納於 Window，且下一批只可能於 `GUARD_END` 後重新決策。所有物理事件採絕對 `int ns` 時戳。

### 19.2 最小同時間結算規則（引擎語意；程式結構不預設）

對時間戳 `t`，Engine 收集所有當下到期且因果上相關的事件，對舊區間 `[t_prev,t)` 的能量與資源狀態只積分一次，然後按下列**邏輯階段**提交；這不是要求必須有五個類別或五個 heap priority 數值：

1. **結算舊區間**：依 `t` 前的 CW／Tag mode，對所有 Tag 結算能量與必要占用，不得讓新模式回溯改寫前一區間。
2. **接收完成結果集合**：蒐集在 `t` 完成的所有 `D2R_END`，按唯一的 Tag/Batch 身分去重；PHY 成敗只抽樣／提交一次。傳給 ServiceManager 的候選成功 payload 仍須逐服務檢查 `t < d_exclusive_ns`，並依服務／Tag 既定需求範圍認列。此處只規定**批次輸入與時間門檻**，跨服務共享與超額分配由 H-03 再定義。
3. **截止與關閉**：在接收結算後統一更新 `SERVICE_DEADLINE`、`DU_WINDOW_END` 等截止／可用性狀態；對已到截止排他上界的服務停止後續認列。到期 `CW_OFF` 僅在本批已無進行中的 D2R 時關閉一次；再進入 Guard，期間無該專用 CW EH。若 `D2R_END` 與 `CW_OFF` 同時刻，對過去的能量仍以 CW ON 結算至 `t`。
4. **啟動新區間或決策**：同時刻的合法 `GUARD_END` 完成後，先套用該時間戳全部截止／資源狀態，才建立新的 Observation；僅在目前 DU Window 尚有效且下一完整批可行時呼叫 Policy。不得讓舊 Window 的 `GUARD_END` 在 `WINDOW_END` 同時觸發新 Paging。
5. **可重現性**：同一時刻的成功 Tag 集合須以與 Event Queue 插入順序無關的資料結算方式處理（例如按 Tag ID 正規化，或集合／多服務同步計帳）；任何零時間衍生事件必須在時間 `t` 的因果閉包內安全完成，不能形成 `t` 上的無限排程迴圈。

**[INVARIANTS]**：`D2R_END` 與批次 CW_OFF／接收結算各執行一次；區間能量不重複積分；不因事件插入順序改變服務成功判定；任何新傳輸都不得超過完整 Paging+D2R+Guard 所需的 Window 截止時刻。此處不對未選定的 Message 細節或完整規範流程作聲稱。

### 19.3 最小 Codex Trace 驗收（規格已列出，尚未執行）

- [ ] **TEST-H01-01**：兩個不同 Tag 的 `D2R_END` 同時完成，交換 Event Queue 插入順序；結果認列／CW_OFF 次數／能量一致。
- [ ] **TEST-H01-02**：`D2R_END == d_exclusive_ns`，無論是否與 `SERVICE_DEADLINE` 同時排入，均不得認列；`d_exclusive_ns-1 ns` 則可在其他條件合法時認列。
- [ ] **TEST-H01-03**：`D2R_END` 與 `CW_OFF` 同時，前一區間的 CW 採能只算一次，Guard 無 CW EH，亦無雙重 PHY 抽樣。
- [ ] **TEST-H01-04**：`GUARD_END == DU_WINDOW_END` 時不可啟動下一批；Window 內資源不足亦不可啟動半批流程。
- [ ] **TEST-H01-05**：零時間衍生事件不會造成同時間點無限迴圈；跨週期 Tag 電量持續，服務統計依新週期重設。

### 19.4 相依關係與下一項 [OPEN / H-02]

- **H-01 [DECIDED; TESTS OPEN]**：同時間事件分階段批次結算；與 R-02.1c 排他 Deadline 一致。
- **H-02 [OPEN]**：Policy 提交的整批 `(Tag, TBS)` 不合法時，引擎應原子拒絕整批並停止本 DU Window 後續 Paging（精簡方案），或採可重現修復／縮批（需另定義如何修復及公平性）？必須避免同一時間無限要求 Policy 重試。
- **H-03 [OPEN]**：ServiceManager 跨服務共享、去重、需求上限、同時結算的最小規則；不由 H-01 先行臆定。
- **H-04、H-05 [OPEN]**：模組最小契約及 Notebook Trace 驗收。

**授權邊界**：本節僅更新 Markdown 決策；未實作模擬器或 Notebook。

## 20. H-02｜Action Validator：超出約束直接拒絕；不自動修復（2026-10-20）[DECIDED / TESTS OPEN]

### 20.1 使用者釐清與決策

- **[DECIDED]** 每一輪 Paging 至多選擇 **8 個 Tag**。這是 Policy Action 和 Validator 都必須遵守的批次上限；不引入額外的「假設只能容納四個 Tag」示例或動態容量最佳化問題。
- **[DECIDED]** `Policy` 僅輸出本批 `(tag_id, TBS)` 集合；固定 BD／SFS 依第 17–18 節既定資源池映射規則配置。若 Action **不合法，Validator 直接拒絕整批**，不自行刪減 Tag、改寫 TBS、調整 BD/SFS，也不把拒絕視為 PHY 失敗或服務成功。
- **[INVARIANT]** Validator 檢查：`1 <= |K_b| <= 8`（若空 Action 代表「本次不排程」，則視為獨立的合法 no-op／停止信號而非一批 Paging）、Tag ID 不重複、每個 TBS 在合法離散集合內、每個 Tag 可排程且有服務需求、固定 CFA 資源映射有效、能量因果及 Paging＋D2R＋Guard 能完整落在當前 DU Window。即使批次數不超過 8，也**不等同**自動證明資源衝突或時間、能量均可行。
- **[SCOPE]** 在首版場景若固定 CFA 資源池對所有至多 8 Tag 的合法組合均可提供互不衝突的映射，可將此當作**明示的配置前提**並做一次初始化驗證；不得僅依「Paging 上限 8」推導物理資源池必然足夠。此為模擬器不變條件，不新增資源配置最佳化研究議題。
- **[DECIDED / H-02b]** 不合法 Action 回報 `INVALID_ACTION`、明確原因與事件時間；**整批原子拒絕，立即停止當前 DU Window 後續 Paging，不在同一時刻或同一 Window 重試 Policy**。既有外生事件、Deadline、Window 結束與能量演進仍由 Engine 正常結算；**下個 DU Window** 才能恢復排程。細節及測試見第 24 節。
- **[FAIR COMPARISON]** Baseline 與 AI 的合法性檢查、拒絕計量及 no-op 語意一致。

### 20.2 最小驗收項目（設計規格，未實作）

- [ ] **TEST-H02-01**：選取 8 個合法 Tag 可進入後續驗證；選取 9 個 Tag 必定遭拒絕。
- [ ] **TEST-H02-02**：重複 Tag ID、不合法 TBS 或無效資源映射時，整批原子拒絕且不篡改 Action。
- [ ] **TEST-H02-03**：能量不足、Paging＋D2R＋Guard 超出當前 Window 時，即使只排程 1 個 Tag 也拒絕。
- [ ] **TEST-H02-04**：拒絕後沒有部分 Paging、沒有新增成功 payload／能量消耗、同一時間戳不會無限重試；記錄可追溯的拒絕原因。
- [ ] **TEST-H02-05**：若首版假設固定資源池完整支援至多 8 個並行 Tag，需有初始化映射驗證；否則明列資源限制並允許拒絕。

### 20.3 狀態及依賴

- **H-01 [DECIDED / TESTS OPEN]** 同時事件批次結算；Deadline 末端排他。
- **H-02 [DECIDED / TESTS OPEN]** Policy 最多 8 Tag，非法 Action 原子拒絕、不修復；**H-02b 已確認終止當前 DU Window 的後續 Paging**（第 24 節）。
- **H-03 [NEXT]** 僅剩 ServiceManager 必要的資料認列細節，尤其「多 Tag 同一時刻成功而超過同一服務剩餘需求」的認列分配，應避免以事件插入順序影響服務公平性。
- **H-04/H-05 [OPEN]** 模組資料契約及 Notebook Trace 驗收。

**實作狀態**：本節僅更新研究／架構決策紀錄；未實作任何模擬器或 Notebook。

## 21. H-03｜同時間成功資料依比例認列（2026-10-20）[DECIDED / INTEGER ROUNDING PROVISIONAL / TESTS OPEN]

### 21.1 使用者選擇 B 與規則範圍

- **[DECIDED]** 當同一時間戳記有多個 Tag 成功完成 D2R，對**同一項仍有資格認列的服務**，若該時刻合計合格新 payload 超過該服務的剩餘需求，則按各 Tag 當次**合格成功新 payload bit 數比例**分配需求內認列量。這是在同時完成集合內的對稱結算，不能按 Event Queue 插入順序先到先得；不改變物理成功資料的原始 bit 數。
- **[INVARIANT]** 對服務 i，先以結算前快照取得 `R_i = max(0, D_i^min-G_i(t^-))`，且服務必須仍活躍、Tag 屬該服務指定集合、成功 payload 為該服務可用之新資料、`t < d_i^exclusive`。令當時同一服務的各 Tag 合格新 payload `b_{i,k} >= 0`，集合合計 `B_i = sum_k b_{i,k}`。若 `B_i <= R_i`，各自新增 `c_{i,k}=b_{i,k}`；若 `B_i > R_i > 0`，理想比例新增 `c^*_{i,k}=R_i*b_{i,k}/B_i`。若 `R_i=0`，一律不再增加需求內認列；只登記必要的物理或超額統計。
- **[ACCOUNTING]** 所有服務各自獨立計算比例及需求上限。**同一成功 payload** 可以同時用於多個仍活躍且需要該 Tag／該內容的服務，各服務分別按自身的 `R_i` 與合格集合認列；在全域**實體 goodput** 僅計一次。重傳或重覆接收同一 payload 不能當作新的 bit 數再計入，應以至少 `(tag_id, payload_id)` 或等價唯一識別去重。
- **[ACCOUNTING]** 服務達標時其 `C_{i,k}`、`G_i` 與公平性所依據的需求內貢獻即凍結；已達標、過期或不需要該 Tag 的服務不獲新增認列。另一項未達標服務對共享 Tag 的後續回傳仍可獨立認列。`D_i^gap=max(0,D_i^min-G_i)`。同時完成結果採**同一個結算前服務快照**再共同提交，避免處理先後造成排序偏差。
- **[ASSUMPTION / APPLICABILITY]** 此規則要求**可按 bit 拆分認列的有效 payload**，不表示標準傳輸區塊本身可以任意切開或 PHY 實際只傳了認列量；TBS（傳輸區塊總長）與有效新 payload bit 數需分離。若未來改為不可分割應用資料單位，須重議計帳規則，不得直接沿用比例拆 bit。
- **[PROVISIONAL / INTEGER BITS]** 首版的 `C` 若使用整數 bit，直接儲存 `R_i*b_{i,k}/B_i` 可能產生分數 bit。**建議**使用可重現的「最大餘數法」：先分配 `floor(c^*_{i,k})`，剩餘整數 bit 依小數餘額由大至小配置，完全同分以固定 `tag_id` 排序；確保新增量之和正好為 `R_i`、任一 Tag 不超過自身合格新 payload、且與 Event Queue 插入順序無關。此為**待確認的最小量化實作細節**，並非使用者另外選定的研究方法。若不先確認，Codex 交接時必須顯式標示為暫定預設，不得當成使用者授權的規則。

### 21.2 最小例子及驗收義務

- **[EXAMPLE]** S1 尚缺 10 bit；同時 A、B 分別成功提供 8 bit 新 payload，則 `B=16>10`，A、B 各新增認列 5 bit。**物理有效新 payload = 16 bit**，該服務合計認列 10 bit，該服務未認列超額 6 bit；不將 6 bit 假作傳輸失敗，也不因此憑空增加其他服務的實體 goodput。
- [ ] **TEST-H03-01**：A/B 同時完成 8/8 bit、剩餘需求 10 bit，認列 5/5，物理 payload 16，該服務超額 6；交換事件插入順序結果不變。
- [ ] **TEST-H03-02**：同時成功 payload 3/7 bit、需求剩 12 bit，不需比例縮減，認列 3/7，缺口仍 2。
- [ ] **TEST-H03-03**：非整除案例 3/4 bit、需求剩 5 bit，若採最大餘數整數量化，理想配額 15/7、20/7，整數為 2/3；無分數 bit、總額恰為 5 且順序無關。
- [ ] **TEST-H03-04**：同一新 payload 同時符合 S1、S2 指定內容時可按各自缺口認列，全球物理 goodput 仍只計一次；相同 `(tag,payload)` 重傳不得重覆計入。
- [ ] **TEST-H03-05**：Deadline 排他邊界 (`t == d_i^exclusive`) 或服務已完成的 payload 對該服務新增認列為零；不影響其他仍活躍服務在合法期限內的認列。
- [ ] **TEST-H03-06**：已完成的服務公平性與認列向量不受其後共享 Tag 成功回傳改寫；跨服務週期需求認列重置但 Tag 能量不重置。

### 21.3 Codex Handoff 狀態及下一項

- **H-01 [DECIDED / TESTS OPEN]**：同時間戳事件批次結算，服務期限排他。
- **H-02 [DECIDED / TESTS OPEN]**：最多 8 Tag/批；非法 Action 原子拒絕、不自動修補。
- **H-03 [DECIDED / TESTS OPEN]**：同時成功造成同服務超額時依有效新 payload 比例認列；整數 bit 的餘額分派僅列為首版暫定實作規則，需確認或明標。
- **H-04 [NEXT]**：決定 Node／Tag／Channel／Policy 最小資料契約與只讀 Observation；避免 Policy 誤讀真實環境或任意修改能量／通道／服務狀態。
- **H-05 [OPEN]**：Notebook 的重現性、Trace 與驗收規格。

**授權邊界**：僅更新 Markdown 決策紀錄，未開始模擬器或 Notebook 實作。

## 22. H-04｜唯讀 Observation 與 DTO 資料契約（2026-10-20）[DECIDED / DTO DESIGN TODO / TESTS OPEN]

### 22.1 使用者確認與範圍

- **[DECIDED / H-04-A]** 使用者確認採用 **唯讀 Observation 快照 + Policy 回傳 Action**；Policy 不直接持有或修改 SimulationEngine、Tag、Channel、ServiceManager 的可變真實狀態。
- **[DECIDED]** Policy 的排程動作只包含 `tag_id`、該 Tag 的 `TBS`，最多 8 Tag/批；BD/SFS、CW 功率及固定 CFA 資源映射**不屬於** Policy Action。引擎經共用 Action Validator 驗證後才可執行。
- **[SCOPE]** 下列 DTO（Data Transfer Object）是 **Codex 待設計的最小邏輯資料契約**；不要求現在指定 Python `class`、`dataclass`、`TypedDict` 或具體資料夾結構，不授權實作。
- **[SEPARATION]** Simulator truth (`Tag` 能量、Channel 參數、服務統計) 與 Node 可觀測資訊在邏輯上分離；首版僅在已明示理想資訊的欄位，允許 Observation 數值等於真值，**不可**因此暴露未來 Trace 或任意內部物件指標。

### 22.2 Codex 必須設計的最小 DTO（欄位為契約草案，命名可在實作時一致調整）

| DTO | 從何而來／由誰消費 | 最小必要欄位或內容 | 不應包含 |
|---|---|---|---|
| `TagObservationDTO` | Engine/Node 整理；Policy 唯讀 | `tag_id`, 本 Window 當前 `snr_db`, 理想估計 `energy_j`、必要的可排程標記 | Tag 可變電池/模式物件、未來 SNR、未授權 PHY 真值 |
| `ServiceObservationDTO` | ServiceManager 整理；Policy 唯讀 | `service_id`, `deadline_exclusive_ns`, 尚缺 `remaining_bits`、指定 Tag IDs、需求內各 Tag 累積貢獻／必要公平性資訊 | 可變服務內部統計引用、未來回傳結果 |
| `SchedulingObservationDTO` | Node 從當下可揭露狀態組裝；Policy 唯讀 | `now_ns`, `window_end_ns` / DU 剩餘時間、本 Window `cw_power`、**已預告**下 Window CW 功率（若可得）、`TagObservationDTO[]`, `ServiceObservationDTO[]`、必要固定組態的唯讀識別／合法 TBS 集合 | 完整 ResourceTimeline 未來窗口、未來 SNR、直接 Engine 物件 |
| `TagTbsActionDTO` | Policy 輸出；Validator 消費 | `tag_id`, `tbs_bits` | BD、SFS、CW 功率、可任意改環境的指令 |
| `PagingBatchActionDTO` | Policy 輸出；Validator 消費 | 一批 `TagTbsActionDTO[]`；空動作語意需維持與 H-02 一致 | 動態 CFA 映射或未驗證的執行時間假設 |
| `ActionValidationResultDTO` | Validator 輸出；Engine/Trace 消費 | `accepted` / 狀態、拒絕 `reason_code`、如合法則已映射的固定 CFA 資源配置（可另成內部執行計畫） | 改寫原 Action 的隱性「修復」 |
| `SimulationEventTraceDTO` | Engine 產生；Notebook 驗收使用 | `time_ns`, `event_type`, `window_id`, `batch_id`、相關 Tag/Service ID、事件結果及必要能量/計帳增量、Action 拒絕原因 | 需憑使用者肉眼才可重現判定的隱含狀態 |

**內部狀態不等於 DTO**：`Tag` 持有實際儲能/模式及 EH/耗能參數；`Channel` 管理本 Window 固定的通道樣本、SNR 與 EH/PHY 計算；`ServiceManager` 持有需求、貢獻、共享資料 ID 去重及截止狀態；`SimulationEngine` 負責時間、事件佇列、實際狀態轉移與批次提交；`Node` 負責把合法當前資訊彙整成 Observation。這些為責任劃分，不要求一對一對應程式類別。

### 22.3 DTO 的約束與最小驗收

- **[INVARIANT] 唯讀／無可變別名**：Policy 修改其收到的容器或物件不得改變 Engine/Tag/Channel/ServiceManager 真實狀態；不向 Policy 提供直接可變參照。DTO 最小欄位須可序列化以支援 trace/replay，並使用整數 `ns` 時間戳。
- **[INVARIANT] 可觀測性**：Node/Policy 可以使用本 DU Window 的當前 CSI、現有理想能量、已知本 Window 邊界及 Donor 已預告的下 Window CW 功率；不得預知未來 Window SNR 或尚未揭露的 UE/DU Trace。
- **[INVARIANT] 同窗資料更新**：本 Window SNR 固定，但能量與剩餘服務需求可隨多批 Paging/D2R/Guard 更新；每次 `GUARD_END` 重新建立 Observation，不重用已過期快照。
- **[INVARIANT] 動作驗證**：固定 CFA 映射可在 Action 驗證後形成引擎內部的執行計畫，不回填修改 Policy 的原始 Action；拒絕不提交部分狀態。
- [ ] **TEST-H04-01**：Policy 嘗試修改 Observation，環境真值不變。
- [ ] **TEST-H04-02**：兩批之間 Tag 能量/服務缺口更新，但同一 Window SNR 不變；下一 Window SNR 依 Channel 更新。
- [ ] **TEST-H04-03**：Policy 看不到尚未揭露的 UE/DU Trace 與下一 Window SNR。
- [ ] **TEST-H04-04**：Action DTO 只有 Tag/TBS，執行計畫中的固定資源映射由共用 Validator/Engine 產生；合法／非法案例可重現。
- [ ] **TEST-H04-05**：相同 Seed、Scenario 與 Policy，DTO/Trace 可重播並比對關鍵計帳結果。

### 22.4 交接清單最新狀態

- **H-01 [DECIDED / TESTS OPEN]** 同時間事件批次結算。
- **H-02 [DECIDED / TESTS OPEN]** 每批至多 8 Tag；非法 Action 原子拒絕，不自動修復。**H-02b 已確認：拒絕後終止當前 DU Window 後續 Paging**（第 24 節）。
- **H-03 [DECIDED / TESTS OPEN]** 同時成功比例認列；整數 bit 最大餘數分配目前僅為暫定，需標記並在交接前確認或列為明示的可替換預設。
- **H-04 [DECIDED / DTO DESIGN TODO / TESTS OPEN]** 唯讀 Observation、純 Action 回傳；上列 DTO 要設計但**未實作**。
- **H-05 [NEXT]** 決定 Notebook 交付驗收門檻（可重現 Trace＋最小 invariant tests），再檢查是否尚有會使 Codex 擅自補規則的阻塞點。

**授權邊界**：本節只有文件修改與 DTO 規格記錄，尚未開始 `.ipynb`、`.py` 或任何模擬器實作。

## 23. H-05｜Notebook + Trace + 自動化測試的交接驗收門檻（2026-10-20）[DECIDED / TESTS NOT RUN]

### 23.1 使用者決策與授權範圍

- **[DECIDED / H-05-A]** 首版採 **Notebook (`.ipynb`) + Event Trace + 自動化 Invariant Tests**。使用固定 Scenario 與 Seed，以可重現的事件紀錄與斷言驗收；**通過首版 Notebook 驗收後**才將核心整理為 `.py`。這是交付順序及驗收要求，**不是**實作授權，也不是已執行測試的證明。
- **[SCOPE]** 首版專注 DES、能量因果、CFA 固定資源映射、服務認列和 Policy/Engine 邊界；不因 H-05 引入新的 AI 模型、通道最佳化器或未驗證之標準訊令。
- **[REPRODUCIBILITY]** 每次執行至少保留 `scenario_id`、完整配置版本／參數快照、`seed`、Policy 識別、初始 Tag 能量、Window 事件時序、原始 Action、Validator 結果、事件 Trace 與服務最終統計。相同版本／Scenario／Seed／Policy 重跑應產生相同關鍵結果；任何隨機數使用位置都需可重現並可追查。
- **[TEST DESIGN]** 自動化斷言在 Notebook 中可直接執行，不以人工觀看 Trace 代替驗收；失敗須顯示事件時間、Window、Batch、Tag/Service 身分與違反的 invariant。完整 `.py` 重構要保持測試與結果一致，不以換檔名視為通過。

### 23.2 五類最小 Scenario 與不可省略的 Invariants

| 類別／ID | 最小測試情境 | 必須自動確認的性質 |
|---|---|---|
| `ACPT-01` 多批 Paging / DU Window | 一個 DU Window 內至少兩次 `Paging → CW_ON/D2R → CW_OFF → Guard`；第二批在第一批 `GUARD_END` 後依新 Observation 選取 | 批次不跨 Window，Guard 無 CW EH；Window 內 SNR 固定，CW 功率固定；Window 結束不得啟動未完成批次 |
| `ACPT-02` 能量因果 / 跨窗持續 | 已初始化滿電的 Tag 經 UE UL、CW ON（包括未排程 Tag 採能）、D2R、Guard、跨 Window／服務週期 | `0 <= E_k(t) <= E_max`；只按實際 CW/模式區間積分且無雙重結算；Action 在足夠能量前才能通過；服務週期更新不重設 Tag 電池 |
| `ACPT-03` Deadline / 同時事件 | `D2R_END`、`CW_OFF`、`SERVICE_DEADLINE` 相同時間戳，另測 `d_exclusive_ns-1` 與 `d_exclusive_ns` | `t < d_exclusive_ns` 才可認列；同時完成集合不受 Event Queue 插入順序影響；單次 PHY 結算／CW_OFF；`GUARD_END == WINDOW_END` 不啟動新批 |
| `ACPT-04` 共享服務 / 超額認列 | 同時兩 Tag 各成功 8 bit，單一服務尚缺 10 bit；再設同 payload 符合另一活躍服務、重複 payload 重傳 | 原服務新增 5/5 bit；各服務需求上限、去重、達標凍結；跨服務可共享認列，同一物理 payload goodput 全域僅算一次；整數化角落情況待明確定規 |
| `ACPT-05` 非法 Action / DTO 邊界 | 9 Tag、重複 ID、無效 TBS、時間或能量不足、CFA 映射衝突；Policy 嘗試改寫 Observation | 整批拒絕、無部分 Paging 或狀態提交、不自動修正；拒絕原因可追蹤；Policy 無法改動內部狀態或看到未來 SNR／未揭露 Timeline；同時間不無限重試 |

### 23.3 Notebook → `.py` 的最小 Gate

- [ ] `GATE-01`：五類 Scenario 皆有固定配置與 Seed，執行並通過對應自動化測試；失敗時有可定位的 Trace。
- [ ] `GATE-02`：同 Scenario/Seed/Policy 連續重跑，輸出事件次序的規範化紀錄與關鍵統計一致；對同時 D2R event 做插入順序置換仍得到相同服務結果。
- [ ] `GATE-03`：能量、時間、資源、去重／Deadline、DTO 隔離各項 Invariant 均通過，且無無限事件循環。
- [ ] `GATE-04`：未封閉的參數與研究假設（PHY/EH 校準、跨 Window 通道模型等）以明示配置或 TODO 呈現，未偽裝為已驗證的 3GPP 要求。
- [ ] `GATE-05`：Notebook 的可用核心 API／DTO／測試規格可抽離到 `.py` 而不改變模型語意；實際轉檔/實作須由後續另行授權。

### 23.4 尚待關閉的最小語意（Codex 交接 Blockers）

1. **[CLOSED / H-02b] 非法 Action 原子拒絕後的時間處理**：已決定 `INVALID_ACTION`、整批不執行、不重試，**停止目前 DU Window 後續 Paging**；外生事件和既有狀態結算照常執行，下個 DU Window 才恢復 Policy 決策。詳細語意與測試見第 24 節。
2. **[OPEN / H-03b] 整數 bit 比例認列**：使用者已定同時成功且超額時按比例分配，但遇到分數 bit 的整數化方法尚未確認。第 21 節提案為「最大餘數法、餘額相同以 tag_id 排序」，仍不得標示為已確認。

**狀態總結（更新至第 24 節）**：H-01、H-02、H-03、H-04、H-05 的主要架構決策均已確認；**H-02b 已確認，僅 H-03b 整數認列規則仍待確認**。其他已記錄的參數校準與科學證據義務屬後續驗證，不應與此混淆。

**授權邊界**：此節僅更新研究及實作交接決策紀錄；未建立 Notebook、Simulator、DTO 程式或執行測試。


## 24. H-02b｜非法 Action 後停止當前 DU Window 排程（2026-10-20）[DECIDED / TESTS OPEN]

### 24.1 使用者選擇 A：精簡失敗處理

- **[DECIDED]** 若 `ActionValidator` 判定本批 Policy Action 不合法，Engine 記錄 `INVALID_ACTION`、`reason_code`、絕對 `time_ns`、`window_id`、原 Action 及 Policy 識別，**原子拒絕整批**；不自動修正、刪 Tag 或縮 TBS。
- **[DECIDED]** 拒絕後設置目前 DU Window 的**停止排程狀態**；不再於該 Window 發出新的 Paging、CW/D2R Batch、Guard，亦不再因後續決策觸發事件呼叫 Policy。**直到下一個 DU Window** 才允許在新的合法決策時點恢復排程。這是失敗後的排程停止，不是把模擬時鐘跳到 Window 終點。
- **[INVARIANT]** 無部分提交：被拒絕的 Action 不導致本批 Paging、D2R、CW ON 或由本批引起的能耗／服務 bit 認列。拒絕不是 `PHY_FAILURE`。原本獨立存在的外生 UE/DU 事件、服務 Deadline 與 Tag 狀態結算仍按 Event Queue 因果順序執行；不得刪除既有事件或凍結自然時間。
- **[FAIRNESS]** 所有 Policy 一致採用此終止規則；記錄拒絕次數與 Window 剩餘可用時間作為診斷，不能將 Engine 主動修復的效益算進任何一方。
- **[NO EXTRA DESIGN]** 不增加即時二次嘗試、Penalty Optimizer 或複雜復原機制；`no-op`（如允許合法空 Action）仍應與 `INVALID_ACTION` 分別標記。

### 24.2 H-02b 必要自動驗收（尚未執行）

- [ ] **TEST-H02b-01**：在 `GUARD_END` 遞交違反上限／非法 TBS 的 Action → 記錄一次 `INVALID_ACTION`，本 Window 不再有任何新 Paging/CW/D2R，也不重試。
- [ ] **TEST-H02b-02**：拒絕時至 Window End 仍有時間 → 時鐘正常推進、既有 Deadline／Window End 仍結算，無被拒批次的耗能或成功 bit。
- [ ] **TEST-H02b-03**：下一 DU Window 可重新建立 Observation 並正常呼叫 Policy；上一 Window 的停止旗標不得漏至下一 Window。
- [ ] **TEST-H02b-04**：同 Scenario／Seed、不同 Policy 受同一拒絕規則；`INVALID_ACTION` 與 PHY 失敗、合法不排程有不同原因碼。

### 24.3 下一項與授權邊界

- **H-01–H-05 [ARCHITECTURE DECIDED / IMPLEMENTATION & TESTS OPEN]**。
- **H-02b [DECIDED / TESTS OPEN]**：拒絕整批，停止當前 DU Window 後續 Paging；不停止 DES 的時間與外生事件。
- **H-03b [NEXT / OPEN]**：同時間成功的比例認列若產生分數 bit，是否採「**最大餘數法（Hamilton）**，固定 `tag_id` 作餘額同分 tie-break」？見第 21.1 節之 Provisional 草案。確認後方可將 Codex Handoff 的整數資料契約視為定稿。
- **不授權實作**：本輪僅修改 Markdown，沒有建立、執行 Notebook 或模擬器。

## 25. H-03b｜整數 bit 最大餘數認列（2026-10-20）[DECIDED / TESTS OPEN]

- **使用者確認**：本次訪談 Q-DESCRIPTION-01 回覆「A」，確認採用最大餘數法（Hamilton）；餘額相同時按 Tag ID 升序。此決策關閉第 21、23、24 節的整數量化未決事項，並使 Codex Handoff 第 6 節具備對應決策來源。
- **規則**：同時成功集合對某服務的合格新 payload 總量 `B` 超過結算前剩餘需求 `R>0` 時，每 Tag 先分配 `(R*b_k)//B` bit；剩餘 bit 按 `(R*b_k)%B` 降序逐一分配，同分按 Tag ID 升序。使用整數運算比較餘額，不以浮點近似排序。Tag ID 必須具備一致的排序契約，具體型別於 DTO 設計時明示。
- **既有分支不變**：`R=0` 不增加認列；`B<=R` 各自全額認列，`B=0` 不進行除法。合格性、去重、Deadline 排他、達標凍結與跨服務獨立認列沿用第 21 節。
- **例子**：`R=5,b_A=3,b_B=4`，認列 `2/3`；`R=1,b_A=b_B=1,A<B`，認列 `1/0`。固定 ID 同分規則可重現，但可能有固定 ID 偏向，不宣稱完全消除量化造成的公平性偏差。
- **待驗收**：總新增認列恰為 `R`，各 Tag 不超過其合格 payload，無分數 bit，交換事件入隊順序結果不變；覆蓋零需求、零 payload、未超額、非整除及餘額同分案例。測試尚未實作或執行。
- **授權邊界**：本次只確認並同步文件；尚未授權 Notebook／Simulator 實作。合法空 Action 的行為後續已於第 26 節確認。

## 26. 合法空 Action：NO_OP 後停止本 Window 排程（2026-10-20）[DECIDED / TESTS OPEN]

- **使用者確認**：訪談 Q-DECISION-01 回答「A」。Policy 回傳空集合為合法 `NO_OP`，不視為不合法的零 Tag Paging batch。
- **執行語意**：記錄 `NO_OP`、時間、Window、Policy 與原 Action；不建立本批 Paging、CW、D2R 或 Guard，不產生本批耗能或服務認列；停止目前 DU Window 後續排程，不在同窗再次呼叫 Policy。下一 DU Window 的合法決策點恢復。
- **時間因果**：停止的是新排程；模擬時間、既有外生事件、服務 Deadline 與自然能量結算照常。不得把時鐘直接跳到窗末而漏掉中間事件，也不得將電池凍結。
- **統計邊界**：`NO_OP` 與 `INVALID_ACTION`、`PHY_FAILURE` 分別記錄；主動不排程不得增加非法動作或 PHY 失敗次數。所有 Policy 共用相同語意。
- **待驗收**：空 Action 僅記錄一次且無同時間無限重試；同窗無新 Paging；既有 Deadline／能量正常結算；下一 Window 可重新排程；無額外批次能耗或認列。尚未實作／執行測試。
- **授權邊界**：僅更新文件決策，不授權 Notebook 或模擬器實作。

## 27. 逐模組原型、情境測試與人類程式理解驗收（2026-10-20）[DECIDED / NOT IMPLEMENTED]

- **使用者明確指示**：進入架構設計與工具選擇規劃；以 `.ipynb` 建立每個模組的原型，每個模組做好後執行對應情境測試，由人類驗證理解程式內容，沒問題後再轉為 `.py`。
- **生效順序**：模組 Interface 與情境案例 → Notebook 原型與自動斷言 → 實際執行情境測試 → 人工逐段導讀、問題修正與接受 → 抽離該模組 `.py` → 同案例複驗。人類未接受前不抽離該模組；沉默或測試通過不視為人工接受。
- **取代範圍**：第 8、23 節及交接規格中「整體 Notebook 驗收全部通過後才可開始任何 `.py`」的舊順序改由本節取代。ACPT-01～05 的跨模組整合測試義務仍保留，單模組驗收不能取代整合驗收。
- **真實進度**：目前只授權架構與工具規劃，尚未開始程式實作；每模組的具體接受尚未發生。參數來源題暫緩到依賴模組實作前，不將未回答視為選 A 或 B。
- **衍生設計**：[模組與工具規劃草案](../../docs/architecture/implementation-plan.md)；模組切分、具體檔案及工具選擇屬建議，非已實作事實。

## 28. Config／DTO 採 dataclass 集中定義（2026-10-20）[DECIDED / SCOPE DETAILS OPEN]

- 使用者指定使用 dataclass，集中在單一 `.py` 管理，類似 C 的 `.h` 共用資料定義。
- 本次仍為討論設計，未授權跳過第 27 節的 Notebook 原型、情境測試及人工接受順序；沒有建立 `.py`。
- **範圍已確認（Q-INFLUENCE-01，使用者回答 A）**：共用檔只集中 Config／DTO／必要 Enum，內部 State 型別定義留各模組；不改變模組狀態所有權或 Policy 唯讀資訊限制。
- **實例入口已確認（Q-TRADEOFFS-02，使用者回答 A）**：原型在 Notebook 情境設定 cell 以具名參數建立 Config 實例，每次 run 保存完整配置快照；首版不需先增加外部 JSON 載入器。
- **停止條件已確認（Q-DECISION-02，使用者回答 A）**：一次 run 完整跑完指定服務週期數，總時間由各週期長度推得；不另設獨立固定時間停止欄位。服務帳逐期重設但 Tag 能量持續，不重新初始化成多個 run。
- **服務配置已確認（2026-10-22，Q-INFLUENCE-02，使用者回答 B）**：Notebook 明列每一期服務設定，各期可相同或不同；首版不自行以 Seed 生成服務需求。每期起點固定、期中不變的既有規則沿用。
- 共用檔的實際檔名／路徑及具體欄位仍待設計；`contracts.py` 為建議。週期長度配置、Deadline 輸入轉換及必要實體參數仍待定稿；配置值來源是否 synthetic 仍未決。
- 衍生討論：[Config／DTO 草案](../../docs/architecture/config-dto.md)。

## 29. 場景時間尺度修正（2026-10-23）[DU WINDOW / SERVICE DEADLINE SCALE DECIDED]

- **使用者明確設定**：DU Window 長度固定 **600 ms = 600,000,000 ns**；此為本研究情境的配置，不宣稱為 3GPP 規定。不再把 Window 長度隨機生成視為首版預設。
- **服務時間語意已確認（Q-DESCRIPTION-02，使用者回答 A）**：「一項服務最少都要 10 s～15 s 起跳」指各項服務的完成期限；不是整批需求更新週期，也不是需傳滿的時間。這不是已確定的 `[10,15] s` 均勻分布或最大值，具體 Deadline 仍逐服務配置。
- **既有範例修正**：先前每週期 100 ms 不符合此場景，已將文件改為秒級 Deadline 的示例。示例中的 20 s 共同週期僅為換算展示，不是使用者已選定長度，不得沿用為正式配置。
- **時序尚未決定**：600 ms 是每個 DU Window 的持續時間，不代表每 600 ms 必定出現一個 Window、無 UE 間隔、或下一 Window 起點可預知。同窗多批、CW 僅 D2R ON、Guard 無 CW EH 等既定規則不變。
- **觀測契約需同步**：先前未來 Window 長度不可預知的描述需在固定長度配置下重新對齊；不能再無條件稱其長度為未知隨機量。未來 Window 起點、UE/DU 完整 Trace 與未來 SNR 仍不得直接提供 Policy，不以此設定虛構額外預知能力。
- **下一項釐清**：Q-DESCRIPTION-02 已關閉；回到尚未回答的 Q-DECISION-03：共同服務需求週期每期各填長度，或全 run 共用固定長度。共同週期仍需符合既有「各服務 Deadline 嚴格位於當期內」的約束，不能直接取某個服務 Deadline 當週期末。未開始實作或測試。

## 30. 所有服務共同從 0 計時（2026-10-23）[COMMON ORIGIN DECIDED / SCOPE RESOLVED BY SECTION 31]

- **使用者修正**：所有服務起點統一從 0 開始。例：服務 1 期限 15 s、服務 2 期限 20 s，兩者均從同一個 0 s 起算，不因在清單中先後排列而將服務 2 延後到 15 s 或下一個週期才啟動。這些秒數是使用者提出的例子，不自動成為全體服務預設值。
- **尚需對齊的範圍**：先前已討論多期服務依序啟動；本次「所有服務從 0」可能表示首版單一 run 只有一批同時啟動的服務，也可能指每個週期內各服務皆以當期起點為相對 0。Q-DESCRIPTION-03 待釐清，不自行取消既有多週期契約，也不自行將全域模擬時鐘每期歸零。
- **先暫緩** Q-DECISION-03 的共同週期長度問題；若首版只需單批服務，該題不應成為拓撲模組開工前的必答問題。DU Window 固定 600 ms、Deadline 排他與傳輸累積的規則不變。
- **設計文件優先級**：舊兩期範例及其中加上 cycle_start 的示例不能直接視為本次需求的已確認表示。未來依此題答案調整 ServiceConfig 的聚合方式及 run 範圍。

## 31. 首版單批服務、輪長取最晚 Deadline（2026-10-23）[DECIDED / NOT IMPLEMENTED]

- **使用者回答 Q-DESCRIPTION-03 的 A 並補充**：首版一輪中全部服務均於全域 `t=0` 出現；本輪服務週期長度取最長的服務完成期限。例：S1 Deadline=15 s、S2=20 s，兩者同時開始，本輪長度 **20 s**。
- **精確表示**：若各服務排他期限為 `d_i>0`，共同起點為 0，則 `T_round=max_i d_i`。本輪不另填可與此矛盾的 ServiceCycle duration，不以服務在資料清單中的位置推遲啟動，也不在輪中加入另一批需求。
- **取代的首版規則**：取代第 28 節及前文首版以獨立指定 N 個依序需求週期決定 run 範圍的設計；多輪續跑／獨立重複實驗留作後續明確需求。Q-DECISION-03（每期自填／全 run 固定長度）因長度改由期限推得而**被新需求取代**，不是使用者選了該題 A 或 B。
- **期限邊界修正**：原 `0<d_i<T_cycle` 的「全部嚴格落在共同週期內」要求在此首版改為 `0<d_i<=T_round`，至少一項相等；成功 payload 對服務 i 仍只在 `D2R_END<d_i` 認列。例：S2 在 19,999,999,999 ns 完成可在其他條件合格時認列，恰在 20,000,000,000 ns 不認列，不因輪末相等而放寬 Deadline。
- **能量及環境**：一輪內 Tag 電量連續演進，不隨某服務完成／到期而重置；DU Window 持續時間固定 600 ms，起點／間隔未決。20 s 不代表有固定數目的 DU Window，也不代表 CW 連續發射 20 s。
- **不新增未決前置**：目前已足以結束這段時間語意對齊，依使用者今日目標立即轉入 IAB 拓撲盤點；不要求先決定多輪策略、精確輪末物理事件收尾或全套 Config。
- **證據界線**：這是模型決策，尚未實作或執行模擬器測試；空服務集合的輪長定義、run 終點既有物理事件收尾可留到依賴模組設計時封閉。

## 32. IAB 首版拓撲規模、共址與非均勻部署（2026-10-23）[MODEL DECISIONS RECORDED / GENERATION DETAILS OPEN]

- **規模已確認（Q-NICHE-01，使用者具體回答 B）**：1 個 Donor 直接連 5 個 IAB Nodes；每個 Node 下有 1 個 UE 及多個 Tags，共 5 個 UE，不是 5 層回傳鏈。Node 整合 Reader、無 UE Reader relay 的既有模型沿用。
- **使用者架構意圖**：稱為 D1T1 共址架構，並明確假設 IAB 拓撲可支援 A-IoT 的 split／IAB-DU Reader 整合。這是已選定研究擴充，不是聲稱 Release-19 TS 已支援。
- **規範已核對**：本地 TS 38.300 V19.4.0 §16.23.2 明確不支援該版本 A-IoT 的 split gNB；TR 38.769 V19.0.0 §3.1 的 D1T1 是 Deployment scenario 1＋Topology 1，不是 Device type 1；同份 TR 的 Table 4.2.1-1 中 D1T1-A2 描述 CW 與 R 節點相同。TR 38.848 V18.0.0 §4.2.2.1 的 D1 是裝置與基地台皆室內。不能由共址直接推導完整 D1 評估條件已選定；Q-DESCRIPTION-04 已回答 A：農場室外研究情境，沿用 T1／共址意圖，不直接套 D1 室內參數。
- **關聯及部署意圖**：Tag 隨機關聯 Node，各 Node 周圍的 Tags 隨機且非均勻分布，Node 分布於不同區域。先記錄意圖，不默認等機率關聯、不默認最近鄰，也不保證不受限抽樣會讓各 Node 自然都有多個 Tag；最低數與取樣規則尚需定稿。
- **數量例子**：使用者提出全場景共 30 Tags，好區 10、中區 13、差區 7（10+13+7=30）；是可配置的非均勻部署例，不是每 Node 各 30，也不是 5 Nodes 強制均分。每 Node 的分區配額及區域定義尚未定案。
- **干擾假設已選定**：Donor–Node 無線回傳無干擾，干擾只考慮 Node–Tag 段。這不等於回傳無路損／零延遲／無限容量，也沒有指定干擾來源為 UE、其他 Node、其他 Tag 或 CW 自干擾；來源、強度與作用方向後續在 Channel 契約封閉，不先實作。
- **原圖已取得並閱讀**：`ReferDoc/Plan/main.pdf`，System Model，11 頁；完整抽文字，第 3、4 頁渲染檢視。第 3 頁是農場／非均勻部署與 TR 38.901 參考；第 4 頁含 2 Nodes／各 1 UE 示意、同心 Distance/SNR zones、距離不唯一決定 SNR 的註記。首版節點數依使用者最新 5 Nodes／5 UE 覆蓋圖中示例。圖未給實際公尺半徑、SNR 門檻或數值干擾場，不憑圖捏造。
- **後續最小待決項**：分區是幾何環帶還是預設鏈路品質；座標／區域半徑與高度；隨機關聯和分區配額的共同生成；Node 最少 Tag 數及干擾來源。已確認規模不重問，先一次處理一項。
- **證據路由**：[來源核對與拓撲盤點](../../docs/architecture/iab-topology-scope.md)。未實作 Notebook／拓撲，未做 PHY／協定符合性測試。

- **戶外文獻調查（2026-10-23）**：使用者選 A 並要求查詢；證據與適用限制見 `docs/architecture/outdoor-literature-evidence.md`。TR38.848戶外50–500 m是設計目標而非共址實測半徑；TR38.769強CW洩漏數值不是三區外部干擾。三份作者／機構原文保存於 `ReferDoc/Literature/A_IoT/` 並記來源與SHA-256。尚未選定本場景半徑、頻段、功率、分區門檻，不將文獻條件當成已決配置。

- **自干擾理想化假設（2026-10-23）[DECIDED]**：Node可完美消除自身CW殘餘自干擾，殘餘功率為0 W而非0 dBm；此模型不模擬自身CW前端飽和／去敏，不影響CW傳播／採能，也不代表其他Node／UE外部干擾消失。使用者另述遠距離所需SNR更好，其含義待Q-DESCRIPTION-05釐清，尚未採遠區更高解碼門檻。

- **距離與SNR（Q-DESCRIPTION-05，已回答A）[DECIDED]**：距離影響實際接收SNR；固定同一PHY設定與目標錯誤率時，成功門檻不因距離另提高。此決定不選定傳播模型、SNR值或分區方式；Q-DESCRIPTION-06接續釐清幾何區或品質區。

- **幾何分區與品質排序（Q-DESCRIPTION-06，已回答A附條件）[DECIDED]**：採近／中／遠距離分區；近區品質須優於遠區，屬使用者system model假設，取代先前允許近區品質反轉的草案。後續Channel須保留排序而不僅是平均趨勢；先以同Node／同Window的接收SNR比較，中區排序、差距及跨Node比較尚未明定。不提高遠區成功門檻。三區半徑待Q-TRADEOFFS-03，候選工程配置未採用。

- **分區尺度（Q-TRADEOFFS-03，已回答A）[DECIDED]**：五個Node共用可配置邊界10／30／50 m；以所屬Node距離d分為近區0<d<=10、中區10<d<=30、遠區30<d<=50（m）。排除d=0，Channel有效最小距離待定；部署半徑不等於通訊／採能成功保證。Q-TRADEOFFS-04接續Node位置固定或依seed生成，未選定具體座標。

- **Node位置來源（Q-TRADEOFFS-04，已回答A）[DECIDED]**：Donor與五個Node的座標於Config明列、run內固定；Tag維持隨機關聯／部署。具體座標及高度尚未定。Q-TRADEOFFS-05接續部署區域可否重疊，幾何是否重疊不等於干擾是否存在。

- **部署區域不重疊（Q-TRADEOFFS-05，已回答A）[DECIDED]**：五個Node的50 m Tag部署區域不重疊；平面圓形座標草案以Node間距大於100 m避免相切，具體座標另給。不將此幾何假設解讀為無跨Node射頻干擾。下一題Q-TRADEOFFS-06為全場三區配額如何分配至Nodes；各Node至少2個及隨機／明列配額為提案，尚未選定。

- **Tag配額分配（Q-TRADEOFFS-06，已回答A）[DECIDED]**：依seed隨機分配各Node三區數量，精確維持全場配額且每Node至少2個，不強制均分或每Node每區都有Tag；先決定歸屬與分區，再在對應區域生成位置。總數小於2倍Node數須拒絕；30與10／13／7為可配置例子。Q-TRADEOFFS-07接續區內按面積均勻或群聚，尚未選定。

- **區內位置分布（Q-TRADEOFFS-07，已回答A）[DECIDED]**：各分區內按面積均勻隨機、角度無偏好，跨區維持精確非均勻配額。依使用者要求盤點剩餘項，見 `docs/architecture/iab-topology-remaining-decisions.md`；空間維度／距離、Tag／UE是否移動、UE座標需求仍待對齊，本輪未另出題。

- **平面與靜態模型 [DECIDED]**：使用者指定高度暫不考慮，首版x／y公尺座標、三區10／30／50 m採水平距離；系統模型靜態，run內位置不變，不加入移動／切換。靜態位置不覆蓋既定Window級通道更新或資源時序。UE是否有固定實體座標待Q-INFLUENCE-03，例子僅用來說明資源身分與距離相關干擾的差別。

- **UE邏輯表示（Q-INFLUENCE-03，已回答A）[DECIDED]**：UE僅ID及所屬Node，不配置實體座標，資源占用交時序模組；不因此設定UE干擾為零。三項拓撲模型邊界均已對齊，Config／DTO、示例座標及生成／驗收草案見 `docs/architecture/iab-topology-design.md`；草案名稱與示例值不是額外使用者決策，尚無Notebook或測試成果。

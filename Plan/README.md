# 剩餘模組與 AOA 排程草案

- 版本：0.2，2026-10-23。狀態：**供討論，尚未核准為執行基準**。
- 已完成：IAB 拓樸已交付；本計畫從「通道品質」開始，不重做拓樸。
- 建議：分四個里程碑完成，先取得可運行首版，再完成正式 Baseline、研究實驗框架，最後交付 CLM 比較結果。
- 您已確認每日可投入 **2 小時**討論、導讀與驗收。暫按每週 5 個工作日、代理協作工程每日 4 小時排程；後兩者仍是待校正假設。
- 第一版估算：工程活動 **273.75 小時**，其中需要您共同參與 **104.75 小時**。共同時數已包含於工程活動時數，不能相加成 378.5 小時的工期。
- 按目前單一 change 在製、完成人工接受後才抽離的方式，排至**第 93 個工作日，約 19 週**；另提議保留 20% 管理準備，約 **111 個工作日／23 週**。不設定尚未確認的開工日或完工日期。
- 這是工程判斷估算，**不是交期承諾、P80 日期或實際績效紀錄**。外部資料取得、未決模型與額外合併等待都可能增加工期。[Needs Verification]

## 12 月底目標：優先閱讀

- 您新增目標為 **2026-12-31 前完成包含既有 CLM 的全部實驗**；原 13 包估算已補 W14／W15，沒有加入 DRL 重建／從頭訓練。
- 原每日 2 h 人工容量不足以支持本版完整範圍於年底完成。
- [加速安排與關鍵日期](05-year-end-acceleration.md)：提議工程協作每日 8 h、指定關卡日人工最多 4 h、共同時段彈性安排，暫排 12/17 完成，保留 9 個工作日。**額外容量尚待您確認。**
- [加速日逐日清單](accelerated-human-load.csv)列您需參與的活動與時數：23 日超過原 2 h，超出部分合計 37 h；這不是在總需求 104.75 h 外再加 37 h。
- 時間表取決於模型來源可取得、CLM 不需重訓及實驗吞吐量足夠；須先以短實驗核實，不能保證全部實驗一定在 12/17 完成。

## 先看這三張圖

| 圖 | 用途 |
|---|---|
| [AOA 主網路](aoa-network.svg)／[文字與 Mermaid 版](aoa-network.md) | 看真正的技術相依。圓圈是事件，箭線才是活動，虛線為 0 h 虛活動。 |
| [資源限制後排程](resource-gantt.svg) | 看實際每天可以做什麼；同時最多推進一個 change。 |
| [每模組的交付關卡](03-aoa-and-control.md#每個工作包的內部活動) | 看 Notebook、人工接受、轉成 .py 與交付各占多少工作。 |

## 四個交付里程碑

| 里程碑 | 完成時可以做什麼 | 基準累計工作日 | 您累計參與 |
|---|---|---:|---:|
| M1：可運行首版，W01–W10 | 5 Nodes 場景完整跑通；通過五類整合驗收；用最小測試策略操作 | 59，約 12 週 | 66.50 h |
| M2：正式 Baseline，另完成 W11 | 依確認的排序及公平性規則比較結果 | 67，約 14 週 | 75.75 h |
| M3：研究實驗框架，另完成 W12–W13 | 核對模型與場景，先跑 Baseline，量測實驗成本 | 83，約 17 週 | 92.25 h |
| M4：CLM 比較及最終交付，另完成 W14–W15 | 既有 CLM 接入，同等資訊下完成對照與重跑文件 | 93，約 19 週 | 104.75 h |

以上是假設相關決策及必要資料能在設計活動內取得的排程；M3／M4 若缺校準依據，就保留模型限制，不宣稱研究可信度已通過。M2 的日程依建議執行次序，並非說 W12 在技術上必須等待 W11。

## 文件閱讀順序

Notebook 設計：[資源時間表逐 cell 原型計畫](../docs/architecture/resource-timeline-notebook-plan.md)，包含導讀順序、範例輸入與驗收情境；[Notebook 原始骨架](../notebooks/03_resource_timeline.ipynb)已補齊核心與示範，等待人工導讀接受。


已整合至既有設計：[600 ms 資源時間表契約](../docs/architecture/resource-timeline-design.md)，包含資料流、事件與通道介接邊界。


資源時間表：[UE／DU 時序完整草案](resource-timeline-draft.md)。共用外層窗口與獨立抽樣已定案；情境間隔數值、實作及驗收仍待完成。


最新設計入口：[原始模型與剩餘設計盤點](design-resumption.md)（2026-10-31）。通道已完成本地人工接受與抽離；下方較早的「待接受」描述保留為歷史脈絡。


目前通道討論入口：[共址背散射與有限碼長公式依據](channel-formula-evidence.md)（2026-10-25）。已選參數來源策略A，公式組合及正式數值仍待接受。

2026-10-29更新[通道模型整合草案](channel-model-draft.md)。已選功率表優先。[鏈路對照](channel-link-binding.md)說明功率、通道計算與接收規則的綁定。實際參數及校準範圍仍待確認。

準備開發時，先讀[通道開發起始表](channel-entry-pack.md)。它包含候選數值、距離方案及已核對的FBL算例。整份仍待接受。

1. [範圍與各模組](01-scope-and-modules.md)：用途、輸入／輸出、對應情境及剩餘決策。
2. [估算與人力容量](02-estimates-and-capacity.md)：三點估算、工時組成、容量與等待敏感度。
3. [AOA、關鍵路徑與進度控制](03-aoa-and-control.md)：CPM 計算、浮時、人工關卡及變更管理。
4. [風險與下一個決策](04-risks-and-decisions.md)：何時需要您決策、何時應停止推進。

## 可重算的排程資料

| 檔案 | 內容 |
|---|---|
| [schedule.json](schedule.json) | 唯一排程輸入：15 個工作包、各階段三點工時、相依及容量 |
| [work-packages.csv](work-packages.csv) | 工作包工時與建議起訖日 |
| [activities.csv](activities.csv) | 90 個實際活動的樂觀／最可能／悲觀值、期望工時與參與者 |
| [cpm.csv](cpm.csv)／[events.csv](events.csv) | 主網路 ES／EF／LS／LF／TF／FF 及事件 E／L |
| [aoa-detail.csv](aoa-detail.csv) | 展開人工接受等關卡的 90 個活動＋7 個虛活動，含完整 CPM |
| [resource-schedule.csv](resource-schedule.csv) | 逐活動排程；小時軸中每 24 單位表示一個工作日，夜間跳過，沒有週末日期映射 |
| [summary.json](summary.json) | 主要計算結果與敏感度 |
| [recalculate.py](recalculate.py)／[render_schedule.py](render_schedule.py) | 重算與繪圖；只處理 Plan，不操作模擬器或遠端 |

```bash
python Plan/recalculate.py
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/pynet-plan-mpl python Plan/render_schedule.py
```

- CSV 使用 UTF-8 BOM，便於試算表閱讀；重新執行會覆寫上述衍生資料及三張 SVG。
- 本計畫只新增規劃文件與計算工具，沒有啟動通道程式實作或建立遠端 Issue／PR。
- 後續實作需求與驗收仍歸 OpenSpec；本目錄管理範圍、工期與相依，不取代產品需求。
- 產品規劃留於 `Plan/`；人工導讀紀錄、工具收據與訪談延續既定的本機 agent worktree 分工。

# IAB 拓撲模組：Config／DTO與Notebook設計草案

更新：2026-10-23。**最新狀態：拓撲Notebook與測試已實作／驗證，待人工理解與接受，尚未抽離.py。** 本文以下保留原設計草案與規劃tree；實際現況以[code-trace](code-trace.md)及 `AgentDoc/openspec/changes/add-iab-topology-notebook/` 的OpenSpec／validation為準，不將歷史「未實作」描述當成目前狀態。沿用[已確認範圍](iab-topology-scope.md)與[剩餘項盤點](iab-topology-remaining-decisions.md)。

## 實作規劃架構圖

[以 Archify 開啟 Notebook 原型與驗收架構](../../.archify/architecture-iab-topology-20261023-131337/iab-topology.html)。這是根據本文件與訪談繪製的設計圖，不是現有程式呼叫關係或模擬器驗證成果。涵蓋設定、驗證、生成、快照、情境測試、表／圖、人工接受及抽離.py；Channel／EH列後續邊界。

## 模組入口與責任

建議唯一生成入口為 `build_topology(config) -> TopologySnapshot`。呼叫端不需管理分配中間狀態；生成器自行驗證Config、分配Tag歸屬／分區、產生座標及檢查結果。

資料流：Notebook設定cell建立Config → 驗證 → 局部亂數生成 → 建立靜態快照 → 驗證 → 同一份快照產生表格及部署圖。這是流程說明，尚無對應可執行函式。

首版只處理平面水平幾何與連線歸屬：1 Donor直連5 Nodes，各1 UE；UE只有ID及所屬Node，沒有物理座標。Tag先關聯Node／分區再生成位置；不加入移動、切換、排程、UE傳播或虛構SNR。近區品質優於遠區及完美消除自身CW自干擾保留為後續Channel的已定約束。

## 固定座標示例（工程草案）

單位m，x／y是示例平面，不代表真實農場經緯度；座標可由Config替換。Donor位置不自動推導回傳品質或容量。

| 元件 | x | y |
|---|---:|---:|
| Donor-1 | 120 | -120 |
| Node-1 | 0 | 0 |
| Node-2 | 120 | 0 |
| Node-3 | 240 | 0 |
| Node-4 | 60 | 120 |
| Node-5 | 180 | 120 |

任兩Node最短間距120 m，大於兩個50 m部署半徑之和100 m。五個區域不重疊，最小間隙20 m。圖框由五個圓域與Donor位置外加顯示留白推得，不額外裁切Tag位置。UE可在獨立邏輯關聯表顯示；不以排版圖示冒充真實座標。

## 最小dataclass草案

名稱是工程提案。Notebook階段在宣告cell定義；取得人工理解與接受後，Config／DTO／必要Enum一起移入單一共用 `.py`，不提前分散至多個檔案。

| 型別 | 建議欄位 | 用途 |
|---|---|---|
| `Position2D` | `x_m`, `y_m` | 有限值的平面公尺座標 |
| `FixedNodeConfig` | `node_id`, `position` | 固定站點資料；由Config中的donor或iab_nodes位置區分角色，不另建重複的Donor／IAB類別 |
| `TopologyConfig` | `donor`, `iab_nodes`, `zone_outer_radii_m`, `zone_tag_counts`, `min_tags_per_node`, `seed` | 預設案例5 Nodes、半徑(10,30,50)、配額(10,13,7)、每Node至少2個；具體seed為示例設定，記錄於快照 |
| `UERecord` | `ue_id`, `parent_node_id` | 一個Node對應一個UE，不加假座標 |
| `TagRecord` | `tag_id`, `parent_node_id`, `zone`, `position` | 可供後續Channel使用的Tag幾何與歸屬 |
| `TopologySnapshot` | `config`, `ues`, `tags` | 不可變的生成結果；保存完整生成設定，後續政策不修改真值 |

`TagZone`可為只有NEAR／MID／FAR的Enum；`zone_outer_radii_m`及`zone_tag_counts`固定依此順序。Tag總數由三區數量相加，不再加入可互相矛盾的獨立total。Node角色與回傳父節點由已定星狀配置推得，不先設計通用多跳圖。

快照及內含資料建議用frozen dataclass與tuple，避免只凍結外層卻留下可修改list。Config驗證仍需顯式執行，dataclass的型別註記不等於執行期驗證。Tag距離、Node計數與連線表由快照推導，不另存可能失去同步的重複欄位；輸出包含5條回傳、5條UE歸屬及每Tag一條接入關係。

## 有限步驟的隨機生成草案

1. 驗證ID、角色數量、有限座標、半徑正值且遞增、三區計數為非負整數、seed型別及每Node最少數量。拒絕bool冒充整數、非整數計數、重複ID、Tag總數不足以及Node部署圓重疊；不能無限重抽以掩蓋不可行配置。
2. 建立局部 `random.Random(seed)`，不改全域亂數狀態。建立具有精確三區名額的Tag清單並隨機打散。
3. 從清單中取出每Node所需最少名額，隨機歸屬到各Node；其餘Tag獨立抽Node。保留每Tag原區域名額，故全場配額精確不變。這是一種明確的生成分布，不宣稱在所有合法分配方式間均勻。
4. 在每Tag所屬Node的對應環帶按面積均勻取樣。設內／外半徑a／b，取U於(0,1]、角度於[0,2π)，使用 `r=sqrt(a*a+U*(b*b-a*a))` 再轉x／y；不直接把r均勻抽樣。近區a=0但排除r=0，這不是對極近距離傳播有效性的聲明。
5. 依Node建立一個UE的邏輯歸屬，建立不可變快照，核對歸屬、數量、距離及三區名額後回傳。使用相同資料產生表與圖，不各自重抽位置。

Config合法性錯誤應給具體原因；生成結果若違反不變量，須明確失敗，不悄悄修正Tag分區或放寬每Node最少數量。浮點幾何邊界的比較／容差應統一並寫入案例，不將容差變成跨區部署自由度。保存快照是重現證據，單靠seed不保證未來不同版本演算法產生相同結果。

## Notebook閱讀順序

| Cell群組 | 讀者應理解的內容 |
|---|---|
| 1 模型與單位 | 已確認假設、此模組輸入／輸出及品質限制 |
| 2 Config／DTO | dataclass／Enum及每個欄位的用途 |
| 3 固定設定 | 上述座標示例、分區配額、seed；列出完整設定 |
| 4 驗證與生成 | 入口、配額分配、面積取樣與快照的關係 |
| 5 結果 | Node／UE歸屬表、Tag座標／分區／距離表、全場與各Node計數 |
| 6 部署圖 | Donor／Node／Tag及三區邊界；UE沒有物理座標 |
| 7 情境驗收 | 對應需求的assert及清楚結果，不以圖畫得出來當成通過 |
| 8 人工導讀 | 資料如何流過每段程式；人工接受前不抽離.py |

依實際環境核對Python、Jupyter與Matplotlib可用性，優先現有套件；只為拓撲不引入NetworkX。模組最終路徑及共用 `.py` 檔名沿用專案布局，在正式任務中具體記錄，不在本文冒稱已存在。

## 最小情境驗收草案

| 情境 | 必須核對 |
|---|---|
| 正常30 Tag例子 | 1 Donor／5 Nodes／5 UE／30 Tags，三區10／13／7，各Node至少2個，無漏配／重複歸屬 |
| 最少可行數量 | 10 Tags時五個Node各2個；9 Tags拒絕；單區配額0仍合法，不要求各Node每區皆有Tag |
| 幾何 | 示例Node最短間距120 m，圓域不重疊；已知座標核對水平距離 |
| 分區邊界 | d=0拒絕；10屬近區、30屬中區、50屬遠區；各邊界內外案例、超50及非法遞增半徑 |
| 非法輸入 | 重複／空ID、錯誤Node數、NaN／Inf座標、負或非整數配額、無效seed、最少數量不符；負座標本身合法 |
| 面積取樣 | 以可控亂數值核對半徑平方插值與邊界；不以單一小樣本直方圖當作分布校準 |
| 重現與隔離 | 同設定／seed同結果，不改全域RNG；輸入或Policy端不能改既有快照；圖表對應同一份結果 |
| Notebook | 乾淨kernel從頭執行，情境斷言通過，提供完整程式路徑及人工trace |

近區SNR優於遠區由後續Channel測試驗證；本模組沒有品質數值，不寫空泛的SNR通過宣告。現階段沒有執行上述測試，示例座標僅做幾何算術核對。

## 預計程式tree與人工接受方式

以下是本次說明提出的工程路徑草案；目前只有設計文件與Archify圖已存在，Notebook、src、tests及code-trace均未建立。保留既有AgentDoc／ReferDoc／TutorialDoc，不搬動或改名。

```text
PY_NetworkSimulator/
├── notebooks/                         # 待建：原型與人工閱讀入口
│   └── 01_iab_topology.ipynb           # 待建：定義→設定→生成→測試→表／圖
├── src/                               # 人工接受Notebook後建立
│   └── network_simulator/
│       ├── __init__.py                # 套件入口
│       ├── contracts.py               # 所有共用Config／DTO／必要Enum
│       ├── topology.py                # 驗證、配額／位置生成、快照
│       └── plotting.py                # 同一快照的表格整理與部署圖
├── tests/                             # 抽離後沿用Notebook相同情境
│   └── test_topology.py
├── docs/architecture/                 # 已存在
│   ├── iab-topology-design.md          # 本設計文件，已存在
│   └── code-trace.md                   # 人工導讀前建立，附絕對路徑與測試對照
└── .archify/                           # 已存在：架構圖及檢查收據
```

Notebook階段把Config／DTO與各函式依責任放在不同cell，先不建立以上.py。接受並抽離後，Notebook改為import共用實作再執行相同示例，不保留兩套手動同步的正式演算法。表格整理先用標準Python資料，圖用已可用的Matplotlib；實際環境待原型執行前核對，不為表格另加依賴。

### 表格與部署圖的實際內容

- 設定摘要：固定座標、三區邊界、全場配額、每Node最少數量與seed。
- Node摘要表：Node ID、x／y、Donor父節點、UE ID、三區Tag數與總數；全場合計核對配額。
- Tag明細表：Tag ID、所屬Node、x／y、水平距離、近／中／遠區；不輸出未計算的SNR／BER。
- 連線／歸屬表：5條Donor→Node、5條Node→UE及每個Tag唯一Node歸屬；UE沒有物理座標。
- 二維部署圖：等比例公尺座標軸、Donor與五Node、各Node的10／30／50 m同心邊界、Tag散點與清楚的分區／歸屬圖例、Donor–Node連線。UE用獨立關聯表呈現，不畫假物理位置。顏色表示距離分區，不假稱為量測SNR。
- 表與圖都從同一快照產生，不重新抽Tag；同一設定與seed重跑時數量、歸屬與座標一致。

人工驗收可使用以下示意配額表理解隨機但受約束的結果；這不是程式已跑出的結果，也不是指定各Node的固定配額：

| Node | 近 | 中 | 遠 | 合計 |
|---|---:|---:|---:|---:|
| 1 | 2 | 2 | 0 | 4 |
| 2 | 3 | 3 | 2 | 8 |
| 3 | 1 | 3 | 1 | 5 |
| 4 | 2 | 3 | 2 | 7 |
| 5 | 2 | 2 | 2 | 6 |
| 全場 | 10 | 13 | 7 | 30 |

### 人工接受的具體流程

1. 代理先完成Notebook與對應自動情境測試，重啟kernel由頭執行，修正範圍內失敗；提供完整輸入、結果與實際測試狀態。
2. 更新架構與tree式code-trace：每個實作檔絕對／相對路徑、責任、需求／測試對照及可點選位置。Notebook cell以標題／穩定識別導讀，不偽造.py行號。
3. 逐段帶使用者閱讀Config／DTO→輸入驗證→歸屬配額→面積取樣→快照→測試→表／圖。以一個Tag追蹤其所屬Node、分區、座標及距離，解釋每步輸入／輸出及錯誤行為。
4. 使用者可修改seed或配額觀察變化，確認精確總數、每Node至少2個、位置落在正確環帶；同seed重現不是只看圖形相似。原型測試與說明應讓使用者理解程式，不要求使用者代替代理找完缺陷。
5. 使用者提出程式或模型疑問時，先解釋／修正，再跑受影響情境，提供差異；問題未解決前不宣稱接受。
6. 使用者明確表示理解並接受此版本Notebook後，才抽離contracts.py／topology.py／plotting.py；讓Notebook import抽離實作，再跑同設定／seed及相同情境，核對Tag歸屬、分區、座標、統計及錯誤行為等價。若改動模型／可觀察行為，須重新處理受影響的人工接受。

這是模組級理解與接受；不等於OpenSpec工作流已歸檔、PR已合併或整體模擬器／Channel科學有效性已驗證。當前沒有上述Notebook／程式／測試／人工接受證據。

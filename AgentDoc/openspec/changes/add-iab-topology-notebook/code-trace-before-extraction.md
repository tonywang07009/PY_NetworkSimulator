# IAB拓撲原型 code trace：待人工理解與接受

## 版本與範圍

- Change：add-iab-topology-notebook；日期2026-10-23。
- 專案絕對根目錄：`/home/tonywang/Net_simluation/PY_NetworkSimulator`。
- 原change位置：`/home/tonywang/Net_simluation/PY_NetworkSimulator/AgentDoc/openspec/changes/add-iab-topology-notebook`；尚未archive，沒有最終archive路徑。
- 固定Git基準：0a5ff65f151febb53416d67855afa9850e2b1b13。實作是未commit工作區，不以HEAD冒充此版本；[版本指紋](source-manifest.json)保存Notebook、測試、執行器及主要結果的SHA-256。
- 既有README／LICENSE及工作流未追蹤修改保留，不屬本次清理／review。Issue／PR未發布，沒有URL／merge證據；[Issue草稿](issue-draft.md)不是遠端Issue。

閱讀順序：[整體圖](../../../../docs/architecture/system.html) → [本模組架構](architecture.html) → 下方Config／DTO → 生成 → 測試 → 表／圖。先交付完整文件，再一段一段討論，不要求一次接受全部程式。

## 實際檔案tree（範圍化，省略無關分支）

```text
/home/tonywang/Net_simluation/PY_NetworkSimulator/
├── AGENTS.md -> agent.md                    # 既有入口
├── agent.md                                # 既有專案規則
├── .gitignore                              # 保留原規則，追加執行暫存
├── notebooks/
│   ├── 01_iab_topology.ipynb                # 新增：本次業務實作及已執行結果
│   └── artifacts/iab-topology/
│       ├── snapshot.json                   # 完整設定＋UE＋Tag結果
│       ├── settings.csv                    # 設定摘要
│       ├── nodes.csv                       # Node三區數量及UE歸屬
│       ├── tags.csv                        # Tag座標／距離／分區
│       ├── links.csv                       # 5回傳＋5 UE歸屬＋30 Tag接入
│       ├── deployment.png                  # 已檢視部署圖
│       └── deployment.svg                  # 可縮放部署圖
├── tests/
│   ├── test_topology_notebook.py            # 新增：公開入口情境測試
│   └── execute_topology_notebook.py         # 新增：乾淨kernel執行及清理
├── docs/architecture/
│   ├── system.archify.json / system.html    # 整體架構與來源
│   ├── iab-topology-design.md               # 設計與規劃沿革
│   └── code-trace.md                        # 指向本份權威導讀
└── AgentDoc/openspec/
    ├── PROGRESS.md / HANDOFF.md             # 目前狀態與下次進入點
    └── changes/add-iab-topology-notebook/
        ├── .openspec.yaml / proposal.md     # change識別／範圍
        ├── design.md / tasks.md             # 技術方案／任務
        ├── specs/iab-topology/spec.md       # 權威需求
        ├── architecture.archify.json       # 本模組圖來源
        ├── architecture.html               # 本模組互動架構圖
        ├── code-trace.md                    # 本文件
        ├── review.md / validation.md        # 審查與執行證據
        ├── notebook-execution.json          # 11 cells／0 errors／kernel已關閉
        ├── pytest-results.txt               # 69 passed
        ├── tdd-evidence.md / tdd-red-*.log    # 真實RED／GREEN沿革
        ├── source-manifest.json             # 此工作區版本指紋
        ├── issue-draft.md                   # 未發布的草稿
        └── architecture-visual/             # 瀏覽器截圖／收據（已存在）
```

圖的finalize／browser／delivery旁檔與system-topology-review／system-topology-visual在實際目錄存在，為節省tree篇幅未逐檔展開。`src/network_simulator/`尚不存在；正式.py未抽離，不能把未來目錄列成既有實作。

## 檔案用途與實際路徑

| 檔案 | 專案相對路徑 | 絕對capture路徑 | 用途／狀態 |
|---|---|---|---|
| [01_iab_topology.ipynb](/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/01_iab_topology.ipynb) | `notebooks/01_iab_topology.ipynb` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/01_iab_topology.ipynb` | 新增；所有業務定義、示例、教學情境與執行結果 |
| [test_topology_notebook.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/test_topology_notebook.py) | `tests/test_topology_notebook.py` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/test_topology_notebook.py` | 新增；69個公開入口情境案例及Notebook載入fixture |
| [execute_topology_notebook.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/execute_topology_notebook.py) | `tests/execute_topology_notebook.py` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/execute_topology_notebook.py` | 新增；暫存kernelspec／乾淨kernel／清理及執行收據 |
| [spec.md](/home/tonywang/Net_simluation/PY_NetworkSimulator/AgentDoc/openspec/changes/add-iab-topology-notebook/specs/iab-topology/spec.md) | `AgentDoc/openspec/changes/add-iab-topology-notebook/specs/iab-topology/spec.md` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/AgentDoc/openspec/changes/add-iab-topology-notebook/specs/iab-topology/spec.md` | 新增；權威需求／驗收 |
| [design.md](/home/tonywang/Net_simluation/PY_NetworkSimulator/AgentDoc/openspec/changes/add-iab-topology-notebook/design.md) | `AgentDoc/openspec/changes/add-iab-topology-notebook/design.md` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/AgentDoc/openspec/changes/add-iab-topology-notebook/design.md` | 新增；接口／TDD／數值端點設計 |
| [tasks.md](/home/tonywang/Net_simluation/PY_NetworkSimulator/AgentDoc/openspec/changes/add-iab-topology-notebook/tasks.md) | `AgentDoc/openspec/changes/add-iab-topology-notebook/tasks.md` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/AgentDoc/openspec/changes/add-iab-topology-notebook/tasks.md` | 新增；實際任務進度 |
| [review.md](/home/tonywang/Net_simluation/PY_NetworkSimulator/AgentDoc/openspec/changes/add-iab-topology-notebook/review.md) | `AgentDoc/openspec/changes/add-iab-topology-notebook/review.md` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/AgentDoc/openspec/changes/add-iab-topology-notebook/review.md` | 新增；Standards／Spec／debt及修正 |
| [validation.md](/home/tonywang/Net_simluation/PY_NetworkSimulator/AgentDoc/openspec/changes/add-iab-topology-notebook/validation.md) | `AgentDoc/openspec/changes/add-iab-topology-notebook/validation.md` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/AgentDoc/openspec/changes/add-iab-topology-notebook/validation.md` | 新增；執行／環境／接受狀態 |
| [source-manifest.json](/home/tonywang/Net_simluation/PY_NetworkSimulator/AgentDoc/openspec/changes/add-iab-topology-notebook/source-manifest.json) | `AgentDoc/openspec/changes/add-iab-topology-notebook/source-manifest.json` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/AgentDoc/openspec/changes/add-iab-topology-notebook/source-manifest.json` | 新增；工作區版本與結果SHA-256 |
| [architecture.html](/home/tonywang/Net_simluation/PY_NetworkSimulator/AgentDoc/openspec/changes/add-iab-topology-notebook/architecture.html) | `AgentDoc/openspec/changes/add-iab-topology-notebook/architecture.html` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/AgentDoc/openspec/changes/add-iab-topology-notebook/architecture.html` | 新增；本change實作與接受邊界圖 |
| [system.html](/home/tonywang/Net_simluation/PY_NetworkSimulator/docs/architecture/system.html) | `docs/architecture/system.html` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/docs/architecture/system.html` | 修改；整體圖明示拓撲已驗證、其餘為規劃 |
| [agent.md](/home/tonywang/Net_simluation/PY_NetworkSimulator/agent.md) | `agent.md` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/agent.md` | 既有支援；專案規則 |
| [.gitignore](/home/tonywang/Net_simluation/PY_NetworkSimulator/.gitignore) | `.gitignore` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/.gitignore` | 追加Python／Notebook暫存ignore；保留既有內容 |
| [deployment.png](/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/artifacts/iab-topology/deployment.png) | `notebooks/artifacts/iab-topology/deployment.png` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/artifacts/iab-topology/deployment.png` | 新增；同一快照的實際匯出結果 |
| [deployment.svg](/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/artifacts/iab-topology/deployment.svg) | `notebooks/artifacts/iab-topology/deployment.svg` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/artifacts/iab-topology/deployment.svg` | 新增；同一快照的實際匯出結果 |
| [links.csv](/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/artifacts/iab-topology/links.csv) | `notebooks/artifacts/iab-topology/links.csv` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/artifacts/iab-topology/links.csv` | 新增；同一快照的實際匯出結果 |
| [nodes.csv](/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/artifacts/iab-topology/nodes.csv) | `notebooks/artifacts/iab-topology/nodes.csv` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/artifacts/iab-topology/nodes.csv` | 新增；同一快照的實際匯出結果 |
| [settings.csv](/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/artifacts/iab-topology/settings.csv) | `notebooks/artifacts/iab-topology/settings.csv` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/artifacts/iab-topology/settings.csv` | 新增；同一快照的實際匯出結果 |
| [snapshot.json](/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/artifacts/iab-topology/snapshot.json) | `notebooks/artifacts/iab-topology/snapshot.json` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/artifacts/iab-topology/snapshot.json` | 新增；同一快照的實際匯出結果 |
| [tags.csv](/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/artifacts/iab-topology/tags.csv) | `notebooks/artifacts/iab-topology/tags.csv` | `/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/artifacts/iab-topology/tags.csv` | 新增；同一快照的實際匯出結果 |

## 第一段：Config／DTO

Notebook `contracts` cell是共用資料的單一宣告處；之後才移至contracts.py。

| 型別／欄位 | 型別／單位 | 使用方式 |
|---|---|---|
| Position2D.x_m／y_m | float或int，m | 平面座標；有限值，負數合法 |
| FixedNodeConfig.node_id／position | str／Position2D | 固定Donor／IAB站點 |
| TopologyConfig.donor／iab_nodes | FixedNodeConfig／tuple | 明列1 Donor與5 Nodes |
| zone_outer_radii_m | 3個正遞增數值，m | 預設(10,30,50)，水平分區 |
| zone_tag_counts | 3個非負整數 | 預設(10,13,7)，總數由和推得 |
| min_tags_per_node／seed | int／int | 最低>=2，局部RNG種子；bool不當整數 |
| UERecord | ue_id／parent_node_id | 沒有position，不推導UE射頻干擾 |
| TagRecord | tag_id／parent_node_id／zone／position | 結果幾何與唯一歸屬 |
| TopologySnapshot | config／ues／tags | frozen資料與tuple，不讓Policy改寫真值 |

Config是輸入，Snapshot是輸出；Tag距離／連線／統計在呈現時推導，不另建一套可能失去同步的數值。輸入型別註記不是驗證，下一段的公開生成入口會驗證。你可先針對此段提出問題；目前尚未取得這一段或整份Notebook的人工接受。

## 第二段：生成與拒絕

已檢視實際呼叫流：`run-example` → `example_config(seed=42)` → `build_topology` → `validate_config` → 局部`random.Random` → 精確區域名額／最低Node名額 → `_position_in_ring` → UERecord／TagRecord → TopologySnapshot。

`distance` cell處理有限值及`classify_distance`；`validation` cell檢查輸入、ID／Node數／配額／重疊。生成不寫檔；非法設定以ValueError回報原因。局部RNG不修改全域狀態。面積取樣不等於均勻半徑，數值端點只作明示的8ulp內修正，結果仍須屬原環帶；不靠無限重抽。

## 第三段：測試與呈現

`tests/test_topology_notebook.py`的fixture只載入標記definitions的code cells，與Notebook使用同一程式；不載入展示副作用。pytest覆蓋正常、最少數量、空分區、邊界、輸入拒絕、ID碰撞、數值溢位、面積取樣、不可變性、RNG、表圖及匯出。

Notebook `scenario-checks`再以公開入口演示8個教學情境。`topology_tables`從快照推導四表；`plot_topology`畫15個圓、36個有物理位置的點（1 Donor＋5 Nodes＋30 Tags）與5條回傳連線；UE僅在歸屬表。`export_topology`寫同一快照JSON、四CSV與PNG／SVG。

實際seed42各Node總數為8／3／8／5／6，全場近10／中13／遠7，沒有強制各6。查看[Node表](../../../../notebooks/artifacts/iab-topology/nodes.csv)、[Tag表](../../../../notebooks/artifacts/iab-topology/tags.csv)、[部署圖](../../../../notebooks/artifacts/iab-topology/deployment.png)。可選一Tag手算其所屬Node距離，再對照分區。

## 需求→實作→測試／證據

[權威規格](specs/iab-topology/spec.md)的逐項對照、代理review與修正見[review](review.md)；[validation](validation.md)保留命令、環境及限制。

| 驗收 | 實作cell／入口 | 測試或原始證據 | 狀態 |
|---|---|---|---|
| 星狀／精確配額 | builder／build_topology | test_builds_exact_global_quotas_and_one_ue_per_node、minimum_count | 通過 |
| 分區與面積 | distance／builder | classify_horizontal_distance、samples_annulus_by_area、rng_endpoint | 通過 |
| 拒絕／不可變／隔離 | contracts／validation／builder | invalid_config、duplicate_ids、snapshot_immutable、global_rng、geometry_difference | 通過 |
| 同快照表圖 | tables／plot／export | tables_preserve、plot_draws_real_geometry、exports_same_snapshot | 通過 |
| 乾淨kernel／清理 | execute_topology_notebook.py | notebook-execution.json | 11 code cells、0 errors、kernel_shutdown=true |
| 整體／change架構 | 兩份Archify來源及HTML | 兩份finalize收據；兩份visual-check收據 | 自動檢查通過；代理檢視兩張桌面截圖 |
| 人工理解／接受 | 本trace＋Notebook完整內容 | 使用者明確回饋 | 尚未接受 |
| .py抽離／等價性 | 未開始 | 無 | 待人工接受後 |

所有測試於`/home/tonywang/Net_simluation/PY_NetworkSimulator`執行；pytest最終69 passed，Notebook真實執行使用RL環境Python3.11.15。base Python3.12用於pytest。重跑方式在validation.md，沒有替換或安裝系統套件。

## 第四段：人工接受與後續停止點

由第一段Config／DTO開始，逐段解釋並回應問題。模型／程式修改後重跑受影響檢查，更新圖與trace。明確接受此Notebook版本前，不建立正式src模組；接受後抽離.py並以同seed／配額／情境核對等價。這次交付不是merge或workflow完成；沒有冒充已接受。缺少遠端發布授權時繼續保留具體草稿，待實際發布前才處理該授權。

## 人工導讀進度（2026-10-23）

使用者已要求開始導讀。第一小段從contracts cell的Position2D、FixedNodeConfig與frozen dataclass開始，以Node-1=(0,0)說明巢狀資料。先建立資料定義與實體運作的責任界線，再讀TopologyConfig、__post_init__及生成結果DTO。此為導讀進行中，不等於使用者已接受本段或整份Notebook；tasks 3.3維持未完成。沒有修改業務程式或重跑無關測試。

### 第一小段已確認，接續TopologyConfig

使用者在釐清frozen dataclass允許初始化、不允許一般後續欄位賦值後，明確表示本段OK並要求繼續。僅記Position2D／FixedNodeConfig／初始化概念已理解；不推定整份Notebook已接受。下一小段說明TopologyConfig六項設定、三區順序、總數推導與__post_init__的tuple整理。

### TopologyConfig導讀回饋：統一tuple，移除轉換

使用者選第三種，要求README註記；已修訂規格與實作，移除__post_init__，三個集合欄位只接受tuple。下方不是自動轉換：build_topology會拒絕list。先前導讀中的list轉tuple說明為歷史版本，不再適用。

[README輸入規則](../../../../README.md)已追加說明，保留原文。69 tests／完整kernel通過；快照結果不變。當前使用者HEAD為a87a2d8effcbd6986c1aaad545d529df2ae26c75，本輪修改仍未commit，沒有更動使用者暫存區。原Git基準保留為初版歷史，不用它冒稱新版本內容。第一小段座標／固定站點已理解；Config此次簡化尚待後續閱讀，不推定整份已接受。

### 導讀轉入第2節：水平分區與輸入驗證

使用者要求直接導讀第2節。已讀實際distance／validation cells；本輪先列四函式分工，再說明_finite_number的型別／有限值／bool與溢位處理。強調有限數值檢查允許0及負數，座標與距離／半徑的領域限制由呼叫端驗證。其餘_validate_radii／classify_distance／validate_config分段續讀；不因轉節推定尚未逐段閱讀的DTO或整份Notebook已接受。無業務程式修改。

### validate_config導讀與排版偏好

使用者要求獨立if驗證區塊間留一空行；規則落於agent.md，已套用validation cell，AST不變，69 pytest通過。本輪先說明函式的檢查順序與設定／站點／ID檢查，再續讀配額、保留ID與幾何；未推定整份Notebook已接受。

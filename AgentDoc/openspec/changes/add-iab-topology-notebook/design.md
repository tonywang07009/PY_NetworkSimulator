## Context

依已確認訪談與docs/architecture/iab-topology-design.md實作；原庫尚無模擬器程式，不重造現有工具。Git基準HEAD為0a5ff65f151febb53416d67855afa9850e2b1b13，既有README／LICENSE等修改保留。首個交付物為Notebook，人工接受前不建立src正式模組。

## Goals / Non-Goals

Goals：靜態平面生成、精確配額、不可變快照、可重現表／圖與公開入口情境測試。Non-Goals：移動、切換、多跳、UE物理座標、SNR／BER／EH、資源排程、正式模組抽離及遠端發布。

## Decisions

- 所有業務定義在Notebook標記definitions的cell；測試harness載入同一cell，不複製正式實作。測試.py僅為基礎設施，不算提前抽離模組。公開seam為build_topology(config)、classify_distance、topology_tables、plot_topology與export_topology。
- 標準庫frozen dataclass／tuple封裝Position2D、FixedNodeConfig、TopologyConfig、UERecord、TagRecord、TopologySnapshot與TagZone。集合設定只接受tuple，不做list轉換，不使用__post_init__；快照深層不可變；顯式ValueError驗證在build_topology入口執行。
- 用局部random.Random(seed)。Tag區域名額打散後，先隨機分派每Node最少名額，再把剩餘Tag隨機分派；不是在所有合法分配間均勻。用環帶面積取樣生成位置；用浮點可表示性／容差核對，不偷偷改分區。
- 表與圖從快照推導，Tag距離／連線／計數不重複保存。JSON完整記錄config及結果、CSV保存表、PNG／SVG保存部署圖。展示文字使用繁中，既有Matplotlib字型若缺中文字則圖中使用清楚英文ID／數字及中文Notebook說明。
- 原base Python有pytest／Matplotlib但無Notebook套件；mcp環境metadata有Notebook套件但kernel實際啟動缺decorator，未視為可用。現有RL Conda環境已實際import IPython／nbclient／ipykernel／Matplotlib。優先重用base測試與RL Notebook環境，不安裝套件／改使用者kernel。執行時以專案暫存kernelspec指定既有RL Python。
- 範例座標：Donor(120,-120)，Nodes(0,0),(120,0),(240,0),(60,120),(180,120)，半徑(10,30,50)，配額(10,13,7)，最低2。圖框由資料外緣推導。seed選工程示例42，不是物理參數。
- 新增tests/test_topology_notebook.py；適當細分TDD垂直slice，public seam測試不綁定分配中間呼叫順序。Notebook包含可直接執行的教學情境摘要，pytest提供完整邊界覆蓋。
- 未獲遠端授權，Issue／PR僅本機草稿。workflow保持github契約，不以未發Issue偽造apply／review狀態；索引先保持spec，進度／驗證證據於本change記錄，待授權再同步。

## Risks / Trade-offs

- [Notebook無法在base環境執行] → 使用已檢查的RL環境，記錄絕對Python路徑與實際版本，建立本地kernelspec，實測乾淨kernel。
- [浮點邊界] → classify_distance採精確排他／含上界；生成檢查允許明示微小幾何計算誤差，不允許跨區或零距離；不可表示幾何明確失敗。
- [seed跨版本不保證同結果] → 保存完整快照與環境版本，重現性聲明限同實作。
- [已忽略AgentDoc／docs] → 本機保留權威OpenSpec與證據；遠端前須處理可讀性，不擅改既有ignore或發布範圍。

## TDD contract

- Model / effort：沿用使用者目前模型與effort，未切換；未暴露精確值不臆測。
- Test boundary：Notebook公開生成／分區／表圖／匯出入口，與Notebook呼叫端共用程式。
- Acceptance links：specs/iab-topology/spec.md全部requirements；review.md保留對照。
- Irreversible side effects：無。生成為記憶體運算；匯出只寫指定本地路徑；測試用tmp_path。無網路／遠端發訊息。
- Boundary gate：clear，依使用者已確認訪談及本次開始授權。
- Test files：tests/test_topology_notebook.py，Notebook情境cell。
- Test evidence：validation.md與tdd-evidence.md記實際RED／GREEN、命令、結果及限制。

## Migration Plan

先Notebook與測試、檢查、架構及導讀。停在人工接受，未接受不抽離.py／sync／archive／PR。後續接受後抽離再跑同情境；無既有正式API需遷移。

## Open Questions

拓撲模型無未決題。人工程式接受、遠端發布及後續Channel參數仍待其既定階段，不阻擋本機原型。

## Review修正的數值端點

面積抽樣公式不變；若座標運算造成邊界距離僅在8個相關ulp內越界，僅向原環帶內側作有界數值修正，實際結果仍須通過原排他／含上界條件。不放寬分區、不重抽；無法表示的幾何仍拒絕。站點間距計算的OverflowError轉為公開入口ValueError。依已核准浮點／拒絕行為補齊，沒有更改模型排序或PHY要求。

## 人工導讀回饋：tuple唯一格式

使用者選擇集合設定直接輸入tuple，要求README註記；移除__post_init__便利轉換，以既有build_topology輸入驗證拒絕list。這是已授權輸入契約修正，更新對應測試，不保留舊自動轉換驗收。保留使用者其餘Notebook註解，不抽離正式.py。

## 人工導讀格式規則

使用者要求獨立if驗證區塊之間空一行，已記入專案agent.md並套用Notebook validate_config；保留if/elif/else關係與使用者註解。此次為排版，AST前後一致，無行為／驗收變更。

## 人工接受後抽離（2026-10-23）

使用者明確表示主要邏輯已理解，要求打包.py後討論ReferDoc說明結構；task3.3接受成立，抽離介面沿用既有設計。contracts.py集中全部dataclass與TagZone；topology.py負責驗證、生成、表格與匯出，plotting.py負責圖形。Notebook改為import，保留教學Markdown、設定與展示情境。

抽離TDD邊界：正式模組的公開build_topology／topology_tables結果，對照抽離前實際Notebook四個場景的extraction-baseline.json；保存完整notebook-before-extraction.ipynb作歷史來源。既有69案例同時覆蓋Notebook import入口及正式模組。沒有新增模型、外部服務或不可逆操作；匯出仍只寫指定本地路徑。測試檔tests/test_topology_extraction.py、tests/test_topology_notebook.py，RED／GREEN見extraction-red.log／extraction-green.log。

保留使用者學習註解；更正「幾何不重疊等於無干擾」與「面積取樣等於畢氏定理」的誤導註解。移除topology_tables中的教學用print，改由Notebook展示查詢結果，正式表格函式只回傳資料。這些不改變快照、表格與抽樣結果。

## 最新實作狀態：已抽離.py

2026-10-23使用者理解主要邏輯並授權後，src/network_simulator/{contracts,topology,plotting}.py已建立，Notebook改import；142 pytest與乾淨kernel通過。先前「尚無src／待人工接受」保留為歷史。使用者選每模組多文件，依write-reviewable-pr原則先交ReferDoc/Implementation/IABTopology中英文合併草稿待檢閱，尚未sync／archive／merge。

## 模組目錄分類：IAB

使用者要求src與tests依模組分類，採src/iab/與tests/iab/。沿用全部dataclass／Enum集中contracts.py的決策，不拆成Node／UE／Tag的重複類別檔。只搬現有模組與測試／fixture，同步Notebook imports、測試root計算、README及當前導讀路徑；不保留舊network_simulator相容包裝，也不新增未實作模組空目錄。

此為行為不變的目錄重整，不新增產品條件，使用既有情境與抽離前保存基準驗證，無需新增只驗證私有路徑的測試。測試邊界維持build_topology／表格／圖／匯出與Notebook入口；無遠端或不可逆副作用，測試輸出在暫存目錄。遷移前後實作.py位元組一致，另跑完整pytest與乾淨kernel確認路徑整合。

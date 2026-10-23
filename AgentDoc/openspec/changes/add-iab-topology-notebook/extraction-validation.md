# .py抽離驗證與文件草稿

## 結果與接受邊界

2026-10-23使用者表示「code 的主要邏輯我認為我已經了解」，明確要求依workflow打包.py；記錄主要邏輯導讀接受，完成tasks3.3。依既定介面抽離contracts.py／topology.py／plotting.py，Notebook改import。tasks4.1完成，10/12；文件內容、抽離檔案安排仍可由使用者檢閱，不能宣稱遠端交付完成。

## 來源與TDD

本輪固定HEAD為a87a2d8effcbd6986c1aaad545d529df2ae26c75，另保存當前使用者修改後的notebook-before-extraction.ipynb。四個場景先由該原型生成extraction-baseline.json，獨立測試fixture位於tests/fixtures/topology-before-extraction.json。抽離後比較快照所有欄位及四份表，未重新生成預期值。

- RED：正式套件不存在時，四項抽離等價案例ModuleNotFoundError，見extraction-red.log。
- GREEN：`MPLBACKEND=Agg MPLCONFIGDIR=/tmp/pynet-extraction-mpl python -m pytest tests/test_topology_notebook.py tests/test_topology_extraction.py -q --tb=short`，142 passed，見extraction-green.log。
- 142＝69個既有案例×Notebook import與正式模組兩入口＋4個保存基準。兩入口共用模組，不是142種獨立情境。
- Notebook：既有RL Python3.11.15執行tests/execute_topology_notebook.py，11 cells、8項教學情境、0 errors、kernel_shutdown=true；見notebook-execution.json。沙箱內最早程序卡住後終止，本機核准執行完成。
- seed42 snapshot.json SHA-256保持`b79d2d5b2733f1b1cba2f12ab29f470f02d03d56a547224725cdf08a1e3e29b6`。圖片位元完全一致未驗證；SVG含生成metadata，不能當快照等價標準。
- 文件中的生成範例已實跑：5 UE／30 Tags、NEAR10／MID13／FAR7、Node總數[8,3,8,5,6]。配額(9,0,0)拒絕並含minimum原因。

## 審查與語意核對

| 軸 | 發現／處理 | 結果 |
|---|---|---|
| Standards | 獨立審查發現最低數與總數if間缺空行，已補；其餘16/17定義AST一致，表格函式僅移除教學print | 修正後142案例複驗通過 |
| Spec | 獨立審查核對原型SHA、fixture、四場景及模組單一來源，無阻擋finding | 無未處理規格缺陷 |
| Ponytail debt | 對src／tests／notebooks執行comment marker掃描，0 marker | 不等於零技術債；無具體延後項目，不建立空TI |

局部語意：OpenSpec人工接受與等價要求→contracts資料所有權、topology生成／表格／匯出、plotting渲染→雙入口原情境及獨立四基準→沒有新增PHY或UE座標；Notebook內保留研究操作，沒有複製第二套業務定義。幾何無干擾與面積公式的誤導註解已更正，其餘使用者註解隨原型保存並移至模組。

## 架構與文件

- 系統圖自動validate／deliver／check／browser-check通過：docs/architecture/system-extraction-review-2/system.finalize-summary.json。
- 詳圖相同四gate通過：extraction-review-2/architecture.finalize-summary.json。本輪未另做人工截圖視覺驗收。初次沙箱deliver失敗收據保留，不算成功。
- 使用者選ReferDoc/Implementation總索引、每模組資料夾及多份章節。再要求參考write-reviewable-pr先交中英文草稿，目前合併為draft.zh-TW.md／draft.en.md，正式章節拆分待回饋。
- 詳細閱讀入口見code-trace.md；文件連結與範例命令以本地實際檔案核對。

## 未完成

ReferDoc草稿人工檢閱、正式拆分、規格sync／archive／PR準備與實際merge仍未完成。沒有commit／push／遠端Issue／PR／CI證據，不將本change或workflow計完成。SNR／BER／EH、外部干擾與跨模組整合均未驗證。

文件檢查：README／code-trace／Implementation共6份Markdown、49個本地連結，0 broken links；範圍內手寫檔git diff --check通過。Matplotlib生成SVG有尾端空白，未將其當手寫程式排版缺陷。乾淨kernel後僅更新Notebook兩段Markdown的舊狀態文字，code cells未改，執行證據仍適用。ReferDoc與AgentDoc沿用既有ignore規則，本次文件保存在本機，尚未納入遠端交付。

## 2026-10-23｜雙語草稿改為標準流程圖

- 依使用者要求，ReferDoc/Implementation/IABTopology/draft.zh-TW.md與draft.en.md的第3節改為兩張標準Mermaid流程圖：生成快照與使用快照。
- 使用起訖、輸入／輸出、處理、子程序及判斷符號；補齊設定拒絕、Tag迴圈、座標生成失敗及輸出操作選擇。匯出的finally範圍與部分輸出失敗限制依實際topology.py說明。
- 只修改文件，未變更.py／Notebook或測試結果；無需重跑業務測試。圖形語意與雙語節點／邊對照可核對；未另產生Archify HTML，既有系統架構圖保留。草稿仍待檢閱，任務維持10/12。

## 2026-10-23｜依讀者回饋改寫產品使用說明

使用者指出文件目的是產品說明書，代理執行的142項檢查不應作為說明主體，術語過多；要求依write-reviewable-pr易讀原則修訂。已重寫Implementation索引及中英文草稿，以功能、準備、設定、操作、結果、常見問題、使用範圍七節呈現。移除測試統計、測試函式、開發版本／交付資訊與非必要術語，既有開發驗證紀錄完整保留於本change；沒有更改產品行為或既有人工接受狀態。

保留標準流程圖，以使用者操作呈現，雙語節點與連線相同。範例改為seed=7且保持預設配額，實際載入Notebook imports並執行該範例及既有教學檢查，確認相容；補充修改Tag數量時預設教學檢查也需調整的現有限制。只更新文件，未重跑完整pytest／kernel，未聲稱新增測試或使用者已驗收。三份文件的本地連結及Markdown結構核對通過，Mermaid未另渲染。仍待使用者檢閱草稿、後續拆文件，任務10/12，未commit／push。

## 2026-10-23｜產品說明風格接受；Notebook列點說明更新

- 使用者明確接受重寫後的產品說明內容，要求後續沿用此風格：先說用途、設定、操作與結果，少用術語，不將代理測試統計當產品說明主體；Notebook說明盡量列點。此偏好供本專案後續文件沿用，不修改共用技能或全域記憶。
- 已改寫notebooks/01_iab_topology.ipynb原有9個Markdown cell，另在表格展示與匯出前各補1個Markdown cell。介紹設定格式、區域邊界、隨機分配、圖表閱讀、預設教學檢查及輸出覆寫／儲存失敗處理。
- 保留全部11個code cells的source、outputs、execution_count與metadata，Notebook層級metadata亦一致。nbformat驗證、cell ID唯一性及Markdown本地連結檢查通過；未重跑未變更的業務測試或kernel。
- 已接受產品說明內容，但本輪未拆分正式多文件、未sync／archive、未commit／push；整個change仍10/12，後續依使用者安排接續交付準備。

## 2026-10-23｜IAB模組目錄分類完成

- 使用者要求來源與測試依模組分類，已將src/network_simulator整體移至src/iab，對應三份測試／執行器及fixture移至tests/iab。全部dataclass與Enum仍集中contracts.py；沒有新增未實作的角色模組或相容包裝。
- Notebook imports改為from iab...；測試與執行器的專案根目錄計算改為parents[2]。README、產品說明相關入口、目前code-trace及架構圖來源路徑已同步。原型與歷史log／收據保留原路徑文字，作歷史證據。
- module-layout-baseline.json核對搬移前後四份正式.py與fixture的SHA完全一致，沒有變更產品行為。`MPLBACKEND=Agg MPLCONFIGDIR=/tmp/pynet-iab-layout python -m pytest tests/iab -q --tb=short`通過142項（既有雙入口69案例＋4基準），原始輸出見module-layout-pytest.log。
- `tests/iab/execute_topology_notebook.py`於既有RL環境完成11 code cells、0 errors、kernel_shutdown=true；新import命令實跑輸出5 UE／30 Tags，Notebook既有列點Markdown保留。
- code-review唯讀獨立審查分Standards／Spec兩軸：無阻擋缺陷，另獨立跑同組142項通過；本輪未新增行為所以沿用既有測試，不新增只測路徑的重複案例。debt掃描0 marker，無新增TI。
- 現行入口文件38個本地連結有效，範圍內diff --check通過。詳圖更新src/iab來源文字後通過Archify四項自動gate，收據iab-layout-review/architecture.finalize-summary.json；本輪未另做人工視覺檢閱。整體圖的模組關係未變，無需重新生成。
- 使用者已接受產品說明風格與Notebook列點說明；本輪依授權分類目錄。任務仍10/12，規格sync／archive／PR／實際merge尚未完成；無commit／push或遠端發布。

## 2026-10-23｜正式文件與主規格同步，本機交付準備

- 依使用者要求再次核對Notebook：所有imports使用iab，新增Markdown列出src/iab與tests/iab，連結改為正式使用說明；code cells、outputs與execution_count由本輪修改前後相等檢查確認未變，nbformat驗證通過。
- 使用者已接受的中英文合併說明拆成10份正式文件（各語言總覽／設定／操作／結果／常見問題），原草稿保留。分章未改實質規則，Notebook與Implementation總索引更新正式入口。
- 主規格AgentDoc/openspec/specs/iab-topology/spec.md已建立，7要求／14情境與delta本文完全相同，主spec及change嚴格驗證通過。
- 建立本機分支feat/iab-topology，無commit／push／stage；Issue／PR草稿、歸檔準備與候選檔案清單已備妥。規格與產品說明不改模型或程式，沿用搬移後情境及kernel證據，不重跑未變程式。
- code-review本輪文件Standards／Spec兩軸無阻擋缺陷；產品文案不混入代理測試統計，PR保留代理／人工／CI區分。
- 未實際archive：archive skill要求先檢查未完成tasks與GitHub Issue映射，當前4.2／4.3及Issue對應未成立，不假勾選或冒稱完成。發布前需取得僅本change之commit／push／Issue／PR授權，再核對最終staged檔案與ignore依賴。
- 現有ReferDoc／AgentDoc忽略規則維持；不整批加入其文件或無關修改。下一步僅缺遠端交付授權及歸檔gate處理；任務10/12，workflow仍active，完成數0。

## 2026-10-23｜使用者授權全部內容發布；Issue已建立

- 使用者明確准許commit／push／Issue／PR，並要求目前內容都push。授權範圍包含現有研究參考、AgentDoc與專案工作流資料；執行快取及本機帳號／Git內部資料不納入。原gitignore不改。
- 已唯讀核對GitHub repo tonywang07009/PY_NetworkSimulator為public，預設分支main，沒有既有IAB Issue或此分支PR；建立Issue #1：https://github.com/tonywang07009/PY_NetworkSimulator/issues/1。
- 歸檔skill與既有task4.3實際merge核對存在順序衝突，未修改規則或假勾選，先發布draft PR保留active change。發布不等於完成／合併；EvoSkill與明日模組討論不啟動下一個change實作。

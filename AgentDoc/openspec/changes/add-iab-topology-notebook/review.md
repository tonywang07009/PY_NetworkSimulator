# Change review與局部語意核對

固定Git基準：0a5ff65f151febb53416d67855afa9850e2b1b13。Notebook／tests為本次新增未提交檔，直接讀取實際檔案；單看git diff HEAD無法涵蓋未追蹤檔。既有README／LICENSE等無關修改不納入審查。

依code-review skill，Standards與Spec由兩個同模型審查代理分別唯讀執行；規格來源為本change proposal／design／spec，準則為agent.md及既有codebase-design／Ponytail。未切換使用者模型／effort。

## Standards

原Notebook／pytest審查未發現具體規範缺陷。補審發現1項Boundary資源清理問題：外部KernelManager使nbclient預設不清理kernel／channels。已採execute(cleanup_kc=True)、finally shutdown及關閉後置檢查；代理複審確認程式修正，最終notebook-execution.json已實測kernel_shutdown=true。

Readability：資料、距離、驗證、生成、表格、圖及匯出分段，均有繁中說明；人工接受前不以smell為由提前抽離正式.py。沒有未解決Standards finding。

## Spec

初審發現2項並先加公開入口失敗案例：

1. Business logic／Boundary：rng.random()=0、angle=tau/1000可使合法外圓座標因浮點誤差超過50 m。已在_position_in_ring只於8個相關ulp內作有界向內修正，最後仍必須符合原環帶，不放寬分類／重抽。
2. Boundary：合法個別整數座標±10**308相減後，math.hypot洩漏OverflowError。validate_config已轉ValueError並附幾何原因。

Spec代理再次執行66 tests並核對原重現條件，確認兩項解決、未發現新增問題；代理的額外RNG端點／角度探測不納入pytest案例數。沒有未解決Spec finding。

## 局部語意對照

| 規格 | 實作（Notebook cell／入口） | 實際測試 | 結果／限制 |
|---|---|---|---|
| 星狀拓撲／精確配額 | builder／build_topology | test_builds_exact_global_quotas_and_one_ue_per_node、test_supports_minimum_count_and_empty_zones | 通過；30只是示例 |
| 分區／面積均勻 | distance、builder／classify_distance、_position_in_ring | test_classifies_horizontal_distance_at_exclusive_inner_boundaries、test_samples_annulus_by_area_not_uniform_radius、外端點案例 | 通過；幾何不代表RF品質 |
| 輸入拒絕 | validation／validate_config | invalid_config、wrong_config、duplicate_ids、overlap、unrepresentable等案例 | 通過；無全域RNG或輸入副作用 |
| 不可變／可重現 | contracts、builder | test_snapshot_is_deeply_immutable_and_freezes_input_sequences、test_reproduces_result_without_reading_or_mutating_global_rng | 通過；限相同實作版本 |
| 表／圖／匯出 | tables、plot、export | test_tables_preserve_snapshot_ids_coordinates_and_link_counts、test_plot_draws_real_geometry_without_invented_ue_positions、test_exports_same_snapshot_as_json_csv_png_and_svg | 通過；快照、表及圖共用資料 |
| Notebook原型 | 全11個code cells、execute_topology_notebook.py | notebook-execution.json、Notebook內8個教學情境 | 通過，kernel已關閉；待使用者理解與接受 |

## Ponytail debt

執行 `git grep --no-index --exclude-standard -nE '(#|//|/[*]) ?(shortcut|ponytail):' -- tests notebooks`：0個marker、0個no-trigger。沒有具體需延後的範圍內缺陷，未建立空tech_improve.md。無marker不代表無技術債。Channel／EH／正式.py抽離是已確認的後續範圍，不拿來取代本次缺陷修正。

## 視覺與接受限制

已觀看實際部署PNG並把Node標籤移至圓域外，避免壓住近區Tag；最終PNG再檢視。整體與change架構均完成finalize、瀏覽器明暗／雙尺寸截圖；已檢視整體暗色與change亮色1440x900，確認文字與路徑可讀。截圖自動收據的visualReview=pending僅表示尚無工具內人類評分，代理檢視記於本文件，不改原收據。

這些是代理檢查，不是使用者人工接受。尚未抽離src.py、sync／archive、發布Issue／PR或合併。

## 人工導讀回饋的局部複驗：tuple唯一格式

使用者明確選擇並要求README註記。Standards局部自審：刪除__post_init__便利轉換、不新增替代邏輯；保留使用者其餘Notebook註解與README原文。Spec局部自審：三個集合欄位的tuple拒絕條件原已存在於validate_config，新增3個list拒絕案例、以合法tuple核對巢狀不可變與幾何溢位。舊「接受list轉換」測試按已修正驗收更新，不以刪測試掩蓋缺陷。

結果69 passed，11 cells乾淨kernel／清理通過，原snapshot.json完全一致；無新增範圍內缺陷或技術債。這是本次受影響內容的局部自審，不冒稱先前代理已審查此次README／新版本。人工理解與接受仍進行中，未抽離.py。

## 人工導讀排版調整

相鄰獨立if區塊插入6個空行，清除空白行上的空白字元；validation cell前後AST完全相同，69 pytest通過。沒有業務邏輯改動，不新增鏡像排版測試或重跑未受影響的kernel／圖表。最新語法與函式實際測試對應此版；完整kernel證據沿用上一個等價版本。

## 2026-10-23｜人工接受後抽離

主要邏輯已獲使用者理解及抽離授權；正式模組與Notebook imports完成142 pytest／乾淨kernel複驗。新兩軸審查及修正、TDD與證據限制見[extraction-validation.md](extraction-validation.md)。先前「待人工接受／尚無src」為歷史狀態，由本節更新；未完成文件檢閱與遠端交付。

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

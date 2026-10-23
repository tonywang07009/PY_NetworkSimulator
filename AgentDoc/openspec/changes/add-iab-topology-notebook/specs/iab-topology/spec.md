## ADDED Requirements

### Requirement: 靜態平面星狀拓撲
系統SHALL建立1個Donor與5個直接回傳Donor的IAB Nodes，每Node對應1個只有ID與Node歸屬的UE。站點座標由Config明列，單位m，忽略高度，run內不移動。輸出SHALL包含每個Tag唯一Node歸屬。

#### Scenario: 正常拓撲
- **WHEN** 以合法5 Node配置建立拓撲
- **THEN** 結果有1 Donor、5 Nodes、5 UE，5條回傳關係、5條UE歸屬及每Tag一條接入關係；UE沒有物理座標

### Requirement: 精確配額與最少Tag數量
系統SHALL依seed隨機分配各Node的三區Tag數量，精確保持全場配額，各Node至少2個Tag（允許提高此最低設定），不強制均分或每Node每區都有Tag。生成SHALL有限步驟完成。

#### Scenario: 非均勻30 Tag例子
- **WHEN** 三區配額為10／13／7且每Node最少2個
- **THEN** 總數30且三區數量精確相符，各Node至少2個

#### Scenario: 最少可行及空分區
- **WHEN** 配額為10／0／0，最低2個
- **THEN** 五個Node各2個，空分區不產生Tag

#### Scenario: 不可行總數
- **WHEN** 配額總數小於5倍每Node最低數量，包括0或9個且最低2個
- **THEN** 拋出含原因的ValueError，不無限重抽、不修改輸入或全域亂數

### Requirement: 幾何環帶與區內面積均勻
系統SHALL以所屬Node水平距離分近／中／遠區，預設邊界10／30／50 m且可配置為三個遞增正值。分區為0<d<=r1、r1<d<=r2、r2<d<=r3。每區內SHALL按面積均勻、角度無偏好生成位置；不得與Node重合。五個部署圓SHALL互不重疊，首版亦拒絕邊界相切。

#### Scenario: 分區邊界
- **WHEN** 判定d為10、30、50 m及各邊界兩側
- **THEN** 10屬近、30屬中、50屬遠，0及大於50拒絕

#### Scenario: 幾何與面積取樣
- **WHEN** 從合法Config生成Tag座標
- **THEN** 每個Tag位於所屬Node對應環帶；均勻的是面積而非半徑，受控亂數例子的面積分位可核對

#### Scenario: 部署區域重疊或相切
- **WHEN** 任兩Node距離小於或等於兩個最外半徑之和
- **THEN** 拋出含原因的ValueError，不把幾何不重疊等同RF無干擾

### Requirement: 輸入拒絕與不可變結果
系統SHALL拒絕空／錯誤Config、錯誤站點或座標型別、空／重複ID、非有限座標、非正或未遞增半徑、負／非整數／bool配額、少於2或非整數最低數量、非整數／bool seed及錯誤Node數；負座標合法。快照SHALL保存完整設定及不可變的巢狀資料，不靜默修正非法設定。TopologyConfig的iab_nodes、zone_outer_radii_m、zone_tag_counts SHALL只接受tuple，不接受list或自動轉換；型別驗證於公開build_topology入口執行。不可表示的數值幾何SHALL明確拒絕。

#### Scenario: 非法設定
- **WHEN** 呼叫端提供上述任一非法值
- **THEN** 公開生成入口拋出含欄位或原因的ValueError，沒有部分外部輸出

#### Scenario: 快照資料隔離
- **WHEN** 呼叫端嘗試修改已生成快照、設定、座標或內含集合
- **THEN** 真值不可被改寫，集合欄位必須為tuple，傳入list時公開入口明確拒絕


#### Scenario: tuple唯一輸入格式
- **WHEN** 三個集合設定欄位任一以list傳入
- **THEN** build_topology拋出含欄位原因的ValueError，不轉換為tuple；合法tuple的生成結果與原有示例一致

### Requirement: 可重現且隔離的亂數
系統SHALL使用拓撲專屬亂數來源，相同設定與seed於相同實作版本生成相同歸屬與座標，不改全域亂數狀態，也不受Policy等其他全域抽樣影響。

#### Scenario: 重跑與全域隔離
- **WHEN** 相同Config重跑，或在兩次生成間進行外部全域亂數抽樣
- **THEN** 拓撲結果一致且生成前後的全域RNG狀態相同；不同seed用代表案例核對可變性

### Requirement: 一致的表格部署圖與輸出
Notebook SHALL從同一快照呈現完整設定摘要、Node三區計數／UE摘要、Tag座標／距離／分區明細、回傳與歸屬表，以及等比例二維部署圖。圖SHALL顯示Donor、5 Nodes、Tag散點、三區邊界與圖例，不替UE發明座標；色彩代表分區而非未計算SNR。可匯出同一快照JSON、CSV與PNG／SVG供人工核對。

#### Scenario: 同一結果的圖表
- **WHEN** 以30 Tag結果建立表格與部署圖
- **THEN** 各表與圖對應同一組ID／座標／歸屬與精確計數，不重新抽樣，匯出可重查

### Requirement: Notebook原型與人工接受
本change SHALL先在Notebook保留Config／DTO／生成／驗證／呈現的實作，提供公開入口情境測試及乾淨kernel從頭執行證據。代理SHALL先完成兩軸review、架構與tree式code-trace，再逐段導讀；使用者明確理解並接受前不得抽離正式模組.py或宣稱已接受／歸檔。接受後SHALL以相同情境核對抽離前後等價性。

#### Scenario: 人工接受前交付
- **WHEN** Notebook情境及乾淨kernel執行通過
- **THEN** 提供Notebook、測試證據、架構與絕對路徑導讀，狀態為待人工接受，未建立正式src模組

#### Scenario: 科學模型邊界
- **WHEN** 呈現拓撲結果
- **THEN** 不宣稱已證明SNR／BER／EH或標準符合性；近區SNR優於遠區、自身CW自干擾完美消除僅保留為後續Channel假設

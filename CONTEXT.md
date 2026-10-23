# IAB／Ambient IoT 模擬器術語

本表區分研究場景中的時間、部署與鏈路概念；規範版本及研究決策的證據見 [R-01](ReferDoc/Plan/R-01_System_Model_and_Baseline_Decision_Record.md)。不描述程式實作。

## 時間

**服務 Deadline**：一項服務必須完成所需有效資料的排他期限；在期限當下完成不算期限前完成。
_Avoid_：實際傳輸時長、DU Window 長度。

**一輪服務**：全部服務於同一個全域 0 起點開始的需求集合；本輪長度為這些服務最晚的 Deadline。
_Avoid_：由服務清單先後依序啟動的批次。

**DU Window**：Node 當次可用來進行相關操作的資源區間；本場景持續時間固定 600 ms，與 Window 出現間隔是不同概念。
_Avoid_：600 ms 一定連續重複、服務需求更新週期。

## 拓撲與部署

**IAB Node／Reader**：本研究將 Reader 整合於 IAB Node，Tag 直接與此 Reader 通訊；在 IAB split 架構下支援這項 A-IoT 整合屬研究擴充。
_Avoid_：已獲 Release-19 A-IoT split gNB 規範支持。

**D1T1**：TR 38.769 所用的 Deployment scenario 1 加 connectivity topology 1；D1 對應 TR 38.848 的室內裝置／室內基地台情境。
_Avoid_：Device type 1、共址的同義詞。

**CW／Reader 共址**：提供 CW 的來源與 Reader 位於同一節點位置；不等於所有 D1 室內場景、頻段及評估數值都適用。
_Avoid_：D1T1 這個標記本身即代表共址。

**部署分區**：以Tag所屬Node的平面水平距離分近／中／遠，預設外邊界10／30／50 m；各區內面積均勻隨機、跨區精確數量可不均。使用者另規定近區SNR優於遠區為system model假設，具體Channel數值仍待定。
_Avoid_：遠區一定有較強干擾、區域名稱即為已校準 SNR。

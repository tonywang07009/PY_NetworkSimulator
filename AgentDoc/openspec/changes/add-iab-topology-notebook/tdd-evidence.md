# TDD證據

以下逐slice記錄實際RED／GREEN，不以未執行案例宣稱通過。

## 實際RED／GREEN

| Slice | RED | GREEN | 語意核對 |
|---|---|---|---|
| 1 配額／歸屬 | tdd-red-01.log：Notebook不存在，公開入口無法載入 | 1 passed | 30／10／13／7、5 UE、每Node至少2 |
| 2 輸入／分區／隔離 | tdd-red-02.log：53 failed、5 passed，缺分區入口及拒絕行為 | 58 passed | 非法輸入明確ValueError、分區邊界、面積分位、凍結與RNG隔離 |
| 3 圖表／匯出 | tdd-red-03.log：3 failed、58 passed，缺公開表／圖／匯出入口 | 61 passed | 15個環帶、36個實際點、40條邏輯關係、JSON／CSV／PNG／SVG同快照 |
| 4 ID／數值幾何 | tdd-red-04.log：2 failed、62 passed，生成ID碰撞與巨座標精度未拒絕 | 64 passed | ID全域唯一、無法表示Tag距離時明確拒絕；自訂半徑／較高最低數量成立 |

命令：`MPLCONFIGDIR=/tmp/pynet-mpl python -m pytest tests/test_topology_notebook.py -q --tb=short`。測試載入Notebook definitions cells，非獨立複製實作。Notebook補教學及分段後回歸仍64 passed。

| 5 Review數值邊界 | tdd-red-05.log：2 failed、64 passed，外圓端點誤拒絕與整數差值溢位 | 66 passed | 8ulp內有界端點修正後仍通過原環帶判定；間距OverflowError轉ValueError |

補充：Standards補審指出外部KernelManager清理。執行器現以cleanup_kc=True、finally shutdown及後置has_kernel檢查落實；真正完整kernel執行收據為notebook-execution.json，kernel_shutdown=true。此基礎設施以完整kernel整合自檢驗證，未編造unit RED紀錄。

## 人工導讀回饋：只接受tuple

依使用者明確選擇第三種輸入契約，先更新spec／design，再新增3個公開入口list拒絕案例。RED為3 failed／66 passed（tdd-tuple-red.log）；移除__post_init__、更新舊自動轉換案例及大整數幾何測試的合法tuple輸入後，GREEN為69 passed。無新增自動轉換或替代抽象。

完整Notebook重跑：11 code cells、0 errors、kernel_shutdown=true；修改前後snapshot.json SHA-256相同。其餘使用者Notebook註解保留。README本輪只追加tuple輸入規則，保留原內容。

## 2026-10-23｜人工接受後抽離

主要邏輯已獲使用者理解及抽離授權；正式模組與Notebook imports完成142 pytest／乾淨kernel複驗。新兩軸審查及修正、TDD與證據限制見[extraction-validation.md](extraction-validation.md)。先前「待人工接受／尚無src」為歷史狀態，由本節更新；未完成文件檢閱與遠端交付。

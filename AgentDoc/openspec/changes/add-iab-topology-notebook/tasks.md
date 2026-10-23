## 1. 規格與環境

- [x] 1.1 沿用已確認訪談，建立proposal／design／specs、TDD contract及本機Issue草稿。
- [x] 1.2 核對既有Python／Notebook／Matplotlib環境，登記workflow並記Git基準；不更動無關工作。

## 2. Notebook原型與TDD

- [x] 2.1 以公開生成入口完成精確配額、最少Tag數、固定Node及UE歸屬的RED／GREEN。
- [x] 2.2 完成幾何分區、面積抽樣、輸入拒絕、不可變性與RNG隔離情境。
- [x] 2.3 完成同一快照的設定／Node／Tag／連線表、部署圖與匯出，核對對應情境。
- [x] 2.4 Notebook加入繁中分段教學與情境摘要，以真正乾淨kernel從頭執行並保存結果／環境證據。

## 3. Review與人工導讀準備

- [x] 3.1 執行Standards／Spec兩軸code-review、ponytail-debt與局部語意核對；修正並複驗範圍內缺陷。
- [x] 3.2 更新整體／本change架構，提供實際tree、絕對路徑code-trace、需求／實作／測試對照及完整交接。
- [x] 3.3 逐段人工導讀，處理回饋並取得使用者明確理解與接受Notebook。

## 4. 人工接受後的交付

- [x] 4.1 接受後才抽離共用contracts.py／topology.py／plotting.py，Notebook改import並以同情境核對等價。
- [ ] 4.2 接受及複驗完成後同步spec、準備archive／README與PR草稿；遠端發布只在獲授權後執行。
- [ ] 4.3 核實使用者手動merge及Issue結果，完成必要知識結案與workflow登記。

實際TDD與語意對照見tdd-evidence.md／review.md；人工接受與遠端發布未完成前，不將整個change標完成。

2026-10-23：使用者明確表示主要邏輯已理解並要求抽離，3.3完成；正式模組／Notebook imports／142 pytest／乾淨kernel複驗完成，4.1完成。ReferDoc採每模組分文件，依使用者後續要求先交中英文合併草稿待檢閱，4.2／4.3尚未完成。

4.2本機準備進度：主規格同步、正式分章文件、README／code-trace與Issue／PR草稿已完成；實際archive與發布仍待gate成立，整項保持未完成。4.3仍待使用者真實merge。詳見archive-preparation.md／delivery-preparation.json。

# 執行與驗證證據

日期：2026-10-23。cwd為 `/home/tonywang/Net_simluation/PY_NetworkSimulator`。

| 檢查 | 已觀察結果 | 原始證據 |
|---|---|---|
| OpenSpec strict | change合法 | `openspec validate add-iab-topology-notebook --strict` |
| 公開入口pytest | 69 passed | [pytest-results.txt](pytest-results.txt)、[TDD](tdd-evidence.md) |
| 真正乾淨kernel | 11個code cells、執行序號1–11、0錯誤、kernel_shutdown=true | [notebook-execution.json](notebook-execution.json) |
| Notebook教學情境 | 8項PASS，結果內嵌於Notebook | [Notebook](../../../../notebooks/01_iab_topology.ipynb) 的scenario-checks cell |
| 部署結果 | 30 Tags；近10／中13／遠7；每Node總數8／3／8／5／6 | [Node表](../../../../notebooks/artifacts/iab-topology/nodes.csv) |
| 整體架構 | validate／deliver／check／browser-check pass | [收據](../../../../docs/architecture/system-tuple-review/system.finalize-summary.json) |
| change架構 | 四個finalize gates pass | [收據](tuple-review/architecture.finalize-summary.json) |
| 圖面 | 部署PNG及兩張架構桌面截圖已由代理檢視 | [review.md](review.md)，非使用者接受 |

## 已驗證可用環境與重跑

- pytest：`/home/tonywang/miniforge3/bin/python`，Python3.12，pytest9.1.1。
- 真正Notebook：`/home/tonywang/miniforge3/envs/RL/bin/python`，Python3.11.15，nbformat5.10.4／nbclient0.10.4／ipykernel7.2.0／Matplotlib3.10.8，版本以執行收據為準。
- mcp環境只有metadata存在，kernel啟動缺decorator，沒有當成成功；未修改該環境或安裝新套件。
- 執行器建立暫存kernelspec，以當前Python啟動kernel；完整清理kernel／channels及暫存檔，不註冊使用者kernel。

```bash
MPLCONFIGDIR=/tmp/pynet-mpl python -m pytest tests/test_topology_notebook.py -q --tb=short
MPLCONFIGDIR=/tmp/pynet-mpl-runner /home/tonywang/miniforge3/envs/RL/bin/python tests/execute_topology_notebook.py
OPENSPEC_TELEMETRY=0 openspec validate add-iab-topology-notebook --strict
```

Notebook UI可選上述RL Python作kernel，或用相同套件環境；不要誤選缺少Notebook依賴的base。沒有默默更動使用者kernel設定。沙箱不允許本機socket／子程序時，測試／渲染僅該步經核准於沙箱外執行；未對外服務。

## 接受狀態

自動驗證與代理review已完成，尚待逐段人工理解／接受Notebook。未建立正式src模組；未歸檔；未發布Issue／PR；未commit／push；workflow尚未完成。幾何驗證不等於SNR／BER／EH／RF或3GPP符合性證據。

## 2026-10-23｜人工接受後抽離

主要邏輯已獲使用者理解及抽離授權；正式模組與Notebook imports完成142 pytest／乾淨kernel複驗。新兩軸審查及修正、TDD與證據限制見[extraction-validation.md](extraction-validation.md)。先前「待人工接受／尚無src」為歷史狀態，由本節更新；未完成文件檢閱與遠端交付。

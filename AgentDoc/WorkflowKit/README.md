# Agent workflow 教材

第一次使用 workflow 開展專案時，Agent 會先介紹完整流程，再於每個階段開始前
說明目的、工作與產出，完成後說明結果、證據與下一步。第二個 workflow 專案起
改用簡短提示；使用者要求深入了解時，再展開當前主題。教學程度與已介紹的階段
保存於既有本機 workflow 紀錄，跨對話續作不重播開場；教學不新增確認關卡。
詳見 [教學流程](skills/workflow/references/delivery.md#teaching-during-delivery)。

新流程採一個 change、一個 Issue、一份 PR。OpenSpec 範圍確認後追蹤 Issue；
實作、測試與 review 完成後，先交付完整 Archify 架構圖及 `code-trace.md`，
再逐段帶使用者人工 trace。導讀包含實際目錄 tree、每個實作檔案的絕對／相對
路徑、用途、符號，以及需求 → 程式 → 測試／原始證據的對照。

人工接受與必要修正後，同步規格並在交付分支準備 archive、架構快照與 README。
程式和上述文件放在同一 PR，由使用者手動合併。Agent 核對實際 merge、版本與
Issue 收尾後，才標記 change 完成；等待期間不開始下一個 change，auto 亦同。
詳見 [GitHub 交付](skills/workflow/references/github.md) 與
[架構／人工 trace](skills/workflow/references/architecture.md)。

[文件管理與訪談學習說明](docs/說明.md) 提供檔案結構、命名與 P.A.R.A 原位整理。
[docs/output.md](docs/output.md) 是 CLI／對話、change 與 Issue／PR 的共同寫作依據，
針對術語、句間承接與修改理由提供前後對照。PR 技能保留使用者認可的版面。
同一規範也適用 OpenSpec、README 與教學：起草前確認讀者及用途，長內容先
結論再展開細節，交付前檢查排版與資訊完整性並改稿。技能指令撰寫參考
[AI Hero：Writing for Agents](https://www.aihero.dev/skills-writing-for-agents)，
規則適用 Luna 與其他模型；實際閱讀成效仍需使用者案例驗證。
`output.md` 使用英文指令，預設要求人讀內容使用繁體中文；使用者明示語言或
專案文件語言規則優先。繁體中文範例移至按需閱讀的
[寫作前後對照](docs/output-examples.zh-TW.md)。英文是否省 token 取決於 tokenizer，未據此宣稱節省比例。
向使用者詢問決策時也適用同一規範，包括提問工具中的題目與選項：先交代目的及
實例，說明選項取捨並保留備註；已回答的問題不重問。

實作以一項可驗證行為為單位：完成程式、呼叫端及測試後，先核對 OpenSpec，
修正明確且範圍內的問題並複驗。change 結束再執行整體 code-review 與
ponytail-debt；可延後的改善保存於目標 OpenSpec 根目錄的 `tech_improve.md`，
記錄原因、證據及「何時需要重新評估」，在人工 trace 時確認。

直接開啟 `index.html`，可離線閱讀互動流程圖及 8 段、90 分鐘教學。

## 檔案配置

| 位置 | 用途 |
|---|---|
| `index.html` | 三段系統流程與互動課程卡 |
| `course/workflow.archify.json`、`workflow.html` | Archify Workflow v2 原始規格與離線互動圖 |
| `course/lesson.json` | 8 張課程卡、練習與目前實作引用 |
| `course/build.py` | 從資料重建流程圖與首頁課程資料 |
| `course/speaker-notes.zh-TW.md` | 與課程卡對應的講者教案 |
| `course/weekly-runbook.zh-TW.md` | 維護節奏與品質演進 |
| `course/sources/` | 原 RedCap 歷史唯讀快照，不是現行操作規則 |
| `docs/tools.md` | 工具能力、情境、限制、檢查與安裝來源 |
| `docs/install.md` | 給 agent 的三平台安裝指南、設定範圍與實際可用性驗證 |
| `docs/platform-validation.md` | 三平台 CI 與 agent／MCP 人工實測的範圍及驗收方式 |
| `docs/skill-contracts.md` | 18 個技能的責任、架構銜接與驗收對照 |
| `docs/output.md` | 英文寫作指令；預設繁體中文輸出，含起草、改稿與排版規則 |
| `docs/output-examples.zh-TW.md` | 按需要讀取的繁體中文修改前後示例 |
| `docs/說明.md` | 文件結構、命名、P.A.R.A 原位整理與訪談學習整合設計 |
| `management/AGENTS.md` | 學員專案規則範本 |
| `management/tech_improve.md` | 放入目標 OpenSpec 根目錄的改善待辦範本 |
| `management/openspec-project/` | 各專案工具路由 spec 與 Toolbox 範本 |
| `skills/` | 18 個技能，含 workflow、llm-wiki、skill-evolution、writing-for-agents |
| `install.py` | 新裝、唯讀升級預覽、逐檔決策、備份與失敗回復 |
| `.github/workflows/verify.yml` | 三平台套件／升級與所選 CLI 檢查；實際執行結果仍須觀測 |
| `verify.py`、`tests/` | 教材一致性、安裝、狀態及候選檢查 |

根目錄 AGENTS.md 為本機規則，透過 /AGENTS.md 忽略追蹤；
management/AGENTS.md 是仍隨套件配送的範本。

## 安裝到練習專案

給 agent 的入口是 [Markdown 安裝指南](docs/install.md)，取代原本的 MCP 工具.txt。
它依 Linux／macOS／Windows 辨識環境、安裝所選工具並驗證 CLI／MCP；
優先專案內設定，使用者層級變更先列差異再確認。三平台完整自動安裝尚待實跑驗證。
可直接交給 agent：

```text
請讀取 docs/install.md，依目前環境完成本專案 workflow 的安裝與驗證。
沿用既有工具及設定，缺少必要資訊才詢問；逐項回報可用、未完成與處理方式。
```

下列指令只配送套件檔案；外部工具設定依安裝指南執行：

```bash
python3 -B verify.py
python3 install.py /absolute/path/to/your-practice-repo
```
- 這邊 絕對路徑請下 ```bash  pwd ``` 來指向你對應的絕對路徑

Windows 若無 python3，使用 python。目標目錄須已存在。安裝產物：

```text
<target>/.agents/skills/<18 skills>/
<target>/.agents/workflow-kit/docs/
<target>/.agents/workflow-kit/management/
<target>/.agents/workflow-kit/初次下提示詞模板.txt
<target>/.agents/workflow-kit/installation.json
```

不覆蓋同名 skills 或既有 workflow-kit 資源，不修改目標 AGENTS.md、
OpenSpec／MCP 設定或個人進度。既有安裝先比較差異並選擇更新範圍；
不要以刪除既有技能作為預設升級方式。

既有安裝先預覽：

```bash
python3 install.py /absolute/path/to/your-practice-repo --upgrade --dry-run
```

沒有待確認檔案時，以 `--upgrade` 更新；使用者改過、刪除過或缺少基準而不同的
檔案會阻止寫入。確認單一檔案的差異後，才使用 `--keep-local` 或 `--replace`。
完整用法與備份恢復見安裝指南。workflow 升級不會連帶升級外部工具。

## 啟動與專案接入

依工具指南準備適用工具及 OpenSpec CLI。各工具的入口形式不同；
安裝連結不代表已健康或每個任務都需要。

```text
$workflow
請啟動或接續目前專案；新流程先以 $grill-with-docs 確認意圖與需求，續作直接接續。
```

新流程以 `$grill-with-docs` 開始，每次釐清一個未決問題，確認目標、範圍、
驗收條件與停止條件後，才進入專案設定及後續交付流程。
續作不必重新確認；只有使用者提出新增需求時，才重新進入釐清，並沿用已確認的決策。
僅查詢狀態或切換模式時，直接完成該操作。

若尚未辨識技能，請 Agent 讀 `.agents/skills/workflow/SKILL.md`。
首次接入時依問題選工具，使用安裝資源中的 management 範本，
把實際專案契約放在對應 OpenSpec，例如：

```text
<project>/openspec/projects/<project-key>/spec.md
<project>/openspec/projects/<project-key>/toolbox.md
```

projects/ 是本教材分組慣例，不是 OpenSpec CLI schema。沿用現有設定，
change／artifact 路徑仍由 CLI 解析；有多個專案時先選擇。
Agent 在既有授權內接入，不直接覆蓋整份 AGENTS.md。

## 推進與品質演進

- 預設每個已核對合併的 change 結束後停下；auto 也須等手動合併才接續。
- 所有 changes 與整體驗收完成才計一次 workflow。
- 同一本機使用者跨專案滿 5 次詢問是否自動接續；拒絕後不再主動重問。
  共用索引位於使用者家目錄的 `.workflow/state.json`，隨時可要求切換模式。
- 新流程結案包含原位索引／摘要／連結整理與訪談／Wiki 學習；每次 Wiki 更新後評估 Skill 改進。舊流程保留原本同意紀錄。
- 已確認路徑、連結與命令筆誤直接修復驗證；品質候選需重複根因兩次、
  成功／失敗證據及可執行比較。
- 候選隔離在專案 Wiki 的 evolution/。同一版本通過兩個不同任務，
  至少一個未用於撰寫候選；版本改變重驗。正確性／完整性優先。
- 合格候選撰寫時才載入 writing-for-agents；skill-creator 處理封裝。
  兩者不改變候選資格、比較驗證或啟用門檻；技能文字變短不等於品質提升。
- 穩定後提出更新建議，由使用者決定指定版本與本機／共用目標。
  拒絕與回退結果保留在 Wiki；回饋不遞迴觸發評估。

安裝不建立個人狀態或 Wiki；實際家目錄寫入依環境權限處理。
llm-wiki 是本套件本地技能，不需要外部 LLM Wiki 桌面程式才能操作。

## 維護與驗證

```bash
python3 -B course/build.py
python3 -B -m unittest discover -s tests
python3 -B verify.py
```

修改後同步 PROVENANCE.json 與 SHA256SUMS。
有 Chromium／Edge 時可執行：

```text
node tests/test_course_browser.mjs <browser-executable> <screenshot-directory>
```

測試使用暫存專案，不寫個人進度或啟用共用 Skill。候選檢查工具只驗證紀錄；
真實 Agent 品質仍須實跑案例並判讀證據。
`course/build.py` 預設只同步課程文字，不覆寫架構圖。修改圖面請編輯
`course/workflow.archify.json`，並使用本機 Archify 專案重新生成：

```text
python -B course/build.py --archify-root .tools/archify --archify-evidence-dir course/new-review
node .tools/archify/archify/bin/archify.mjs visual-check course/workflow.html --json --require-provenance --out-dir course/new-review/visual
```

找不到 Chrome 時，可將 `ARCHIFY_CHROME` 環境變數設為已安裝的 Edge／Chromium 執行檔。
閱讀教材不需要安裝 Archify；只有重新生成圖面時才需要本機 CLI。
本機 Archify 由使用者指定的 https://github.com/tt-a1i/archify 下載至 .tools/archify；
實際版本、revision 與生成證據記在 PROVENANCE.json。工具 checkout 不隨 install.py 配送。
圖面修改後使用新的證據目錄，保留上一版紀錄；實際目前路徑由 PROVENANCE.json 記錄。
本次紀錄為 `course/workflow.delivery.json`、`course/review-implementation-debt/workflow.finalize.json` 與該目錄的 browser／visual receipts；
舊 `archify-delivery.json`、`archify-browser.json` 留作歷史紀錄。
歷史截圖不證明本次畫面；本次驗證範圍見 docs/validation.md。手機閱讀大型圖面可使用縮放／平移。

## 訪談與尚未設計的項目

起始模板只需填問題／使用者、期望改善、限制、來源與未知事項。grill-with-docs
依六面向逐題詢問，每題提供實例、選項與選填備註，每面向最多 10 題含追問與
最後澄清。interview/ 保存進度，實作前回問未決事項；不以沉默代替同意。
文獻權衡採彭明輝相關章節的方法摘要，PDF 不配送。

CLM 整合列為未來待辦，先比較現有 agent 審查與加入 CLM 的真實增益，再決定是否導入；
不安裝模型、不呼叫評分 API，也不再以 Jev／TypeSafe 作為整合方向。
tag 與跨專案偏好共享仍待設計。套件測試不代表已完成真實專案的 GitHub 發布或 Agent 品質驗證。

---
name: confined-space-planner
description: 密閉空間施工計劃生成器。觸發詞：密閉空間、密閉空間施工計劃、confined space、危險評估報告、工作許可證、密閉空間安全、沙井作業、儲水缸作業、管道作業、密閉空間風險評估、施工安全計劃。基於澳門第32/2023號行政法規、CEM承建商安全管理手冊及ISO 31000，自動生成合法、合規的《密閉空間施工計劃》，涵蓋風險評估、許可證、安全措施、緊急救援全流程。
version: 1.0.0
icon: ⛑️
author: David-CB666
metadata:
  clawdbot:
    requires:
      bins: [python]
    commands:
      run: python {baseDir}/cli/main.py run
---

# 密閉空間施工計劃生成器

> 自動生成符合澳門法規的密閉空間施工計劃，涵蓋風險評估 → 許可證 → 安全措施 → 應急預案。

## 快速開始

提供以下 4 類信息，即可自動生成完整計劃：

1. **項目信息** — 名稱 / 地點 / 承建商
2. **空間描述** — 類型 / 尺寸 / 出入口 / 結構 / 周邊環境
3. **工作內容** — 性質 / 人數 / 工時 / 物料設備
4. **特殊要求** — 業主要求 / 已知危害

## 法規依據

| 法規 | 用途 |
|:-----|:-----|
| 澳門第32/2023號行政法規 §161-172 | 法定定義、危險評估、許可證、17項安全措施 |
| CEM 承建商安全管理手冊 A.2.5/C.1.8 | 項目級標準、合資格人員、檢查清單 |
| ISO 31000 + 密閉空間風險指南 | 風險矩陣、危害識別、控制措施層級 |

## 處理流程（5 步）

```
用戶輸入 → 情境分析 → 危害識別 → 控制措施生成 → 文檔撰寫 → 合規審查 → 輸出 docx
```

## 輸出文檔結構

封面 → 編制依據 → 工程概况 → 危險評估報告 → 工作許可證 → 安全措施 → 應急預案 → 附件

## 詳細文檔索引

| 文檔 | 內容 |
|:-----|:-----|
| [references/input-requirements.md](references/input-requirements.md) | 用戶輸入規範（4 類 12 項參數） |
| [references/process-flow.md](references/process-flow.md) | 5 步處理流程詳細分解 |
| [references/regulations-summary.md](references/regulations-summary.md) | 法規摘要（32/2023、CEM、ISO 31000） |
| [references/hazard-library.md](references/hazard-library.md) | 危害識別庫 + 氣體容忍標準 + 風險矩陣 |
| [references/control-measures.md](references/control-measures.md) | 控制措施庫（工程/行政/PPE/緊急救援） |
| [references/document-templates.md](references/document-templates.md) | 3 套文檔模板結構 |
| [references/compliance-checklist.md](references/compliance-checklist.md) | 合規檢查清單 |

## 參考文件

> 以下文件為本技能的法規依據，存放於用戶本地，技能本身不附帶文件內容。

| 文件 | 說明 |
|:-----|:-----|
| 澳門第32/2023號行政法規 | 第32/2023號行政法規《建築業職業安全健康法例》§161-172 |
| 密閉空間風險指南 | 澳門勞工事務局《密閉空間工作是全指南》 |
| 密閉空間作業指引 | 密閉空間作業安全作業指引 |
| CEM 承建商安全管理手冊 | CEM Contractors Safety Management Manual (A.2.5/C.1.8) |

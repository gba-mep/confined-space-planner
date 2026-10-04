---
name: confined-space-planner
triggers: ["密闭空间", "密闭空间施工计划", "confined space", "危险评估报告", "工作许可证", "密闭空间安全", "沙井作业", "储水缸作业", "管道作业", "密闭空间风险评估", "施工安全计划"]
description: 密闭空间施工计划生成器。触发词：密闭空间、密闭空间施工计划、confined
  space、危险评估报告、工作许可证、密闭空间安全、沙井作业、储水缸作业、管道作业、密闭空间风险评估、施工安全计划。基于[当地安全法规]、CEM承建商安全管理手册及ISO
  31000，自动生成合法、合规的《密闭空间施工计划》，涵盖风险评估、许可证、安全措施、紧急救援全流程。
version: 1.0.0
icon: ⛑️
author: gba-mep
metadata:
  clawdbot:
    requires:
      bins:
        - python
    commands:
      run: python {baseDir}/cli/main.py run
disable: true
---

# 密闭空间施工计划生成器

> 自动生成符合安全法规的密闭空间施工计划，涵盖风险评估 → 许可证 → 安全措施 → 应急预案。

## 快速开始

提供以下 4 类信息，即可自动生成完整计划：

1. **项目信息** — 名称 / 地点 / 承建商
2. **空间描述** — 类型 / 尺寸 / 出入口 / 结构 / 周边环境
3. **工作内容** — 性质 / 人数 / 工时 / 物料设备
4. **特殊要求** — 业主要求 / 已知危害

## 法规依据

| 法规 | 用途 |
|:-----|:-----|
| [当地安全法规] §161-172 | 法定定义、危险评估、许可证、17项安全措施 |
| [安全管理手册] A.2.5/C.1.8 | 项目级标准、合资格人员、检查清单 |
| ISO 31000 + 密闭空间风险指南 | 风险矩阵、危害识别、控制措施层级 |

## 处理流程（5 步）

```
用户输入 → 情境分析 → 危害识别 → 控制措施生成 → 文档撰写 → 合规审查 → 输出 docx
```

## 输出文档结构

封面 → 编制依据 → 工程概况 → 危险评估报告 → 工作许可证 → 安全措施 → 应急预案 → 附件

## 详细文档索引

| 文档 | 内容 |
|:-----|:-----|
| [references/input-requirements.md](references/input-requirements.md) | 用户输入规范（4 类 12 项参数） |
| [references/process-flow.md](references/process-flow.md) | 5 步处理流程详细分解 |
| [references/regulations-summary.md](references/regulations-summary.md) | 法规摘要（[法规编号]、CEM、ISO 31000） |
| [references/hazard-library.md](references/hazard-library.md) | 危害识别库 + 气体容忍标准 + 风险矩阵 |
| [references/control-measures.md](references/control-measures.md) | 控制措施库（工程/行政/PPE/紧急救援） |
| [references/document-templates.md](references/document-templates.md) | 3 套文档模板结构 |
| [references/compliance-checklist.md](references/compliance-checklist.md) | 合规检查清单 |

## 参考文件

> 以下文件为本技能的法规依据，存放于用户本地，技能本身不附带文件内容。

| 文件 | 说明 |
|:-----|:-----|
| [当地安全法规] | [当地安全法规]《建筑业职业安全健康法例》§161-172 |
| 密闭空间风险指南 | [劳工部门]《密闭空间工作是全指南》 |
| 密闭空间作业指引 | 密闭空间作业安全作业指引 |
| [安全管理手册] | [Safety Management Manual] (A.2.5/C.1.8) |

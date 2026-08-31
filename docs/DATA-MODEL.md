# Core Data Model — Phase 1 v0.1

## Purpose

Phase 1 将 Phase 0 的概念转成机器可读实体。所有 schema 使用 JSON Schema Draft 2020-12，当前 `schema_version` 为 `0.1.0`。

## Entity flow

Event → Evidence → Edge → Scenario → Exposure → Alert

Capability 与上述链条并行，供 Exposure 与 Preparedness Engine 判断 Readiness Gap、Base Autonomy、转换能力与行动可行性。

## Entities

### Event
描述发生了什么。包含 P0/P1/P2、观测域、A/B/C/D 映射和事件状态，但不直接声明因果。

### Evidence
描述“凭什么这么判断”。每条 evidence 强制区分：
- fact
- forecast
- correlation
- causality
- opinion

并记录来源类型、是否一手来源、独立性、交叉验证数量和置信度。

### Edge
描述节点之间的传导关系。状态严格使用 H0/H1/H2/H3/Hx，并支持 common-cause、反证、时滞、持续性和 falsification condition。

H2/H3 在 schema 层要求至少两个 evidence reference；是否真正独立、是否足以构成因果，仍由 Evidence/Audit 层判断。

### Scenario
描述“如果这些边继续发展，会发生什么”。必须记录 Probability、Impact、Velocity、Lead Time、Reversibility，以及触发条件和证伪条件。

### Exposure
把 Event/Scenario 映射到一个不透明 subject_ref。公开数据不得用真实姓名、地址或可定位资产信息。

### Capability
描述现实准备能力与依赖：状态、容量验证级别、自治时间、单点故障、Dual-Use Value、Conversion latency。

### Alert
是对用户的输出，而不是新闻本身。P-Level、Global Stage、Personal R-Level、Governance G-Level 分字段保存，禁止混成一个“风险等级”。

## Public/private rule

公开仓库可以保存 schema、模型和 synthetic examples；真实 Personal Exposure 与 Capability operational data 必须进入独立私有数据层。

## Non-goals of Phase 1

- 不在本阶段定义 Coupling Density 精确公式；
- 不在本阶段冻结 R-Level 触发阈值；
- 不在本阶段存放真实个人资产清单；
- 不把 correlation 自动升级成 causality。

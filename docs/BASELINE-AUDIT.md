# Baseline Audit Framework — Phase 3A

## Objective

把 Preparedness 从“我好像有这些东西”升级成“哪些能力已被验证、能维持多久、第一失效点在哪里”。

核心纪律：

> 拥有 ≠ 可用；可用 ≠ 可持续；可持续 ≠ 自给。

## Capability Audit

每项关键能力至少记录：

- domain
- criticality
- verification status
- availability status
- autonomy days
- dependencies
- backup status
- single points of failure
- maintenance status
- replenishment status
- conversion latency
- last verified time
- evidence refs

### Verification ladder

- stated：口述/文档陈述，未实测
- measured：有测量数据，但未完整压力测试
- field_tested：现实条件下完成测试
- audited：按定义、证据和边界完成独立复核

只有 field_tested / audited 且 availability 为 available/degraded，才进入 confirmed domain。

## Base Autonomy Days

Base Autonomy Days 不取平均。

只有 required domains 全覆盖，且所有 critical capabilities 的 availability/autonomy 已知，才允许计算。

计算规则：

`Base Autonomy Days = min(critical capability autonomy_days)`

因此第一失效点决定真实自治上限。

### Fail closed

- required domain 缺失 → INCOMPLETE，禁止虚构自治天数
- critical capability 的 availability/autonomy 未知 → UNKNOWN
- critical capability 明确 unavailable → DEGRADED / 0 days，即使 autonomy_days 尚未填写
- 全部关键能力已知 → AUDITED

## Single Point of Failure

关键能力出现以下任一情况即标记：

- 显式 single_points_of_failure 非空
- critical dependency 没有 backup
- critical dependency backup 状态 unknown

系统必须把它们作为 readiness gap 输出，而不是藏在平均分下面。

## Public/private rule

本公开仓库只保存 audit schema、算法和 synthetic examples。

真实现金流、资产数量、厂房/土地、井水、光伏/储能、车辆、食品、医疗、通信、Physical AI 部署、人员与位置数据必须进入私有 state 层。

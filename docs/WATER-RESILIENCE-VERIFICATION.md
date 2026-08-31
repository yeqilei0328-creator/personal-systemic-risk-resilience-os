# Water Resilience Verification v0.1

## Why water is audited as a chain

“有井”只能证明一个潜在水源存在，不能证明在停电、污染、泵故障或长期高负荷条件下仍有可饮用水。

水韧性链：

`Source → Extraction → Power → Storage → Treatment → Quality → Distribution → Maintenance/Spares → Outage Test`

任何关键环节未知，都会限制验证等级。对 extraction power requirement 和 treatment requirement 这类尚未确认的事实，允许显式记录为 `null/unknown`，不得为了通过 schema 强行填写 true/false。

## Verification ladder

### stated
只知道水源存在或有人陈述存在。

### measured
至少有可复核的供水测量，例如：
- 持续流量测试；或
- 可用储水容量测量。

这仍然不等于停电可用，也不等于可饮用。

### field_tested
必须通过现实 outage/degraded-mode 测试：
- 断开正常外部依赖后仍能取水；
- 若目标包括饮用水，水质有适当实验室/权威证据；
- 若需要处理，处理路径已实际测试；
- 记录测试持续时间。

系统只记录 **minimum demonstrated continuity**，不因为井能持续出水就写“无限自治”。

### audited
在 field_tested 基础上，还要求：
- evidence 完整；
- maintenance current；
- 独立复核完成；
- 关键 dependency 有可用 backup；
- 已知 SPOF 已清除或降级处理。

## Potability safety gate

以下信息不能单独证明饮水安全：
- 肉眼清澈；
- 无异味；
- 口感正常；
- TDS/电导率；
- 普通家用传感器。

如系统用途包含 potable/mixed，只有适当实验室或主管机构证据才通过 potability gate。具体检测项目应依据当地水源风险和适用标准确定。

## Measurements to collect

1. source verification
2. flow / pump-test result
3. usable storage
4. extraction power path
5. backup power
6. treatment path
7. water-quality evidence
8. daily demand assumption
9. outage/degraded-mode test duration
10. pump/filter/spares and maintenance
11. critical dependencies / SPOFs

## Autonomy discipline

- `storage_autonomy_days = usable_storage / daily_demand` only when both are measured/defensible.
- Continuous well flow creates a **continuous_source_candidate**, not an infinite-day claim.
- Outage testing produces a **minimum demonstrated continuity** lower bound.
- Base Autonomy should only consume a water autonomy value that is defensible under the relevant scenario.

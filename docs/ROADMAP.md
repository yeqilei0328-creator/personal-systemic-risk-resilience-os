# Roadmap — Pre-V1.0

## Phase 0 — Architecture Baseline — COMPLETE
- [x] 总体架构
- [x] 四元多边模型
- [x] 告警等级分离
- [x] Preparedness 概念
- [x] 情报触达原则
- [x] 反末日偏差机制
- [x] Public/private data boundary

## Phase 1 — Data Model — COMPLETE
- [x] Event schema
- [x] Evidence schema
- [x] Edge schema
- [x] Scenario schema
- [x] Exposure schema
- [x] Asset/capability schema
- [x] Alert schema

## Phase 2 — Quantification — COMPLETE
- [x] Coupling Density v0.1
- [x] Buffer Depletion v0.1
- [x] Edge validation scoring / recommendation
- [x] R-level action thresholds v0.1
- [x] Deterministic tests and CI

## Phase 3 — Baseline Audit

### Phase 3A — Audit Framework — COMPLETE
- [x] Capability Audit schema
- [x] Preparedness Snapshot schema
- [x] Base Autonomy / First Failure Point
- [x] Missing/unknown fail-closed behavior
- [x] Single Point of Failure detection
- [x] Public-method / private-state contract

### Phase 3B — Private Operational State Bootstrap — COMPLETE
Separate private operational-state layer established, pinned to public method version and validation-enabled.

### Phase 3C — Capability Verification & Baseline Completion — NEXT

Private audit domains:
- [ ] 现金流
- [ ] 流动性 / 金融资产
- [ ] 房产 / 资产处置
- [ ] 工业空间 / 厂房
- [ ] 土地 / 转换能力
- [ ] 水源 / 净化 / 储水
- [ ] 光伏 / 储能 / 离网能力
- [ ] 车辆 / 机动
- [ ] Physical AI / 防御性感知与巡检
- [ ] 网络 / 通信 / 离线计算
- [ ] 食品 / 农业转换
- [ ] 医疗 / 卫生
- [ ] 工具 / 备件 / 维修
- [ ] 离线知识库
- [ ] 人员 / 技能 / 可信网络

Exit gate:
- required private domains sufficiently covered;
- critical capabilities no longer unknown where evidence can reasonably be obtained;
- first-failure point and autonomy are derived only from measured/field-tested/audited evidence;
- real SPOFs and readiness gaps are explicitly surfaced.

## Phase 4 — Playbooks — NOT STARTED
- [ ] 金融危机
- [ ] 台海 / 区域战争
- [ ] 能源 / 粮食冲击
- [ ] 极端气候 / 自然灾害
- [ ] 网络 / 电力 / 物流中断
- [ ] 多系统闭环危机

## Phase 5 — Red Team & V1.0 Gate — NOT STARTED
- [ ] Historical calibration / backtest
- [ ] False-positive / false-negative audit
- [ ] 模型反证
- [ ] 行动成本与可逆性审计
- [ ] 数据完整性审计
- [ ] 用户批准后冻结 V1.0

See `docs/PROJECT-STATE.md` for the current execution checkpoint.

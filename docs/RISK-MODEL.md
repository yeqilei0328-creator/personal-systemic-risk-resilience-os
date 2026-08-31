# Four-Source Multi-Edge Risk Model — Draft 0.2

## Core hypothesis

系统风险的危险程度，不仅取决于单个冲击强度，更取决于：

- Risk Correlation：风险相关性；
- Coupling Density：系统耦合密度；
- Feedback Closure：反馈闭合程度；
- Buffer Depletion：系统缓冲能力衰减。

## Global stages

- Stage I — Point Risk Rise：单点风险上升。
- Stage II — Multi-System Coupling：多系统耦合。
- Stage III — Feedback Formation：闭合反馈正在形成/已形成。
- Stage IV — Critical Transition：临界跃迁 / Regime Shift。

当前架构纪律：Stage II 与 Stage III 必须通过“边”的证据判定，不能凭新闻数量或主观末日感升级。

## Edge validation

一条边从 hypothesis 升级为 validated edge，至少需要：
1. 明确的时序关系；
2. 两个以上独立高质量证据源；
3. 存在可解释机制；
4. 排除明显共同原因或标记为 common-cause；
5. 至少一个量化观测指标；
6. 记录反证与替代解释。

建议状态：
- H0 Hypothesis
- H1 Supported
- H2 Validated
- H3 Strong / Persistent
- Hx Falsified

## Coupling Density

初版不做伪精确百分比。先计算：
- 已验证边数量；
- H2/H3 边占比；
- 跨一级变量边数量；
- 同一冲击同时触发的一级变量数量；
- 关键节点入度/出度；
- Buffer 状态。

## Closed Feedback Loop

仅当路径最终回到起点并存在现实强化证据时认定。示例：
Geopolitics → Energy → Inflation → Rates/Fiscal → Growth/Social Stress → Geopolitics。

## Anti-double-count rule

若多个节点由同一上游冲击驱动，必须标记 common cause，不得按多个独立事件重复计票。

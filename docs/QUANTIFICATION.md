# Quantification v0.1

## Principle

本阶段拒绝单一“末日总分”。原因很简单：把战争、油价、债券、气候和 AI 估值压成一个 73.6 的数字，看起来像科学，实际上很容易只是精致的胡扯。

v0.1 输出四类可审计结果：

1. Coupling Vector + C0-C3
2. Buffer Vector + B0-B3
3. Edge State Recommendation H0/H1/H2/H3/Hx
4. Personal Action Gate R0-R5

所有阈值均为 **provisional**。它们是可测试的工程假设，不是自然常数。

## 1. Coupling Density v0.1

### Reported vector

- supported edge count
- validated edge count
- H3 strong edge count
- validated cross-variable edge count
- unique directed A/B/C/D pairs
- independent directed pairs after common-cause exclusion
- raw pair density
- independent pair density
- active variable breadth
- persistent validated edge count
- common-cause share
- longest independent simple path

### C bands

- C0 Sparse：独立 validated directed pairs < 2。
- C1 Emerging：>=2 pairs，至少涉及 2 个一级变量。
- C2 Dense：>=4 pairs，至少 3 个一级变量，且 >=2 条 persistent/structural validated edges。
- C3 Networked：>=6 pairs，A/B/C/D 全覆盖，>=4 persistent edges，>=2 H3 edges，且存在长度 >=3 的独立传导路径。

**C-band ≠ Global Stage。**
Stage III 仍然需要真实 feedback closure 证据，不能因为 C3 就自动宣布闭环成立。

### Common-cause rule

被标记 `common_cause.present=true` 的 validated edge 仍计入 raw evidence，但不计入 independent pair density。目的就是防止“一场战争同时推高油价、通胀和收益率”被算成三个互相独立的冲击。

## 2. Buffer Depletion v0.1

单个 buffer 的剩余比例：

`remaining = (current - minimum_viable) / (baseline - minimum_viable)`

限制在 0..1。

系统不取简单平均值，优先看 criticality >=4 的 buffer：

- 最弱关键 buffer 剩余比例
- <75% / <50% / <25% 的关键 buffer 数量
- 正在净消耗的关键 buffer 数量
- 最早触及 minimum viable floor 的估计天数

### B bands

- B0 Healthy：关键 buffer 均 >=75%，且没有净消耗。
- B1 Strained：最弱关键 buffer <75%，或至少一个关键 buffer 正在净消耗。
- B2 Low：最弱关键 buffer <50%。
- B3 Depleted：最弱关键 buffer <=10%，或至少两个关键 buffer <25%。

它表达“系统还能吸收多少冲击”，不是资产价格预测。

## 3. Edge validation gates

H2 至少要求：

- >=2 个独立高质量支持来源；
- mechanism documented；
- temporal ordering confirmed；
- quantitative metric observed；
- unresolved common cause = false；
- unresolved high-quality counterevidence = false。

v0.1 的“高质量”最低线：
- provenance >= 0.70
- independence >= 0.60
- confidence >= 0.60

H3 进一步要求：
- >=3 个独立高质量来源；
- 至少 3 个 assessment windows 持续成立；
- edge persistence 为 persistent 或 structural。

若 falsification condition 被触发，推荐 Hx。

推荐值不自动覆盖人工审计状态。它是机器的结构化建议，不是神谕。

## 4. Personal R-Level gates

R-Level 是行动等级，不是 Global Stage。

- R0 Normal：没有个人行动门槛被触发。
- R1 Watch：有材料值得盯，但不足以做高成本动作。
- R2 Prepare：开始低成本、可逆、双用途准备；可以由“高后果 + 长准备周期”提前触发。
- R3 Alert：高影响 + 实质暴露 + 概率/速度上升 + 行动窗口压缩。
- R4 Emergency：直接/当地扰动或严重治理退化已经影响现实连续性。
- R5 Survival：当前 life-safety capability 已经失效。

v0.1 的概率门槛只是 calibration seed。未来必须用历史事件、误报/漏报和行动成本回测。

## 5. What this model must never do

- 不把 C3 自动翻译成 Stage III。
- 不把 B3 自动翻译成 R4。
- 不把 correlation 自动升级为 causality。
- 不把多个 common-cause downstream effects 重复计票。
- 不把“模型建议”伪装成确定预测。
- 不允许一个漂亮总分掩盖第一失效点。

# World Intelligence Engine — Radar Precision Upgrade v0.1

## Objective

精准捕捉“改变判断”的全球事件，而不是制造坏消息流。

现有新闻推送对话继续作为用户前台。升级重点放在后台判断、状态记忆、去重、耦合变化与精准告警。

## Preserve

- P0 / P1 / P2
- Physical AI Radar
- 前台简洁结论
- 后台 Evidence · Behavior · Systems
- “没有改变判断的新闻，不应该打扰用户”

## Input domains

- 地缘政治与军事冲突
- 能源、粮食、水与航运
- 财政、主权债务、利率、房地产、银行与资本流动
- 气候、厄尔尼诺、自然灾害
- AI CapEx、估值、融资、技术周期
- 全球贸易、供应链、资本体系
- 社会动荡、治理变化
- Physical AI Radar

## Target pipeline

Discovery
→ Event Fingerprint / Dedup
→ Source Quality / Provenance
→ Claim Split
→ Fact / Forecast / Correlation / Causality / Opinion
→ Behavior vs Rhetoric
→ Counterevidence / Falsification
→ Four-Source Mapping (A/B/C/D)
→ Edge Delta
→ Coupling Delta
→ Buffer Delta
→ Scenario Delta
→ Personal Exposure / Lead-Time Delta
→ Alert Gate
→ Existing news-push conversation

## Precision alert gate

默认只在以下条件之一成立时通知：
- P0 must-know 事件；
- 多环节同步恶化；
- 新的或更强 validated edge；
- Coupling Density 有实质改变；
- feedback-loop candidate 强化/削弱；
- Buffer 明显耗尽或恢复；
- Scenario probability / velocity / Lead Time 有实质变化；
- Global Stage / Personal R-Level 改变；
- 关键假设被证伪；
- Action Playbook 需要改变。

其余更新进入状态存储，不主动打扰。

## Alert suppression

必须具备：
- duplicate suppression
- update-vs-new-event detection
- cooldown
- material-change threshold
- hysteresis around thresholds
- explicit “no substantive change = no notification”

## Chain Watch v0.1

第一条显式共振链：

Climate / El Niño
→ Food & Energy
→ Inflation / Inflation Expectations
→ Fed / Monetary Policy
→ UST 10Y / 30Y + Financial Conditions / Fiscal Pressure
→ AI CapEx / Tech Valuation / Financing Stress

每一环必须区分：
- Fact
- Forecast
- Correlation
- Causality
- Counterevidence

输出的是链条状态变化，不是孤立头条。

## Output contract

前台告警回答：
1. 发生了什么变化？
2. 哪条边/链发生变化？
3. 为什么重要？
4. 哪些关键部分仍未证实？
5. 有什么反证/缓冲？
6. Global Stage 是否变化？
7. Personal action 是否变化？
8. 下一个升级/降级信号是什么？

Keep concise.

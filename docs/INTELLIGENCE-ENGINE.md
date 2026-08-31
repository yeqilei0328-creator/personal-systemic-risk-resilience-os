# World Intelligence Engine — Draft 0.2

## Objective

精准捕捉“改变判断”的全球事件，而不是制造坏消息流。

## Input domains

- 地缘政治与军事冲突
- 能源、粮食、水与航运
- 财政、主权债务、利率、房地产、银行与资本流动
- 气候、厄尔尼诺、自然灾害
- AI CapEx、估值、融资、技术周期
- 全球贸易、供应链、资本体系
- 社会动荡、治理变化
- Physical AI Radar

## Processing pipeline

Discovery → Dedup → Source Quality → Claim Split → Fact/Forecast/Correlation/Causality → Cross-source Verification → Four-Source Mapping → Edge Update → Scenario Update → Exposure Update → Alert Gate

## Precision gate

只有以下情况默认主动通知：
- P0 事件；
- 多环节同步恶化；
- Coupling Density 明显改变；
- 新闭环候选形成；
- 风险等级改变；
- 关键假设被证伪；
- Lead Time 明显缩短；
- Action Playbook 需要改变。

若无实质变化，不通知。

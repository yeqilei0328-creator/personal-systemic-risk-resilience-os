# China Intelligence / Physical AI / Global Risk Resonance
## 推送逻辑与运行逻辑底层架构规范 V0.3

**文档状态：** Operational Specification  
**版本：** V0.3  
**日期：** 2026-08-31  
**适用范围：** China Morning Intelligence Brief、Physical AI Radar、Global Risk Resonance  
**核心原则：** 后台复杂，前台简单；事实先于判断；行为重于语言；系统重于单条新闻；变化重于重复；宁缺毋滥。

---

# 0. 这套系统到底要解决什么

这不是“新闻摘要器”。

它的目标是把公开世界中的大量、重复、互相矛盾、带有立场、宣传、匿名消息和信息噪声的材料，转换成三个层次的输出：

1. **中国情报简报**
   - 每天回答：中国相关真正值得知道的事情是什么？
   - 什么已经确认？
   - 什么仍是未确认 Claim？
   - 哪些变化会影响经济、金融、政策、外交、安全、产业和技术？

2. **Physical AI Radar**
   - 每天回答：全球 Physical AI / 无人系统 / 机器人 / 边缘智能领域，有没有足以改变工程判断的新东西？
   - 是论文、Demo、商业部署，还是经过真实环境或战场验证？
   - 对 Physical AI OS 的架构、能力、安全和工程路线有什么实际影响？

3. **Global Risk Resonance**
   - 不统计“坏新闻数量”。
   - 监测多个风险系统是否开始通过能源、航运、供应链、财政、金融、粮食、基础设施等通道发生真实耦合。
   - 只有共振程度跨过阈值时才报警。

系统的核心不是“看到更多”，而是：

> **减少假信息、减少重复、减少叙事绑架，提高事实密度、行为密度和系统判断密度。**

---

# 1. 总体运行拓扑

```text
                      ┌────────────────────────────┐
                      │       Scheduler / Trigger   │
                      └──────────────┬─────────────┘
                                     │
                  ┌──────────────────┼──────────────────┐
                  │                  │                  │
                  ▼                  ▼                  ▼
        China Intelligence    Physical AI Radar   Global Risk Resonance
                  │                  │                  │
                  └──────────────┬───┴──────────────────┘
                                 ▼
                     Multi-source Discovery
                                 ▼
                      Candidate Event Pool
                                 ▼
                    Cluster / Deduplicate
                                 ▼
                       Atomic Claim Split
                                 ▼
                    Evidence Acquisition
                                 ▼
                Independence / Provenance Check
                                 ▼
                  Claim Confidence A / B / C / D
                                 ▼
                 Evidence · Behavior · Systems
                                 ▼
          Importance / Relevance / Coupling Assessment
                                 ▼
                    Material Change Detection
                                 ▼
              Output Gate / Alert Threshold Gate
                                 ▼
                     Front-end Simplification
                                 ▼
                     Judgment Ledger Update
                                 ▼
                       Posterior Revision
```

---

# 2. 当前实际推送形态

## 2.1 China Morning Intelligence Brief V0.3

**状态：启用**

- 频率：每天一次
- 时间：08:00
- 模式：固定时点运行
- 内容：
  - 中国重要事件 P0-P2
  - 固定附带 `Physical AI Radar｜全球物理智能前沿`
- 不再启用：
  - 晚间重复简报
  - 每小时 China / Physical AI P0 扫描

原因不是“少看新闻”，而是减少推送噪声。日常信息统一压缩到晨报；真正跨系统升级的重大风险交给独立条件监测。

---

## 2.2 Global Risk Resonance

**状态：启用**

- 模式：Condition Watch
- 检查频率：约每 6 小时一次
- 正常情况下：**保持沉默**
- 只有达到共振阈值或出现足以改变总体判断的重大事件时才推送。

它不是第二份新闻简报，而是一个异常检测器。

---

# 3. 运行纪律

整个系统遵守以下硬规则：

### Rule 1：单一媒体不能决定“什么值得被看见”

Reuters、AP、FT、WSJ、Bloomberg 等只能成为发现源和证据源之一。

不能采用：

```text
Reuters 首页有什么
    ↓
今天就看什么
```

而必须采用：

```text
多个来源并行扫描
    ↓
形成候选事件池
    ↓
按事件真实重要性筛选
```

---

### Rule 2：转载不等于独立验证

例如：

```text
Reuters 原始报道
↓
Yahoo 转载
↓
MSN 转载
↓
地方媒体翻译
```

只能算：

> **1 个原始来源**

不能算四个独立来源。

---

### Rule 3：报道存在 ≠ 报道内容已经成为事实

可以确认：

> Reuters 报道“某匿名官员称 X”。

不能因此改写为：

> X 已经发生。

---

### Rule 4：官方声明也不是天然事实

官方来源对以下内容通常具有高证据价值：

- 法律文本
- 行政命令
- 任免
- 财报
- 政策文件
- 已公开预算
- 已签署协议
- 官方统计数据库

但在以下领域必须保持区分：

- 战果
- 伤亡
- 击落数量
- 敌方损失
- 战争责任
- 动机
- 情报判断
- 外交归因

这些仍然属于 Claim，需要独立验证。

---

### Rule 5：不为了凑数推送

一天只有一个真正重要事件，就只推一个。

Physical AI 一天没有值得改变工程判断的新内容，就明确写：

> 无重要新增。

而不是把普通机器人新品、公司营销稿、benchmark 提高 2% 包装成“技术革命”。

---

# 4. 多源采集层

## 4.1 第一层：全球主流独立媒体

默认平行扫描：

- Reuters
- AP
- AFP
- Bloomberg
- Financial Times
- Wall Street Journal
- New York Times
- BBC
- Washington Post
- Nikkei Asia / 日本经济新闻
- South China Morning Post

这些来源主要承担：

- 快速发现
- 独立采访
- 跨国信息拼接
- 市场与政策反应
- 现场核验
- 匿名渠道发现

但任何一家都没有“事实裁决权”。

---

## 4.2 第二层：中国专业财经与产业媒体

必要时扫描：

- 财新
- 第一财经
- 经济观察报等高质量专业来源
- 证券、产业、公司专业媒体

用途主要是：

- 补中国本地产业背景
- 监管与企业信息
- 政策执行层细节
- 国内金融市场反馈

---

## 4.3 第三层：原始来源

这是事实确认的重要基础。

### 中国

包括但不限于：

- 国务院
- 外交部
- 国防部
- 国家统计局
- 中国人民银行
- 财政部
- 商务部
- 海关总署
- 国家发改委
- 工信部
- 网信办
- 中国证监会
- 交易所
- 法院
- 上市公司公告
- 企业财报

### 境外

例如：

- White House
- USTR
- US Treasury
- US Commerce
- Pentagon / US military
- EU Commission
- NATO
- WTO
- IMF
- World Bank
- 各国政府和监管机构
- 公司 SEC / exchange filing
- 官方预算和法律文本

---

## 4.4 第四层：Physical AI 原始技术源

优先级高于科技媒体二次报道：

- arXiv
- IEEE
- ACM
- 顶级会议论文
- 作者实验室
- 大学/研究机构
- 官方 GitHub
- 官方模型仓库
- 公司技术博客
- 产品技术文档
- 标准组织
- 专利与公开技术报告

媒体只用于：

- 商业背景
- 真实部署
- 事故
- 市场采用
- 产业影响

---

## 4.5 第五层：战争、高对抗与安全来源

包括：

- 各国军方原始材料
- Defense News
- Breaking Defense
- 高质量调查媒体
- 公开视频
- 独立 OSINT
- 地理定位
- 卫星图像
- 武器残骸分析
- 企业硬件确认
- 官方战报

其中必须记录 **证据类型**，不能把它们混成一种来源。

---

## 4.6 第六层：自然灾害与系统风险原始数据

重点包括：

- GDACS
- NASA disaster response
- NOAA
- USGS
- 气象机构
- 地震机构
- 各国灾害管理部门
- 水文机构
- 卫星监测
- 电网/港口/航运公开数据
- 国际能源与粮食机构

---

# 5. 时间窗口设计

系统不是只搜“过去 24 小时”。

不同任务使用不同时间尺度。

## 5.1 T0：即时窗口

通常：

- 0-24h

用于：

- 新事件发现
- 最新伤亡
- 政策公布
- 战场变化
- 市场即时反应
- 新论文/新产品/新部署

---

## 5.2 T1：短期上下文

通常：

- 3-15 天

用于判断：

- 这是第一次出现，还是持续趋势？
- 数字是否恶化？
- 是否只是旧新闻重复？
- 行为是否连续？
- 市场是否已经反应过？

---

## 5.3 T2：结构窗口

通常：

- 30-90 天

用于：

- Global Risk Resonance
- 联盟重组
- 财政和军事资源投入
- 能源航运持续扰动
- 军备趋势
- 中国政策方向
- AI资本周期

---

# 6. 候选事件池

所有发现先进入 **Candidate Event Pool**。

此时不做最终结论。

建议内部事件对象：

```yaml
event_id:
first_seen:
last_updated:
domain:
actors:
location:
event_type:
raw_sources:
primary_sources:
candidate_claims:
material_change:
priority_candidate:
system_links:
```

候选池包括：

- 中国政策
- 宏观经济
- 金融市场
- 产业
- 科技
- 外交
- 军事
- 台海/南海
- 制裁与出口管制
- 重大企业
- 灾害
- Physical AI
- 战争无人系统
- 能源
- 航运
- 供应链
- 全球风险

---

# 7. 事件聚类与去重

不同媒体会用完全不同的标题描述同一事件。

系统按以下字段判断是否属于同一事件：

```text
Actor
+ Action
+ Object
+ Location
+ Time Window
+ Consequence
```

形成：

> Event Cluster

例如：

- “美国袭击伊朗导弹阵地”
- “美军重新对伊朗开火”
- “Pentagon confirms strike near Strait of Hormuz”

如果指向同一行动，则属于一个 Cluster。

---

## 7.1 Material Change

同一事件只有出现真实变化才重新升级：

- 伤亡明显变化
- 政策正式落地
- 调查变成起诉
- 谈判变成协议
- 宣言变成预算
- 预算变成采购
- 采购变成交付
- Demo 变成部署
- 测试变成规模生产
- 军事威胁变成实际攻击
- 航运风险变成实际停航
- 市场预期变成真实价格传导

这叫：

> **Material Change Detection**

不是标题更新检测。

---

# 8. Claim 原子化

每个事件必须拆成多个独立 Claim。

例如：

> “A 国计划购买 24 架 J-10CE，首批 6 架已经交付。”

必须拆成：

```text
Claim 1：A国已经接收J-10CE
Claim 2：已公开看到至少6架
Claim 3：总订单为24架
Claim 4：采购行为意味着战略转向
```

这四个 Claim 的证据等级完全可以不同。

---

## 8.1 Claim 类型

至少区分：

- 存在性 Claim
- 时间 Claim
- 数量 Claim
- 身份 Claim
- 行为 Claim
- 法律状态 Claim
- 因果 Claim
- 动机 Claim
- 意图 Claim
- 预测 Claim
- 战果 Claim
- 技术性能 Claim
- 商业规模 Claim

因果、动机、预测的证据门槛高于“某件事发生了”。

---

# 9. Claim 可信度 A / B / C / D

## A｜已确认

通常满足以下一种或多种：

- 原始法律/政策/监管文件
- 可核验官方数据库
- 公司正式财报/公告
- 真实公开行动
- 公开交付/部署
- 多个相互独立的高质量来源一致确认
- 可验证视频/卫星/地理定位证据
- 技术论文原文 + 可复核实验

A 不代表“永远不会修正”。

它只表示：

> 以当前公开证据，该 Claim 已达到事实使用标准。

---

## B｜高可信未确认

典型情况：

- Reuters / Bloomberg / FT 等高质量独立采访
- 两个以上独立记者渠道指向相同事实
- 高可信匿名官员消息
- 已存在部分行为证据，但缺少正式文件
- 战场多源信息高度一致但没有完整独立验证

注意：

> **匿名知情人士最高通常只能到 B。**

不能因为媒体声誉高就自动变成 A。

---

## C｜发展中 / 未充分验证

例如：

- 单一匿名来源
- 单一官方战报
- 未定位公开视频
- 企业自报性能
- 战场 Telegram / social claim
- 未有交叉验证的采购数量
- 早期事故数字

---

## D｜分析 / 意见 / 预测

包括：

- 评论文章
- 战略判断
- 因果模型
- 预测
- 专家观点
- 本系统的推断

D 不等于没价值。

它只是必须和事实分开。

---

# 10. 来源独立性验证

系统检查：

```text
Source A 是否自己采访？
Source B 是否只是引用 Source A？
Source C 是否来自同一匿名官员？
Source D 是否来自同一新闻稿？
```

真正独立来源必须至少在以下某个维度独立：

- 独立记者采访
- 独立官方文件
- 独立现场验证
- 独立卫星/视频/地理证据
- 独立公司公告
- 独立数据库

---

# 11. Source Reputation Ledger

来源信誉不是固定常数。

系统按 **领域 × Claim 类型** 动态评价。

例如：

```text
Reuters
外交人事：强
市场即时报道：强
战场数量：仍需验证

官方军方
己方行动存在性：较强
敌方损失数量：明显降权

企业新闻稿
产品存在：强
产品性能：中低
市场领先地位：低
```

---

## 11.1 动态信誉维度

可以长期记录：

- 原始报道比例
- 后续被确认比例
- 更正频率
- 匿名来源依赖度
- 标题夸张度
- 专业领域强项
- 战场 Claim 准确度
- 企业 PR 复制程度
- 独家提前量
- 错误方向是否系统性偏置

---

## 11.2 不永久封杀低信誉来源

低信誉来源仍可能用于：

- Narrative monitoring
- Propaganda detection
- 异常信号
- 反向指标
- 线索发现

但不能独立完成事实升级。

这样避免建立新的信息茧房。

---

# 12. Evidence 层

对每个 Claim，系统内部至少回答：

1. 谁说的？
2. 他是否有能力知道？
3. 他是否有动机误导？
4. 有没有原始文件？
5. 有没有独立来源？
6. 有没有物理行为证据？
7. 有没有反证？
8. 有没有关键未知项？
9. 数字是否稳定？
10. 事实与解释是否被混在一起？

---

# 13. Behavior 层

这套系统的核心原则之一：

> **语言是低成本信号，行为是高价值信号。**

因此优先观察：

- 调兵
- 部署
- 发射
- 攻击
- 撤离
- 建设
- 采购
- 预算
- 生产
- 制裁执行
- 港口停运
- 船舶改道
- 保险提价
- 资本投入
- 工厂扩产
- 公司真实收入
- 产品真实交付
- 真实机器人部署
- 实际开源
- 真实战场使用

---

# 14. Costly Signal Test

系统判断一个行为是否具有更高信息价值时，会问：

### 14.1 是否消耗真实资源？

例如：

- 钱
- 军事资产
- 外汇
- 产能
- 人员
- 政治资本
- 时间

### 14.2 是否持续？

一次发言很容易。

连续数月：

- 扩军
- 采购
- 建岛
- 扩产
- 制裁
- 调整供应链

信息价值更高。

### 14.3 是否难以逆转？

例如：

```text
讲话 < 备忘录 < 正式协议 < 预算 < 建厂 < 实际部署
```

越靠后，Costly Signal 越强。

---

# 15. Rhetoric–Action Gap

系统主动比较：

```text
说了什么
vs
真正做了什么
```

例如：

> “不会升级冲突”

但同时：

- 增兵
- 调舰
- 追加弹药
- 部署防空
- 提高保险费
- 商船改道

系统会优先相信行为。

反过来也一样。

如果媒体不断描述“危机升级”，但：

- 部队没有增加
- 航运正常
- 油价回落
- 保险不变
- 外交渠道恢复

则应降低风险判断。

---

# 16. Narrative Gap

不同媒体对同一事件会使用不同叙事。

系统不把叙事差异本身当成事实差异。

例如：

```text
Media A：战略突破
Media B：危险升级
Media C：正常军事活动
Official：防御性行动
```

后台把这些分解成：

- 可验证行为
- 解释
- 情绪语言
- 国家利益
- 受众定位

然后重新判断。

---

# 17. Counter-evidence 与遗漏变量

系统必须主动寻找“为什么这个判断可能错”。

例如：

> 油价上涨 = 战争升级？

反证可能是：

- OPEC减产
- 美元变化
- 库存下降
- 季节性需求
- 炼厂事故

因此不能看到两个事件时间接近，就自动写因果箭头。

---

# 18. Systems 层

事件不是孤立存在。

系统至少拆成：

```text
Actor
Capability
Intent
Action
Constraint
Resource
Relationship
Feedback
Outcome
```

---

## 18.1 Capability ≠ Intent

有能力不代表准备行动。

## 18.2 Intent ≠ Action

政治语言不能替代真实行动。

## 18.3 Action ≠ Outcome

做了某件事不代表达到目标。

## 18.4 Outcome 会重新改变下一轮 Intent / Capability

因此整个世界更接近：

```text
State(t)
    ↓
Action
    ↓
Reaction
    ↓
New Constraints
    ↓
New State(t+1)
```

而不是线性新闻故事。

---

# 19. 系统耦合

Global Risk Resonance尤其关注：

> 不同风险系统之间是否出现真实传导边。

例如：

```text
中东战争
↓
霍尔木兹通行下降
↓
油轮战争险上涨
↓
原油/LNG上涨
↓
运输成本
↓
通胀预期
↓
利率路径
↓
企业融资成本
```

如果中间只有媒体讨论，没有真实价格、流量、预算或资源变化，不算强耦合。

---

## 19.1 Coupling Density

可以理解为：

> 一段时间内，不同风险系统之间被现实数据验证的有效传导边数量和强度。

比“有几个红灯”更重要。

---

## 19.2 Closed Feedback Loop

最危险的不是单向传导，而是反馈环：

```text
战争
↓
能源价格
↓
通胀
↓
财政压力
↓
政治不稳定
↓
军备/保护主义
↓
供应链成本
↓
更高通胀
```

一旦形成持续闭环，系统风险等级需要上调。

---

# 20. 中国事件重要性 P0-P3

可信度 A/B/C/D 与重要性 P0-P3 是两套完全不同的轴。

```text
A = 很确定
不代表
P0 = 很重要
```

---

## P0｜系统级重大事件

可能显著改变：

- 中国宏观经济制度
- 金融稳定
- 国家领导层
- 战争状态
- 台海/南海重大军事状态
- 中美关系基本结构
- 系统性制裁
- 金融系统
- 重大国家级科技禁令
- 极端大型灾害

P0 极少。

---

## P1｜高影响事件

可能改变：

- 一个重要政策方向
- 一个产业周期
- 一段外交关系
- 一个关键军事平衡
- 一个重要宏观变量

---

## P2｜值得记录

重要，但暂不足以改变总体状态。

---

## P3｜背景信息

通常不推送。

包括：

- 普通讲话
- 例行会议
- 重复观点
- 小幅市场波动
- 普通企业 PR
- 无新增事实的外交表态

---

# 21. China Morning Intelligence Brief 输出门

后台完成后，前台最多只留下少量结果。

## 21.1 今日总判断

最多 3 条。

回答：

> 今天世界/中国真正改变了什么？

---

## 21.2 事件格式

只保留 P0-P2。

每个事件最多四个字段：

### ① 发生了什么

只讲事实。

### ② 我们的判断

说明：

- A/B/C/D
- 当前到底能确认什么

### ③ 为什么重要

只讲真实影响。

### ④ 下一观察点

必须是一个能够验证未来路径的 observable signal。

---

## 21.3 可选第五句

只有必要时：

> **主要争议/未确认点：**

避免用户把 B/C Claim 当成事实。

---

# 22. Physical AI Radar

Physical AI Radar 不是机器人新闻栏目。

唯一的问题是：

> **这条信息会不会改变 Physical AI OS / AI物理智能体的工程判断？**

---

# 23. Physical AI 扫描范围

至少覆盖：

- UAV
- FPV
- swarm
- quadruped
- robot dog
- UGV
- humanoid
- robotic arm
- biomimetic robot
- micro robot
- perception
- detection
- segmentation
- tracking
- VLM
- VLA
- world model
- planning
- control
- multi-agent
- digital twin
- edge AI
- local AI
- low-power inference
- degraded runtime
- offline autonomy
- automated security
- fixed sensor + mobile robot
- counter-UAS
- EW
- GNSS-denied navigation
- communication relay
- autonomous target recognition

---

# 24. Physical AI 成熟度分级

一条技术必须说明“到底走到哪一步”。

```text
Research
↓
Simulation
↓
Lab Prototype
↓
Real-world Prototype
↓
Pilot
↓
Commercial Deployment
↓
Scaled Deployment
```

战争环境增加：

```text
Claimed Battlefield Use
↓
Media/OSINT Verified
↓
Repeated Battlefield Validation
↓
Doctrine / Procurement / Scaled Production
```

---

# 25. 战场 Claim 特殊证据梯

必须明确区分：

1. 官方战报
2. 企业自报
3. 公开视频
4. 独立地理定位
5. OSINT多源验证
6. 媒体现场核验
7. 残骸/硬件证据
8. 多次重复部署
9. 正式采购 / 规模生产 / 训练体系写入

“一个视频里看起来像”不能升级成“战争范式已经改变”。

---

# 26. Physical AI 工程相关性过滤器

每条候选必须回答：

### 是否改变以下之一？

- Device Adapter
- Capability Manifest
- source-neutral perception
- sensor fusion
- mission planning
- world model
- VLA policy
- runtime scheduling
- multi-agent coordination
- edge inference
- degraded runtime
- safety gate
- human authorization
- telemetry
- failure recovery
- digital twin
- counter-UAS
- fixed/mobile sensor coordination

如果答案都是“不”，大概率不值得推。

---

# 27. Physical AI Action Tag

## IGNORE

噪声、营销、重复、没有工程价值。

## WATCH

有潜力，但证据不足或成熟度太低。

## TECH-RADAR

值得正式进入技术雷达长期跟踪。

## ENGINEERING-IMPACT-PROPOSAL

已经足以提出：

> 是否需要改变系统架构、接口、Safety、Runtime 或工程 Roadmap？

这是最高工程等级。

---

# 28. Global Risk Resonance 五类核心信号

## Signal 1｜多个地缘冲突同步升级

重点：

- 俄乌
- 中东
- 南海
- 台海
- 其他具有外溢性的冲突

不是看“有没有战争”，而是看：

- 烈度
- 地理范围
- 参与者
- 武器层级
- 关键基础设施
- 联盟介入
- 是否同步升级

---

## Signal 2｜能源与航运通道

重点：

- Hormuz
- Red Sea
- Suez
- Bab el-Mandeb
- 关键油气运输线

观察：

- 船舶数量
- 改道
- 停航
- 油轮费率
- 战争险
- LNG
- Brent / WTI
- 港口状态

---

## Signal 3｜东亚安全结构

观察：

- 台海
- 南海
- 美日韩
- 菲律宾
- 澳大利亚
- 日本
- 东盟
- 基地
- 军演
- ISR
- 导弹
- 无人系统
- 联盟义务
- 军费
- 军工生产

---

## Signal 4｜极端天气与大型自然灾害

观察：

- 洪水
- 台风
- 山火
- 地震
- 冰川
- 冰湖
- 泥石流
- 热浪
- 干旱

但事件数量本身不是重点。

必须进一步看：

- 电网
- 港口
- 水电
- 粮食
- 交通
- 跨境基础设施
- 供应链

---

## Signal 5｜价格与实体传导

这是确认“共振”的重要桥梁。

观察：

- 原油
- LNG
- 粮食
- 海运
- 空运
- 战争险
- 供应链
- 通胀预期
- 利率
- 股市
- 信用利差
- 企业融资

---

# 29. Global Systemic Risk Index

至少维护以下维度：

| 维度 | 状态 |
|---|---|
| 俄乌 | 低 / 中 / 中高 / 高 / 极高 |
| 中东 | 同上 |
| 南海/台海 | 同上 |
| 全球军事联盟重组 | 同上 |
| 无人系统军备竞争 | 同上 |
| 能源/航运 | 同上 |
| 极端天气 | 同上 |
| 大型自然灾害 | 同上 |
| 全球系统性风险 | 同上 |

同时记录趋势：

```text
↓↓
↓
→
↑
↑↑
```

---

# 30. Global Risk Resonance 触发阈值

正常情况下：

> **不推送。**

只有以下情况之一成立才推送：

## Trigger A

五类核心信号中：

> **至少 3 类同时明显恶化**

而且必须有真实行为或数据证据，不是新闻标题数量增加。

---

## Trigger B

出现单一重大事件，足以改变全球系统判断。

例如：

- 霍尔木兹实际长期封锁
- 主要大国直接参战
- 东亚重大军事冲突
- 全球大型金融事故
- 极端大型能源冲击
- 多个关键基础设施同步失效

---

## Trigger C

出现新的强耦合边：

例如：

```text
战争
→ 航运中断
→ 能源价格
→ 保险
→ 金融市场
```

如果此前只有第一层，现在已经传到第四、第五层，可以触发新通知。

---

# 31. 共振告警输出格式

告警必须非常短。

只包括：

### ① 发生了什么

### ② 哪些风险正在共振

### ③ 为什么这次不是普通坏新闻堆积

### ④ Global Systemic Risk Index

### ⑤ 未来30-90天三个关键观察点

---

# 32. 防重复告警逻辑

已经报警过不代表后面每次检查都继续报警。

只有出现 **new information / material delta** 才再次推送。

例如：

第一次：

```text
军事冲突
→ 油价上涨
```

第二次如果只是油价继续维持：

> 不需要重复。

但如果出现：

```text
军事冲突
→ 航运下降
→ 保险上涨
→ 柴油贸易流重构
```

则属于新的系统传播层，可再次告警。

---

# 33. 判断账本 Judgment Ledger

每一次重要判断都应留下“当时版本”。

建议字段：

```yaml
timestamp:
event_id:
claim_id:
initial_confidence:
event_priority:
system_state:
current_finding:
predicted_path_1:
predicted_path_2:
tail_risk:
watch_signal:
source_set:
source_limitations:
later_result:
posterior_update:
error_type:
```

---

# 34. 为什么要保留判断账本

否则人脑会自动产生：

> “我早就知道。”

判断账本强制记录：

- 当时知道什么
- 当时不知道什么
- 当时概率是多少
- 之后到底发生什么

这样才能校准：

- 来源信誉
- 自己的预测
- 哪些变量经常被遗漏

---

# 35. Posterior Revision

新证据出现后，不是简单覆盖旧结论。

而是：

```text
Prior
+
New Evidence
+
Source Reliability
+
Counter Evidence
=
Posterior
```

例如：

```text
B 高可信
↓
官方文件出现
↓
A 已确认
```

或者：

```text
B 高可信
↓
政策最终未实施
↓
回看匿名来源和行为证据
↓
降低该类来源未来权重
```

---

# 36. Sources 与 Judgment 双重校准

系统不仅审计媒体，也审计自己。

## Source Ledger

回答：

> 谁在什么领域更可靠？

## Judgment Ledger

回答：

> 我们在哪种问题上容易判断错？

例如：

- 是否过度重视外交语言？
- 是否低估政策执行延迟？
- 是否把相关性误认为因果？
- 是否被单周灾害密度放大情绪？
- 是否过早判断技术会商业化？

---

# 37. Access Failure 处理

如果重要来源：

- robots 拒绝
- paywall
- 页面失效
- 只能看到摘要
- 无法读取正文

必须：

1. 明确标记访问限制。
2. 尝试原始来源。
3. 尝试其他独立媒体。
4. 不假装读过全文。
5. 如果核心结论高度依赖不可访问来源，降低置信度。
6. 在末尾“来源覆盖”披露。

---

# 38. Source Concentration Gate

如果一个重要事件：

- 只有一家媒体
- 只有匿名消息
- 其他媒体全部引用它

则必须明确：

> **单源偏置**

不能因为网上出现50个搜索结果就当成50个证据。

---

# 39. 数字动态事件

以下数字特别容易变化：

- 战争伤亡
- 灾害伤亡
- 失踪
- 无人机击落
- 导弹数量
- 订单金额
- 融资金额

处理方式：

```text
timestamp + source + confidence
```

必须明确：

> 截至什么时候。

旧数字不能和新数字混算。

---

# 40. 灾害事实判定

灾害需要拆分：

```text
Event existence
Casualty
Missing
Affected population
Cause
Secondary risk
Infrastructure impact
```

其中：

- 灾害发生可以 A
- 伤亡数字可能 C→B→A
- “气候变化导致这次灾害”通常需要更高因果证据

不能偷换。

---

# 41. 战争事实判定

战争信息至少拆成：

```text
Attack occurred
Weapon type
Launch count
Intercept count
Damage
Casualty
Target
Attribution
Intent
Strategic effect
```

其中“战略效果”通常不是 A 类事实。

---

# 42. 市场传导确认

系统性风险不能只用新闻语言确认。

至少寻找：

- price
- volume
- spread
- traffic
- insurance
- shipping
- inventory
- yield
- credit
- capacity utilization

即：

> **现实世界有没有付出价格？**

---

# 43. 每日输出不是完整数据库

后台可以存在几十个候选事件。

前台只输出：

```text
Top Judgments
+
P0-P2 China
+
Top Physical AI
+
Source Coverage
```

前台简洁不是分析少，而是筛选更严格。

---

# 44. 标准运行伪代码

```python
def run_intelligence_cycle():

    sources = parallel_discovery()

    candidate_pool = build_candidate_event_pool(sources)

    clusters = cluster_and_deduplicate(candidate_pool)

    for event in clusters:

        claims = split_into_atomic_claims(event)

        for claim in claims:
            evidence = collect_evidence(claim)
            provenance = check_source_independence(evidence)
            counter = search_counter_evidence(claim)
            claim.confidence = grade_A_B_C_D(
                evidence,
                provenance,
                counter
            )

        event.behavior = extract_observable_actions(event)
        event.costly_signals = evaluate_costly_signals(event)
        event.rhetoric_gap = compare_words_vs_actions(event)
        event.system_state = update_system_graph(event)

        event.material_change = detect_material_change(event)
        event.priority = grade_P0_P3(event)

    china_output = select_P0_P2(clusters)
    physical_ai_output = select_engineering_relevant(clusters)

    update_judgment_ledger()

    publish_daily_brief(
        china_output,
        physical_ai_output
    )
```

Global Risk：

```python
def run_global_risk_watch():

    signals = evaluate_five_core_signals()

    coupling = measure_real_cross_system_transmission(signals)

    feedback = detect_closed_feedback_loops()

    index = update_global_systemic_risk_index(
        signals,
        coupling,
        feedback
    )

    if threshold_crossed(index) or material_delta_detected():
        notify()
    else:
        stay_silent()
```

---

# 45. 当前前台模板

```markdown
# China Morning Intelligence Brief V0.3
DATE

### 今日总判断

- Judgment 1
- Judgment 2
- Judgment 3

## P1/P2｜Event

**① 发生了什么：**

**② 我们的判断：**

**③ 为什么重要：**

**④ 下一观察点：**

# Physical AI Radar｜全球物理智能前沿

### Event

**① 技术/事件：**

**② 程度：**

**③ 对项目意义：**

**④ 动作：TECH-RADAR**

**来源覆盖：**
```

---

# 46. Global Risk Alert 模板

```markdown
## Global Risk Resonance｜多风险共振升级

### ① 发生了什么

### ② 正在共振的维度

### ③ 为什么不同于普通坏新闻堆积

### ④ Global Systemic Risk Index

| Dimension | State | Trend |
|---|---|---|

### ⑤ 未来30-90天三个观察点
```

---

# 47. “不推送”也是系统输出

以下情况必须沉默：

- 只有重复新闻
- 只有外交措辞
- 只有普通公司 PR
- 只有单篇未经验证论文
- 只有战场宣传
- 只有一个风险维度波动
- 新闻数量增加但没有系统传导
- 市场没有给出真实成本信号
- 技术没有改变工程路线

这一步非常重要。

一个好的情报系统不是“尽量多提醒”。

而是：

> **只有真正值得打断用户时才打断。**

---

# 48. 核心红线

## 禁止 1

把匿名知情人士写成已确认事实。

## 禁止 2

把转载数量当独立证据数量。

## 禁止 3

用媒体声誉替代 Claim 级验证。

## 禁止 4

用官方声明直接证明战争结果。

## 禁止 5

用一次 Demo 推断产业成熟。

## 禁止 6

用新闻密度推断系统风险。

## 禁止 7

把相关性写成因果。

## 禁止 8

为了每日固定栏目凑数。

## 禁止 9

来源无法访问却假装全文核验。

## 禁止 10

重复昨天已经讲过、今天没有 Material Change 的内容。

---

# 49. 最终判断标准

每一条真正推送给用户的信息，至少应该经得起下面五个问题：

### Q1：这是真的，还是只是有人这么说？

### Q2：有真实行为吗？

### Q3：这个行为有成本吗？

### Q4：它改变了什么系统状态？

### Q5：下一步什么证据会证明我们判断对或错？

如果五个问题都答不清楚，这条信息通常还不配进入高优先级简报。

---

# 50. 一句话总架构

```text
多源发现
→ 去重
→ Claim原子化
→ 来源独立性
→ 证据分级
→ 行为/成本验证
→ 言行差与反证
→ 系统耦合
→ 事实判定
→ P0-P3 / A-D
→ Material Change
→ 推送阈值
→ 极简输出
→ 判断账本
→ 后验修正
```

最终目的不是预测世界每一步。

而是让系统在信息极度混乱的时候，仍然能回答：

> **现在真正发生了什么？**
>
> **什么还不能确认？**
>
> **哪些行为比语言更值得相信？**
>
> **哪些风险已经开始互相传导？**
>
> **什么变化值得现在打断用户？**
>
> **下一条能证伪我们的证据是什么？**

---

# Appendix A｜当前运行状态快照（2026-08-31）

| 模块 | 状态 | 运行方式 | 推送逻辑 |
|---|---|---|---|
| China Morning Intel V0.3 | ENABLED | 每日 08:00 | 固定晨报 |
| Physical AI Radar | ENABLED | 随晨报 | 只保留高工程价值 |
| Global Risk Resonance | ENABLED | 约每6小时条件检查 | 达阈值才通知 |
| China Evening Intel V0.3 | DISABLED | - | 不运行 |
| China + Physical AI P0 Hourly | DISABLED | - | 不运行 |

> 注：任务“运行”与客户端是否开启系统级推送通知属于不同层。本文描述的是情报任务本身的运行和触发逻辑。

---

# Appendix B｜推荐的长期演进方向

后续如果进一步工程化，建议把整套系统拆成以下持久化对象：

```text
Source Registry
Event Store
Claim Store
Evidence Graph
Source Reputation Ledger
Judgment Ledger
System State Graph
Risk Coupling Graph
Physical AI Tech Radar
Alert History
```

其中最重要的不是再增加更多新闻源，而是逐步形成：

> **Evidence Graph + Judgment Ledger + Risk Coupling Graph**

这样系统才会从“每次重新搜新闻”，升级为真正拥有历史判断、来源校准和系统状态记忆的 Intelligence OS。

# WI-MACRO01｜PSRRO 上游一次性中国宏观原件数值交付（限定 AMBER）

- Work unit: [#59](https://github.com/yeqilei0328-creator/personal-systemic-risk-resilience-os/issues/59)，RIOS downstream [#92](https://github.com/yeqilei0328-creator/reality-intelligence-os/issues/92)，Owner 2026-11-09 对“在获准范围内交付一项真实中国宏观指标并让 R2 实际 G1 验收”明确表示 **执行**。
- 权限解释：**AMBER exact-scope 仅限一个 PUBLIC、单次、离线验证的官方宏观数值 sidecar 与只读消费合同**；不授权新的外源采集服务、通用指标存储、计划任务、生产写入、PRIVATE 仓库改变、跨项目经济决策或独立中国经济周期结论。
- 架构路线：复用既有 PSRRO `intelligence_reviewed_export.py` 及 `EventClaimStateStore/SourceStateStore` 的 Event/Claim/Source 结构，不动旧 Schema 和 RIOS C0 原冻结。TECH_RADAR_DECISION: proposed_scope_widening; GPT control plane 对 REUSE 结果核对后，限定只新增一个可独立拒判的版本化 one-shot sidecar，而不是 DUAL new-industry framework。该 sidecar 是 PSRRO 原生主权的数据证明，不是 RIOS 第二套真相库。

## 本次验证的原始来源和语义

- 来源：国家统计局，[2026年10月中国采购经理指数运行情况](https://www.stats.gov.cn/sj/zxfbhjd/202610/t20261031_1965718.html)。研究数据：**2026-10 制造业 PMI 49.3%**，源原单位百分号 `percent`、测度 `LEVEL`、季节调整扩散指数；不是同比增长 49.3%。
- 来源权利：[国家统计局网站服务条款](https://www.stats.gov.cn/wzgl/202302/t20230217_1912857.html) 允许下载和使用已发布统计数据、要求注明来源并依法使用；**不等于许可批量爬取、批量再分发、商业产品通用接入**。本次仅单次官方公开页面读取，用于隔离研究验证。
- PSRRO 在授权 Mac 上直接获取**一次**该 NBS 网页（不是 RIOS 直采）：2026-11-09 22:21:16 北京时间的文件本地 mtime，HTTP 200，原始 HTML 422003 bytes，SHA256 `fe2dcf9b22d438483a2f3ed4c42db143f7956106ebd19c7eb0ff194bd9e886cc`。HTTP 响应、URL 及时间为本地 HTTPS 获取证据，**不是官方数字签名或第三方时间戳认证**。完整网页只保留授权 Mac 的私有临时目录，**不提交 Git**。
- 官网显示 `2026/10/31 09:30` 是**页面陈述的发布时间**；本次无法独立证明该 HTML 在历史 2026-10-31 09:30 即已经可以访问。上游 SourceObservation 的 `published_at=null`，展示 `publisher_displayed_clock=09:30` 但 `original_release_time_independently_attested=false`，真实取得仅 11月9日。任何早期回测必须严格拒判未来修订/时间推演。
- 该页当前获取时是否修订、早期版本存在与否均不证明，sidecar `vintage_status=CURRENT_RETRIEVAL_ONLY_NO_HISTORICAL_VINTAGE`，`supersedes_vintage=null`；G2 两独立统计期以及历史修订完全不随 G1 开通。

## 工程交付

- `src/psrro/intelligence_reviewed_macro.py`：离线 HTML 实际字节校验 + 既有 PSRRO reviewer packet 及其 native manifest/所有文件哈希交叉校验，确认真实官方源文本包含当前指定数值、官方页面标题和展示日期；取值严格由网页可见正文，拒绝来源错位、单量值变化、虚构精准发布时间和脏方法代码。**无任何 HTTP、索引爬虫或公共源适配器**。
- `schemas/psrro-reviewed-macro-one-shot.v0.1.schema.json`：41 字段 fail-closed 唯一产品小合同，含 `indicator_id`、国家、统计期、测度、原单位和值、原件 bytes 哈希、审核来源、method commit、R1 Native Event/Claim/Source/Assessment引用、review-manifest 摘要、发布陈述与实际获取区分、vintage 信息。
- `scripts/export_reviewed_macro_once.py`：只接受已存在审核包、其原生只读目录与本地文件，在新的隔离 `/tmp` 目录原子输出 `reviewed-macro.json`；若 PSRRO 方法仓工作树脏、现有目录/符号链接、原始来源不符、审核链不符，fail closed。
- `tests/test_intelligence_reviewed_macro.py`：合成原生 Event/Claim/Source + 合成 HTML 的正负例：数值、发布日期、页面标题、篡改的 native Claim、虚假 first-published clock、伪造官方地址、错误权限、非临时目录、symlink、重复输出和稳定哈希。合成测试不能替代 PSRRO 一次性真实来源验证。
- 该 sidecar 不能自动成为正式 RIOS C0 事件，也不自动输出国家统计局来源许可证；后续只通过新的受限 **R1 versioned read-only projection** 交给 R2 一次验收，R2 严禁自行访问 NBS。

## 最小拒判范围和门禁

- 只是 **G1 一项原件当前版本在检索时已被审阅的实证**；不代表 R1 已建立持续宏观生产流、RIOS Portfolio R1 #85/#86 已正式退出、已拥有 G2 两期历史 revision 或 G3 中国经济周期预测。
- 所有产物在本地临时目录保存，Git 只保留公共方法、合成测试和非敏感 source/reviewer digest；不向 PSRRO PRIVATE 写入任何事实、改 method-pin 或创建通知。
- 先以精确 PSRRO CI/method HEAD 合并，**再**从合并后的 clean method main 运行真正的 one-shot 原件/原生审核 sidecar；以该 method commit 作为下游严格 pin。RIOS 不得相信未合并开发树引用的 producer_commit。
- `SOURCE=PSRRO_PUBLIC_ONLY`，`RIOS_NBS_DIRECT_FETCH=0`，`PUBLIC_RAW_HTML_IN_GIT=0`，`PSRRO_PRIVATE_WRITE=0`，`SCHEDULER_CREATED=0`，`FORECAST_CREATED=0`。

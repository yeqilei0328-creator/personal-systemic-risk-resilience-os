# WI-MACRO02｜9–10月 PMI 双公报 G2/G3 联合只读试验（2026-11-09）

## Owner 指令与权威边界

Owner 明确要求“G2G3一起验证”。本轮仅完成 **R1/PSRRO 本地两份真实 PUBLIC 官方公报只读审阅+离线版本化联合证据**、由 RIOS 分别判定 G2 和 G3。继承 C0 联邦：原始来源与事实只由 PSRRO 拥有，RIOS 消费已校验的 R1 工件，不直接拉取国家统计局或建新的事实数据库。实施技术雷达：`TECH_RADAR_DECISION / REUSE existing reviewed Event/Claim/Source stores + smallest one-off PSRRO cross-edition sidecar`。不增加 provider、定时抓取、历史回填、通用 schema、PRIVATE 或生产写入，用户没有授权预测或实际经营动作。

原 PSRRO G1 PMI 工作 [#59](https://github.com/yeqilei0328-creator/personal-systemic-risk-resilience-os/issues/59) 已闭环，不修改旧 `psrro-reviewed-macro-one-shot.v0.1` 或其 method pin。新工作是**有限跨期与跨发布文本核验**，不让宏观样本“假装长期完整”。

## 两份原件

| 统计期 | PSRRO 原始第一方 HTTPS | 官方原文指标（LEVEL, percent） | 本轮 R1 获取限制 |
|---|---|---|---|
| 2026-09 | [国家统计局9月PMI公报](https://www.stats.gov.cn/zwfwck/sjfb/202609/t20260930_1965449.html) | 制造业 PMI **50.1**，新订单 **50.5**，生产 **51.7** | 本轮 Nov9 一次 HTTP 200，186255 bytes，SHA256 `047cf98e1029862267438906eafa9d6f4aa7a0653d2c5857b1d37b7707df813e`；PSRRO reviewed原生 Sept Event/Claim/Source manifest SHA256 `726d62c286dc671a03014a73960a47a74466e2885566ffa7fac26edd1f158d2f` |
| 2026-10 | [国家统计局10月PMI公报](https://www.stats.gov.cn/sj/zxfbhjd/202610/t20261031_1965718.html) | 制造业 PMI **49.3**，新订单 **49.4**，生产 **49.8**；大型企业 PMI **50.2**（反例） | 复用 G1 Nov9 先前下载原件，422003 bytes，SHA256 `fe2dcf9b22d438483a2f3ed4c42db143f7956106ebd19c7eb0ff194bd9e886cc`；原有 Event/Claim/Source manifest SHA256 `83b2731d946988537fe9ef967b9f2865f091776089d7cdcc6008e5323acc767a`，G1 记录 SHA256 `ee02eda8871e55bd28704e5c55abfaad60176a3a30f87000ab79781b1e22ac49` |

PSRRO 真实收到9月 URL的 **一次 HTTP 200**，页面时间展示 2026-09-30 09:30；10月页面展示 2026-10-31 09:30，但**均没有独立历史首次上网时间或原版文件的可信归档证明**，两份原始 HTML 都是2026-11-09目前内容的检索版本。原始文件只保存在隔离 `/private/tmp/psrro-macro-g2g3-joint-20261109` / G1已有临时路径，不能放入 Git，也不获得无限网站抓取许可。

## 上游真实方法与验证范围

- `src/psrro/intelligence_reviewed_pmi_joint.py` + `scripts/export_reviewed_pmi_joint_once.py` + 新的 `schemas/psrro-reviewed-pmi-cross-edition.v0.1.schema.json`；只从 **两个已经存在的官方 HTML 本地文件、两份 PSRRO approved reviewed event packet、它们原生 store 与 manifest、已通过 G1 的10月记录** 生成一个受控当前检索版观察快照。**内部无 HTTP**。
- 官方 9月与10月各自原文的数值必须直接与文件字节相符；同一指标的日期单位 LEVEL 不误当同比；10月公报表格重列9月 PMI 50.1、新订单50.5、生产51.7 与 9月公报目前显示一致。
- 这一点只能证明**本次检索得到的两份网页目前互相一致**；“不存在版本修订”“9月30日时就已获得上述原版字节”都没有证据，`historical_revision_lineage=NOT_ATTESTED`、`historical_original_release_bytes_at_publication_time_attested=false`。
- 强制指向 PSRRO既有 R1真实 Event/Claim/Source 的 manifest HASH、publisher/source URL、独立来源组；10月必须与 G1 one-shot 记录及原网页再次校验。任何 URL伪造、文件变更、数值变动、Claim和manifest不一致、发布时刻冒充、输出目录覆盖 => fail closed。
- 输出同时包含扩散指数跨期变化（PMI **-0.8个百分点**，新订单 **-1.1**、生产 **-1.9**）、大型企业10月 PMI **50.2** 的反证。9月和10月同属 NBS 官方来源，不可据“两个不同月份”宣称两家独立机构的因果佐证。

## 预期联合门禁与停止点

- **G2-A 两个实际统计期 & 官方跨公报核对**：可单独验收 PASS，但都只是在 Nov9 R1 检索时的实际网页内容；不是实时源 API、没有单独日期级首次发布归档证明。
- **G2-B 同统计期真实更正/修订原件和历史 as-of**：目前无已确认原始版本与修订版本数值变动。两份“数值一致”不能按“修订链已通过”计分；要求明确 `BLOCKED_NO_ATTESTED_HISTORICAL_REVISION_LINEAGE`，不能把 R1-02 FAO 另一个系列的历史研究挪来替中国 PMI 放行。
- **G3-A 制造业调查景气定向变化卡**：只允许叙述9→10月 PMI、新订单、生产指数由50以上变为50以下以及“**大企业PMI仍高于50**”这一真实反例。两项 R2 核心候选 `cn.pmi.manufacturing` / `cn.pmi.new_orders` 指标形成有限观察，但产出指数本轮不计入 R2 已设的 12项覆盖计数。
- **G3-B 中国整体周期阶段、因果 H 条件**：仍缺 CPI/PPI/工业/消费/投资/房地产/融资的原生 R1 证据、连续统计期、领先滞后、独立来源及反证，必须保持 `UNKNOWN` 与 `BLOCKED_INSUFFICIENT_MULTIDOMAIN_CAUSAL_EVIDENCE`；**不得**生成“中国经济进入衰退”“政策应对必然”或具体商业预测/动作。

所有新增 PSRRO 代码属于单次研究方法/副证据，不改变既有冻结合同。后续 RIOS 只读，CI、准确提交 SHA、合并后复跑、独立门禁回执均需完成，整体 RIOS #92 仍 OPEN、R1 #85/#86 未结项。

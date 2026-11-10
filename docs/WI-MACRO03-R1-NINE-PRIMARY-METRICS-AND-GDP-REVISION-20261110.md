# WI-MACRO03｜R1 真实来源与历史修订补证：9项宏观 + 2024年度GDP（2026-11-10）

**Owner 直接指令：** “由 R1 补齐真实历史修订证据和缺失的宏观领域数据，另外检查今天的运行状态，我看到早上给我推送了。”本工作只改变 PSRRO PUBLIC 一次性来源证明方法和研究证据。RIOS R2 不访问 NBS/MOF/PBOC，PSRRO PRIVATE/生产系统无任何写入。既有 PMI G1、G2/G3 一次性侧证据方法及 C0 原生出口继续沿用。

**授权与路由：** `AUTHORITY_ROUTER=GREEN_READONLY_ONE_SHOT_R1_PUBLIC_OFFICIAL_REVIEW`；任何新的常驻宏观供应商、自动抓取、源类扩张、跨仓泛化 schema、正式周期模型放行均另需明确 AMBER；`EXECUTION_ROUTER=GPT_DESKTOP`；`TECH_RADAR_DECISION=REUSE_PSRRO_REVIEWED_NATIVE_AND_SOURCE_BYTES`（指 reuse 既有 PSRRO 本地公开审核 exporter，不增加新服务）；`FALLBACK_ROUTER=FAIL_CLOSED_IF_PUBLISHER_OR_VINTAGE_NOT_ATTESTED`。Owner 此次明确推进 R1 上游，但没有授权 PRIVATE/生产更改、常驻采集、自动商务/设备执行。

## 1. 实际数据取得、来源归属与验收真实性

2026-11-10 授权 Mac 的 R1 工作区 `/private/tmp/psrro-r1-macro-gap-20261110/` 已使用 **恰好 10 个显式公开官方网页 URL、每个只请求一次**，均为 HTTPS HTTP 200 且最终 URL 与计划一致。原始 HTML 已保存于该目录，均有 SHA256、字节数、实测检索时间和请求收据，**不会提交仓库**。国家统计局 9月/10月 PMI 的此前来源审核维持原 G1/G2/G3 已验记录，不重复获取。新来源为：

| PUBLIC 原始公告 | 统计窗口 | 当前页面原文核对的核心指标 |
| --- | --- | --- |
| [NBS CPI](https://www.stats.gov.cn/zwfwck/sjfb/202611/t20261109_1965795.html) | 2026-10 MONTH | `cn.cpi.yoy=0.7%` |
| [NBS PPI](https://www.stats.gov.cn/zwfwck/sjfb/202611/t20261109_1965794.html) | 2026-10 MONTH | `cn.ppi.yoy=5.7%` |
| [NBS工业增加值](https://www.stats.gov.cn/zwfwck/sjfb/202610/t20261019_1965617.html) | 2026-09 MONTH | `cn.industrial.va.yoy=5.5%` |
| [NBS社会消费品零售](https://www.stats.gov.cn/sj/zxfb/202610/t20261019_1965614.html) | 2026-09 MONTH | `cn.retail.sales.yoy=1.1%`（与1–9月值恰同，不得倒用累计数） |
| [NBS固定资产投资](https://www.stats.gov.cn/sj/zxfb/202610/t20261019_1965616.html) | 2026-01..09 YTD | `cn.fai.ytd.yoy=-7.2%` |
| [NBS房地产市场](https://www.stats.gov.cn/sj/zxfbhjd/202610/t20261019_1965615.html) | 2026-01..09 YTD | `cn.realestate.investment.ytd.yoy=-20.6%`；`cn.realestate.sales_area.ytd.yoy=-13.2%`（同一官方来源，不算独立确认两次） |
| [NBS规模以上工业利润](https://www.stats.gov.cn/zwfwck/sjfb/202610/t20261027_1965697.html) | 2026-01..09 YTD | `cn.industrial.profit.ytd.yoy=15.5%` |
| [MOF前三季度财政收支](https://gks.mof.gov.cn/tongjishuju/202610/t20261023_4003380.htm) | 2026-01..09 YTD | `cn.fiscal.land_use_revenue.ytd.yoy=-27.9%`（财政部原件） |

注意：YOY 是同比变化百分数，不是价格/产量指数 LEVEL；YTD 为年初累计同比，绝不能拿作9月单月同比。CPI/PPI 是10月份，其他多数是9月份或1–9月，不能用“同月同步因果”冒充经济周期推断。面向 R2 的固定候选12项中，本轮新增9项已获 R1 原文+native双证，**另有两项此前的 PMI/新订单**；**人民银行社融存量同比**必须保持未验收。

### PBOC 不偷换来源

前期 `cn.credit.afre_stock.yoy` 候选静态链接实际是 **2025 年的人民银行 PDF**，不能作为2026年10月或9月的一手版本。2026年9月社融存量同比+7.1%有新华社/地方政府公开引用，但本轮没有找到并成功读取经过准入的 **适用统计期人民银行原始正式文件**。此项保持 `R1_PRIMARY_ORIGINAL_MISSING`，不用新华社转载替代第一手原文，也不将无数字源写入正式宏观覆盖率。

### 原生工程真相

原始审阅工件本地冻结在 `reviewed-native/{source_id}/reviewed-packet.json` 和 `reviewed-native/{source_id}/native/`。每个 source 使用既有 PSRRO PUBLIC `intelligence_reviewed_export.export_reviewed_packet` 的 Event/Claim/SourceObservation/MaterialChange；审核人声明 `ai_assistant`，每条 native 的源 URL、原始二进制 SHA256、SourceObservation `retrieved_at`、`reviewed_at`、完整 native artifact manifest SHA256 交叉绑定。申明“reviewer-attributed”不代表官网数字签名、可信第三方时间戳或历史首发版次保全。10份原件、10份 native 记录真实本地源 ledger SHA256 `b080cbb67ccf2866a7eb8e8b690a4988d4ae74192366668c7b896862cca11792`，只在私有临时工作目录保存，不上传用户个人、业务和外部敏感内容。

## 2. 真正同统计期、不同官方版本的修订

- **2024年中国全年 GDP 初步核算**：[NBS 原文](https://www.stats.gov.cn/xxgk/sjfb/zxfb2020/202501/t20250118_1958363.html)，现价年度绝对额 `1,349,084亿元`，官方信息公开页面成文日期 2025-01-18。原始 HTML SHA256 `3313c8e100e9b7cc7ae9bea838e2148b6bdd13b8317f9e14ad01340d8b1e95dc`。
- **同一2024年GDP最终核实**：[NBS 2025-12-26 原始公告](https://www.stats.gov.cn/xxgk/sjfb/zxfb2020/202512/t20251226_1962144.html)，现价年度 GDP `1,348,066亿元`，官方公告明确“比初步核算数减少1018亿元”；原始 HTML SHA256 `b6b6b5c74b9e044818a92eb3eec356fbcd9215c9649f760db9b91eb2a282233e`。
- 同一 `indicator_id=cn.gdp.annual.nominal`、`period=2024-01-01..2024-12-31`、`NOMINAL_LEVEL / 亿元`，**真实源官方数值修订 = −1,018亿元**，不是同比增速变动。官方实际 GDP 不变价增长5.0%，仍持平。
- **限制非常重要：** 2026-11-10 才取得两份当前页面的HTML。可凭官方最终公告和两个官方现有公开发布证实同年同量口径确实存在“初步→最终”修订，但不能凭今日文件声称 2025-01-18 的原始网页字节已在那个历史时刻被存档，亦不能宣称准确首次发布的绝对时刻/无前修订。故 `official_revision_supported=true`、`historical_first_available_timestamp_attested=false`、`historical_asof_backtest_authorized=false`，不把年度 GDP 修订冒认为 PMI 的原本 G2 同序列修订通过。

## 3. 版本化交付与拒判

- `config/r1-macro03-official-source-proof.v0.1.json` 是**仅本轮10个明确源**的数值与上下文锚定规则，含来源 URL/原始字节 SHA、统计期间、官方源原单位、预期 9 个核心数值、GDP初版与最终版数字。它不是循环采集队列，不包含任何代码执行或连接凭据。
- `src/psrro/intelligence_reviewed_macro_gap.py` 只读取上述本地 raw HTML、审核 native、运营员本地一次性 HTTP 收据，逐条校验原始文本的限定上下文正则、单位/方向/YTD/YOY、native Claim 和原始源/manifest、真实来源 SHA/取回日期。上游 R1 自己生产一份**只读研究投影**，不在 RIOS 再建 Event/Claim 事实库。
- `schemas/psrro-r1-macro03-source-provenance.v0.1.schema.json`、`scripts/export_r1_macro_gap_once.py`：schema 验证、干净 PSRRO method commit pin、原子输出仅一个新的 `/tmp` 目录；任何未审批 URL、未完成源、时间/哈希/口径不符、旧目录覆盖或方法脏仓皆拒绝。
- `tests/test_intelligence_reviewed_macro_gap.py`：合成原文断言和拒判（数值、方向、GDP 修订、YOY/YTD、来源/HTTP、统计期、缺失或重复指标、非法输出目录、时区），全库与 CI。
- 后续 RIOS 可据已合并的此确切源 sidecar 和既有两项 PMI，只读验证 **11/12** 原件核验，不得把 `R1_REVIEWED_PUBLIC_CURRENT_COPY` 解释成 R2所有历史修订、实时自动数据中台或 G3因果链通过。两条数据主线分开：**来源/数值覆盖** 与 **历史版本/时滞/独立反证可靠性**。

## 4. 今天 V0.4 和 R1-06 是另一条验收链

2026-11-10 08:00 V0.4 唯一晨报原生 `run=b0c1abdf-3494-8325-b5d0-c524c706ed18`：实际 07:59:31 启动、08:00:38 完成、内容未截断、GitHub Issue #66 [评论 #6754813807](https://github.com/yeqilei0328-creator/reality-intelligence-os/issues/66#issuecomment-6754813807) 7候选实写；原生通知实际送达字段 `delivery_status=unknown`。RIOS [R1-06 #86](https://github.com/yeqilei0328-creator/reality-intelligence-os/issues/86) 于08:39独立核验两真实自然日运行及 GitHub 候选接收身份 PASS，但这不审核 7 条外部原始新闻真实性，也不表示全 R1 出口正式放行。没有修改 V0.4 任务或创建第二份通知。

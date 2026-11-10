# WI-MACRO04｜人民银行社融存量同比第一方原件，一次性真实审阅（2026-11-10）

## 用户指令与来源主权

Owner 要求“把 R1 最后一项人民银行原件 #65 处理掉”。源所有权仍在 **PSRRO PUBLIC R1**，**RIOS R2 仅消费**审核后的版本化证据。遵守原 #65 的 one-shot 公共官方原件权限，没有取得对人民银行持续抓取、自动调度、个人身份凭证、PRIVATE/生产写入、周期预测或经营决策的授权。

此次摆脱过去错误的 `2025/11/*.pdf` 研究候选链接：已从[人民银行主站](https://www.pbc.gov.cn/) → [调查统计司2026年统计数据](https://www.pbc.gov.cn/diaochatongjisi/116219/116319/2026ntjsj/index.html) → [社会融资规模（存量统计表 HTM）](https://www.pbc.gov.cn/diaochatongjisi/116219/116319/2026ntjsj/shrzgm/index.html)，发现直接官方原始 HTML：
[2026 年社会融资规模存量统计表](https://www.pbc.gov.cn/diaochatongjisi/attachDir/2026/10/2026101417444554195.htm)。

## 真正的原始文件与统计语义

- R1 在授权 Mac **一次**公开 HTTPS GET，HTTP **200**，最终 URL 与上方人民银行官网 HTM 链接一致，text/html，57,401 bytes，SHA256 **`8649f9da169e8c89985781bfb26f222f277adc59685315836c0c133dc0056794`**，采用 GB2312/GB18030 编码、Excel HTML 结构。
- 存于隔离 `/private/tmp/psrro-r1-pboc-afre-20261110/pboc-2026-afre-stock.html`；raw 原件、source receipt、reviewer packet、native artifacts 不进 Git。
- 唯一正式指标 `cn.credit.afre_stock.yoy`：CN，全国；统计期 2026-09-01..2026-09-30，9月末 `period_mode=STOCK`、`measure=YOY`、`unit=percent`、**同比增速7.1%**。同一9月末绝对存量为 **468.17万亿元**，为交叉验证辅助字段，不是同比增速本身。
- 原网页表格列顺序是2026.1至2026.12，每月“存量/增速%”两列。以**8月**464.80万亿元/7.2%为前置对照，**9月**468.17万亿元/7.1%为目标，**10月以后列尚空**。强制完整年列标题、原生存量行、月份双列和辅助数据一致，拒绝流量/增量误读、月份错位、2025旧PDF替代。
- PBC链接文件名含 **20261014**（只能说明原始文件名中的日期提示）；R1真正下载发生在**2026-11-10**。本次没有证据证明2026-10-14当天此准确字节版本就已上网，也没有独立网站首次发布时间/全部修订归档。官方现存原表可证明当前公开原始数据，不能直接补 G2 历史首次可用性门禁。
- 本源和之前PSRRO审查的NBS PMI或财政部原文属于三个不同官方发布者，但不能仅据此认定跨领域因果关系。

## 真实 PSRRO R1 工程路径

- 本地 operator 辅助审阅脚本，仅将获得的原始人民银行网页转换为一组**现有** `psrro-reviewed-public-event.v0.1` packet。通过已有 `export_reviewed_packet` 生成 Event/Claim/SourceObservation/MaterialChange（PUBLIC reviewer-attributed、一条Claim、一个原始Source），manifest SHA256 **`9a981acedbb92be8d7af2a23d5d10db507f3fe309cd2389555487918492a6bf6`**。审核人声明 `ai_assistant`，并非中国人民银行数字签名。
- 新最小 R1方法 `src/psrro/intelligence_reviewed_pboc_afre.py`，仅验证已冻结原始字节 SHA、官方月度存量双列、源URL、时刻、native事件四原件及manifest、reviewer/Claim真实性和统计口径；无HTTP代码。对应 `scripts/export_reviewed_pboc_afre_once.py`、`schemas/psrro-reviewed-pboc-afre-one-shot.v0.1.schema.json`；仅允许在新 `/tmp` 路径输出一次性定版 sidecar，旧输出不覆盖、无通知及私有写入。
- `tests/test_intelligence_reviewed_pboc_afre.py` 12个合成 positive/negative checks：错误年份/月份、存量错列、同比误读、8月错列、未来10月数据伪造、原始文件篡改、错误输出路径。不是“访问任何统计页的通用爬虫”。
- 本次 `TECH_RADAR_DECISION=REUSE_EXISTING_PSRRO_REVIEWED_NATIVE`；`AUTHORITY_ROUTER=GREEN_READ_ONLY_AND_ONE_SHOT_PUBLIC_SOURCE_REVIEW`；`EXECUTION_ROUTER=GPT_DESKTOP`；`FALLBACK_ROUTER=FAIL_CLOSED`。新增字段仅属研究侧有限 sidecar，不改变旧 PMI/GDP/source method pins。

## R2 待独立接受的严格门禁

确认 R1 formal method 已按 exact-head PR/CI/merged main 生成正式 one-shot R1工件后，由 **RIOS C0 shadow** 实际读取人民银行原生 Event/Claim/Source，再配合前一轮 `11/12` 已验 R1证据，检查发布者是PBOC、2026-09，STOCK/YOY/percent 7.1，不是2025旧PDF。通过时才给 `12/12_CURRENT_PRIMARY_SOURCE_REVIEWED`。

**禁止放行的事项不改变**：G2历史原始首次发布/修订版次以及历史 as-of 回测无完整证明，G3整体中国经济周期阶段、跨期时滞/因果H仍BLOCKED，RIOS #52预测融合集成 PRE-GATE、PSRRO PRIVATE/生产变更0，V0.4日更唯一任务不修改。

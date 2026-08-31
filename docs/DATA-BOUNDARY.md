# Public / Private Data Boundary

## Decision

本仓库为公开工程仓库。`main` 是以下内容的工程事实源：

- 系统使命与架构；
- 风险模型；
- 数据 schema；
- 评分和审计规则；
- 情报处理逻辑；
- Preparedness 方法；
- Playbook 模板；
- 公开、可复核、可脱敏的示例数据。

## Never commit to public main

- 精确家庭/个人住址或基地位置；
- 真实资产数量、余额、现金流、负债和账户信息；
- 可识别的房产、厂房、土地清单；
- 水、电、储能、食品、燃料等真实库存与容量；
- 安防盲区、摄像头/无人机部署、通信拓扑、密钥、凭据；
- 人员名单、联系电话、家庭关系、行程与撤离路线；
- 任何会降低现实安全边界的数据。

## Operational data

真实个人暴露、资产状态和基地能力应存放在独立私有数据层。公开仓库中的代码与 schema 可以读取该数据层，但公开仓库本身不得成为敏感 operational data 的存储位置。

## Principle

Open methodology, private exposure.

公开方法，私有暴露。

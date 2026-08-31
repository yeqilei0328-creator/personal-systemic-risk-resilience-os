# Private Operational State Integration

## Architecture

Public Method Repository
→ schemas / algorithms / audit rules / synthetic examples

Private State Layer
→ real exposures / capabilities / finance / site / communications / food / people

两者必须分开。

## Recommended private layout

```text
state/
  capabilities/
  exposures/
  finance/
  assets/
  sites/
  communications/
  food/
  medical/
  people/
  scenarios-private/
```

公开仓库中的 schema 可以用于验证 private state，但 private values 不反向提交到 public main。

## Pinning

私有 state 层每次运行应记录：

- public schema version
- public main commit/tag
- assessment timestamp

避免“模型已经升级，但私有数据还按旧 schema 解释”的漂移。

## Local integration

建议通过环境变量或本地配置指向私有 state 目录，例如：

`PSRRO_STATE_DIR=/secure/path/to/state`

该路径必须在 public repository 的 git ignore 边界之外，或明确处于已忽略目录。

## Never mirror publicly

不要把以下内容复制到公开 Issue、PR、examples 或日志：

- 真实财务余额/现金流/负债
- 可定位的房产、厂房、土地
- 水、电、食品、燃料真实容量
- 安防盲区、通信拓扑、密钥、凭据
- 人员、电话、行程、撤离路线

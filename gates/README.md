# 工程门禁体系

门禁不是建议清单，而是阶段完成条件。每个门禁必须记录：

- 检查对象
- 执行命令或观察方法
- 结果
- 证据位置
- 未通过项
- 风险接受人
- 重新检查日期

项目已有 CI、代码评审和发布门禁优先；本目录提供通用结构，不强制某种工具。

## 门禁顺序

1. [01-intake-gate.md](01-intake-gate.md)：需求和现状调查
2. [02-architecture-gate.md](02-architecture-gate.md)：架构和技术选型
3. [03-implementation-gate.md](03-implementation-gate.md)：实现和功能闭环
4. [04-security-gate.md](04-security-gate.md)：安全、隐私和依赖
5. [05-performance-gate.md](05-performance-gate.md)：性能、容量和稳定性
6. [06-release-gate.md](06-release-gate.md)：发布、迁移和回滚
7. [07-large-engine-gate.md](07-large-engine-gate.md)：大型引擎和实时系统
8. [08-engineering-standards-gate.md](08-engineering-standards-gate.md)：日常工程规范

## 结果等级

- **PASS**：证据完整，允许进入下一阶段。
- **PASS WITH RISK**：有已批准风险和明确补救期限。
- **BLOCKED**：缺少关键证据、存在高风险缺陷或无法安全继续。
- **NOT APPLICABLE**：写出不适用原因，不能只留空。

# 自动化工程门禁和检查脚本

Markdown 规范负责解释原则，机器可读规则负责稳定执行。自动检查不能替代
人工设计评审，但必须阻止明显的结构、证据、秘密和引用错误。

## 1. 目录

```text
automation/
  engineering-gate-rules.json
  evidence-schema.json
  evidence-example.json
  project-profile-schema.json
  project-profile-example.json
  detect_project_profile.py
  run_project_gates.py
  quality-rubric.json
  quality-assessment-example.json
  score_quality.py
  run_engineering_gate.py
```

脚本是 Skill 的辅助工具，不是目标产品的技术栈要求。目标项目可以把同样的
规则迁移到 PowerShell、Bash、Node、Go 或 CI 平台。

## 2. 规则级别

- `blocker`：发现即失败，除非明确传入项目批准的豁免。
- `error`：默认失败，可由项目规则明确降级。
- `warning`：输出风险，不能伪装成通过。
- `info`：提供审计信息。

规则定义至少包含 `id`、`severity`、`scope`、`description` 和 `check`。
规则文件只描述通用安全检查；语言、格式化器、构建器和测试命令从项目
配置传入，不能假定所有项目都使用同一工具。

## 3. 默认检查

脚本默认检查：

1. Skill 主文件存在且 frontmatter 完整。
2. Markdown 相对引用指向存在文件。
3. 新增文件没有明显私钥、token、云凭据和连接字符串。
4. 交付证据中的 `NOT_RUN` 不被写成 `PASS`。
5. 机器规则 JSON 可解析且规则字段完整。
6. 工作区路径在指定根目录内。
7. 如果传入 `--evidence`，阶段证据符合 schema，且 PASS 阶段内部没有未执行
   或失败检查。
8. 项目 profile、门禁命令和质量评估可以被独立验证。

脚本不尝试判断业务是否正确，也不通过正则证明没有安全问题。安全扫描
结果只能作为第一层门禁，仍需项目自己的 SAST、依赖扫描和人工评审。

## 4. 使用方式

```text
python automation/run_engineering_gate.py --root .
python automation/run_engineering_gate.py --root . --changed path/to/file
python automation/run_engineering_gate.py --root . --format json
python automation/run_engineering_gate.py --root . --evidence path/to/evidence.json
python automation/run_engineering_gate.py --root . --allow-warning
```

退出码：

```text
0 = 没有 blocker/error
1 = 存在 blocker/error
2 = 参数或规则文件错误
```

阶段证据格式见 `automation/evidence-schema.json`，示例见
`automation/evidence-example.json`。`PASS` 只能表示当前证据完整且所有
检查通过；`NOT_RUN`、`BLOCKED`、`UNKNOWN` 和 `WAIVED` 必须保留真实原因。

项目画像使用 `project-profile-schema.json`；工具链执行器读取画像中的参数
数组，默认只计划不执行，显式传入 `--execute` 才运行。质量评分使用
`quality-rubric.json`，评分不能覆盖阻塞项。

## 5. 项目接入要求

接入项目时应增加项目专属规则：

- 语言和格式化检查。
- 编译/类型检查。
- 测试和覆盖率阈值。
- i18n key 对齐。
- schema/vector 校验。
- 依赖、许可证和秘密扫描。
- 构建目标和产物白名单。
- UI/API/CLI 真实验收。

所有检查必须报告命令、目标、配置、退出码、时间和产物路径。无法执行的检查
标记 `NOT_RUN` 或 `BLOCKED`，不能自动降级为通过。

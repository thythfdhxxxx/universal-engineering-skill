# 项目适配器和项目画像

通用 Skill 不应把所有项目当成同一种工程。项目适配器负责读取目标项目的
语言、框架、构建、测试、规则、目录和发布方式，并生成项目专属 profile。

## 1. 适配器优先级

按以下顺序确定项目事实：

1. 用户本次明确要求。
2. 项目根规则和子目录规则。
3. 构建清单、锁文件、schema、CI 配置和实际入口。
4. 真实命令探测结果。
5. 文件名和目录名推断。
6. 通用默认值。

低优先级信息不能覆盖高优先级信息。冲突必须进入 profile 的
`conflicts`，不能静默选择。

## 2. 自动探测范围

至少检查：

| 事实 | 典型来源 |
| --- | --- |
| 语言 | `CMakeLists.txt`、`Cargo.toml`、`go.mod`、`package.json`、`pyproject.toml`、`build.gradle` |
| 框架 | 依赖清单、源码入口、插件配置、构建 target |
| 构建 | presets、Makefile、npm scripts、Gradle tasks、UBT 配置 |
| 测试 | CTest、cargo test、go test、pytest、Vitest、Jest、Gradle test |
| 规则 | AGENTS、CLAUDE、CONTRIBUTING、目录内规则 |
| 包管理 | lockfile、vcpkg、Conan、Cargo、npm、Maven、Gradle、pip |
| 平台 | CI 矩阵、构建脚本、平台目录、目标 SDK |
| 发布 | Dockerfile、installer、package、signing、release workflow |

探测是线索，不是授权。构建文件中没有命令不能推断命令一定可运行。

## 3. 项目 profile 必须包含

```text
项目身份：
根目录：
语言和版本：
框架和版本：
目标平台：
模块和目录所有权：
规则文件：
构建命令：
测试命令：
格式/静态检查：
依赖/许可证检查：
安全检查：
性能检查：
发布命令：
环境变量：
秘密来源：
禁止触碰路径：
生成物路径：
风险和冲突：
人工确认项：
探测时间和证据：
```

## 4. 规则合并

项目专属 profile 分为：

- `detected`：工具探测得到，不能直接覆盖项目规则。
- `declared`：项目维护者确认的事实。
- `inherited`：通用 Skill 的默认规则。
- `overrides`：有负责人、原因和期限的例外。

最终规则使用：

```text
project rules > declared profile > detected profile > universal defaults
```

`overrides` 不能降低安全、数据完整性和用户工作区保护要求，除非有明确的
安全批准和替代控制。

## 5. 适配器输出

适配器应生成：

1. `project-profile.json`：事实和证据。
2. `project-gates.json`：本项目要运行的门禁。
3. `project-assumptions.md`：未确认事实、冲突和人工确认项。
4. `project-commands.md`：可复现命令和工作目录。

生成过程默认只写到指定输出目录，不修改业务源码、不安装依赖、不执行发布。

## 6. 适配失败

以下情况标记 `UNKNOWN` 或 `BLOCKED`：

- 同时存在多个冲突构建系统。
- 只发现生成物，没有源构建入口。
- 测试命令需要未提供的秘密、服务或许可证。
- 规则文件互相冲突。
- 项目根目录无法确定。
- 检测到可能是参考软件、缓存或第三方目录而不是目标项目。

不能因为探测失败就回退到“默认使用熟悉技术栈”。

## 7. 维护

项目 profile 应随项目版本更新。语言、框架、构建、测试、发布或目录发生
变化时重新生成并评审。profile 中的每条命令都要能追溯到文件、负责人和
最后验证时间。

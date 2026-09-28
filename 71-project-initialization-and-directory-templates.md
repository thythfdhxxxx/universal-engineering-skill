# 项目初始化和目录模板

目录不是装饰，而是所有权、依赖方向、构建、测试和交付边界的可视化表达。
使用模板前先服从目标项目已有结构。

## 1. 初始化顺序

1. 写产品边界、支持平台、许可证和非目标。
2. 选语言、构建系统、包管理、测试和格式化工具。
3. 建立模块所有权和依赖方向。
4. 建立配置、日志、错误、i18n、协议和版本策略。
5. 建立 CI、门禁、秘密管理和发布渠道。
6. 创建最小可运行入口和最小测试。
7. 再加入业务模块，不先复制一个空壳大目录。

## 1.1 文件树和文件归属必须自动形成

AI 在创建或修改软件文件前，必须先形成文件树和文件归属清单。默认产物为
`docs/architecture/file-tree.md`；项目已有架构文档位置时使用项目既有位置，
不能重复创建第二份权威清单。

文件树产物至少包含：

```text
# 项目文件树

项目类型：
仓库根目录：
现有规则和构建入口：
目录所有权和依赖方向：

## 当前树
<只记录与项目相关的源码、测试、配置、文档、脚本和资源目录>

## 目标树
<本次任务涉及的新增或调整目录>

## 文件归属清单
| 路径或模式 | 类别 | 所属模块 | 职责 | 允许依赖 | 生成方式 | 对应测试 |
| --- | --- | --- | --- | --- | --- | --- |
```

每个计划文件只能有一个 owning module。`类别`至少从 `source`、`test`、
`config`、`schema`、`resource`、`documentation`、`tool`、`script`、
`generated`、`secret-excluded` 中选择。实现期间新增、移动或删除文件时，必须
在同一变更中更新清单；清单与实际文件树不一致时不能报告完成。

文件放置决策按以下顺序执行：

1. 用户要求和项目已有规则。
2. 现有模块的所有权、依赖方向和构建注册方式。
3. 本文件的项目类型模板。
4. 通用目录模板。

如果已有目录可以承载职责，不得为了整齐新建同义目录。新目录必须记录 owner、
允许依赖、构建/测试注册位置和创建理由。

## 1.2 文件树生成流程

文件树不是只列目录名的展示图，而是实现计划和模块边界的机器可核对记录。AI
必须按以下顺序形成它：

1. 确定仓库根目录，排除 `.git`、依赖缓存、构建输出、临时目录和第三方源码。
2. 读取根规则、子目录规则、README、许可证、构建清单、包清单、CI 和测试注册。
3. 生成当前树，只列真实存在且属于项目的目录和关键文件；不要把缓存或扫描结果当源码。
4. 识别可执行入口、模块 owner、公共接口、数据/协议真源、测试入口和生成物路径。
5. 根据本次需求生成目标树和文件清单，标明新增、修改、移动、删除和不变文件。
6. 检查每个目标文件是否已有归属、依赖方向、构建注册和测试位置；缺一项就先补设计。
7. 只创建最小必要目录。空目录、重复的 `common`/`utils`/`misc` 目录和没有 owner
   的临时目录不能作为实现结果。

对于已有大型项目，`当前树`可以使用模块摘要和受影响子树，不要求把第三方依赖或
   全部生成文件展开；但每个本次修改路径必须精确列出。对于新项目，目标树必须在
   第一个业务文件创建前确定，并包含最小入口、最小测试、构建文件和 README。

## 1.3 文件类别判定

路径不能只按扩展名决定归属，要同时看创建者、消费者、生命周期和是否进入发布包：

| 类别 | 判定标准 | 默认放置 | 提交规则 |
| --- | --- | --- | --- |
| `source` | 手写、参与产品运行时 | `src/`、`apps/`、`packages/`、`services/` | 必须有 owner、构建入口和测试 |
| `public-interface` | 被其他模块/服务/插件依赖的 API、头文件、客户端 | 模块 `include/`、`contracts/`、`api/` | 记录兼容和版本策略 |
| `test` | 只在验证中执行 | `tests/` 或模块旁的测试目录 | 不得被生产代码依赖 |
| `schema` | 协议、配置、数据库或交换格式真源 | `schemas/`、`protocol/`、模块 `schema/` | 生成类型不能反过来成为真源 |
| `config` | 非秘密的默认值、环境声明、部署参数 | `config/`、模块 `config/`、`infra/` | 示例和生产配置分开 |
| `resource` | 运行时读取的图片、字体、翻译、模板、模型、静态文件 | 其 owner 的 `resources/`、`assets/`、`i18n/` | 必须进入资源清单或构建目标 |
| `migration` | 数据、配置、协议、索引或资源版本迁移 | `migrations/`、`db/migrations/`、模块迁移目录 | 有版本、前置检查、校验和回滚说明 |
| `documentation` | 人或工具阅读的说明、决策、运行手册 | `docs/`、模块 `README.md` | 引用真实路径和命令 |
| `tool` | 开发时使用的程序或代码生成器 | `tools/` | 不被产品运行时反向依赖 |
| `script` | 构建、测试、迁移、发布、维护入口 | `scripts/`、`ci/`、`automation/` | 记录参数、工作目录和退出码 |
| `generated` | 由 schema、模板、编译器或工具可重复生成 | `generated/`、`build/`、`dist/` | 按项目规则提交或忽略，禁止手改 |
| `secret-excluded` | 密钥、令牌、个人数据、本地状态 | 仓库外的秘密管理器或用户目录 | 不得进入 Git、日志和测试输出 |

`source`、`public-interface`、`test`、`schema` 和 `resource` 的 owner 必须能在
文件树中追溯到同一个模块。一个文件同时看似属于多个类别时，优先保留单一真源，
把其他形式标为生成物或适配层，而不是复制两份手写内容。

## 1.4 目录决策规则

选择目录时按“边界先于方便”执行：

1. 先问文件由谁拥有、谁调用、谁发布、谁测试、谁负责迁移；答案不同的职责不能塞进同一目录。
2. 再检查依赖方向：领域层不依赖 UI/数据库，UI/API 不拥有领域状态，工具不成为运行时依赖。
3. 再检查构建边界：目录必须能对应 target、package、service、workspace 或资源注册边界。
4. 最后才考虑语言惯例和文件数量；文件少不等于可以放到根目录或 `utils`。

默认约束：

- 公共接口与内部实现分开；C/C++ 等语言可用 `include/` 与 `src/` 镜像，其他语言遵循其包边界。
- 测试优先镜像被测模块；跨模块行为放 `integration`，公开契约放 `contract`，完整用户路径放 `system`/`e2e`。
- 同一功能的资源、翻译、schema、迁移和文档靠近其 owner；跨模块共享资源必须有明确 owner 和兼容策略。
- 业务代码不得放在 `tools/`、`scripts/`、`examples/`、`benchmarks/` 或 `tests/` 中绕过依赖边界。
- 不用目录名掩盖职责：`misc`、`stuff`、`tmp`、无说明的 `common` 和无限增长的 `utils` 需要拆分或记录例外。

## 1.5 常见项目形态的自动归属

### 单体应用

使用 `src/domain`、`src/application`、`src/infrastructure`、`src/presentation` 和
`tests/`；配置、schema、资源和迁移按 owner 放置。入口文件只负责启动和装配，
不能成为所有业务逻辑的容器。

### 多模块或单仓库

使用 `apps/<app>`、`services/<service>`、`packages/<package>` 或项目已有等价结构。
每个可部署应用/服务拥有自己的入口、配置、测试和发布定义；共享包只放稳定契约、
无状态库或明确复用的基础能力。跨包依赖必须在文件树中记录方向，不能用共享包
收容所有业务代码。

### 桌面、编辑器和引擎

区分 `core/runtime`、`application`、`document`、`rendering`、`platform`、`ui`、
`editor`、`tools` 和 `plugins`。Runtime/core 不依赖 Editor/UI；渲染器不拥有
领域状态；平台差异集中在 adapter；工具生成可复现产物。

### Web、服务和 Worker

区分 `web`、`api`、`worker`、`contracts`、`domain`、`client`、`infra` 和对应测试。
每个服务拥有自己的数据边界和迁移；`contracts` 不得变成所有业务逻辑的共享垃圾桶。

### 数据、模型和内容管线

区分原始输入、可审计处理脚本、版本化中间产物和发布资产，例如 `data/raw`、
`data/processed`、`pipelines/`、`models/`、`assets/`。原始数据和模型权重是否提交
必须按许可证、大小和可复现策略记录；缓存不能伪装成输入源。

## 1.6 文件变更同步门禁

任何新建、移动、重命名或删除文件，都要在 `file-tree.md` 的文件清单中同步更新，
并检查以下消费者：

- 构建目标、包入口、源码清单和资源清单；
- 测试注册、测试发现规则和测试 fixture；
- schema/协议生成器、数据库迁移注册和版本表；
- 配置加载、依赖注入、插件发现、路由和命令注册；
- 安装包、容器、部署、发布和许可证清单；
- README、架构文档、运行手册和示例路径。

文件树交付前必须满足：每个列出的路径真实存在或明确标为 planned/deleted；
每个新增源文件可追溯到构建和测试入口；每个生成文件可追溯到生成器和源输入；
每个秘密或本地状态都有排除位置；实际树中不能存在清单没有解释的本次新增文件。

## 2. 通用模块化模板

```text
project/
  docs/
    architecture/
    decisions/
    requirements/
    operations/
  schemas/
  config/
  src/
    domain/
    application/
    infrastructure/
    presentation/
    platform/
  tests/
    unit/
    integration/
    contract/
    system/
    fixtures/
  tools/
  scripts/
  examples/
  benchmarks/
  packaging/
  automation/
```

`domain` 不依赖 UI 和基础设施；`application` 编排用例；`infrastructure`
实现外部依赖；`presentation` 只负责交互映射；测试替身不能反向进入生产模块。

通用文件放置规则：

| 文件类型 | 默认位置 | 约束 |
| --- | --- | --- |
| 领域模型和业务规则 | `src/domain/` | 不依赖 UI、数据库或具体外部服务 |
| 用例和流程编排 | `src/application/` | 调用领域能力，协调副作用 |
| 数据库、网络、文件和第三方适配 | `src/infrastructure/` | 不把外部实现渗入领域层 |
| UI、HTTP、RPC、CLI 入口 | `src/presentation/` | 只做输入输出映射和展示状态 |
| 操作系统适配 | `src/platform/` | 集中处理平台差异 |
| 测试 | `tests/` | 按 unit/integration/contract/system 分类，与 owner 对齐 |
| 协议和稳定数据格式 | `schemas/` | 生成类型放生成目录，源 schema 保留单一真源 |
| 默认配置和示例配置 | `config/` | 秘密值只来自受控外部来源 |
| 开发、构建和维护工具 | `tools/` 或 `scripts/` | 不被生产运行时反向依赖 |
| 文档和决策记录 | `docs/` | 文档引用的路径必须真实存在 |
| 构建、打包和缓存输出 | `build/`、`dist/` 等 | 标记为 generated，不当作源码修改 |

根目录通常只保留项目身份、构建和协作入口，例如 `README.md`、许可证、构建清单、
包清单、锁文件、格式化配置、CI 配置和 `.env.example`。真实秘密、机器本地路径、
运行时数据库、下载缓存和临时日志不放根目录，也不作为配置源提交。

禁止把生产代码放进 `tests/`、`tools/`、`scripts/` 或 `examples/` 来绕过模块
边界；禁止把密钥、个人数据和本地状态写入仓库；禁止把生成文件当作手写源文件
继续编辑。测试目录可以镜像生产模块，但测试替身不得被生产模块依赖。

## 3. 桌面和编辑器模板

```text
src/
  core/
  application/
  document/
  rendering/
  platform/
  ui/
  plugins/
  resources/
tests/
  core/
  application/
  ui/
  end_to_end/
```

UI 不直接修改文档核心；文档 session 负责生命周期；渲染缓存是派生数据；
平台代码集中在 adapter。

## 4. Web 和服务模板

```text
apps/
  web/
  api/
  worker/
packages/
  contracts/
  domain/
  client/
  config/
infra/
  migrations/
  deployment/
tests/
  contract/
  integration/
  browser/
```

共享 `contracts` 只能放稳定契约和生成类型，不能把所有业务逻辑塞进共享包。
每个服务拥有自己的数据边界和迁移。

## 5. 引擎模板

```text
engine/
  runtime/
  core/
  memory/
  jobs/
  object/
  resource/
  reflection/
  serialization/
  input/
  physics/
  animation/
  audio/
  renderer/
  editor/
  tools/
  plugins/
  samples/
  tests/
  benchmarks/
```

Runtime 不依赖 Editor；Tools 生成可复现产物；renderer 不拥有领域状态；
每个模块有公开接口、线程模型、性能预算和测试入口。

## 6. 初始化完成条件

- 能从干净环境配置、构建和运行最小程序。
- 至少有一个真实功能从入口到持久化/输出的闭环。
- CI 能执行格式、构建、单元测试和门禁。
- 许可证、依赖、秘密、平台和发布边界已记录。
- 新人可以根据 README 在不依赖个人机器状态的情况下复现。

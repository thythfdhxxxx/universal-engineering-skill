---
name: universal-engineering
description: >-
  Guides AI agents through complete software development across desktop, web,
  backend, CLI, mobile, and automation projects. Use when implementing,
  extending, refactoring, or finishing software where requirements, reference
  products, language/toolchain choice, architecture, UI, engines, rendering,
  performance, security, testing, operations, migration, delivery quality, and
  project file-tree and file-ownership planning all matter.
---

# Universal Engineering

这是一套通用的软件工程执行规范。它不预设语言、框架、平台或产品类型。
目标项目已有的规则、架构、工具链、许可证和目录结构始终优先；本 Skill
只在项目规则没有覆盖时提供默认判断。

## 1. 总体原则

- 先理解现状，再改代码。先读项目规则、README、构建文件、入口、类型、
  测试和相关模块，不凭文件名猜架构。
- 用户要实现功能时，默认执行完整修改、验证和交付，不只给方案或伪代码。
- 任务必须闭环：需求、数据模型、UI/接口、运行时消费者、持久化、错误、
  测试、文档和实际验收不能只完成其中一段。
- 选择技术时比较至少两个合理方案，按项目现状、风险、性能、维护成本、
  可测试性、部署和迁移成本选择；不要为了炫技引入新技术。
- 参考软件用于理解行为和完整性，不等于允许复制代码、资源、配置或受限
  许可证内容。先确认许可证，再用本项目技术栈重建等价能力。
- 不把“能编译”当成“完成”，不把“控件存在”当成“功能实现”，不把
  “测试数量增加”当成“测试有效”。
- 所有结论都要有证据：源码、测试、构建、运行结果、性能数据或明确记录
  的限制。不能把猜测写成完成状态。

## 2. 优先级

遇到规则冲突时按以下顺序处理：

1. 用户本次明确要求和安全边界。
2. 目标项目的根规则、目录规则和团队工程规范。
3. 目标项目的构建、测试、协议和许可证约束。
4. 本 Skill 的通用流程。
5. AI 自己的偏好。

如果项目规则不清楚，先记录假设并采用最小、可回滚、符合现有代码风格的
实现。只有缺少关键信息会导致错误或数据风险时才向用户提问。

## 3. 标准执行流程

### 阶段 A：调查

1. 查看工作区状态，识别用户已有修改，禁止覆盖。
2. 找到项目规则文件和构建入口。
3. 识别产品入口、模块边界、数据流、依赖和测试入口。
4. 读取目标功能的现有实现、调用方、类型、资源和测试。
5. 搜索参考软件对应模块，记录行为差异和许可证限制。

### 阶段 B：定义

建立短而具体的实现清单：

- 用户流程和成功标准
- 数据模型和状态转换
- 页面、命令、接口或事件入口
- 加载、空、禁用、失败、取消、重试和恢复状态
- 持久化、迁移、权限和敏感数据
- 性能预算和后台任务边界
- 测试层级和验收方式
- 不适用能力及其替代反馈

### 阶段 C：设计

先确定 owning module 和单一真源，再设计实现。明确：

- 谁拥有状态
- 谁负责副作用
- 谁负责用户可见错误
- 谁负责取消和生命周期
- 谁负责写文件或调用网络
- 哪些数据是持久化真相，哪些只是缓存或派生数据

### 阶段 C.1：形成文件树和文件归属

开发新项目、添加功能或跨目录修改前，必须先形成当前文件树和目标文件归属清单，
不能先创建文件再猜目录。具体规则和模板见
[71-project-initialization-and-directory-templates.md](71-project-initialization-and-directory-templates.md)。

执行时必须：

1. 扫描仓库根目录、已有规则、构建入口、源码入口、测试入口和生成物目录，确认项目类型。
2. 优先使用项目已有的目录和模块；只有在职责、依赖方向或交付边界确实不同且清单记录理由时，才能新建目录。
3. 在项目既有架构文档目录中生成或更新 `file-tree.md`；没有既有位置时使用 `docs/architecture/file-tree.md`。
4. 为每个计划新增或修改的文件记录路径、用途、所属模块、允许依赖、文件类别、是否生成以及对应测试。
5. 实现过程中发现新文件或移动文件时，先更新清单，再修改代码；交付时检查清单与实际树一致。
6. 将源代码、测试、配置、协议、资源、文档、工具、脚本、生成物和秘密分开归类；生成物和秘密不得作为普通源文件提交。

项目规则、已有架构和构建约束优先于通用目录模板。文件树无法确定时记录冲突或假设，
不得用文件名猜测模块归属。

### 阶段 D：实现

按最小可验证切片开发。每完成一段就运行对应的格式检查、类型检查、聚焦
测试或构建。不得先堆积大量未经验证的代码。

### 阶段 E：验证

至少完成：

- 静态检查、格式检查或类型检查
- 受影响模块的单元/集成测试
- 实际构建目标
- CTest、测试运行器或项目规定的完整测试
- 真实界面、API、CLI 或服务启动检查
- 失败、取消、重试和重启后的持久化检查

### 阶段 F：交付

报告已修改内容、验证命令、验证结果、未解决问题和剩余风险。若验证因
环境缺失未完成，明确写出未执行的命令，不能用“应该可以”替代。

## 4. 按任务读取专题规则

- 需求、竞品、参考软件：阅读 [01-requirements-and-reference.md](01-requirements-and-reference.md)
- 架构和技术选型：阅读 [02-architecture-and-technology-selection.md](02-architecture-and-technology-selection.md)
- 编码、重构和模块质量：阅读 [03-implementation-and-code-quality.md](03-implementation-and-code-quality.md)
- UI、桌面、Web 和交互：阅读 [04-ui-and-interaction.md](04-ui-and-interaction.md)
- 异步、性能、并发和可靠性：阅读 [05-async-performance-reliability.md](05-async-performance-reliability.md)
- 数据、安全、协议和存储：阅读 [06-data-security-protocols.md](06-data-security-protocols.md)
- 测试、验收、发布和回归：阅读 [07-testing-acceptance-release.md](07-testing-acceptance-release.md)
- 工作区保护和交付：阅读 [08-workspace-protection-delivery.md](08-workspace-protection-delivery.md)
- 语言、工具链和代码组织：阅读 [09-language-toolchain.md](09-language-toolchain.md)
- 大型引擎、实时系统和编辑器：阅读 [10-realtime-engine-and-editor.md](10-realtime-engine-and-editor.md)
- 渲染、资源和内容管线：阅读 [11-rendering-assets-content-pipeline.md](11-rendering-assets-content-pipeline.md)
- API、插件和跨进程集成：阅读 [12-api-plugin-integration.md](12-api-plugin-integration.md)
- 可观测性、运维和线上质量：阅读 [13-observability-operations.md](13-observability-operations.md)
- 依赖、供应链和许可证：阅读 [14-dependencies-supply-chain.md](14-dependencies-supply-chain.md)
- 迁移、兼容性和版本演进：阅读 [15-migration-compatibility.md](15-migration-compatibility.md)
- 文档、协作和变更管理：阅读 [16-documentation-collaboration.md](16-documentation-collaboration.md)
- 平台、构建、打包和发布渠道：阅读 [17-platform-build-packaging.md](17-platform-build-packaging.md)
- 技术选型决策矩阵：阅读 [18-decision-matrices.md](18-decision-matrices.md)
- 领域模型和状态机：阅读 [19-domain-modeling-state.md](19-domain-modeling-state.md)
- 分布式后端和服务治理：阅读 [20-distributed-backend.md](20-distributed-backend.md)
- 实时网络、联机和同步：阅读 [21-networking-multiplayer.md](21-networking-multiplayer.md)
- 脚本、反射和序列化：阅读 [22-scripting-reflection-serialization.md](22-scripting-reflection-serialization.md)
- 内容协作、版本控制和工作区：阅读 [23-content-collaboration-source-control.md](23-content-collaboration-source-control.md)
- 设计系统、无障碍和国际化：阅读 [24-design-accessibility-localization.md](24-design-accessibility-localization.md)
- Web 前端工程：阅读 [25-web-frontend-engineering.md](25-web-frontend-engineering.md)
- CLI、自动化和开发者工具：阅读 [26-cli-automation-tools.md](26-cli-automation-tools.md)
- 移动端和平台集成：阅读 [27-mobile-platform-integration.md](27-mobile-platform-integration.md)
- AI/ML 功能工程：阅读 [28-ai-ml-feature-engineering.md](28-ai-ml-feature-engineering.md)
- 性能分析和容量规划：阅读 [29-performance-capacity-planning.md](29-performance-capacity-planning.md)
- 发布工程、SRE 和灾难恢复：阅读 [30-release-sre-disaster-recovery.md](30-release-sre-disaster-recovery.md)
- 项目治理和工程度量：阅读 [31-project-governance-metrics.md](31-project-governance-metrics.md)
- 大型软件成熟度检查：阅读 [32-large-software-maturity.md](32-large-software-maturity.md)
- 产品策略和用户研究：阅读 [33-product-strategy-research.md](33-product-strategy-research.md)
- 系统工程、需求追踪和验收：阅读 [34-systems-requirements-traceability.md](34-systems-requirements-traceability.md)
- 软件类型和领域架构：阅读 [35-domain-architecture-profiles.md](35-domain-architecture-profiles.md)
- 内存、资源和生命周期管理：阅读 [36-memory-resource-lifecycle.md](36-memory-resource-lifecycle.md)
- 数据导向设计、ECS 和场景图：阅读 [37-data-oriented-ecs-scene-graph.md](37-data-oriented-ecs-scene-graph.md)
- 物理、音频、输入和动画系统：阅读 [38-physics-audio-input-animation.md](38-physics-audio-input-animation.md)
- 威胁建模、隐私和合规：阅读 [39-threat-modeling-privacy-compliance.md](39-threat-modeling-privacy-compliance.md)
- 身份、权限、计费和账户体系：阅读 [40-identity-permissions-billing.md](40-identity-permissions-billing.md)
- 搜索、索引和数据发现：阅读 [41-search-indexing-data-discovery.md](41-search-indexing-data-discovery.md)
- 插件生态、市场和在线更新：阅读 [42-plugin-ecosystem-marketplace.md](42-plugin-ecosystem-marketplace.md)
- 模糊测试、属性测试和混沌验证：阅读 [43-fuzz-property-chaos-testing.md](43-fuzz-property-chaos-testing.md)
- 内容本地化和多地区发布：阅读 [44-localized-content-publishing.md](44-localized-content-publishing.md)
- 开发者体验、构建缓存和内部平台：阅读 [45-developer-experience-platform.md](45-developer-experience-platform.md)
- 客户支持、诊断和反馈闭环：阅读 [46-support-diagnostics-feedback.md](46-support-diagnostics-feedback.md)
- 架构评审和长期演进：阅读 [47-architecture-review-evolution.md](47-architecture-review-evolution.md)
- 大型软件分阶段路线图：阅读 [48-large-software-roadmap.md](48-large-software-roadmap.md)
- 交付前总检查表：阅读 [49-master-delivery-checklist.md](49-master-delivery-checklist.md)
- 编译器和构建系统深度规范：阅读 [50-compiler-build-deep.md](50-compiler-build-deep.md)
- 图形渲染系统深度规范：阅读 [51-rendering-system-deep.md](51-rendering-system-deep.md)
- 存储引擎和数据库深度规范：阅读 [52-storage-database-deep.md](52-storage-database-deep.md)
- 编译器、DSL 和语言工具深度规范：阅读 [53-language-tools-deep.md](53-language-tools-deep.md)
- 形式化方法和可证明正确性：阅读 [54-formal-methods.md](54-formal-methods.md)
- 复杂工作区和编辑器深度规范：阅读 [55-complex-workspace-ui.md](55-complex-workspace-ui.md)
- 确定性模拟和回放系统：阅读 [56-deterministic-simulation.md](56-deterministic-simulation.md)
- 音视频和实时媒体深度规范：阅读 [57-media-pipeline-deep.md](57-media-pipeline-deep.md)
- SDK、生态和开发者平台深度规范：阅读 [58-sdk-ecosystem-deep.md](58-sdk-ecosystem-deep.md)
- AI Agent 系统深度规范：阅读 [59-ai-agent-deep.md](59-ai-agent-deep.md)
- 深度设计和决策模板：阅读 [60-deep-design-templates.md](60-deep-design-templates.md)
- 执行阶段、产物和判定：阅读 [63-execution-stages-and-artifacts.md](63-execution-stages-and-artifacts.md)
- 语言和技术选型决策树：阅读 [64-language-and-technology-decision-tree.md](64-language-and-technology-decision-tree.md)
- 桌面软件完整开发手册：阅读 [65-desktop-software-playbook.md](65-desktop-software-playbook.md)
- Web 和服务端完整开发手册：阅读 [66-web-and-server-playbook.md](66-web-and-server-playbook.md)
- UE5 类大型引擎开发手册：阅读 [67-ue5-and-large-engine-playbook.md](67-ue5-and-large-engine-playbook.md)
- 编译器、数据库和实时系统手册：阅读 [68-compiler-database-realtime-playbook.md](68-compiler-database-realtime-playbook.md)
- AI Agent 软件开发手册：阅读 [69-ai-agent-software-playbook.md](69-ai-agent-software-playbook.md)
- 自动化工程门禁和检查：阅读 [70-automated-gates-and-checks.md](70-automated-gates-and-checks.md)
- 项目初始化和目录模板：阅读 [71-project-initialization-and-directory-templates.md](71-project-initialization-and-directory-templates.md)
- 复杂功能案例模板：阅读 [72-complex-feature-case-templates.md](72-complex-feature-case-templates.md)
- AI 执行协议：阅读 [73-ai-execution-protocol.md](73-ai-execution-protocol.md)
- 项目适配器和项目画像：阅读 [74-project-adapter-and-profile.md](74-project-adapter-and-profile.md)
- 工具链门禁适配器：阅读 [75-toolchain-gate-adapters.md](75-toolchain-gate-adapters.md)
- 质量评分和工程成熟度：阅读 [76-quality-maturity-and-scoring.md](76-quality-maturity-and-scoring.md)
- Skill 自身版本治理：阅读 [77-skill-versioning-and-governance.md](77-skill-versioning-and-governance.md)
- 软件自身版本治理和迁移：阅读 [78-software-version-governance-and-migration.md](78-software-version-governance-and-migration.md)
- 所有项目都应按阶段执行门禁，阅读 [gates/README.md](gates/README.md)
- 日常软件开发规范：阅读 [61-general-development-norms.md](61-general-development-norms.md)
- 反模式和正确替代方案：阅读 [62-antipatterns-and-correct-patterns.md](62-antipatterns-and-correct-patterns.md)
- 工程规范门禁：阅读 [gates/08-engineering-standards-gate.md](gates/08-engineering-standards-gate.md)
- 任务清单和交付模板：阅读 [templates.md](templates.md)

## 4.1 深度执行模式

当任务涉及大型软件、参考软件对照、跨模块变更或高风险数据时，必须加载
63-78 中与任务对应的专题，并按 63 号专题为每阶段产出证据。至少运行
`automation/run_engineering_gate.py`；复杂项目还要先运行
`automation/detect_project_profile.py`，再根据 profile 运行
`automation/run_project_gates.py` 和 `automation/score_quality.py`。自动门禁
通过不等于业务功能通过。

## 4.2 AI 执行状态

AI 必须显式区分 `RECEIVED`、`PREFLIGHT`、`UNDERSTANDING`、`INVESTIGATING`、
`DESIGNING`、`IMPLEMENTING`、`VERIFYING`、`DELIVERING`、`COMPLETE`、
`BLOCKED` 和 `WAITING_FOR_USER`。没有当前证据时不得从阻塞或未执行状态直接
声称完成；具体停止、确认、反猜测和防漏改规则见 73 号专题。

## 5. 永久禁止事项

- 不读现有代码就重写模块。
- 不看参考实现就凭印象简化用户要求。
- 不使用静态假数据、空回调、无效按钮或只改变内存的假保存。
- 不在 UI 线程执行不可预测的网络、磁盘、扫描、解析或大量计算。
- 不吞掉异常、错误、取消或权限失败。
- 不泄露凭据、个人数据、内部路径或完整请求到日志和测试输出。
- 不用测试删除、断言削弱、关闭构建目标或忽略失败来制造“通过”。
- 不执行会覆盖用户工作的 destructive Git 命令。
- 不把与任务无关的重构、格式化和依赖升级混入交付。
- 不因为项目规模大就跳过边界、文档、测试、性能或迁移设计。
- 不因为项目是引擎、实时程序或底层工具就默认允许未定义行为、全局状态、
  线程竞态、资源泄漏或不可诊断的崩溃。
- 不提交只有结论没有证据的设计；每个阶段必须有输入、产物、检查项和通过
  标准。
- 不把门禁文档当成形式主义：门禁失败必须修复、记录豁免理由，或明确停止
  交付。

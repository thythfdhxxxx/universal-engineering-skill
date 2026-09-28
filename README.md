# Universal Engineering Skill

这是一个不绑定语言、框架和平台的通用开发 Skill，适用于：

- 桌面软件
- Web 应用
- 后端服务
- CLI 工具
- 移动应用
- 自动化工具
- 插件和扩展

## 使用方式

把整个 `universal-engineering-skill` 目录放入目标 AI 支持的 Skill 目录，
保留内部的 `SKILL.md` 和专题 Markdown 文件，不要只复制主文件。

使用时先加载 `SKILL.md`，再按任务加载对应专题。完整专题目录如下：

开发新项目或新增功能时，AI 必须先扫描项目并形成文件树和文件归属清单，默认
写入 `docs/architecture/file-tree.md`（项目已有架构文档位置时遵循项目位置）。
每个新增或修改文件都要记录所属模块、职责、依赖方向、类别、生成方式和对应测试。
详见 `71-project-initialization-and-directory-templates.md`。

- 做需求和参考软件对照：`01-requirements-and-reference.md`
- 做架构或技术选型：`02-architecture-and-technology-selection.md`
- 写代码或重构：`03-implementation-and-code-quality.md`
- 做界面和交互：`04-ui-and-interaction.md`
- 做异步、性能和并发：`05-async-performance-reliability.md`
- 做数据、安全、协议和存储：`06-data-security-protocols.md`
- 做测试、验收和发布：`07-testing-acceptance-release.md`
- 处理工作区和交付：`08-workspace-protection-delivery.md`
- 语言、编译器和工具链：`09-language-toolchain.md`
- UE5 类大型引擎和实时系统：`10-realtime-engine-and-editor.md`
- 渲染、资源和内容管线：`11-rendering-assets-content-pipeline.md`
- API、插件和跨进程集成：`12-api-plugin-integration.md`
- 可观测性和线上运维：`13-observability-operations.md`
- 依赖、供应链和许可证：`14-dependencies-supply-chain.md`
- 迁移、兼容性和版本演进：`15-migration-compatibility.md`
- 文档、协作和变更管理：`16-documentation-collaboration.md`
- 多平台构建、打包和发布渠道：`17-platform-build-packaging.md`
- 技术选型矩阵：`18-decision-matrices.md`
- 领域模型和状态机：`19-domain-modeling-state.md`
- 分布式后端和服务治理：`20-distributed-backend.md`
- 实时网络、联机和同步：`21-networking-multiplayer.md`
- 脚本、反射和序列化：`22-scripting-reflection-serialization.md`
- 内容协作、版本控制和工作区：`23-content-collaboration-source-control.md`
- 设计系统、无障碍和国际化：`24-design-accessibility-localization.md`
- Web 前端工程：`25-web-frontend-engineering.md`
- CLI、自动化和开发者工具：`26-cli-automation-tools.md`
- 移动端和平台集成：`27-mobile-platform-integration.md`
- AI/ML 功能工程：`28-ai-ml-feature-engineering.md`
- 性能分析和容量规划：`29-performance-capacity-planning.md`
- 发布工程、SRE 和灾难恢复：`30-release-sre-disaster-recovery.md`
- 项目治理和工程度量：`31-project-governance-metrics.md`
- 大型软件成熟度检查：`32-large-software-maturity.md`
- 产品策略和用户研究：`33-product-strategy-research.md`
- 系统工程、需求追踪和验收：`34-systems-requirements-traceability.md`
- 软件类型和领域架构：`35-domain-architecture-profiles.md`
- 内存、资源和生命周期管理：`36-memory-resource-lifecycle.md`
- 数据导向设计、ECS 和场景图：`37-data-oriented-ecs-scene-graph.md`
- 物理、音频、输入和动画系统：`38-physics-audio-input-animation.md`
- 威胁建模、隐私和合规：`39-threat-modeling-privacy-compliance.md`
- 身份、权限、计费和账户体系：`40-identity-permissions-billing.md`
- 搜索、索引和数据发现：`41-search-indexing-data-discovery.md`
- 插件生态、市场和在线更新：`42-plugin-ecosystem-marketplace.md`
- 模糊测试、属性测试和混沌验证：`43-fuzz-property-chaos-testing.md`
- 内容本地化和多地区发布：`44-localized-content-publishing.md`
- 开发者体验、构建缓存和内部平台：`45-developer-experience-platform.md`
- 客户支持、诊断和反馈闭环：`46-support-diagnostics-feedback.md`
- 架构评审和长期演进：`47-architecture-review-evolution.md`
- 大型软件分阶段路线图：`48-large-software-roadmap.md`
- 交付前总检查表：`49-master-delivery-checklist.md`
- 编译器和构建系统深度规范：`50-compiler-build-deep.md`
- 图形渲染系统深度规范：`51-rendering-system-deep.md`
- 存储引擎和数据库深度规范：`52-storage-database-deep.md`
- 编译器、DSL 和语言工具深度规范：`53-language-tools-deep.md`
- 形式化方法和可证明正确性：`54-formal-methods.md`
- 复杂工作区和编辑器深度规范：`55-complex-workspace-ui.md`
- 确定性模拟和回放系统：`56-deterministic-simulation.md`
- 音视频和实时媒体深度规范：`57-media-pipeline-deep.md`
- SDK、生态和开发者平台深度规范：`58-sdk-ecosystem-deep.md`
- AI Agent 系统深度规范：`59-ai-agent-deep.md`
- 深度设计和决策模板：`60-deep-design-templates.md`
- 执行阶段、产物和判定：`63-execution-stages-and-artifacts.md`
- 语言和技术选型决策树：`64-language-and-technology-decision-tree.md`
- 桌面软件完整开发手册：`65-desktop-software-playbook.md`
- Web 和服务端完整开发手册：`66-web-and-server-playbook.md`
- UE5 类大型引擎开发手册：`67-ue5-and-large-engine-playbook.md`
- 编译器、数据库和实时系统手册：`68-compiler-database-realtime-playbook.md`
- AI Agent 软件开发手册：`69-ai-agent-software-playbook.md`
- 自动化工程门禁和检查：`70-automated-gates-and-checks.md`
- 项目初始化和目录模板：`71-project-initialization-and-directory-templates.md`
- 复杂功能案例模板：`72-complex-feature-case-templates.md`
- AI 执行协议：`73-ai-execution-protocol.md`
- 项目适配器和项目画像：`74-project-adapter-and-profile.md`
- 工具链门禁适配器：`75-toolchain-gate-adapters.md`
- 质量评分和工程成熟度：`76-quality-maturity-and-scoring.md`
- Skill 自身版本治理：`77-skill-versioning-and-governance.md`
- 软件自身版本治理和迁移：`78-software-version-governance-and-migration.md`
- Skill 版本：`VERSION`、`skill-manifest.json`、`CHANGELOG.md`
- 阶段门禁目录：`gates/README.md`
- 日常软件开发规范：`61-general-development-norms.md`
- 反模式和正确替代方案：`62-antipatterns-and-correct-patterns.md`
- 工程规范门禁：`gates/08-engineering-standards-gate.md`
- 需要清单或报告格式：`templates.md`

## 推荐使用提示

```text
请使用 universal-engineering skill 完成本任务。
先读取项目已有规则和当前实现，再按任务加载相关专题。
项目已有规范优先于通用规则。
请直接实现、验证并报告结果，不只给方案。
```

## 作为项目根规则

如果目标 AI 不支持 Skill 目录，可以把主 `SKILL.md` 内容复制为项目根目录
的 `AGENTS.md`、`CLAUDE.md` 或该工具支持的规则文件，并把专题文件放在
同一目录或规则文件可以访问的文档目录中。

复制后仍要保留以下原则：

1. 目标项目已有规则优先。
2. 参考软件只借鉴行为，不直接复制受限代码。
3. 所有功能必须有运行时闭环、错误处理、测试和实际验收。
4. 未执行的构建、测试和运行不能写成已通过。

## 深度执行模式

当开发大型软件或复杂功能时，不只阅读主文件。按任务加载 63-78 专题，
使用阶段产物模板记录需求、架构、实现、验证和交付证据，并运行：

```text
python automation/run_engineering_gate.py --root .
```

复杂项目可以生成画像并执行已声明门禁：

```text
python automation/detect_project_profile.py --root . --output project-profile.json
python automation/run_project_gates.py --root . --profile project-profile.json
python automation/run_project_gates.py --root . --profile project-profile.json --execute
python automation/score_quality.py --assessment quality-assessment.json
```

这些脚本默认不安装依赖、不上传代码、不发布产物；目标项目仍必须执行自己
的编译、类型检查、测试、安全扫描、性能验证和真实运行验收。

## UE5 类大型项目

如果开发的是游戏引擎、渲染引擎、编辑器、实时仿真或其他大型基础设施，
至少同时加载：

```text
02-architecture-and-technology-selection.md
03-implementation-and-code-quality.md
05-async-performance-reliability.md
09-language-toolchain.md
10-realtime-engine-and-editor.md
11-rendering-assets-content-pipeline.md
14-dependencies-supply-chain.md
17-platform-build-packaging.md
19-domain-modeling-state.md
21-networking-multiplayer.md
22-scripting-reflection-serialization.md
29-performance-capacity-planning.md
30-release-sre-disaster-recovery.md
32-large-software-maturity.md
```

这套规则不会强制使用 C++、Rust 或某一个图形 API，而是要求根据目标平台、
团队能力、实时预算、工具链和长期维护成本做出有证据的选择。

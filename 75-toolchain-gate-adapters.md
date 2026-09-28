# 工具链门禁适配器

本专题规定如何把项目 profile 转换成真实门禁。适配器只执行项目明确声明
的命令，不擅自安装依赖、不上传代码、不发布产物、不执行 shell 拼接。

## 1. 门禁类别

```text
format       格式化和规范检查
typecheck    类型、schema、接口检查
build        编译、打包或生成
unit         单元测试
integration  集成测试
system       真实系统/浏览器/桌面验收
dependency   依赖、许可证、供应链
security     SAST、秘密、漏洞和权限检查
performance  benchmark、容量和资源预算
package      安装包、签名、完整性和清单
```

每个类别定义是否必需。不存在该类别时标记 `NOT_APPLICABLE`，不能悄悄跳过。

## 2. 通用命令模型

```json
{
  "id": "build-debug",
  "category": "build",
  "required": true,
  "command": ["cmake", "--build", "--preset", "debug"],
  "cwd": ".",
  "timeout_seconds": 1800,
  "environment": {},
  "artifacts": ["build/"],
  "allow_exit_codes": [0]
}
```

默认使用参数数组和 `shell=false`。必须明确工作目录、超时、环境变量、允许
退出码和预期产物。秘密不能放进命令、环境文件或日志。

## 3. 常见生态适配

### CMake/C++

先确认 preset、编译器、生成器、配置和 target，再执行 configure、build、
CTest、静态分析、sanitizer 和 benchmark。不能只运行 `cmake --build` 就
宣称测试通过。

### Rust/Cargo

确认 toolchain、workspace、features、目标平台和 lockfile。区分 `cargo check`、
`cargo test`、`cargo clippy`、格式检查、基准和发布构建。

### Go

确认 module、Go 版本、workspace、CGO 和目标平台。按项目规则执行
`go test`、race、vet、build、coverage 和依赖扫描。

### Node/TypeScript

确认 package manager、lockfile、workspace、scripts、Node 版本和构建产物。
区分 lint、typecheck、unit、browser、build、audit 和 bundle 分析。

### Java/Kotlin/Gradle

确认 wrapper、JDK、Gradle version、模块和 profile。执行编译、单测、集成、
静态分析、依赖和打包验证；不要使用机器全局 Gradle 替代 wrapper。

### .NET/C#

确认 SDK、solution、target framework、configuration 和 workload。执行
restore、build、test、analyzer、pack 和平台运行验证。

### Python

确认 Python、虚拟环境、lockfile、包构建和测试 runner。区分格式、类型、
单测、集成、构建和依赖漏洞检查。

### UE/大型引擎

确认引擎版本、Target、Configuration、平台 SDK、Cook/Package 入口和资源
构建。构建通过不能替代编辑器运行、资产验证、帧预算和打包运行。

### Docker

确认 Dockerfile、context、build args、基础镜像来源、扫描和运行验收。禁止
把秘密写进镜像层；镜像构建通过不能替代容器健康、权限和数据持久化验证。

## 4. 结果判定

```text
PASS         命令真实执行且允许退出码，产物和后置检查满足要求
FAIL         命令执行但失败、产物缺失或后置检查失败
BLOCKED      环境/权限/依赖缺失导致未能执行
NOT_RUN      配置中存在但本次未执行
NOT_APPLICABLE 项目明确声明不适用且有理由
WAIVED       有负责人、原因、期限和替代控制
```

必需门禁为 `FAIL` 或 `BLOCKED` 时，不能交付为完成。`WAIVED` 不等于通过，
必须在最终报告中单独显示。

## 5. 安全边界

- 只执行 profile 中明确列出的命令。
- 默认禁止 shell 字符串、管道、重定向和命令替换。
- 工作目录必须在项目根目录内。
- 环境变量只允许非敏感声明；秘密使用项目批准的注入机制。
- 每条命令记录版本、工作目录、退出码、耗时和产物。
- 超时后停止并标记 `BLOCKED` 或 `FAIL`，不能继续猜测。

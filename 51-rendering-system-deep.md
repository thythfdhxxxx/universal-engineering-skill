# 图形渲染系统深度规范

## 1. 渲染层级

推荐区分：

```text
Platform Window
  -> Graphics Device
  -> RHI / API Adapter
  -> Resource and Synchronization
  -> Render Graph
  -> Scene Visibility
  -> Passes and Materials
  -> Post Process / UI / Debug
```

游戏逻辑、编辑器和 UI 不直接持有 API 原生句柄。后端能力通过 feature
query、resource capability 和明确的降级路径暴露。

## 2. Render Graph

每个 pass 声明资源读写、生命周期、队列、屏障和依赖。图编译器负责：

- 拓扑排序
- 资源别名
- 屏障
- 队列同步
- 无效 pass 删除
- 调试标记
- GPU 时间统计

禁止通过全局状态和隐式 flush 隐藏资源依赖。

## 3. GPU 资源

纹理、缓冲、管线、描述符、采样器和 staging 资源定义创建、上传、读写、
同步、回收、设备丢失和恢复。资源句柄不能在 GPU 仍使用时销毁。

## 4. 帧预算

定义 CPU 游戏线程、CPU 渲染线程、提交线程、GPU、上传、显存和同步预算。
记录平均、P95、峰值和低端设备表现。GPU 等待必须能定位到 pass 和资源。

## 5. Shader

Shader 源、include、宏、变体、平台目标、反射布局和缓存版本可追踪。限制
变体数量，编译失败能定位文件、行、平台、材质和变体。

## 6. 设备丢失

验证设备移除、驱动重置、窗口最小化、后台恢复、显存不足和 swapchain
重建。失败时释放旧资源、通知上层、重建可恢复资源并保留用户数据。

## 7. 渲染验收

必须有空场景、最小场景、大场景、材质失败、shader 失败、资源缺失、截图
回归、GPU 捕获、设备丢失和 Shipping 构建验证。

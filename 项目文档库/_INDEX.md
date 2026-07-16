# 文档索引 / Index

> 维护规则见 `README.md` 与 `00_AI优先查阅说明.md`。AI 接到任务时**先读本目录**，依据 `last_verified` 与 `scope` 判断是否需要回到 `C:\ai\RuyiDify` 重新读码/联网。

| 文档 | 标题 | last_verified | scope | 可信度 |
|------|------|---------------|-------|--------|
| [00_AI优先查阅说明.md](./00_AI优先查阅说明.md) | 项目文档库公约 + AI 查阅顺序 | 2026-07-15 | 全局约定（用户指令） | 📄 用户指令 |
| [01_项目全貌.md](./01_项目全貌.md) | 项目全貌与模块职责 | 2026-07-15 | 根 AGENTS.md、README、目录结构、api/web AGENTS | ✅代码确认/📄文档说明 |
| [02_运行架构.md](./02_运行架构.md) | 运行架构与组件协作 | 2026-07-15 | docker-compose*.yaml、api/Dockerfile、entrypoint.sh | ✅代码确认 |
| [03_知识库端到端流程.md](./03_知识库端到端流程.md) | 知识库链路 | 2026-07-15 | controllers、dataset_service、indexing_runner、tasks、retrieval_service | ✅代码确认 |
| [04_启动方式报告.md](./04_启动方式报告.md) | 启动方式理论盘点 | 2026-07-15 | Makefile、package.json、docker compose、api entrypoint | ✅代码确认/⏳部分待验证 |
| [04b_启动验证实操记录.md](./04b_启动验证实操记录.md) | **Docker Compose 真实启动验证** | 2026-07-15 | 真实执行 `docker compose up -d` + 访问验证 | ✅ 真实运行验证 |
| [05_配置入口地图.md](./05_配置入口地图.md) | 配置入口地图 | 2026-07-15 | docker/.env.example、docker/envs/*、api/.env.example | ✅代码确认 |
| [06_学习资源分类.md](./06_学习资源分类.md) | 学习资源分类 | 2026-07-15 | examples/知识库/*、docs/资料/知识库开发入门/* | ✅代码确认/📄文档说明 |
| [08_Ollama接入Embedding.md](./08_Ollama接入Embedding.md) | **本地 Ollama Embedding 接入（双通道验证）** | 2026-07-15 | 真实配置 Ollama+Tongyi 并端到端索引到 completed | ✅ 真实运行验证 |

## 重读触发条件（AI 判断用）
- `last_verified` 距今 > 90 天；或
- 上游版本号变化（当前 `dify-api==1.15.0`）；或
- 用户声明「已升级/最新版已变」。

## 模板（新增文档时复制）
```
# NN_标题.md
- last_verified: YYYY-MM-DD
- scope: <本次读码/读文档/运行的范围>
- evidence: ✅代码确认 / 📄文档说明 / 🔗推断 / ⏳待验证 / ✅真实运行验证
```

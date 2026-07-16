# RuyiDify 项目文档库（Project Documentation Library）

> **项目文档库定义：** 每个项目专属的、沉淀非上游分析/架构/启动/学习资料的文档目录，供**人类与其他 AI 共同阅读与维护**。本目录即 **RuyiDify 项目**的项目文档库。
> 它不属于 RuyiDify 仓库本身（仓库在 `C:\ai\RuyiDify`），用于沉淀**项目分析、架构梳理、启动方式、学习顺序**等资料。
> 所有结论均基于某一时刻对源码/脚本的**只读**核验或**真实运行**验证，并标注来源与可信度。

> ⚠️ **AI 必读：** 接到本项目任务时，**先查看项目文档库**（本目录），优先读 `00_AI优先查阅说明.md` → `README.md` → `_INDEX.md` → 对应文档。只有在项目文档库**未提供 / 不足 / 已过期**时才深入源码或联网搜索。详见 [`00_AI优先查阅说明.md`](./00_AI优先查阅说明.md)。

---

## 0. 目录定位与维护约定（维护者必读）

**为什么单独建目录：**
- RuyiDify 是从开源 Dify 拉出的「实战课」分支（见 `C:\ai\RuyiDify\AGENTS.md` 与 `docs\博客\`）。
- 上游代码会随 Dify 更新而变化；本目录记录的是**我们对它的理解快照**，不应随仓库提交/合并被冲掉，也不应污染上游文档（`docs/`、`README.md`）。
- 路径说明（本机只有 C 盘，没有 D/E 盘）：
  - 项目源码：`C:\ai\RuyiDify`（用户原称 `D:\ai\RuyiDify`）
  - 项目文档库：`C:\RuyiTypora\项目\ai\RuyiDify`（即本目录；用户原称 `E:\RuyiTypora\项目\ai\RuyiDify`）

**人类与 AI 共读规则：**
1. 每份文档顶部都有 `last_verified` 时间戳与 `scope` 字段。
2. AI 接到「理解/改动本项目」类任务时，按 `00_AI优先查阅说明.md` 的顺序查阅，**优先用文档**，必要时才回源码/联网。
3. 判断是否需要「深度重读源码」的依据：
   - 距 `last_verified` 超过 **90 天**，或
   - 上游版本号变化（当前核验基于 `dify-api==1.15.0`，见 `C:\ai\RuyiDify\api\pyproject.toml:3`），或
   - 用户明确说「最新版已变 / 升级过」。
4. 文档只能靠**真实运行/读码**更新，禁止凭 Dify 通用经验补全命令。
5. 不在此目录写入密钥、Token、真实环境变量值（与仓库 `AGENTS.md` 的保密要求一致）。

---

## 1. 目录结构（便于长期维护与扩展）

```
RuyiDify/                         ← 本目录（非上游文档）
├── README.md                     ← 本文件：定位、维护约定、索引
├── _INDEX.md                     ← 文档索引 + 每篇的 last_verified / scope / 可信度
├── 01_项目全貌.md                ← 关系定位、技术栈、模块职责表
├── 02_运行架构.md                ← Web/API/Celery/Redis/DB/向量库/对象存储/模型/Compose 协作
├── 03_知识库端到端流程.md        ← Dataset→Document→Segment→Embedding→Index→Retrieval→QA 真实路径
├── 04_启动方式报告.md            ← 所有启动方式盘点、步骤、组件/端口、风险
├── 05_配置入口地图.md            ← 本地/Docker/模型/Embedding/向量库/API Key 配置项
├── 06_学习资源分类.md            ← docs\资料 + examples\知识库 的分类与可学内容
└── 07_关键文件地图.md           ← 关键符号→文件路径速查表
```

**扩展约定：** 新增分析文档时，复制 `_INDEX.md` 中的条目模板，保持字段一致（last_verified、scope、evidence 等级）。

---

## 2. 证据等级说明（贯穿所有文档）

| 标记 | 含义 | 说明 |
|------|------|------|
| ✅ 代码确认 | 直接读源码/脚本得到 | 以 `文件:行号` 标注 |
| 📄 文档说明 | 来自仓库自带文档/README | 以文档路径标注 |
| 🔗 调用关系推断 | 由导入/入口串联推断 | 需后续运行验证 |
| ⏳ 尚未验证 | 必须运行才能确认 | 附最小验证方法 |

---

## 3. 当前快照（last_verified = 2026-07-15）

- 项目版本：`dify-api==1.15.0`（api/pyproject.toml:3）；docker 镜像 `langgenius/dify-api:1.15.0`、`langgenius/dify-web:1.15.0`
- 核验范围：根 `AGENTS.md`、`api/AGENTS.md`、`web/AGENTS.md`、`Makefile`、`docker/*.yaml`、`docker/.env.example`、`api/pyproject.toml`、`web/package.json`、`examples/知识库/*`、`docs/资料/知识库开发入门/*`、关键 KB 代码路径
- 未执行：任何安装、启动、迁移、外部 API 调用（严格遵守执行边界）

> 下一步：AI 在 2026-10-15 之后或版本升级后再次深度阅读源码前，应先读 `_INDEX.md` 判断是否需要重读。

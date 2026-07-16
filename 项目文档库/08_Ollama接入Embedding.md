# 08 · 本地模型（Ollama）接入知识库 Embedding 实操

- last_verified: 2026-07-15
- scope: 真实在 `C:\ai\RuyiDify`（Docker Compose 已启动）+ 本机 Ollama 容器，配置 Embedding 并端到端验证
- evidence: ✅ 真实运行验证（API 创建数据集→文档→索引 completed，DB 段数确认）
- 关联: `03_知识库端到端流程.md`、`04b_启动验证实操记录.md`

## 1. 架构结论（已验证）
RuyiDify 在 Dify 1.15 上可用**双模型通道**：
- **本地通道 Ollama**：embedding 模型 `nomic-embed-text`（137M, 768 维），运行于独立 `ollama` 容器，挂在 `docker_default` 网络，api 容器经 `http://ollama:11434` 调用。免密钥、离线、免费。
- **云端通道 Tongyi/通义(Qwen)**：插件 `langgenius/tongyi`，默认 LLM=`qwen3.7-max`、rerank=`qwen3-rerank`、tts=`qwen3-tts-flash`、speech2text=`paraformer-realtime-v1`。无需 VPN 即可从 daemon 容器直连 DashScope（0.09s, 401=待填密钥）。

> ⚠️ 关键发现：本机网络对**大文件下载严重限速**（GitHub/DockerHub镜像/PyPI 均曾停滞）；但**普通 HTTPS API 调用正常**。OpenAI 的 API 在 Docker 容器内**不可达**（容器不继承宿主机 VPN 路由），故云端只用 Tongyi 等国内厂商。

## 2. 已验证的配置事实（来自 DB / 日志）
| 项 | 值 | 来源 |
|----|----|------|
| Ollama 插件 | `langgenius/ollama:1.0.0` 已安装并 running (pid=589) | plugin_daemon 日志 |
| Ollama 服务地址 | `http://ollama:11434`（同 `docker_default` 网络服务名） | api 容器 curl 200/0.003s |
| embedding 模型 | `nomic-embed-text`（容器内 `ollama list` 可见，274MB） | ollama 容器 |
| 默认 embedding | `text-embedding / nomic-embed-text / langgenius/ollama/ollama` | `provider_models` 表 |
| 默认 LLM | `llm / qwen3.7-max / langgenius/tongyi/tongyi` | `tenant_default_models` 表 |
| Tongyi 插件 | `langgenius/tongyi:0.2.4` 已安装 running (pid=691) | plugin_daemon 日志 |

## 3. 端到端验证结果（2026-07-15 真实执行）
通过 Dify 数据集 API 全流程跑通：
1. `POST /v1/datasets` 建库（high_quality）→ 200，dataset_id 落地
2. `POST /v1/datasets/<id>/document/create-by-text` 上传文本 + `indexing_technique=high_quality` + `embedding_model=nomic-embed-text` → 文档创建成功
3. 轮询/查 `documents`：`indexing_status=completed`，word_count=129
4. DB `document_segments`：`count=1, completed=1` → **本地 Ollama embedding 真实生效**

结论：**本地 embedding 通道完全可用**，知识库索引可到 `completed`。

## 4. 在控制台的配置步骤（用户侧，AI 不处理密钥）
1. 左侧 Integrations → Model Provider → Ollama → Setup
2. **Model Type = Text Embedding**，Model Name = `nomic-embed-text`，Base URL = `http://ollama:11434`，API Key 留空 → Add
3. （如需本地 LLM 问答）`ollama pull qwen2.5:7b` 后用 Model Type=LLM 添加同名模型
4. Tongyi → Setup → 填 DashScope API Key（自建，AI 不接触密钥本身）→ 其 `qwen3.7-max` 即作为默认 LLM

> 注意：Base URL 必须填 `http://ollama:11434`（容器服务名），不是 localhost / host.docker.internal。
> 填 `Ollama` 作 Model Name 或 Model Type=LLM 会报 404 `model 'Ollama' not found`（那是 provider 名，不是模型名）。

## 5. 启动 Ollama 容器（如未运行）
```bash
cd C:\ai\RuyiDify\docker
docker run -d --name ollama --network docker_default -p 11434:11434 \
  -v ollama_data:/root/.ollama --restart unless-stopped ollama/ollama:latest
docker exec ollama ollama pull nomic-embed-text      # 约 274MB，网络正常时数十秒
```
（镜像若本地缺失：`docker pull ollama/ollama:latest` 经已配置 mirror 可拉，本机网络慢时需耐心/换网络）

## 6. 历史阻塞与解决（沉淀，避免重蹈）
- 早期 `plugins.dify.ai` DNS 解析失败（NXDOMAIN）→ 无关，1.15 用 `marketplace.dify.ai`（可达）。
- plugin 安装卡在 `uv pip install`（PyPI 限速）→ 网络恢复/换网络后 OpenAI 与 Ollama 插件均安装成功。
- OpenAI 保存密钥超时 → 容器内不可达 api.openai.com（无 VPN 路由）；改用 Tongyi 等国内厂商解决。
- Ollama 镜像拉取曾停滞 → 后续网络好转后 8.06GB 镜像完整拉下。

## 7. 待验证 / 注意
- 本地 LLM 问答未实测（仅配了 Tongyi 云端 LLM）；若要纯离线 Q&A，需 `ollama pull` 一个 chat 模型并设为默认 LLM。
- 重启 Docker Desktop 或宿主机后，`ollama` 容器因 `--restart unless-stopped` 自动起；若手动删过需重跑第 5 节。

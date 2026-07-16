---
title: Dify 知识库文档支持类型
updated: 2026-07-15
maintainer: ruyi
status: stable
source: RuyiDify 源码 api/core/rag/extractor/extract_processor.py（Dify 1.15）
source_last_verified: 2026-07-15
---

# Dify 知识库文档支持类型

> 【代码确认】本文所列支持类型均来自 RuyiDify（dify-api==1.15.0）源码
> `api/core/rag/extractor/extract_processor.py` 的 `ExtractProcessor.extract()` 分发逻辑，
> 核对日期 **2026-07-15**。不同 `ETL_TYPE` 配置下支持范围不同，详见下文。

## 1. 总体统计

Dify 知识库（Dataset）的文档来源分两大类：

| 来源类别 | 说明 |
|---|---|
| 文件上传（FILE） | 本地/接口上传的文档文件，按扩展名分发到对应抽取器 |
| 非文件数据源 | Notion 工作区、网页（Website：Firecrawl / WaterCrawl / JinaReader） |

**文件类支持类型数量：**
- 默认模式（`ETL_TYPE` 非 `Unstructured`）：**8 种**扩展名族
- Unstructured 模式（`ETL_TYPE=Unstructured`）：**14 种**扩展名族（在默认基础上新增 6 种）

## 2. 默认模式支持的文件类型（8 种）

| 扩展名 | 类型 | 抽取器 | 说明 |
|---|---|---|---|
| `.txt` | 纯文本 | TextExtractor | 任意未匹配扩展名的文件也走此分支（兜底） |
| `.md` / `.markdown` / `.mdx` | Markdown | MarkdownExtractor | 默认模式直接用原生抽取 |
| `.pdf` | PDF | PdfExtractor（pypdfium2） | 逐页抽取，支持提取图片 |
| `.html` / `.htm` | 网页/HTML | HtmlExtractor | 抽取正文 |
| `.docx` | Word（新版） | WordExtractor | 支持表格与图片提取 |
| `.csv` | 逗号分隔值 | CSVExtractor | 自动探测编码 |
| `.xlsx` / `.xls` | Excel | ExcelExtractor | 按工作表拆分 |
| `.epub` | 电子书 | UnstructuredEpubExtractor | 默认模式亦支持 |

## 3. Unstructured 模式额外支持的类型（+6 种，共 14 种）

当 `ETL_TYPE=Unstructured`（需配置 `UNSTRUCTURED_API_URL` / `UNSTRUCTURED_API_KEY`）时，在默认 8 种之外新增：

| 扩展名 | 类型 | 抽取器 |
|---|---|---|
| `.doc` | Word（旧版） | UnstructuredWordExtractor |
| `.msg` | Outlook 邮件 | UnstructuredMsgExtractor |
| `.eml` | 邮件文件 | UnstructuredEmailExtractor |
| `.ppt` | PowerPoint（旧版） | UnstructuredPPTExtractor |
| `.pptx` | PowerPoint（新版） | UnstructuredPPTXExtractor |
| `.xml` | XML | UnstructuredXmlExtractor |

> 注：`.md/.markdown/.mdx`、`.html/.htm`、`.pdf`、`.docx`、`.csv`、`.xlsx/.xls`、`.epub`、`.txt` 在 Unstructured 模式下同样支持（部分走 unstructured 服务，如 `.md` 在自动模式下使用 UnstructuredMarkdownExtractor）。

## 4. 非文件数据源（2 类）

| 数据源 | 说明 |
|---|---|
| Notion | 通过 Notion 集成导入页面/数据库 |
| Website（网页） | 支持 Firecrawl、WaterCrawl、JinaReader 三种抓取 Provider |

## 5. 主流文档类型（推荐优先使用）

从生态成熟度与抽取质量看，最主流、最常用的类型有：

1. **`.txt` / `.md`** —— 纯文本与 Markdown，结构清晰、抽取最稳定，适合技术文档与笔记。
2. **`.pdf`** —— 论文、报告、手册最通用，PDF 是第一大常见知识库来源。
3. **`.docx`** —— Office Word 文档，企业资料常见。
4. **`.csv` / `.xlsx`** —— 表格数据，适合结构化知识导入。
5. **`.html`** —— 网页存档与导出。

## 6. 配置入口

| 配置项 | 作用 | 位置 |
|---|---|---|
| `ETL_TYPE` | 选择 `Unstructured` 或默认抽取管道 | api 环境变量（`.env`） |
| `UNSTRUCTURED_API_URL` | Unstructured 服务地址（启用额外类型需配置） | api 环境变量 |
| `UNSTRUCTURED_API_KEY` | Unstructured 服务密钥 | api 环境变量 |

## 7. 关键结论

- Dify 知识库在**默认模式**支持 **8 种**文件类型（txt/md/pdf/html/docx/csv/xlsx/epub）。
- 切换 **Unstructured 模式**后支持 **14 种**文件类型（新增 doc/msg/eml/ppt/pptx/xml）。
- 此外还支持 **Notion** 与 **Website** 两类非文件数据源。
- 主流/推荐类型：**PDF、Markdown、TXT、DOCX、CSV/XLSX、HTML**。

## 8. 代码依据

- 主分发逻辑：`api/core/rag/extractor/extract_processor.py`（`ExtractProcessor.extract`，约第 92–182 行）。
- 抽取器实现目录：`api/core/rag/extractor/`（pdf_extractor.py、word_extractor.py、markdown_extractor.py、html_extractor.py、csv_extractor.py、excel_extractor.py、text_extractor.py、unstructured/ 等）。

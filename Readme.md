# QMT API 文档生成工具

本目录包含用于爬取、格式化和生成 QMT API 文档的 Python 脚本工具链。这些工具可以从官方网页抓取内容，将其转换为 Markdown 格式，并进行后续的深度格式化修复（链接替换、代码块缩进等）。

## 环境要求

运行脚本前，请确保安装了以下依赖库：

- `requests`
- `beautifulsoup4`
- `pathlib` (标准库)
- `re` (标准库)

推荐使用 `uv` 进行运行管理。

## 使用流程

请按照以下顺序执行脚本以生成最终文档。

### 1. 爬取文档 (`qmt_crawler.py`)

运行爬虫脚本，从官网抓取 HTML 页面，下载图片，并将其整合成单一的 Markdown 文件。

```bash
uv run python qmt_crawler.py
```

- **输入**: 预定义的 QMT 官网 URL 列表。
- **输出**: `QMT_Docs/QMT_API_Documentation.md` (及 `QMT_Docs/images/` 目录下的图片)。

### 2. 准备工作文件

后续的修复脚本默认针对 `QMT_API_Documentation_Format.md` 文件进行操作（为了区分原始爬取版本和格式化后的版本）。请将生成的文档复制或重命名：

```bash
# Windows (CMD)
copy QMT_Docs\QMT_API_Documentation.md QMT_Docs\QMT_API_Documentation_Format.md

# PowerShell / Bash
cp QMT_Docs/QMT_API_Documentation.md QMT_Docs/QMT_API_Documentation_Format.md
```

### 3. 修复内部链接 (`fix_links.py`)

原始网页中包含大量 "在新窗口打开" 的外部链接或纯文本引用（如 "参见数据字典"）。此脚本会扫描文档中的 headers，将这些引用替换为指向当前文档对应章节的内部 Markdown 锚点。

```bash
uv run python fix_links.py
```

- **目标文件**: `QMT_Docs/QMT_API_Documentation_Format.md`

### 4. 修复代码块缩进 (`indent_code_blocks.py`)

在 Markdown 中，嵌套在列表项内的代码块（fence block）如果缺乏正确的缩进，会导致列表结构断裂。此脚本会识别嵌套列表中的代码块，并根据父级列表项的缩进级别自动添加 4 空格（或相应倍数）的缩进，确保文档结构正确。

```bash
uv run python indent_code_blocks.py
```

- **目标文件**: `QMT_Docs/QMT_API_Documentation_Format.md`

## 最终产物

执行完上述步骤后，最终可用的高质量文档为：

**`QMT_Docs/QMT_API_Documentation_Format.md`**

建议使用支持 Markdown 的编辑器（如 VS Code, Obsidian, Typora）查看。

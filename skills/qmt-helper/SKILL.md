---
name: qmt-helper
description: QMT (MiniQMT/XtQuant) Python API 文档索引与精准检索技能。当用户提到 QMT、XtQuant、MiniQMT、xtdata、xttrader、行情订阅、委托下单、撤单、持仓查询、资产查询、A股程序化交易等关键词时，必须激活此技能。不要一次性读取整个文档，而是先查阅 ./references/api_index.md 中的行号索引，再按需读取 ./references/QMT_API_Documentation.md 的对应行号范围。
---

# QMT API (XtQuant) Helper Skill

本技能帮助 Claude 快速、精准地定位和检索 XtQuant (QMT Python API) 文档内容，并根据文档生成正确的代码。

完整文档 [./references/QMT_API_Documentation.md](./references/QMT_API_Documentation.md) 超过 6000 行。禁止一次性全部读取，否则会溢出上下文窗口、增加延迟并浪费大量 Token。

## 使用流程

1. **禁止一次性读取整个文档文件。**
2. 收到用户关于 QMT 的问题后，先读取 [./references/api_index.md](./references/api_index.md)，从中找到对应功能的行号范围。
3. 使用 `Read` 工具，通过 `offset`（起始行号）和 `limit`（读取行数）参数，从 [./references/QMT_API_Documentation.md](./references/QMT_API_Documentation.md) 中只提取需要的段落。
4. `api_index.md` 中已包含大部分接口的函数名和核心参数摘要，简单问题可以直接依据索引回答，无需再读取原文档。

## API 模块范围
文档分为两大核心模块：
- **XtQuant.XtData (行情模块)**: 行号 `36 - 1455`
- **XtQuant.Xttrade (交易模块)**: 行号 `2141 - 4367`
- **完整示例代码**: 行号 `4368 - 6050`

详细的接口与行号对照表请查阅 [./references/api_index.md](./references/api_index.md)。

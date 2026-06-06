# QMT API (XtQuant) 精准检索地图与行号索引

本索引提供了 [./QMT_API_Documentation.md](./QMT_API_Documentation.md) 中所有模块、数据接口、数据结构和示例代码的精准行号。在编写代码或回答问题时，请使用 `Read` 工具通过行号（配合 `offset` 和 `limit` 参数）只提取需要的段落。

---

## 1. 核心模块概览
* **快速开始**: 行号 [18 - 35](./QMT_API_Documentation.md#L18-L35)
* **XtData 行情模块**: 行号 [36 - 2140](./QMT_API_Documentation.md#L36-L2140)
  * **接口概述与运作原理**: 行号 [157 - 248](./QMT_API_Documentation.md#L157-L248)
  - **核心行情数据获取与订阅**: 行号 [249 - 988](./QMT_API_Documentation.md#L249-L988)
  - **财务数据接口**: 行号 [989 - 1109](./QMT_API_Documentation.md#L989-L1109)
  - **基础行情信息（合约/板块/指数成分权）**: 行号 [1110 - 1455](./QMT_API_Documentation.md#L1110-L1455)
  - **附录：行情字段、数据字典、财务报表字典**: 行号 [1456 - 2140](./QMT_API_Documentation.md#L1456-L2140)
* **Xttrade 交易模块**: 行号 [2141 - 4367](./QMT_API_Documentation.md#L2141-L4367)
  - **快速入门（简单策略）**: 行号 [2280 - 2423](./QMT_API_Documentation.md#L2280-L2423)
  - **进阶：交易运行逻辑与字典**: 行号 [2424 - 2635](./QMT_API_Documentation.md#L2424-L2635)
  - **交易数据结构定义（持仓类等）**: 行号 [2636 - 2925](./QMT_API_Documentation.md#L2636-L2925)
  - **系统设置与状态连接接口**: 行号 [2926 - 3142](./QMT_API_Documentation.md#L2926-L3142)
  - **操作接口（买、卖、撤单、资金划拨）**: 行号 [3143 - 3461](./QMT_API_Documentation.md#L3143-L3461)
  - **查询接口（资产、持仓、委托、成交查询）**: 行号 [3462 - 4213](./QMT_API_Documentation.md#L3462-L4213)
  - **交易回调类**: 行号 [4214 - 4367](./QMT_API_Documentation.md#L4214-L4367)
* **完整实例代码**: 行号 [4368 - 6050](./QMT_API_Documentation.md#L4368-L6050)
  - **行情订阅与实时刷新示例**: 行号 [4370 - 4899](./QMT_API_Documentation.md#L4370-L4899)
  - **交易实盘（单股/全推/下单撤单）示例**: 行号 [4900 - 6050](./QMT_API_Documentation.md#L4900-L6050)

---

## 2. 核心接口快速索引

### 2.1 行情订阅与获取模块 (XtData)
* **订阅单股行情**: `subscribe_quote` -> [./QMT_API_Documentation.md:253 - 296](./QMT_API_Documentation.md#L253-L296)
* **订阅全推行情**: `subscribe_whole_quote` -> [./QMT_API_Documentation.md:297 - 334](./QMT_API_Documentation.md#L297-L334)
* **反订阅行情数据**: `unsubscribe_quote` -> [./QMT_API_Documentation.md:335 - 353](./QMT_API_Documentation.md#L335-L353)
* **阻塞线程接收行情**: `run` -> [./QMT_API_Documentation.md:354 - 372](./QMT_API_Documentation.md#L354-L372)
* **获取行情数据**: `get_market_data_ex` / `get_market_data` -> [./QMT_API_Documentation.md:571 - 644](./QMT_API_Documentation.md#L571-L644)
* **获取除权因子**: `get_divid_factors` -> [./QMT_API_Documentation.md:666 - 686](./QMT_API_Documentation.md#L666-L686)
* **下载历史行情**: `download_history_data` -> [./QMT_API_Documentation.md:687 - 756](./QMT_API_Documentation.md#L687-L756)
* **获取节假日/交易日历**: `get_holidays` / `get_trading_calendar` -> [./QMT_API_Documentation.md:778 - 817](./QMT_API_Documentation.md#L778-L817)

### 2.2 合约与板块查询模块 (XtData)
* **获取合约基础信息**: `get_instrument_detail` -> [./QMT_API_Documentation.md:1112 - 1183](./QMT_API_Documentation.md#L1112-L1183)
* **获取板块成分股**: `get_stock_list_in_sector` -> [./QMT_API_Documentation.md:1259 - 1277](./QMT_API_Documentation.md#L1259-L1277)
* **管理自定义板块**: `add_sector` / `remove_sector` -> [./QMT_API_Documentation.md:1318 - 1417](./QMT_API_Documentation.md#L1318-L1417)

### 2.3 交易设置与连接 (Xttrade)
* **创建API实例**: `XtQuantTrader` -> [./QMT_API_Documentation.md:2930 - 2961](./QMT_API_Documentation.md#L2930-L2961)
* **连接交易服务**: `connect` -> [./QMT_API_Documentation.md:3022 - 3050](./QMT_API_Documentation.md#L3022-L3050)
* **注册回调类**: `register_callback` -> [./QMT_API_Documentation.md:2962 - 2993](./QMT_API_Documentation.md#L2962-L2993)
* **初始化API环境**: `prepare` -> [./QMT_API_Documentation.md:2994 - 3021](./QMT_API_Documentation.md#L2994-L3021)
* **连接/断开与主循环线程**: `start` / `stop` -> [./QMT_API_Documentation.md:3051 - 3142](./QMT_API_Documentation.md#L3051-L3142)

### 2.4 下单与撤单模块 (Xttrade)
* **同步委托下单**: `order_stock` -> [./QMT_API_Documentation.md:3203 - 3238](./QMT_API_Documentation.md#L3203-L3238)
* **异步委托下单**: `order_stock_async` -> [./QMT_API_Documentation.md:3239 - 3274](./QMT_API_Documentation.md#L3239-L3274)
* **同步撤销订单**: `cancel_order_stock` -> [./QMT_API_Documentation.md:3275 - 3338](./QMT_API_Documentation.md#L3275-L3338)
* **异步撤销订单**: `cancel_order_stock_async` -> [./QMT_API_Documentation.md:3339 - 3402](./QMT_API_Documentation.md#L3339-L3402)

### 2.5 账户与资产查询 (Xttrade)
* **查询资产**: `query_stock_asset` -> [./QMT_API_Documentation.md:3464 - 3492](./QMT_API_Documentation.md#L3464-L3492)
* **查询委托**: `query_stock_orders` -> [./QMT_API_Documentation.md:3493 - 3522](./QMT_API_Documentation.md#L3493-L3522)
* **查询成交**: `query_stock_trades` -> [./QMT_API_Documentation.md:3523 - 3551](./QMT_API_Documentation.md#L3523-L3551)
* **查询持仓**: `query_stock_positions` -> [./QMT_API_Documentation.md:3552 - 3580](./QMT_API_Documentation.md#L3552-L3580)

---

## 3. 核心数据结构与字典索引

### 3.1 核心状态字典 (数据值定义)
* **账号类型 (account_type)**: [./QMT_API_Documentation.md:2448 - 2457](./QMT_API_Documentation.md#L2448-L2457)
* **报价类型 (price_type)**: [./QMT_API_Documentation.md:2542 - 2575](./QMT_API_Documentation.md#L2542-L2575)
* **委托状态 (order_status)**: [./QMT_API_Documentation.md:2576 - 2591](./QMT_API_Documentation.md#L2576-L2591)
* **多空/交易方向**: [./QMT_API_Documentation.md:2617 - 2635](./QMT_API_Documentation.md#L2617-L2635)

### 3.2 常用属性字段说明
* **资金资产 (XtAsset)**: 包含 `cash`, `frozen_cash`, `total_asset` 等 -> [./QMT_API_Documentation.md:2638 - 2648](./QMT_API_Documentation.md#L2638-L2648)
* **委托详情 (XtOrder)**: 包含 `order_id`, `stock_code`, `order_status`, `price`, `volume` 等 -> [./QMT_API_Documentation.md:2649 - 2671](./QMT_API_Documentation.md#L2649-L2671)
* **持仓详情 (XtPosition)**: 包含 `stock_code`, `volume`, `can_use_volume`, `open_price`, `market_value` 等 -> [./QMT_API_Documentation.md:2692 - 2708](./QMT_API_Documentation.md#L2692-L2708)

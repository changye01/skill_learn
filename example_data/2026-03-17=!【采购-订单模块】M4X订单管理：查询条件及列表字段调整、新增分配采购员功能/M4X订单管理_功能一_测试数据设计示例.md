# M4X订单管理 功能一 测试数据设计示例

> 主输入：需求对应测试用例（示例编号为功能一代表性用例）
>
> reference-pack：`reference-packs/tables/*.sql` + `reference-packs/table_samples/*.csv`
>
> 补充参考：当前需求文档中的接口返回字段说明、状态映射说明、历史修复 SQL

## 输入材料

- 测试用例：`功能一：列表新增查询条件、列表新增字段` 的代表性用例
- reference-pack：`reference-packs/`
- 技术方案/接口说明：当前需求文档中 `purchase_site_id`、`order_status`、`product_source_tag/product_source_type`、历史修复 SQL 说明

## 测试数据设计

| 编号 | 测试用例编号 | 数据目标 | 涉及表 | 关键字段 | 建议取值/样例来源 | 数据操作 | 关联关系 | 备注/待确认项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TD-001 | TC-F1-001 | 验证列表按账号 `purchase_site_id` 过滤时，可返回命中账号的订单任务 | `supplier_order_m4x_task`, `orders` | `trade_order_code`, `purchase_site_id`, `orders_code`, `site_id` | 参考 `table_samples/supplier_order_m4x_task.csv` 中 `ORDER_001/SITE_001`，并与 `orders.csv` 中相同订单号建立对应关系 | 预置 | `supplier_order_m4x_task.trade_order_code = orders.orders_code`，且 `supplier_order_m4x_task.purchase_site_id` 应与 `orders.site_id` 对齐 | 若现有样例中同订单号未直接成对出现，可补造一组同账号关联数据 |
| TD-002 | TC-F1-002 | 验证列表按订单状态 `DCD` 查询时，仅返回目标状态订单 | `supplier_order_m4x_task`, `orders` | `trade_order_code`, `orders_status`, `purchase_site_id` | 参考 `table_samples/orders.csv` 中 `ORDER_011` 的 `orders_status=DCD`；如无对应任务记录，补造同 `trade_order_code` 的任务数据 | 预置/补造 | `supplier_order_m4x_task.trade_order_code = orders.orders_code` | `order_status` 来自订单表还是接口层映射需按技术方案确认，但当前材料显示查询值取 `orders.orders_status` |
| TD-003 | TC-F1-003 | 验证明细行产品来源类型为 `28` 时，接口返回 `product_source_tag=M4L` | `supplier_order_m4x_task_detail`, `product` | `somt_id`, `product_id`, `product_source_type` | 参考 `table_samples/supplier_order_m4x_task_detail.csv` 中 `PRODUCT_001`，以及 `product.csv` 中 `PRODUCT_001.product_source_type=28` | 预置 | `supplier_order_m4x_task_detail.product_id = product.product_id` | `product_source_tag` 是派生字段，必须参考技术方案中的 `28 -> M4L` 映射 |
| TD-004 | TC-F1-004 | 验证明细行产品来源类型为 `31` 时，接口返回 `product_source_tag=M4X` | `supplier_order_m4x_task_detail`, `product` | `somt_id`, `product_id`, `product_source_type` | 参考 `table_samples/supplier_order_m4x_task_detail.csv` 中 `PRODUCT_002`，以及 `product.csv` 中 `PRODUCT_002.product_source_type=31` | 预置 | `supplier_order_m4x_task_detail.product_id = product.product_id` | `product_source_tag` 是派生字段，必须参考技术方案中的 `31 -> M4X` 映射 |
| TD-005 | TC-F1-005 | 验证历史缺失账号数据经修复后，可回填任务表账号并支持后续查询 | `supplier_order_m4x_task`, `supplier_order_dbs_task`, `orders` | `purchase_site_id`, `trade_order_code`, `orders_code`, `site_id` | 参考 `supplier_order_m4x_task.csv` 与 `orders.csv` 的账号字段；补造一组 `purchase_site_id` 为空、`orders.site_id` 非空的历史任务数据 | 缺失态/修复后态 | `supplier_order_m4x_task.trade_order_code = orders.orders_code`；`supplier_order_dbs_task.trade_order_code = orders.orders_code` | 修复动作本身不在本 skill 执行范围内，此处只设计“修复前空值”和“修复后回填”的验证数据 |

## 待确认项

- `purchase/api/m4x-order/list` 的 `order_status` 查询是否直接使用 `orders.orders_status` 原值，还是存在额外接口层转换。
- `product_source_tag` 仅定义了 `28 -> M4L`、`31 -> M4X`；其他来源类型是否需要返回空字符串，需按技术方案确认。
- 若要验证“账号列表接口去重”，建议补充一组相同 `purchase_site_id` 的多任务样例数据。

## 补充说明

- 当前示例只覆盖功能一的代表性数据设计，不覆盖功能二、功能三。
- 能直接复用的样例主要来自 `supplier_order_m4x_task_detail.csv` 与 `product.csv` 的产品来源类型样例。
- 账号查询、状态查询、历史修复更依赖跨表配对关系，若现有样例不成对，应按当前结构补造最小闭环样例。

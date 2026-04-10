# M4X 功能一 Reference Pack

该实例包仅覆盖当前需求中的“功能一：列表新增查询条件、列表新增字段”。

## 保留内容

- `tables/*.sql`：单表 DDL
- `table_samples/*.csv`：保留全字段的样例数据

## 使用方式

- 这份 pack 只提供表结构和样例数据。
- 业务关系、接口规则、修复逻辑请结合需求文档和技术文档使用。
- 后续如需补充新的表，直接在 `tables/` 下增加对应 `CREATE TABLE` 文件，并在 `table_samples/` 下补同名样例数据。

## 当前样例表

- `supplier_order_m4x_task`
- `supplier_order_m4x_task_detail`
- `orders`
- `product`
- `supplier_order_dbs_task`

## 脱敏说明

- 当前样例并不是“整表完全脱敏”，而是对部分标识类字段做稳定映射处理。
- `trade_order_code/orders_code` 已做稳定映射脱敏。
- `purchase_site_id/site_id` 已做稳定映射脱敏。
- `somt_id/product_id/so_id/so_code/job_number` 已做稳定映射脱敏。
- `seller_job_number` 如涉及人员标识，也应按同类规则理解和处理。
- 其余字段可能仍保留业务样例信息，使用或外传时需遵守内部数据规范。

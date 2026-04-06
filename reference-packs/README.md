# M4X 功能一 Reference Pack

该实例包仅覆盖当前需求中的“功能一：列表新增查询条件、列表新增字段”。

## 保留内容

- `tables/*.sql`：单表 DDL
- `table_samples/*.csv`：脱敏后的全字段样例数据

## 使用方式

- 这份 pack 只提供表结构和样例数据。
- 业务关系、接口规则、修复逻辑请结合需求文档和技术文档使用。
- 后续如需补充新的表，直接在 `tables/` 下增加对应 `CREATE TABLE` 文件，并在 `table_samples/` 下补对应样例数据。

## 当前样例表

- `supplier_order_m4x_task`
- `supplier_order_m4x_task_detail`
- `orders`
- `product`
- `supplier_order_dbs_task`

## 脱敏说明

- `trade_order_code/orders_code` 已做稳定映射脱敏。
- `purchase_site_id/site_id` 已做稳定映射脱敏。
- `somt_id/product_id/so_id/so_code/job_number` 已做稳定映射脱敏。
- 样例数据保留全字段，便于后续直接参考。

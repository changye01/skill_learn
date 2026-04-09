# M4X订单管理 测试执行清单

> 基线稿：`M4X订单管理_结构化测试用例.md`

## 输入材料

- 结构化测试用例：`M4X订单管理_结构化测试用例.md`
- reference-pack：`reference-packs/`
- 技术方案/接口说明：`docs/m4x-order-tech.md`

## TC-001 账号精确查询命中订单

### 前置条件

- 测试账号已具备订单管理查询权限
- 系统中存在账号为 `acct_001`、订单号为 `PO20260317001` 的订单数据

### 测试步骤

1. 进入订单管理列表页
2. 在账号查询框输入 `acct_001`
3. 点击查询

### 预期结果

- 列表命中订单 `PO20260317001`
- 列表中的账号字段展示为 `acct_001`

### 输入数据

#### 表：`supplier_order_m4x_task`


| trade_order_code | purchase_site_id | buyer_user_id  |
| ---------------- | ---------------- | -------------- |
| PO20260317001    | acct_001         | buyer_zhangsan |


#### 表：`orders`


| orders_code   | site_id  | orders_status | assign_buyer_id |
| ------------- | -------- | ------------- | --------------- |
| PO20260317001 | acct_001 | OP            | buyer_zhangsan  |


### 说明

- `supplier_order_m4x_task.trade_order_code = orders.orders_code`
- 本用例重点验证账号查询条件与列表命中关系

### 待确认项

- 无

## TC-002 分配采购员后列表展示最新采购员

### 前置条件

- 测试账号具备“分配采购员”操作权限
- 订单 `PO20260317002` 当前未分配采购员

### 测试步骤

1. 进入订单管理列表页
2. 选中订单 `PO20260317002`
3. 点击“分配采购员”
4. 选择 `buyer_lisi` 并提交
5. 返回列表页查看采购员列

### 预期结果

- 分配成功
- 列表采购员字段展示为 `buyer_lisi`
- 日志中记录本次分配操作

### 输入数据

#### 表：`orders`


| orders_code   | site_id  | orders_status | assign_buyer_id |
| ------------- | -------- | ------------- | --------------- |
| PO20260317002 | acct_002 | OP            | buyer_lisi      |


#### 表：`supplier_order_m4x_log`


| trade_order_code | log_type     | operator_id |
| ---------------- | ------------ | ----------- |
| PO20260317002    | ASSIGN_BUYER | buyer_lisi  |


### 说明

- 本用例需要关注操作后主表与日志表是否同步
- 若页面展示采购员中文名，则需结合技术方案确认映射关系

### 待确认项

- 采购员列展示的是账号还是姓名，需以技术方案为准


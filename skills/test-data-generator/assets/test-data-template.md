# {{REQUIREMENT_NAME}} 测试数据设计

> 主输入：已确认测试用例 + `reference-pack`
>
> 补充输入：技术方案、接口说明、状态映射说明、历史修复 SQL（如有）
>
> 若存在派生字段、状态映射、历史修复、跨系统同步等规则而材料不足，应先提示“建议补充技术方案作为参考”，并将无法确认内容保留在 `备注/待确认项`。

## 输入材料

- 测试用例：`{{TEST_CASE_PATH}}`
- reference-pack：`{{REFERENCE_PACK_PATH}}`
- 技术方案/接口说明：`{{TECH_DOC_PATH_OR_NONE}}`

## 测试数据设计

| 编号 | 测试用例编号 | 数据目标 | 涉及表 | 关键字段 | 建议取值/样例来源 | 数据操作 | 关联关系 | 备注/待确认项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {{DATA_ID}} | {{CASE_ID}} | {{DATA_GOAL}} | {{TABLES}} | {{KEY_FIELDS}} | {{VALUE_SOURCE}} | {{DATA_ACTION}} | {{RELATIONSHIP}} | {{NOTES}} |

## 待确认项

- 待确认项 1：

## 补充说明

- 哪些数据可以直接复用 `table_samples/*.csv`
- 哪些数据需要补造、变造或保留缺失态
- 哪些规则来自技术方案，哪些来自样例推断

# {{REQUIREMENT_NAME}} 测试数据清单

> 主输入：已确认测试用例 + `reference-pack`
>
> 补充输入：技术方案、接口说明、状态映射说明、历史修复 SQL（如有）
>
> 若存在派生字段、状态映射、历史修复、跨系统同步等规则而材料不足，应先提示“建议补充技术方案作为参考”，并将无法确认内容保留在 `待确认项`。确认版 Markdown 通过校验后，如有需要，再派生 `测试数据清单.csv`。

## 输入材料

- 测试用例：`{{TEST_CASE_PATH}}`
- reference-pack：`{{REFERENCE_PACK_PATH}}`
- 技术方案/接口说明：`{{TECH_DOC_PATH_OR_NONE}}`

## 一、基础记录池

### {{POOL_ID}} {{POOL_NAME}}

#### 表：`{{TABLE_NAME}}`

| {{FIELD_1}} | {{FIELD_2}} | {{FIELD_3}} |
| --- | --- | --- |
| {{VALUE_1}} | {{VALUE_2}} | {{VALUE_3}} |

### {{POOL_ID_2}} {{POOL_NAME_2}}

#### 角色池 / 修复前 / 修复后 / 修改后预期（按需选一种）

| {{COLUMN_1}} | {{COLUMN_2}} |
| --- | --- |
| {{VALUE_1}} | {{VALUE_2}} |

## 二、测试用例清单

## {{CASE_ID}} {{CASE_TITLE}}

### 引用基础记录

- `{{POOL_ID}}` 中 `{{RECORD_KEY}}`
- `{{POOL_ID_2}}` 中 `{{RECORD_KEY_2}}`

### 补充说明（如无可删除）

| 项目 | 值 |
| --- | --- |
| {{ITEM_NAME}} | {{ITEM_VALUE}} |

### 验证点

- {{ASSERTION_1}}
- {{ASSERTION_2}}

## 三、待确认项

- 待确认项 1：
- 待确认项 2：

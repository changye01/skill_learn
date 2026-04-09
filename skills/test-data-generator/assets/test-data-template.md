# {{REQUIREMENT_NAME}} 测试执行清单

> 基线稿：已确认的 `结构化测试用例.md`
>
> 主输入：`结构化测试用例.md` + `reference-pack`（通常位于 `reference-packs/...`）
>
> 核心输入：技术方案
>
> 补充输入：接口说明、状态映射说明、历史修复 SQL（如有）
>
> 若存在派生字段、状态映射、历史修复、跨系统同步、权限或日志规则而缺少技术方案，应先提示“缺少技术方案，当前只能输出低置信度草稿”，并将无法确认内容保留在对应 `TC` 的 `待确认项`。候选版 Markdown 通过校验后，才可视为确认版。

## 输入材料

- 结构化测试用例：`{{TEST_CASE_PATH}}`
- reference-pack：`{{REFERENCE_PACK_PATH}}`
- 技术方案/接口说明：`{{TECH_DOC_PATH_OR_NONE}}`

## {{CASE_ID}} {{CASE_TITLE}}

> `CASE_ID` 必须使用 `TC-xxx` 格式，例如 `TC-001`

### 前置条件

- {{PRECONDITION_1}}
- {{PRECONDITION_2}}

### 测试步骤

1. {{STEP_1}}
2. {{STEP_2}}
3. {{STEP_3}}

### 预期结果

- {{EXPECTED_RESULT_1}}
- {{EXPECTED_RESULT_2}}

### 输入数据

#### 表：`{{TABLE_NAME_1}}`


| {{FIELD_1}} | {{FIELD_2}} | {{FIELD_3}} |
| ----------- | ----------- | ----------- |
| {{VALUE_1}} | {{VALUE_2}} | {{VALUE_3}} |


#### 表：`{{TABLE_NAME_2}}`


| {{COLUMN_1}} | {{COLUMN_2}} | {{COLUMN_3}} |
| ------------ | ------------ | ------------ |
| {{DATA_1}}   | {{DATA_2}}   | {{DATA_3}}   |


### 说明

- {{NOTE_1}}
- {{NOTE_2}}

### 待确认项

- {{TODO_1_OR_无}}
- {{TODO_2_OR_可删除}}

## {{CASE_ID_2}} {{CASE_TITLE_2}}

> `CASE_ID_2` 必须使用 `TC-xxx` 格式，例如 `TC-002`

### 前置条件

- {{PRECONDITION_A}}

### 测试步骤

1. {{STEP_A1}}
2. {{STEP_A2}}

### 预期结果

- {{EXPECTED_A1}}

### 输入数据

#### 表：`{{TABLE_NAME_3}}`


| {{FIELD_A1}} | {{FIELD_A2}} |
| ------------ | ------------ |
| {{VALUE_A1}} | {{VALUE_A2}} |


### 说明

- {{NOTE_A1}}

### 待确认项

- 无
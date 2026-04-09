# {{REQUIREMENT_NAME}} 结构化测试用例

> 配套输出：除本 Markdown 文件外，还应同步生成一个 UTF-8 编码、中文列名的 `CSV` 文件，字段与本模板保持一致，推荐命名为 `<需求名称>_表格版用例.csv`。
>
> Markdown 默认按第一阶段场景地图中的“场景分组”组织；每个场景组下使用 5 列表格承载测试用例。CSV 保持平铺结构，但编号顺序应与 Markdown 按分组展开后的顺序一致。
>
> 用户确认第二阶段结果后，必须先保存本 Markdown 与配套 CSV，再运行校验；未保存或校验未通过前，不得直接切换到下游 `test-data-generator`。

## 场景组1：{{SCENE_GROUP_1}}

| 编号 | 测试功能点 | 前置条件 | 测试步骤 | 预期结果 |
| --- | --- | --- | --- | --- |
| {{CASE_ID_1}} | {{TEST_POINT_1}} | {{PRECONDITION_1}} | {{STEPS_1}} | {{EXPECTED_RESULT_1}} |
| {{CASE_ID_2}} | {{TEST_POINT_2}} | {{PRECONDITION_2}} | {{STEPS_2}} | {{EXPECTED_RESULT_2}} |

## 场景组2：{{SCENE_GROUP_2}}

| 编号 | 测试功能点 | 前置条件 | 测试步骤 | 预期结果 |
| --- | --- | --- | --- | --- |
| {{CASE_ID_3}} | {{TEST_POINT_3}} | {{PRECONDITION_3}} | {{STEPS_3}} | {{EXPECTED_RESULT_3}} |

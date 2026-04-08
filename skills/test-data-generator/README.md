# 测试数据设计 Skill

一个与 `test-case-generator` 串联使用的 Skill，用于把“已确认测试用例”进一步转成“可执行前的数据准备清单”，并在需要时派生一份给测试人员直接使用的 `CSV` 清单。

## 目标

把“测试用例 -> 测试数据准备”的过程单独拆出来，明确回答：

1. 为了执行这些用例，需要准备哪些数据。
2. 哪些数据可以复用，哪些需要单独补造、变造或保留缺失态。
3. 哪些规则可以确定，哪些仍需技术方案补充确认。

默认目标是 `数据清单清晰可执行 + 测试人员可直接拿来验证用例`，而不是直接产出可执行 SQL。

## 适用范围

适用于以下场景：

- 根据已确认测试用例设计测试数据
- 结合数据库表结构和样例数据补齐执行前置
- 为复杂筛选、状态映射、派生字段、多表关联设计数据准备方案
- 在测试执行前先产出人可读、可评审的 Markdown 测试数据清单
- 给测试人员产出可直接阅读和执行的 CSV 数据清单

默认不包含以下内容，除非用户明确要求：

- 自动执行插数或清数
- 自动连真实数据库造数据
- 通用 SQL/JSON/fixture 批量生成
- 多数据库方言适配

## 设计原则

- 先看测试用例，再设计数据
- 以 `reference-pack` 为结构依据，以技术方案为补充参考
- 正式输出优先是 `测试数据清单.md`，不是工程化 fixture
- 优先抽取“基础记录池”，再让各测试用例引用或补充增量
- 能确认的写清楚，不能确认的沉淀为 `待确认项`
- 覆盖正常、边界、异常、缺失、历史修复、多表关联和派生字段
- 禁止把技术规则“脑补”成确定性结论
- 覆盖完整不等于堆大量重复记录

## 建议输入

### 主输入

1. 已确认测试用例
2. `reference-pack`：
   - `reference-packs/tables/*.sql`
   - `reference-packs/table_samples/*.csv`

### 补充输入

- 技术方案
- 接口说明
- 状态/枚举映射说明
- 历史修复 SQL 或迁移说明

### 输入优先级

1. 测试用例：决定要准备哪些数据
2. `reference-pack`：决定字段、结构、样例形态
3. 技术方案：补充派生规则、状态映射、修复逻辑、跨系统链路

## 工作流程

1. 确认测试用例和 `reference-pack` 路径。
2. 判断是否存在派生字段、状态映射、历史修复、跨系统链路等复杂规则。
3. 若有复杂规则但缺少技术方案，先提示补充参考材料。
4. 以测试用例为主拆出数据需求地图。
5. 读取 `tables/*.sql` 和 `table_samples/*.csv`，先沉淀公共的“基础记录池”。
6. 输出 Markdown `测试数据清单` 草稿。
7. 根据覆盖清单补漏，并保留 `待确认项`。
8. 用户确认后保存正式 Markdown 文件。
9. 运行校验脚本做 Markdown 结构校验。
10. 如需要，再从确认版 Markdown 派生 `测试数据清单.csv`。
11. 再运行一次校验，确认 Markdown 与 CSV 清单一致。

## 推荐输出结构

推荐优先输出 `Markdown`，结构如下：

1. `基础记录池`
2. `测试用例清单`
3. `待确认项`

其中每条测试用例建议固定包含：

- `引用基础记录`
- 必要的补充说明或覆盖字段
- `验证点`

推荐文件名：

- `<需求名称>_测试数据清单.md`

如果 Markdown 确认并通过校验后，用户仍需要 CSV，再输出：

- `<需求名称>_测试数据清单.csv`

CSV 推荐列：

- 测试用例编号
- 测试功能点
- 数据目标
- 涉及表
- 关键字段
- 建议数据值
- 样例来源
- 数据准备方式
- 验证方式
- 备注/待确认项

## 目录结构

```text
test-data-generator/
├── SKILL.md
├── README.md
├── references/
│   ├── data-design-rules.md
│   ├── data-coverage-checklist.md
│   └── csv-checklist-spec.md
├── assets/
│   ├── test-data-template.md
│   └── test-data-checklist-template.csv
└── scripts/
    ├── validate_test_data.py
    └── test_validate_test_data.py
```

## 规则来源

- 测试数据设计规则：`references/data-design-rules.md`
- 覆盖检查清单：`references/data-coverage-checklist.md`
- Markdown 输出模板：`assets/test-data-template.md`
- CSV 清单模板：`assets/test-data-checklist-template.csv`
- CSV 清单规范：`references/csv-checklist-spec.md`
- 输出校验脚本：`scripts/validate_test_data.py`

## 搭配方式

推荐串联方式：

1. 先用 `test-case-generator` 生成并确认测试用例
2. 再用 `test-data-generator` 基于测试用例 + `reference-pack` 生成 `测试数据清单.md`
3. 确认并校验 Markdown 清单稿
4. 如果测试执行需要表格清单，再派生 `测试数据清单.csv`
5. 如果需求存在派生字段、状态映射、历史修复等隐含规则，再补充技术方案作为参考

## 技术方案补充建议

出现以下信号时，建议补充技术方案或接口说明：

- 接口返回字段不是数据库原字段
- 需要按状态码映射展示文案或标签
- 字段需要经业务规则转换后才可判断
- 存在历史修复逻辑、迁移逻辑或兼容逻辑
- 涉及跨系统同步、异步任务或多系统落库

## 验证方式

对生成后的 Markdown 文档运行：

```bash
python scripts/validate_test_data.py <Markdown文件路径> [测试数据清单CSV路径]
```

脚本会检查：

- 旧版表格稿：是否包含关键字段/栏目，是否至少包含一条数据设计记录
- 新版清单稿：是否包含 `基础记录池`、`测试用例清单`、`引用基础记录`、`验证点`、`待确认项`
- 新版清单稿：是否至少包含一条 `TC-xxx`
- 如果传入 CSV，还会检查 CSV 列头是否符合规范
- 如果传入 CSV，还会检查测试用例编号集合和顺序是否与 Markdown 一致

当前仍然只做轻量结构校验，不做重型语义判断，也不校验业务规则真伪或字段值是否一定能直接落库。内容层面的补漏仍建议结合 `references/data-coverage-checklist.md` 和人工评审完成。

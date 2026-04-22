# Test Case Generator Skill

用于把需求文档拆成两阶段产物：

1. `测试场景地图`：先确认“测什么”
2. `结构化测试用例`：再展开“怎么测”

如果后续还要补齐执行数据、表记录和备注，应继续串联 `test-data-generator`。

## 适用范围

适合：

- 根据需求文档生成功能测试用例
- 结合技术文档、接口文档、原型补齐覆盖
- 先评审场景，再落结构化用例

默认不包含以下内容，除非用户明确要求：

- 性能测试
- 兼容性测试
- 安全测试
- 测试数据生成

## 输出

### 第一阶段：`测试场景地图`

用于沉淀场景分组、补充维度、待确认项和超范围项，推荐文件名：

- `<需求名称>_测试场景地图.md`

### 第二阶段：`结构化测试用例`

默认按场景组分段，每组使用 5 列 Markdown 表格：

- `编号`
- `测试功能点`
- `前置条件`
- `测试步骤`
- `预期结果`

推荐文件名：

- `<需求名称>_结构化测试用例.md`

## 使用建议

- 先确认完整场景地图，再生成第二阶段用例
- 用户已确认的规则，建议单独沉淀为 `本次确认规则`
- 第二阶段确认后应立即保存，不要只停留在对话里
- 正式保存时应覆盖旧版本，不要把历史草稿追加到确认版

推荐输入优先级：

1. `Markdown (.md)`
2. `UTF-8 纯文本 (.txt)`
3. `Word (.docx)`，建议先转 `Markdown`
4. `PDF`

## 目录结构

```text
test-case-generator/
├── SKILL.md
├── README.md
├── references/
│   ├── test-design-rules.md
│   ├── coverage-checklist.md
│   └── quality-rubric.md
├── assets/
│   ├── scene-template.md
│   ├── test-case-template.md
│   └── test-case-example.md
└── scripts/
    ├── validate_cases.py
    └── test_validate_cases.py
```

## 参考文件

- 模板：`assets/scene-template.md`
- 模板：`assets/test-case-template.md`
- 示例：`assets/test-case-example.md`
- 规则：`references/test-design-rules.md`
- 覆盖清单：`references/coverage-checklist.md`
- 质量评审：`references/quality-rubric.md`
- 校验脚本：`scripts/validate_cases.py`
- 校验脚本测试：`scripts/test_validate_cases.py`

## 验证方式

从仓库根目录运行：

```bash
python skills/test-case-generator/scripts/validate_cases.py <测试用例文件路径>
```

如果你已经在当前目录 `skills/test-case-generator/` 下，也可以运行：

```bash
python scripts/validate_cases.py <测试用例文件路径>
```

脚本会检查：

- 是否包含关键字段
- 是否存在综合场景或端到端场景

其中“综合场景”或“端到端”需要出现在已解析表格数据行的 `测试功能点` 列中。

结构校验通过后，建议再参考 `references/quality-rubric.md` 做一轮轻量内容评审。

## 下一步

如果目标变成“这些用例执行时需要准备哪些数据”，建议在确认 `结构化测试用例` 后，补齐技术方案和 `reference-pack`，再继续使用 `test-data-generator`。
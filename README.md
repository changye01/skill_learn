# Skill Learn

实用 Claude Code Skills 集合，以单个 `skill-learn` 插件提供多个 Claude Skills，目前包含测试用例生成与测试执行数据补齐两个 Skill。

## 插件安装与管理

### Claude Code Plugin Marketplace（推荐）

安装插件

```bash
claude plugins marketplace add "changye01/skill_learn"
claude plugins install "skill-learn"
```

更新插件：

```bash
claude plugins marketplace update "skill-learn"
claude plugins install "skill-learn"
```

卸载插件：

```bash
claude plugins uninstall "skill-learn" --scope user
```

如需同时移除 marketplace：

```bash
claude plugins marketplace remove "skill-learn"
```

安装完成后，Claude 会在同一个 `skill-learn` 插件下按需触发以下两个 Skills。

## 当前包含的 Skills

### `test-case-generator`

测试用例生成工具，基于需求文档先生成场景地图，再生成结构化测试用例。

**触发方式：** 说“生成测试用例”、“测试场景梳理”、“需求转测试用例”等

**功能：**

- 先生成 Markdown 场景地图，明确“测什么”
- 在确认场景地图后生成结构化测试用例，明确“怎么测”
- 默认以“覆盖全面”为目标，同时控制重复和机械膨胀
- 内置验证脚本检查结构化测试用例文档完整性

### `test-data-generator`

测试数据设计工具，基于已确认测试用例与 `reference-pack` 生成 `测试执行清单.md`，并校验 Markdown 结构完整性。

**触发方式：** 说“生成测试执行清单”、“补齐测试前置数据”、“根据测试用例设计测试数据”等

**功能：**

- 保留 `结构化测试用例.md` 作为基线稿，再按 `TC` 补齐执行信息与测试数据
- 输出 `测试执行清单.md` 草稿，按表分块展示测试数据并保留待确认项
- 内置验证脚本检查 Markdown 结构完整性

## 使用示例

### `test-case-generator`

- “请根据这个需求文档生成测试场景地图”
- “把这份需求拆成结构化测试用例”
- “补齐这批测试用例的边界和异常场景”

### `test-data-generator`

- “根据已确认测试用例生成测试执行清单”
- “基于 reference-pack 设计测试前置数据”
- “输出测试执行清单并校验 Markdown 结构是否完整”

### 真实示例

下面是一条真实会话里“先生成测试用例，再继续生成测试数据”的最小链路示例：
```text
在claude中执行 /Users/changye/changye_workspace/changye/skill_learn/example_data/2026-03-17=!【采购-订单模块】M4X订单管理：查询条件及列表字段调整、新增分配采购员功能/2026-03-17=!【采购-订单模块】M4X订单管理：查询条件及列表字段调整、新增分配采购员功能.md 生成测试用例
```
然后基于已确认的结构化测试用例，继续让 Claude 生成测试执行清单：

```text
根据 `M4X订单管理_结构化测试用例.md` 和 `reference-packs/` 生成测试执行清单
```

在这次会话里，完整产出流程是：

1. `test-case-generator` 先读取需求文档，拆出查询条件、列表字段、分配采购员、历史数据修复、日志调整等测试对象
2. 先生成 `M4X订单管理_测试场景地图.md` 草稿，并把“账号精确匹配”“订单状态枚举值”“采购员范围”“是否允许清空”等问题收敛到 `本次确认规则`
3. 用户补充并确认规则后，再正式落地结构化测试用例和 CSV
4. 随后 `test-data-generator` 基于 `M4X订单管理_结构化测试用例.md` 和 `reference-packs/` 继续补齐每条 `TC` 的测试数据、说明和待确认项，输出 `测试执行清单.md`

最终在需求文档同目录产出了 4 个文件：

- `M4X订单管理_测试场景地图.md`
- `M4X订单管理_结构化测试用例.md`
- `M4X订单管理_表格版用例.csv`
- `M4X订单管理_测试执行清单.md`

---

## 项目结构

```text
skill_learn/
├── .claude-plugin/              # Claude Code marketplace 与 plugin 配置
├── skills/
│   ├── test-case-generator/     # 测试用例生成 Skill
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   ├── references/
│   │   └── assets/
│   └── test-data-generator/     # 测试执行清单 Skill
│       ├── SKILL.md
│       ├── scripts/
│       ├── references/
│       └── assets/
├── reference-packs/             # 表结构与样例数据参考包
└── docs/                        # 设计文档和计划
```

## Skill 架构说明

每个 Skill 遵循统一的组件结构：


| 组件                   | 用途      | 加载时机                 |
| -------------------- | ------- | -------------------- |
| SKILL.md frontmatter | 触发条件    | 始终在上下文 (~100 tokens) |
| SKILL.md body        | 工作流程指令  | 触发后加载 (<5k tokens)   |
| scripts/             | 确定性执行任务 | 执行时运行，不读入上下文         |
| references/          | 详细参考资料  | 按需读取                 |
| assets/              | 模板和示例   | 复制/修改使用              |


## 添加新 Skill

1. 在 `skills/` 目录下创建新目录
2. 添加 `SKILL.md` 文件（必需）
3. 根据需要添加 scripts/、references/、assets/
4. 如需修改插件元信息，更新 `/.claude-plugin/plugin.json`
5. 提交并推送

## 许可

MIT
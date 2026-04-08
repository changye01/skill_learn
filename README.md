# Skill Learn

实用 Claude Code Skills 集合，以单个 `skill-learn` 插件提供多个 Claude Skills，目前包含测试用例生成与测试数据设计两个 Skill。

## 安装

### Claude Code Plugin Marketplace（推荐）

在 Claude Code 中运行：

```bash
claude plugins marketplace add "changye01/skill_learn"
claude plugins install "skill-learn"
```

安装完成后，Claude 会在同一个 `skill-learn` 插件下按需触发以下 Skills。

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

测试数据设计工具，基于已确认测试用例与 `reference-pack` 设计测试数据清单，并支持校验 Markdown 与 CSV 一致性。

**触发方式：** 说“生成测试数据清单”、“补齐测试前置数据”、“根据测试用例设计测试数据”等

**功能：**
- 优先收敛可复用基础记录池，减少重复准备
- 输出测试数据清单草稿，区分基础数据、增量数据和待确认项
- 可按需派生测试人员可直接使用的 CSV 清单
- 内置验证脚本检查 Markdown 结构及 Markdown/CSV 一致性

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
│   └── test-data-generator/     # 测试数据设计 Skill
│       ├── SKILL.md
│       ├── scripts/
│       ├── references/
│       └── assets/
├── reference-packs/             # 表结构与样例数据参考包
└── docs/                        # 设计文档和计划
```

## Skill 架构说明

每个 Skill 遵循统一的组件结构：

| 组件 | 用途 | 加载时机 |
|------|------|----------|
| SKILL.md frontmatter | 触发条件 | 始终在上下文 (~100 tokens) |
| SKILL.md body | 工作流程指令 | 触发后加载 (<5k tokens) |
| scripts/ | 确定性执行任务 | 执行时运行，不读入上下文 |
| references/ | 详细参考资料 | 按需读取 |
| assets/ | 模板和示例 | 复制/修改使用 |

## 添加新 Skill

1. 在 `skills/` 目录下创建新目录
2. 添加 `SKILL.md` 文件（必需）
3. 根据需要添加 scripts/、references/、assets/
4. 如需修改插件元信息，更新 `/.claude-plugin/plugin.json`
5. 提交并推送

## 许可

MIT

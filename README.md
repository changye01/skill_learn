# Skill Learn

实用 Claude Code Skills 集合，当前包含一个面向需求文档的测试用例生成 Skill。

## 安装

### 方式 1：Plugin Marketplace（推荐）

在 Claude Code 中运行：

```
/plugin marketplace add changye01/skill_learn
```

安装后启用：

```
/plugin install skill-learn@changye01
```

### 方式 2：npx

```bash
npx skills add changye01/skill_learn -y -g
```

## 当前包含的 Skill

### test-case-generator

测试用例生成工具，基于需求文档先生成场景地图，再生成结构化测试用例。

**触发方式：** 说“生成测试用例”、“测试场景梳理”、“需求转测试用例”等

**功能：**
- 先生成 Markdown 场景地图，明确“测什么”
- 在确认场景地图后生成结构化测试用例，明确“怎么测”
- 默认以“覆盖全面”为目标，同时控制重复和机械膨胀
- 内置验证脚本检查结构化测试用例文档完整性

> 当前仓库只保留 `test-case-generator`。后续会继续增加新的 Skills。

---

## 项目结构

```
skill_learn/
├── .claude-plugin/              # Claude Code plugin 配置
├── .cursor-plugin/              # Cursor plugin 配置
├── skills/
│   └── test-case-generator/     # 测试用例生成 Skill
│       ├── SKILL.md
│       ├── scripts/
│       ├── references/
│       └── assets/
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
4. 在 `.claude-plugin/marketplace.json` 的 plugins 数组中添加条目
5. 提交并推送

## 许可

MIT

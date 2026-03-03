# Skill Learn

实用 Claude Code Skills 集合。

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

## 包含的 Skills

### 1. tech-design-doc

技术设计文档生成工具，通过引导式提问生成完整的 Markdown 格式设计文档。

**触发方式：** 说"写设计文档"、"技术方案"、"TDD"

**功能：**
- 引导式提问，逐步完善设计文档
- 自动生成包含背景、方案设计、接口定义、实现计划的完整文档
- 内置验证脚本检查文档完整性

### 2. code-review-checklist

代码审查清单生成工具，通过通用规则 + 语言专项规则逐项检查代码。

**触发方式：** 说"code review"、"代码审查"、"审查清单"

**功能：**
- 6 项通用审查规则（命名、错误处理、安全性、可读性、DRY、边界情况）
- Python 专项规则（PEP 8、类型提示、异常处理、Pythonic 写法）
- 输出 Markdown 格式审查报告
- 内置验证脚本检查清单完整性

---

## 项目结构

```
skill_learn/
├── .claude-plugin/              # Claude Code plugin 配置
├── .cursor-plugin/              # Cursor plugin 配置
├── skills/
│   ├── tech-design-doc/         # 技术设计文档 Skill
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   ├── references/
│   │   └── assets/
│   └── code-review-checklist/   # 代码审查清单 Skill
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

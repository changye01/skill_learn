# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Claude Code Skills 集合项目，用于创建和管理自定义 Skills。Skills 是扩展 Claude Code 能力的模块，可以定义工作流程、引导式问答和验证逻辑。

## 项目结构

```
skill_learn/
├── .claude-plugin/            # Claude Code marketplace 与 plugin 配置
├── skills/
│   ├── test-case-generator/   # 测试用例生成 Skill
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   ├── references/
│   │   └── assets/
│   └── test-data-generator/   # 测试数据设计 Skill
│       ├── SKILL.md
│       ├── scripts/
│       ├── references/
│       └── assets/
├── reference-packs/           # 表结构与样例数据参考包
├── docs/plans/                # 设计和实现计划文档
└── .venv/                     # Python 虚拟环境 (Python 3.14)
```

## Skill 组件说明

| 组件 | 用途 | 加载时机 |
|------|------|----------|
| SKILL.md frontmatter | 触发条件（name + description）| 始终在上下文 |
| SKILL.md body | 工作流程指令 | 触发后加载 |
| scripts/ | 确定性执行任务 | 执行时，不读入上下文 |
| references/ | 详细参考资料 | 按需读取 |
| assets/ | 输出资源（模板、示例）| 复制/修改使用 |

## 常用命令

```bash
# 激活虚拟环境
source .venv/bin/activate

# 验证结构化测试用例完整性
python skills/test-case-generator/scripts/validate_cases.py <测试用例路径>

# 验证测试执行清单完整性
python skills/test-data-generator/scripts/validate_test_data.py <测试执行清单路径>

# 安装插件
claude plugins marketplace add "changye01/skill_learn"
claude plugins install "skill-learn"
```

## 添加新 Skill

1. 在 `skills/` 目录下创建新目录
2. 添加 `SKILL.md` 文件，包含 YAML frontmatter（name + description）
3. 根据需要添加 scripts/、references/、assets/ 子目录
4. 如需修改插件元信息，更新 `/.claude-plugin/plugin.json`
5. 提交并推送

## 语言偏好

本项目使用中文编写文档和注释。

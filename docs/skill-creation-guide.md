# Claude Code Skill 创建完整指南

本文档记录了从零创建一个完整 Skill 并发布到 GitHub 的全过程，包括每个步骤的原因说明。

---

## 目录

1. [Skill 是什么](#1-skill-是什么)
2. [Skill 的组成部分](#2-skill-的组成部分)
3. [创建 Skill 的完整步骤](#3-创建-skill-的完整步骤)
4. [发布到 GitHub](#4-发布到-github)
5. [创建 Plugin Marketplace](#5-创建-plugin-marketplace)
6. [安装、卸载与更新](#6-安装卸载与更新)
   - [6.1 安装方式汇总](#61-安装方式汇总)
   - [6.2 卸载 Skill](#62-卸载-skill)
   - [6.3 更新 Skill](#63-更新-skill)
   - [6.4 查看已安装的 Skill](#64-查看已安装的-skill)
   - [6.5 安装位置说明](#65-安装位置说明)

---

## 1. Skill 是什么

Skill 是扩展 Claude Code 能力的模块化包，本质上是**预定义的工作流程和专业知识**。

### 为什么需要 Skill？

| 问题 | Skill 如何解决 |
|------|---------------|
| 重复性任务每次都要重新描述 | 一次定义，随时触发 |
| Claude 不了解特定领域知识 | 通过 references/ 注入专业知识 |
| 需要执行确定性操作 | 通过 scripts/ 提供可执行脚本 |
| 输出格式不统一 | 通过 assets/ 提供模板 |

---

## 2. Skill 的组成部分

### 2.1 目录结构

```
skill-name/
├── SKILL.md              # 必需：主文件
├── scripts/              # 可选：可执行脚本
├── references/           # 可选：参考文档
└── assets/               # 可选：模板和示例
```

### 2.2 各组件详解

#### SKILL.md（必需）

Skill 的核心文件，分为两部分：

**Frontmatter（YAML 元数据）**
```yaml
---
name: tech-design-doc
description: 技术设计文档生成工具。用于：(1) 新功能开发前的方案设计 (2) 通过引导式提问生成完整设计文档 (3) 输出 Markdown 格式。当用户说"写设计文档"、"TDD"、"技术方案"时触发。
---
```

| 字段 | 作用 |
|------|------|
| `name` | Skill 名称，用于 `/skill-name` 触发 |
| `description` | **最重要**：决定何时自动触发，需包含功能说明和触发场景 |

**为什么 description 这么重要？**
- Claude 根据 description 判断是否触发 Skill
- 需要包含具体的触发词（如"写设计文档"、"技术方案"）
- 使用编号列举功能点，便于 Claude 理解

**Body（Markdown 内容）**
- 工作流程指令
- 引导问题清单
- 资源引用说明
- 只在 Skill 触发后加载，节省 context

#### scripts/（可选）

存放可执行脚本，用于需要**确定性执行**的任务。

```python
#!/usr/bin/env python3
"""validate_doc.py - 检查文档完整性"""

def validate(filepath):
    # 检查逻辑
    pass
```

**为什么用脚本而不是让 Claude 写代码？**
- 确定性：每次执行结果一致
- 效率：避免重复编写相同代码
- 可测试：脚本可以独立测试
- Token 节省：脚本可执行但不需读入 context

#### references/（可选）

存放参考文档，供 Claude **按需读取**。

```
references/
├── writing-guide.md    # 写作指南
└── checklist.md        # 自检清单
```

**为什么要单独放 references 而不是写在 SKILL.md 里？**
- **渐进式加载**：SKILL.md 保持精简，详细内容按需加载
- **节省 context**：只在需要时读取
- **易于维护**：内容分类清晰

#### assets/（可选）

存放输出资源，如模板、示例、图片等。

```
assets/
├── template.md    # 文档模板
└── example.md     # 完整示例
```

**assets 和 references 的区别？**

| | references/ | assets/ |
|--|-------------|---------|
| 用途 | 给 Claude 读的参考 | 给输出用的素材 |
| 加载时机 | Claude 按需读取理解 | 复制/修改后输出 |
| 示例 | 写作指南、API 文档 | 模板、示例、图片 |

---

## 3. 创建 Skill 的完整步骤

### 步骤 1：创建目录结构

```bash
mkdir -p tech-design-doc/scripts tech-design-doc/references tech-design-doc/assets
cd tech-design-doc
git init
```

**为什么要 git init？**
- Skill 通常作为独立仓库发布
- 便于版本管理和分发
- 支持 Git 方式安装

### 步骤 2：编写 SKILL.md

```markdown
---
name: tech-design-doc
description: 技术设计文档生成工具。用于：(1) 新功能开发前的方案设计...
---

# 技术设计文档生成器

## 工作流程
1. 了解背景
2. 设计方案
3. 定义接口
4. 规划实现
5. 生成文档

## 资源
- 写作指南：见 `references/writing-guide.md`
- 文档模板：使用 `assets/template.md`
```

### 步骤 3：编写 scripts/

```python
#!/usr/bin/env python3
"""validate_doc.py"""
import sys
import re

REQUIRED_SECTIONS = ["背景", "方案设计", "接口定义", "实现计划"]

def validate(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    missing = [s for s in REQUIRED_SECTIONS if s not in content]
    return missing

if __name__ == "__main__":
    missing = validate(sys.argv[1])
    if missing:
        print(f"❌ 缺少章节：{missing}")
        sys.exit(1)
    print("✅ 文档完整")
```

```bash
chmod +x scripts/validate_doc.py  # 添加执行权限
```

### 步骤 4：编写 references/

**writing-guide.md** - 各章节写作要点
**checklist.md** - 自检清单

### 步骤 5：编写 assets/

**template.md** - 空白模板（占位符）
**example.md** - 完整示例（真实案例）

### 步骤 6：提交到 Git

```bash
git add -A
git commit -m "feat: complete skill"
```

---

## 4. 发布到 GitHub

### 4.1 单个 Skill 发布

直接推送到 GitHub：

```bash
git remote add origin git@github.com:username/skill-name.git
git push -u origin main
```

其他人安装：
```bash
npx skills add username/skill-name -y -g
```

### 4.2 Skills 集合发布

如果要一次安装多个 Skills，需要改成集合结构：

```
my-skills/
├── README.md
└── skills/
    ├── skill-1/
    │   └── SKILL.md
    ├── skill-2/
    │   └── SKILL.md
    └── skill-3/
        └── SKILL.md
```

**为什么要这个结构？**
- `npx skills add` 会自动发现 `skills/` 目录下的所有 Skill
- 一个仓库可以包含多个相关的 Skill
- 类似 superpowers 的组织方式

---

## 5. 创建 Plugin Marketplace

要支持 `/plugin marketplace add` 方式安装，需要添加 marketplace 配置。

### 5.1 添加 marketplace.json

```
my-skills/
├── .claude-plugin/
│   └── marketplace.json    # 新增
├── README.md
└── skills/
    └── tech-design-doc/
```

**marketplace.json 内容：**

```json
{
  "name": "my-skills",
  "version": "1.0.0",
  "description": "我的 Skills 集合",
  "owner": {
    "name": "username",
    "email": ""
  },
  "plugins": [
    {
      "name": "tech-design-doc",
      "description": "技术设计文档生成工具",
      "version": "1.0.0",
      "source": "./",
      "category": "development",
      "keywords": ["documentation", "design"],
      "skills": [
        "./skills/tech-design-doc"
      ]
    }
  ]
}
```

### 5.2 字段说明

| 字段 | 说明 |
|------|------|
| `name` | Marketplace 名称 |
| `plugins` | Plugin 列表 |
| `plugins[].name` | Plugin 名称，用于 `/plugin install xxx` |
| `plugins[].source` | Plugin 源路径 |
| `plugins[].skills` | 该 Plugin 包含的 Skills 路径 |

### 5.3 为什么需要 marketplace.json？

- 让 Claude Code 识别这是一个 Plugin Marketplace
- 定义 marketplace 中有哪些 plugins
- 每个 plugin 包含哪些 skills
- 支持 `/plugin marketplace add` 和 `/plugin install` 命令

---

## 6. 安装、卸载与更新

### 6.1 安装方式汇总

### 方式 1：Plugin Marketplace（推荐）

```bash
# 添加 marketplace
/plugin marketplace add username/repo-name

# 安装特定 plugin
/plugin install plugin-name

# 重启 Claude Code
```

**优点：**
- 官方支持的方式
- 可以选择性安装
- 版本管理

### 方式 2：npx skills

```bash
npx skills add username/repo-name -y -g
```

**优点：**
- 一条命令安装
- 支持多个 AI Agent（Claude Code、Cursor、Codex 等）
- 自动创建符号链接

### 方式 3：Git Clone

```bash
git clone git@github.com:username/repo.git ~/.claude/skills/skill-name
```

**优点：**
- 简单直接
- 便于修改和调试

### 方式 4：Git Submodule

```bash
git submodule add git@github.com:username/repo.git .claude/skills/skill-name
```

**优点：**
- 项目级安装
- 便于团队共享
- 可锁定版本

---

### 6.2 卸载 Skill

#### 方式 1：Plugin Marketplace 安装的 Skill

```bash
# 卸载特定 plugin
/plugin uninstall plugin-name

# 移除 marketplace（可选）
/plugin marketplace remove marketplace-name
```

#### 方式 2：npx skills 安装的 Skill

```bash
# 手动删除安装目录
rm -rf ~/.agents/skills/skill-name
rm -rf ~/.claude/skills/skill-name   # 如果有符号链接
```

#### 方式 3：手动安装的 Skill

```bash
# 删除 skill 目录
rm -rf ~/.claude/skills/skill-name

# 如果是项目级安装
rm -rf .claude/skills/skill-name
```

**卸载后需要重启 Claude Code 才能生效。**

---

### 6.3 更新 Skill

#### 方式 1：Plugin Marketplace 安装的 Skill

```bash
# 更新特定 plugin 到最新版本
/plugin update plugin-name

# 或者先卸载再重新安装
/plugin uninstall plugin-name
/plugin install plugin-name
```

#### 方式 2：npx skills 安装的 Skill

```bash
# 重新运行安装命令会覆盖旧版本
npx skills add username/repo-name -y -g
```

#### 方式 3：Git Clone 安装的 Skill

```bash
# 进入 skill 目录拉取最新代码
cd ~/.claude/skills/skill-name
git pull origin main
```

#### 方式 4：Git Submodule 安装的 Skill

```bash
# 更新 submodule
git submodule update --remote .claude/skills/skill-name
```

**更新后需要重启 Claude Code 才能加载新版本。**

---

### 6.4 查看已安装的 Skill

```bash
# 查看 Plugin Marketplace 安装的
/plugin list

# 查看全局安装的 skills
ls ~/.claude/skills/
ls ~/.agents/skills/

# 查看项目级安装的 skills
ls .claude/skills/
```

---

### 6.5 安装位置说明

| 安装方式 | 安装位置 | 作用范围 |
|----------|----------|----------|
| Plugin Marketplace | `~/.claude/plugins/cache/` | 全局 |
| npx skills (-g) | `~/.agents/skills/` + 符号链接到 `~/.claude/skills/` | 全局 |
| Git Clone 到 ~/.claude/skills/ | `~/.claude/skills/` | 全局 |
| Git Clone 到 .claude/skills/ | `.claude/skills/` | 当前项目 |

**符号链接的好处：**
- 一份代码，多个 AI Agent 共享（Claude Code、Cursor、Codex 等）
- 更新一处，所有 agent 同时生效

---

## 附录：完整示例仓库结构

```
changye01/tech-design-doc/
├── .claude-plugin/
│   └── marketplace.json
├── README.md
└── skills/
    └── tech-design-doc/
        ├── SKILL.md
        ├── scripts/
        │   └── validate_doc.py
        ├── references/
        │   ├── writing-guide.md
        │   └── checklist.md
        └── assets/
            ├── template.md
            └── example.md
```

**安装命令：**
```bash
# Marketplace 方式
/plugin marketplace add changye01/tech-design-doc
/plugin install tech-design-doc

# npx 方式
npx skills add changye01/tech-design-doc -y -g
```

---

## 参考资料

- [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
- [GitHub - anthropics/skills](https://github.com/anthropics/skills)

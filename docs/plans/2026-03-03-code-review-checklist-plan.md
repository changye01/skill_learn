# Code Review Checklist Skill 实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 创建一个引导式 Code Review Skill，展示 Skill 的完整架构（SKILL.md / scripts / references / assets）

**Architecture:** 在 `code-review-checklist/skills/code-review-checklist/` 下创建标准 Skill 目录结构。SKILL.md 定义引导式工作流，references/ 存放审查规则，assets/ 存放输出模板，scripts/ 存放验证脚本。

**Tech Stack:** Python 3（验证脚本）、Markdown（规则和模板）

---

### Task 1: 创建目录结构

**Files:**
- Create: `code-review-checklist/skills/code-review-checklist/` 目录
- Create: `code-review-checklist/skills/code-review-checklist/scripts/` 目录
- Create: `code-review-checklist/skills/code-review-checklist/references/` 目录
- Create: `code-review-checklist/skills/code-review-checklist/assets/` 目录

**Step 1: 创建目录结构**

```bash
mkdir -p code-review-checklist/skills/code-review-checklist/{scripts,references,assets}
```

**Step 2: 验证目录结构**

```bash
tree code-review-checklist/
```

Expected:
```
code-review-checklist/
└── skills/
    └── code-review-checklist/
        ├── assets/
        ├── references/
        └── scripts/
```

---

### Task 2: 创建 references/general-rules.md

**Files:**
- Create: `code-review-checklist/skills/code-review-checklist/references/general-rules.md`

**Step 1: 创建通用审查规则文件**

```markdown
# 通用代码审查规则

以下规则适用于所有语言。审查时逐项检查，给出 `[x]`（通过）或 `[!]`（不通过）。

---

## 1. 命名规范

检查要点：
- 变量名是否能表达其用途（避免 `a`, `tmp`, `data` 等模糊命名）
- 函数名是否描述了它做什么（动词开头：`get_user`, `calculate_total`）
- 类名是否是名词，且能表达其职责
- 布尔变量是否用 `is_`/`has_`/`can_` 前缀

---

## 2. 错误处理

检查要点：
- 外部调用（网络、文件、数据库）是否有错误处理
- 错误信息是否包含足够的上下文（哪个操作、什么输入、什么错误）
- 是否区分了可恢复和不可恢复的错误
- 是否避免了静默吞掉异常

---

## 3. 安全性

检查要点：
- 是否有硬编码的密钥、密码、Token
- 用户输入是否经过验证/转义（防止注入攻击）
- 敏感数据是否记录到日志中
- 文件路径是否可能被路径穿越攻击利用

---

## 4. 可读性

检查要点：
- 函数是否短小（建议不超过 30 行）
- 嵌套层级是否过深（建议不超过 3 层）
- 复杂逻辑是否有注释说明「为什么」（而非「做了什么」）
- 代码分组是否合理（空行分隔逻辑块）

---

## 5. DRY（Don't Repeat Yourself）

检查要点：
- 是否有超过 3 行的重复代码块
- 重复逻辑是否可以提取为函数
- 魔法数字/字符串是否定义为常量

---

## 6. 边界情况

检查要点：
- 是否处理了空值/None/null
- 是否处理了空列表/空字符串
- 是否处理了极大/极小输入
- 除法运算是否检查了除零
```

**Step 2: 确认文件已创建**

```bash
wc -l code-review-checklist/skills/code-review-checklist/references/general-rules.md
```

Expected: 约 60 行

---

### Task 3: 创建 references/python-rules.md

**Files:**
- Create: `code-review-checklist/skills/code-review-checklist/references/python-rules.md`

**Step 1: 创建 Python 专项规则文件**

```markdown
# Python 专项审查规则

以下规则仅在审查 Python 代码时使用，作为通用规则的补充。

---

## 1. PEP 8 规范

检查要点：
- 缩进是否使用 4 个空格
- 行长度是否不超过 88 字符（black 默认）或 79 字符（PEP 8 默认）
- import 顺序是否正确（标准库 → 第三方 → 本地）
- 类和顶层函数之间是否有两个空行

---

## 2. 类型提示

检查要点：
- 公开函数是否有参数和返回值类型提示
- 复杂数据结构是否使用 TypeAlias 或 TypedDict
- 是否避免了 `Any` 类型（除非确实需要）
- Optional 参数是否标注为 `X | None`

---

## 3. 异常处理

检查要点：
- 是否避免了裸 `except:`（应捕获具体异常）
- 是否避免了 `except Exception:`（太宽泛）
- 是否使用了 `raise ... from e` 保留异常链
- 资源清理是否使用了 `with` 语句或 `finally`

---

## 4. Pythonic 写法

检查要点：
- 是否使用列表推导代替简单的 for+append
- 是否使用 `enumerate()` 代替手动计数器
- 是否使用 `pathlib.Path` 代替字符串拼接路径
- 是否使用 f-string 代替 `%` 或 `.format()`
```

**Step 2: 确认文件已创建**

```bash
wc -l code-review-checklist/skills/code-review-checklist/references/python-rules.md
```

Expected: 约 45 行

---

### Task 4: 创建 assets/review-template.md

**Files:**
- Create: `code-review-checklist/skills/code-review-checklist/assets/review-template.md`

**Step 1: 创建输出模板文件**

```markdown
# Code Review: {{FILE_NAME}}

> 日期: {{DATE}}
> 语言: {{LANGUAGE}}
> 审查人: Claude

---

## 通用规则

- [ ] **命名规范** —
- [ ] **错误处理** —
- [ ] **安全性** —
- [ ] **可读性** —
- [ ] **DRY** —
- [ ] **边界情况** —

## {{LANGUAGE}} 专项

{{LANGUAGE_RULES}}

---

## 总结

- 通过项: {{PASS_COUNT}} / {{TOTAL_COUNT}}
- 需改进: {{FAIL_COUNT}} 项

### 主要建议

{{SUGGESTIONS}}
```

**Step 2: 确认文件已创建**

```bash
wc -l code-review-checklist/skills/code-review-checklist/assets/review-template.md
```

Expected: 约 28 行

---

### Task 5: 创建 scripts/validate_review.py

**Files:**
- Create: `code-review-checklist/skills/code-review-checklist/scripts/validate_review.py`

**Step 1: 创建验证脚本**

```python
#!/usr/bin/env python3
"""检查 Code Review 清单的完整性"""

import sys
import re


def validate(filepath: str) -> dict:
    """验证审查清单，返回统计信息和问题列表"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"错误：文件不存在 - {filepath}")
        sys.exit(2)

    lines = content.split('\n')
    issues = []
    total = 0
    checked = 0
    failed = 0

    for i, line in enumerate(lines, 1):
        # 匹配清单项: - [ ] 或 - [x] 或 - [!]
        match = re.match(r'^- \[([ x!])\] ', line)
        if not match:
            continue

        total += 1
        mark = match.group(1)

        if mark == ' ':
            issues.append(f"  第 {i} 行：未审查 - {line.strip()}")
        elif mark == 'x':
            checked += 1
        elif mark == '!':
            failed += 1
            # 检查下一行是否有备注
            next_line = lines[i] if i < len(lines) else ''
            if not next_line.strip().startswith('>'):
                issues.append(f"  第 {i} 行：标记为不通过但缺少备注 - {line.strip()}")

    return {
        'total': total,
        'checked': checked,
        'failed': failed,
        'unchecked': total - checked - failed,
        'issues': issues,
    }


def main():
    if len(sys.argv) != 2:
        print("用法: python validate_review.py <清单文件路径>")
        print("示例: python validate_review.py code-review-2026-03-03.md")
        sys.exit(1)

    filepath = sys.argv[1]
    result = validate(filepath)

    print(f"审查项统计：共 {result['total']} 项")
    print(f"  ✅ 通过: {result['checked']}")
    print(f"  ❌ 不通过: {result['failed']}")
    print(f"  ⬜ 未审查: {result['unchecked']}")

    if result['issues']:
        print(f"\n问题：")
        for issue in result['issues']:
            print(issue)
        sys.exit(1)
    else:
        print(f"\n✅ 审查清单已完整填写")
        sys.exit(0)


if __name__ == "__main__":
    main()
```

**Step 2: 添加执行权限并测试**

```bash
chmod +x code-review-checklist/skills/code-review-checklist/scripts/validate_review.py
python code-review-checklist/skills/code-review-checklist/scripts/validate_review.py
```

Expected: 输出用法提示

---

### Task 6: 创建 SKILL.md

**Files:**
- Create: `code-review-checklist/skills/code-review-checklist/SKILL.md`

**Step 1: 创建 SKILL.md 文件**

```markdown
---
name: code-review-checklist
description: 代码审查清单生成工具。用于：(1) 对指定文件进行结构化代码审查 (2) 通过通用规则+语言专项规则逐项检查 (3) 输出 Markdown 格式审查报告。当用户说"code review"、"代码审查"、"审查清单"、"review checklist"时触发。
---

# Code Review 清单生成器

## 工作流程

1. **确定目标** — 询问要审查的文件或代码
2. **确定语言** — 询问编程语言，加载对应的专项规则
3. **加载规则** — 读取 `references/general-rules.md` + 语言专项规则
4. **逐项审查** — 按规则逐项检查代码，给出通过/不通过判定
5. **生成报告** — 基于 `assets/review-template.md` 生成审查清单文件
6. **验证完整性** — 运行 `scripts/validate_review.py` 确认清单已填写完整

## 引导问题

### 第 1 步：确定目标
- 你要审查哪个文件？请提供文件路径。

### 第 2 步：确定语言
- 这是什么编程语言？
  - Python（将额外使用 `references/python-rules.md`）
  - 其他语言（仅使用通用规则）

## 审查标记说明

- `[x]` = 通过
- `[!]` = 不通过（必须附带 `> 建议:` 说明）

## 资源

- **通用规则**: 所有语言通用的 6 项审查要点，见 `references/general-rules.md`
- **Python 专项**: Python 特有的 4 项审查要点，见 `references/python-rules.md`
- **输出模板**: 审查报告模板，见 `assets/review-template.md`

## 验证

生成审查报告后，运行验证脚本检查完整性：

\`\`\`bash
python scripts/validate_review.py <报告路径>
\`\`\`

如果提示有未审查项或缺少备注，根据提示补充。
```

**Step 2: 确认文件已创建**

```bash
wc -l code-review-checklist/skills/code-review-checklist/SKILL.md
```

Expected: 约 48 行

---

### Task 7: 创建 README.md（供培训讲解用）

**Files:**
- Create: `code-review-checklist/README.md`

**Step 1: 创建 README**

```markdown
# Code Review Checklist Skill

演示 Claude Code Skill 架构的示例项目，用于团队内部培训。

## Skill 架构说明

```
code-review-checklist/
└── skills/
    └── code-review-checklist/
        ├── SKILL.md              ← 入口：触发条件 + 工作流程
        ├── scripts/
        │   └── validate_review.py  ← 确定性任务：验证清单完整性
        ├── references/
        │   ├── general-rules.md    ← 按需加载：通用审查规则
        │   └── python-rules.md     ← 按需加载：Python 专项规则
        └── assets/
            └── review-template.md  ← 输出模板：审查报告模板
```

### 各组件加载时机

| 组件 | 加载时机 | Token 消耗 |
|------|----------|-----------|
| SKILL.md frontmatter | 始终在上下文 | ~100 tokens |
| SKILL.md body | 触发后加载 | <5k tokens |
| references/*.md | 审查时按需读取 | 按需 |
| assets/*.md | 生成报告时读取 | 按需 |
| scripts/*.py | 执行时运行，不读入上下文 | 0 |

## 快速体验

对任意 Python 文件运行审查：

> 请帮我 code review 这个文件：path/to/your_file.py

## 扩展方式

添加新语言支持只需：

1. 在 `references/` 下新建 `<语言>-rules.md`
2. 在 SKILL.md 的引导问题中添加该语言选项
```

**Step 2: 确认文件已创建**

```bash
cat code-review-checklist/README.md | head -5
```

---

### Task 8: 端到端验证

**Step 1: 确认目录结构完整**

```bash
tree code-review-checklist/
```

Expected:
```
code-review-checklist/
├── README.md
└── skills/
    └── code-review-checklist/
        ├── SKILL.md
        ├── assets/
        │   └── review-template.md
        ├── references/
        │   ├── general-rules.md
        │   └── python-rules.md
        └── scripts/
            └── validate_review.py
```

**Step 2: 验证脚本可运行**

```bash
python code-review-checklist/skills/code-review-checklist/scripts/validate_review.py
```

Expected: 输出用法提示，退出码 1

**Step 3: 用一个测试清单验证脚本逻辑**

创建一个临时测试文件 `/tmp/test-review.md`：

```markdown
# Code Review: test.py

## 通用规则
- [x] **命名规范** — 良好
- [!] **错误处理** — 缺少异常处理
  > 建议: 添加 try/except
- [x] **安全性** — 无问题
- [x] **可读性** — 清晰
- [x] **DRY** — 无重复
- [x] **边界情况** — 已处理
```

```bash
python code-review-checklist/skills/code-review-checklist/scripts/validate_review.py /tmp/test-review.md
```

Expected: `✅ 审查清单已完整填写`

**Step 4: 初始化 git 仓库并提交**

```bash
cd code-review-checklist && git init && git add -A && git commit -m "feat: 创建 code-review-checklist skill"
```

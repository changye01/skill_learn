# Code Review Checklist Skill 设计文档

日期: 2026-03-03

## 目标

创建一个演示用 Skill，通过引导式 Code Review 工作流，展示 Skill 的完整架构（SKILL.md / scripts / references / assets）。面向团队内部培训，帮助同事理解和创建自己的 Skill。

## 目录结构

```
code-review-checklist/
├── SKILL.md                      # 触发条件 + 审查工作流
├── scripts/
│   └── validate_review.py        # 验证清单完整性
├── references/
│   ├── general-rules.md          # 通用审查规则
│   └── python-rules.md           # Python 专项规则
└── assets/
    └── review-template.md        # 输出模板
```

## 各组件职责

| 组件 | 职责 | 加载时机 |
|------|------|----------|
| SKILL.md frontmatter | 触发条件（name + description） | 始终在上下文 (~100 tokens) |
| SKILL.md body | 审查工作流指令 | 触发后加载 (<5k tokens) |
| references/general-rules.md | 通用审查规则（6 项） | 审查时按需读取 |
| references/python-rules.md | Python 专项规则（4 项） | 用户选择 Python 时读取 |
| assets/review-template.md | Markdown 输出模板 | 生成报告时读取 |
| scripts/validate_review.py | 验证清单是否填写完整 | 生成后执行 |

## 工作流程

```
用户触发 → 询问审查目标（文件/PR）
         → 询问语言（决定加载哪个 references/）
         → 读取通用规则 + 语言规则
         → 逐项审查代码
         → 基于模板生成 Markdown 清单
         → 运行 validate_review.py 检查完整性
```

## 触发条件

当用户说 "code review"、"代码审查"、"审查清单"、"review checklist" 时触发。

## 审查规则

### 通用规则（6 项）

1. 命名规范 — 变量/函数/类命名是否清晰
2. 错误处理 — 是否有适当的异常/错误处理
3. 安全性 — 是否有硬编码密钥、SQL 注入等风险
4. 可读性 — 代码结构是否清晰，是否有必要注释
5. DRY — 是否有重复代码
6. 边界情况 — 是否处理了空值、极端输入等

### Python 专项规则（4 项）

1. PEP 8 — 是否符合编码规范
2. 类型提示 — 关键函数是否有 type hints
3. 异常处理 — 是否用了具体异常而非裸 except
4. Pythonic — 是否使用了惯用写法

## 验证脚本逻辑

检查生成的 Markdown 文件：
- 所有 `[ ]` 是否已改为 `[x]`（通过）或 `[!]`（不通过）
- 不通过项是否有备注说明（`>` 开头的行）

## 输出示例

```markdown
# Code Review: user_service.py
日期: 2026-03-03
语言: Python

## 通用规则
- [x] 命名规范 — 函数命名清晰
- [!] 错误处理 — process_order() 缺少异常处理
  > 建议: 添加 try/except 处理数据库连接失败

## Python 专项
- [x] PEP 8 — 符合规范
- [!] 类型提示 — calculate_total() 缺少返回类型
  > 建议: 添加 -> Decimal
```

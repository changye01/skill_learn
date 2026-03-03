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

```bash
python scripts/validate_review.py <报告路径>
```

如果提示有未审查项或缺少备注，根据提示补充。

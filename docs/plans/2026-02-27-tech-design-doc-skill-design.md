# tech-design-doc Skill 设计文档

> 日期：2026-02-27
> 目的：学习 Skill 编写，涵盖所有核心组件

---

## 1. 需求概述

| 项目 | 选择 |
|------|------|
| 场景 | 新功能开发 |
| 结构 | 简洁版（背景、方案设计、接口定义、实现计划）|
| 交互 | 引导式（通过提问逐步完善）|
| 语言 | 中文 |
| 学习目标 | 涵盖 Skill 各组成部分 |

---

## 2. Skill 整体结构

```
tech-design-doc/
├── SKILL.md                    # 核心主文件
├── scripts/
│   └── validate_doc.py         # 文档完整性检查脚本
├── references/
│   ├── writing-guide.md        # 写作指南
│   └── checklist.md            # 自检清单
└── assets/
    ├── template.md             # 文档模板
    └── example.md              # 完整示例
```

---

## 3. 各组件设计

### 3.1 SKILL.md

**Frontmatter:**

```yaml
---
name: tech-design-doc
description: 技术设计文档生成工具。用于：(1) 新功能开发前的方案设计 (2) 通过引导式提问生成完整设计文档 (3) 输出 Markdown 格式。当用户说"写设计文档"、"TDD"、"技术方案"时触发。
---
```

**Body 内容:**

- 工作流程（5 步：背景 → 方案 → 接口 → 计划 → 生成）
- 资源引用说明
- 验证脚本使用说明

### 3.2 scripts/validate_doc.py

- 功能：检查文档是否包含必需章节
- 输入：文档文件路径
- 输出：缺失章节列表或成功提示
- 退出码：0=完整，1=有缺失

### 3.3 references/

**writing-guide.md:**
- 各章节写作要点
- 常见问题解答

**checklist.md:**
- 分章节的自检清单
- Checkbox 格式便于逐项检查

### 3.4 assets/

**template.md:**
- 空白文档模板
- 包含所有章节骨架和占位符

**example.md:**
- 完整的示例文档（用户登录优化）
- 展示各章节的实际写法

---

## 4. 学习要点总结

| 组件 | 用途 | 加载时机 |
|------|------|----------|
| SKILL.md frontmatter | 触发条件 | 始终在上下文 |
| SKILL.md body | 工作流程指令 | 触发后加载 |
| scripts/ | 确定性执行任务 | 执行时，不读入上下文 |
| references/ | 详细参考资料 | 按需读取 |
| assets/ | 输出资源 | 复制/修改使用 |

---

## 5. 下一步

使用 writing-plans skill 创建实现计划。

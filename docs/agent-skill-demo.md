# Agent & Skill 演示文档

> 本文档用于向团队演示 Claude Code 中 Agent、MCP 和 Skill 的核心概念及实际使用效果。

---

## 1. 三个核心概念

### 1.1 Agent（智能体）

Agent 是具备**自主决策能力**的 AI 执行单元。它能够：

- 理解用户意图，拆解为多个步骤
- 自主选择调用哪些工具、按什么顺序执行
- 根据中间结果动态调整后续行为
- 并行派发子任务（Sub-Agent）提升效率

```
用户: "根据这份需求文档生成测试用例"
  │
  Agent 自主决策链：
  ├─ 识别意图 → 测试用例生成
  ├─ 发现匹配 Skill → 触发 test-case-generator
  ├─ 加载测试设计规则（references/）
  ├─ 先生成场景地图
  ├─ 用户确认后再展开结构化测试用例
  └─ 运行验证脚本（scripts/）确认完整性
```

### 1.2 MCP（Model Context Protocol）

MCP 是标准化的**工具调用协议层**，定义了模型如何与外部工具交互。

| 职责 | 说明 |
|------|------|
| 工具发现 | 模型知道有哪些工具可用 |
| 调用规范 | 统一的输入/输出格式 |
| 结果返回 | 工具执行结果回传给模型 |

**类比**：USB 协议 — 不管插什么设备（数据库、API、文件系统），接口标准统一。

### 1.3 Skill（技能）

Skill 是固化的**领域知识 + 工作流程**，告诉 Agent "遇到这类任务该怎么做"。

| 组件 | 用途 | 类比 |
|------|------|------|
| SKILL.md frontmatter | 触发条件 | 岗位职责描述 |
| SKILL.md body | 工作流程 | 操作手册 |
| references/ | 领域知识 | 参考资料库 |
| assets/ | 输出模板 | 文档模板 |
| scripts/ | 确定性验证 | 质检工具 |

### 1.4 三者的关系

```
┌─────────────────────────────────────────────┐
│                  Agent（大脑）                │
│         理解意图 → 规划步骤 → 执行任务        │
│                                             │
│   ┌───────────────┐   ┌───────────────────┐ │
│   │  MCP（双手）   │   │  Skill（方法论）   │ │
│   │               │   │                   │ │
│   │ 读写文件       │   │ 工作流程           │ │
│   │ 执行命令       │   │ 审查规则           │ │
│   │ 搜索代码       │   │ 输出模板           │ │
│   │ 调用 API       │   │ 验证脚本           │ │
│   └───────────────┘   └───────────────────┘ │
└─────────────────────────────────────────────┘

MCP  → 能做什么（能力层）→ "我能读文件、跑命令、调 API"
Skill → 怎么做事（知识层）→ "生成测试用例时先出场景地图，再展开结构化用例"
Agent → 自主决策（智能层）→ "用户要从需求生成用例，我来调 Skill 和工具完成"
```

---

## 2. 实战演示：Test Case Generator Skill

### 2.1 演示场景

对一份需求文档生成测试场景与结构化测试用例，展示 Skill 如何引导 Agent 按“两阶段流程”完成工作。

**输入**：需求文档，如 `example_data/【26668】M4X订单管理：查询条件及列表字段调整、新增分配采购员功能.pdf`

**触发方式**：

```
用户输入: 根据需求文档生成测试用例
```

### 2.2 Skill 执行流程

Agent 触发 `test-case-generator` Skill 后，按以下流程自动执行：

```
Step 1  确定输入材料   → 需求文档 + 补充资料
Step 2  拆解需求点     → 页面/接口/日志/历史数据等
Step 3  加载规则       → references/test-design-rules.md
Step 4  生成场景地图   → 基于 assets/scene-template.md
Step 5  覆盖检查       → references/coverage-checklist.md
Step 6  用户确认场景   → 确认“测什么”
Step 7  生成测试用例   → 基于 assets/test-case-template.md
Step 8  验证完整性     → 运行 scripts/validate_cases.py
```

### 2.3 测试设计规则一览

Skill 会在生成场景时自动补齐这些维度：

| 维度 | 检查要点 |
|------|----------|
| 正常流程 | 主流程是否可执行 |
| 边界条件 | 空值、极值、特殊字符、清空 |
| 异常场景 | 非法输入、无匹配、失败路径 |
| 权限控制 | 可操作角色与无权限角色 |
| 日志校验 | 操作人、文案、任务 ID |
| 数据一致性 | 页面、接口、库表是否一致 |
| 数据持久化 | 修改后刷新或重查是否保留 |
| 综合场景 | 端到端链路是否完整 |

### 2.4 场景地图输出示例（节选）

```markdown
# 某需求测试场景地图

## 场景分组

### 场景组 1：正常流程
- 覆盖点：列表展示、条件查询、修改采购员

### 场景组 2：边界与异常
- 覆盖点：特殊字符账号、无匹配、取消弹窗

### 场景组 3：综合场景
- 覆盖点：同步 -> 查询 -> 分配采购员 -> 创建 PO -> 校验日志
```

### 2.5 验证脚本输出

```
$ python scripts/validate_cases.py example_cases.md

✅ 测试用例文档结构完整
```

---

## 3. 对比：没有 Skill vs 有 Skill

| 维度 | 直接让 Agent 做 | 使用 Skill |
|------|-----------------|-----------|
| 工作流 | 容易直接平铺写用例 | 固定为先场景后用例 |
| 覆盖性 | 容易漏掉日志、权限、综合场景 | 通过规则和清单系统补齐 |
| 输出格式 | 风格不稳定 | 基于模板统一输出 |
| 完整性 | 可能缺少关键字段 | 验证脚本确保结构完整 |
| 可维护性 | 每次重新描述方法 | 修改规则文件即可全局生效 |

---

## 4. Skill 的组成结构

以 `test-case-generator` 为例：

```
skills/test-case-generator/
├── SKILL.md                          # 触发条件 + 工作流程
├── scripts/
│   └── validate_cases.py             # 验证测试用例完整性
├── references/
│   ├── test-design-rules.md          # 测试设计规则
│   └── coverage-checklist.md         # 覆盖检查清单
└── assets/
    ├── scene-template.md             # 场景地图模板
    └── test-case-template.md         # 结构化测试用例模板
```

**各组件加载时机**：

```
用户触发 Skill
  │
  ├─ [始终在上下文] SKILL.md frontmatter（name + description）
  │
  ├─ [触发后加载]   SKILL.md body（工作流指令）
  │
  ├─ [按需读取]     references/test-design-rules.md
  │                 references/coverage-checklist.md
  │
  ├─ [输出时使用]   assets/scene-template.md
  │                 assets/test-case-template.md
  │
  └─ [执行时调用]   scripts/validate_cases.py
```

---

## 5. 如何创建自己的 Skill

### 快速上手

```bash
# 1. 创建目录结构
mkdir -p skills/my-skill/{scripts,references,assets}

# 2. 编写 SKILL.md（必需）
cat > skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: 我的 Skill 描述。用于：(1) 功能一 (2) 功能二。当用户说"关键词"时触发。
---

# 工作流程
1. 第一步
2. 第二步
3. 生成输出
EOF

# 3. 安装到 Claude Code
npx skills add username/repo-name -y -g
```

### 详细指南

完整的创建步骤和发布流程见 [Skill 创建完整指南](./skill-creation-guide.md)。

---

## 6. 总结

| 概念 | 一句话 | 价值 |
|------|--------|------|
| **Agent** | 自主决策的 AI 执行体 | 理解意图，串联工具和知识完成任务 |
| **MCP** | 标准化工具调用协议 | 让 Agent 能操作外部世界 |
| **Skill** | 固化的领域知识和工作流 | 让 Agent 按团队规范做事，输出一致可复现 |

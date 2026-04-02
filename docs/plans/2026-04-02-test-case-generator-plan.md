# Test Case Generator Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建一个面向需求文档、默认追求覆盖全面的测试用例生成 Skill，采用“先场景地图、后结构化用例”的两阶段工作流。

**Architecture:** 在 `skills/test-case-generator/` 下创建标准 Skill 目录。`SKILL.md` 负责触发与流程，`README.md` 负责说明规则与原则，`references/` 负责约束测试设计与覆盖检查，`assets/` 负责两阶段输出模板，`scripts/` 负责结果完整性校验。实现过程遵循小步提交和先验证后完成的原则。

**Tech Stack:** Markdown、Python 3

---

### Task 1: 创建基础目录与插件登记

**Files:**
- Create: `skills/test-case-generator/`
- Create: `skills/test-case-generator/references/`
- Create: `skills/test-case-generator/assets/`
- Create: `skills/test-case-generator/scripts/`
- Modify: `.claude-plugin/marketplace.json`
- Review: `.cursor-plugin/plugin.json`

- [ ] **Step 1: 创建 Skill 目录结构**

Run: `mkdir -p skills/test-case-generator/{references,assets,scripts}`
Expected: 目录创建成功

- [ ] **Step 2: 更新 `.claude-plugin/marketplace.json`，新增 `test-case-generator` 条目**

插入一个与现有插件风格一致的新条目：

```json
{
  "name": "test-case-generator",
  "description": "测试用例生成工具，基于需求文档先生成场景地图，再生成结构化测试用例",
  "version": "1.0.0",
  "source": "./",
  "author": {
    "name": "changye01",
    "email": ""
  }
}
```

- [ ] **Step 3: 验证插件配置可读**

Run: `python -m json.tool .claude-plugin/marketplace.json >/dev/null`
Expected: 退出码 0

- [ ] **Step 4: 确认 Cursor 插件配置无需单独登记**

检查 `.cursor-plugin/plugin.json` 是否通过 `skills: "./skills/"` 自动暴露新 Skill；若是，则记录“无需修改”。

### Task 2: 编写 `README.md`

**Files:**
- Create: `skills/test-case-generator/README.md`

- [ ] **Step 1: 写 README 标题与定位**

包含：

```markdown
# Test Case Generator Skill

一个基于需求文档自动生成测试场景和结构化测试用例的 Skill。
```

- [ ] **Step 2: 写 README 的核心章节**

至少包含以下章节：

```markdown
## 目标
## 适用范围
## 设计原则
## 两阶段生成流程
## 目录结构
## 输出物说明
## 规则来源
## 使用方式
## 验证方式
```

- [ ] **Step 3: 在 README 中明确写入已确认原则**

必须包含这些表述：

```markdown
- 先场景，后用例
- 覆盖全面，但不以数量最大化为目标
- 默认补齐权限、日志、数据一致性、数据持久化、综合流程
- 超范围项只提示，不默认混入功能测试主体
```

- [ ] **Step 4: 检查 README 是否能独立解释整个 Skill**

Run: `python - <<'PY'
from pathlib import Path
text = Path("skills/test-case-generator/README.md").read_text(encoding="utf-8")
for keyword in ["设计原则", "两阶段生成流程", "验证方式"]:
    assert keyword in text, keyword
print("ok")
PY`
Expected: 输出 `ok`

### Task 3: 编写 `references/test-design-rules.md`

**Files:**
- Create: `skills/test-case-generator/references/test-design-rules.md`

- [ ] **Step 1: 写需求拆解规则**

必须覆盖：

```markdown
- 页面
- 接口
- 任务
- 日志
- 历史数据修复
```

- [ ] **Step 2: 写场景扩展规则**

必须覆盖：

```markdown
- 正常
- 边界
- 异常
- 权限
- 状态流转
- 日志
- 数据一致性
- 数据持久化
- 端到端
```

- [ ] **Step 3: 写去重和超范围控制规则**

必须明确：

```markdown
- 禁止机械穷举
- 禁止多个用例仅标题不同而内容重复
- 性能/兼容性/安全性默认只提示，不进入主体
```

- [ ] **Step 4: 检查规则文件是否使用可执行语言**

Run: `python - <<'PY'
from pathlib import Path
text = Path("skills/test-case-generator/references/test-design-rules.md").read_text(encoding="utf-8")
for keyword in ["必须", "默认", "禁止"]:
    assert keyword in text, keyword
print("ok")
PY`
Expected: 输出 `ok`

### Task 4: 编写 `references/coverage-checklist.md`

**Files:**
- Create: `skills/test-case-generator/references/coverage-checklist.md`

- [ ] **Step 1: 写覆盖检查清单**

至少包含以下检查项：

```markdown
- 显式需求点是否全部映射
- 是否有正常流程
- 是否有边界条件
- 是否有异常场景
- 是否有权限控制
- 是否有日志校验
- 是否有数据一致性校验
- 是否有数据持久化校验
- 是否有历史数据处理校验
- 是否有综合流程场景
- 是否标记信息不足项
- 是否标记超范围项
```

- [ ] **Step 2: 确认清单格式适合逐项自查**

Run: `python - <<'PY'
from pathlib import Path
lines = Path("skills/test-case-generator/references/coverage-checklist.md").read_text(encoding="utf-8").splitlines()
assert sum(line.lstrip().startswith("- ") for line in lines) >= 10
print("ok")
PY`
Expected: 输出 `ok`

### Task 5: 编写输出模板

**Files:**
- Create: `skills/test-case-generator/assets/scene-template.md`
- Create: `skills/test-case-generator/assets/test-case-template.md`

- [ ] **Step 1: 创建场景地图模板**

模板至少包含以下标题：

```markdown
# {{REQUIREMENT_NAME}} 测试场景地图
## 功能模块
## 需求点列表
## 场景分组
## 补充维度
## 信息不足待确认项
## 超范围项
```

- [ ] **Step 2: 创建结构化测试用例模板**

模板至少包含以下字段：

```markdown
- 需求名称
- 用例编号
- 模块
- 场景组
- 用例标题
- 关联需求点
- 前置条件
- 测试步骤
- 预期结果
- 优先级
- 备注
```

- [ ] **Step 3: 验证模板字段完整**

Run: `python - <<'PY'
from pathlib import Path
scene = Path("skills/test-case-generator/assets/scene-template.md").read_text(encoding="utf-8")
case = Path("skills/test-case-generator/assets/test-case-template.md").read_text(encoding="utf-8")
for keyword in ["场景分组", "信息不足待确认项", "超范围项"]:
    assert keyword in scene, keyword
for keyword in ["测试步骤", "预期结果", "优先级", "关联需求点"]:
    assert keyword in case, keyword
print("ok")
PY`
Expected: 输出 `ok`

### Task 6: 编写 `SKILL.md`

**Files:**
- Create: `skills/test-case-generator/SKILL.md`

- [ ] **Step 1: 写 frontmatter**

前言应满足：

```markdown
---
name: test-case-generator
description: 用于基于需求文档生成测试场景和结构化测试用例。当用户说“生成测试用例”“测试场景”“需求转测试用例”等时触发。
---
```

- [ ] **Step 2: 写主流程**

必须明确以下顺序：

```markdown
1. 确定输入材料
2. 拆解需求点
3. 读取测试设计规则
4. 生成场景地图
5. 读取覆盖检查清单补漏
6. 标记信息不足项与超范围项
7. 用户确认场景地图
8. 生成结构化测试用例
9. 运行验证脚本
```

- [ ] **Step 3: 写引导问题和默认策略**

必须写清：

```markdown
- 默认目标为覆盖全面
- 先场景后用例
- 非功能测试默认不纳入主体
```

- [ ] **Step 4: 检查 `SKILL.md` 是否引用了所有支撑文件**

Run: `python - <<'PY'
from pathlib import Path
text = Path("skills/test-case-generator/SKILL.md").read_text(encoding="utf-8")
for keyword in [
    "references/test-design-rules.md",
    "references/coverage-checklist.md",
    "assets/scene-template.md",
    "assets/test-case-template.md",
    "scripts/validate_cases.py",
]:
    assert keyword in text, keyword
print("ok")
PY`
Expected: 输出 `ok`

### Task 7: 编写 `scripts/validate_cases.py`

**Files:**
- Create: `skills/test-case-generator/scripts/validate_cases.py`
- Test: `/tmp/invalid-cases.md`
- Test: `/tmp/valid-cases.md`

- [ ] **Step 1: 先写一个最小失败示例作为脚本设计依据**

创建一个临时 Markdown 文件，故意缺少“预期结果”或“超范围项”，用于验证脚本会失败。

- [ ] **Step 2: 实现校验脚本**

脚本至少检查第二阶段结构化测试用例文档中的以下字段：

```python
required_keywords = [
    "需求名称",
    "场景组",
    "关联需求点",
    "测试步骤",
    "预期结果",
    "优先级",
]
```

脚本还应检查：

```python
- 至少存在一组“综合场景”或“端到端”场景
- 缺失项应逐条打印
- 校验失败返回非 0
```

- [ ] **Step 3: 运行脚本验证失败路径**

Run: `python skills/test-case-generator/scripts/validate_cases.py /tmp/invalid-cases.md`
Expected: 退出码非 0，并打印缺失字段

- [ ] **Step 4: 运行脚本验证成功路径**

Run: `python skills/test-case-generator/scripts/validate_cases.py /tmp/valid-cases.md`
Expected: 退出码 0，并打印校验通过

### Task 8: 端到端检查与文档收口

**Files:**
- Review: `skills/test-case-generator/README.md`
- Review: `skills/test-case-generator/SKILL.md`
- Review: `skills/test-case-generator/references/test-design-rules.md`
- Review: `skills/test-case-generator/references/coverage-checklist.md`
- Review: `skills/test-case-generator/assets/scene-template.md`
- Review: `skills/test-case-generator/assets/test-case-template.md`
- Review: `skills/test-case-generator/scripts/validate_cases.py`

- [ ] **Step 1: 检查目录结构完整**

Run: `python - <<'PY'
from pathlib import Path
required = [
    "skills/test-case-generator/README.md",
    "skills/test-case-generator/SKILL.md",
    "skills/test-case-generator/references/test-design-rules.md",
    "skills/test-case-generator/references/coverage-checklist.md",
    "skills/test-case-generator/assets/scene-template.md",
    "skills/test-case-generator/assets/test-case-template.md",
    "skills/test-case-generator/scripts/validate_cases.py",
]
missing = [path for path in required if not Path(path).exists()]
assert not missing, missing
print("ok")
PY`
Expected: 输出 `ok`

- [ ] **Step 2: 检查 Python 语法无误**

Run: `python -m py_compile skills/test-case-generator/scripts/validate_cases.py`
Expected: 退出码 0

- [ ] **Step 3: 在仓库根目录查看变更并确认仅包含目标文件**

Run: `git status --short`
Expected: 只出现本次新增或修改的 Skill 相关文件

# Skill Learn

`skill-learn` 是一个 Claude Code Skills 插件，当前包含两个面向测试工作的 Skill：

- `test-case-generator`：先生成 `测试场景地图`，再生成 `结构化测试用例`
- `test-data-generator`：基于已确认用例、技术方案和 `reference-pack` 补齐 `测试执行清单`

## 安装与管理

推荐通过 Claude Code Plugin Marketplace 安装：

```bash
claude plugins marketplace add "changye01/skill_learn"
claude plugins install "skill-learn"
```

更新：

```bash
claude plugins marketplace update "skill-learn"
claude plugins install "skill-learn"
```

卸载：

```bash
claude plugins uninstall "skill-learn" --scope user
```

如需同时移除 marketplace 条目，请按你当前 CLI 实际使用的插件标识执行 `claude plugins marketplace remove ...`。

## Skills

### `test-case-generator`

适用于“生成测试用例”“测试场景梳理”“需求转测试用例”等场景。

- 先产出 `测试场景地图`，明确“测什么”
- 再产出 `结构化测试用例`，明确“怎么测”
- 默认追求覆盖完整，但避免机械膨胀
- 提供结构校验脚本

### `test-data-generator`

适用于“生成测试执行清单”“补齐测试前置数据”“根据测试用例设计测试数据”等场景。

- 以 `结构化测试用例` 为基线继续补齐执行信息
- 把技术方案作为规则主输入
- 结合 `reference-pack` 输出按 `TC` 展开的 `测试执行清单`
- 提供结构校验脚本

## 最小使用路径

1. 用 `test-case-generator` 生成并确认：
   - `<需求名称>_测试场景地图.md`
   - `<需求名称>_结构化测试用例.md`
2. 再补齐技术方案、接口说明和 `reference-pack`
3. 用 `test-data-generator` 继续生成：
   - `<需求名称>_测试执行清单.md`

从仓库根目录运行校验脚本：

```bash
python skills/test-case-generator/scripts/validate_cases.py <测试用例文件路径>
python skills/test-data-generator/scripts/validate_test_data.py <测试执行清单文件路径>
```

## 真实示例

下面保留一条来自外部业务工作区的真实使用链路，用来说明两个 Skill 的串联方式。该示例中的 `example_data/...` 和 `reference-packs/...` 路径只是当时会话里的实际输入路径，不属于本仓库内容。

```text
@example_data/2026-03-17=!【采购-订单模块】M4X订单管理：查询条件及列表字段调整、新增分配采购员功能 生成测试用例
```

这类会话通常会按下面顺序完成：

1. 先用 `test-case-generator` 输出并确认 `测试场景地图`
2. 再落地 `<需求名称>_测试场景地图.md` 和 `<需求名称>_结构化测试用例.md`
3. 补齐技术方案、接口说明和 `reference-pack`
4. 再用 `test-data-generator` 继续生成 `<需求名称>_测试执行清单.md`

示例中常见的追加输入类似：

```text
根据 `【采购-订单模块】M4X订单管理：查询条件及列表字段调整、新增分配采购员功能_结构化测试用例.md`、当前会话中的技术方案和 `/Users/changye/changye_workspace/changye/skill_test/reference-packs/` 生成测试执行清单
```

本次示例使用的 `reference-pack` 参考路径为：

- `/Users/changye/changye_workspace/changye/skill_test/reference-packs/`

其中包含：

- `tables/*.sql`，例如 `tables/orders.sql`
- `table_samples/*.csv`，例如 `table_samples/orders.csv`
- `README.md`

`tables/orders.sql` 片段示例：

```sql
CREATE TABLE `orders` (
  `orders_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'order_id',
  `orders_code` varchar(32) NOT NULL DEFAULT '' COMMENT '订单编码',
  `site_id` varchar(64) NOT NULL DEFAULT '' COMMENT '订单来源站点ID',
  ...
)
```

`table_samples/orders.csv` 片段示例：

| orders_id | orders_code | orders_user_id | site_id | order_user_email | orders_status |
| --- | --- | --- | --- | --- | --- |
| 172464703 | ORDER_010 | radello77 | SITE_005 | go6q9wgwkk+17e184393@allegromail.pl | OP |
| 1769776067 | ORDER_012 | orrarcher | SITE_006 | 21f7a31e1d065b284f65@members.ebay.com | OC |

最终通常会在需求文档同目录落地 3 个文件：

- `【采购-订单模块】M4X订单管理：查询条件及列表字段调整、新增分配采购员功能_测试场景地图.md`
- `【采购-订单模块】M4X订单管理：查询条件及列表字段调整、新增分配采购员功能_结构化测试用例.md`
- `【采购-订单模块】M4X订单管理：查询条件及列表字段调整、新增分配采购员功能_测试执行清单.md`

## 项目结构

```text
skill_learn/
├── .claude-plugin/              # 插件配置
├── skills/
│   ├── test-case-generator/
│   └── test-data-generator/
├── reference-packs/             # 表结构与样例数据参考包
└── scripts/                     # 仓库级辅助脚本
```

## Skill 结构

每个 Skill 目录通常包含：

| 组件 | 用途 |
| --- | --- |
| `SKILL.md` | 触发条件与工作流程 |
| `scripts/` | 确定性校验或辅助脚本 |
| `references/` | 规则、清单、说明文档 |
| `assets/` | 模板与示例 |

## 添加新 Skill

1. 在 `skills/` 下创建目录
2. 添加 `SKILL.md`
3. 按需补充 `scripts/`、`references/`、`assets/`
4. 如需更新插件元信息，修改 `.claude-plugin/plugin.json`

## 许可

MIT
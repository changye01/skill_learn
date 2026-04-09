#!/usr/bin/env python3
"""validate_test_data.py 的单元测试"""

import pytest

from validate_test_data import main, validate


@pytest.fixture
def tmp_execution_plan(tmp_path):
    """创建临时测试执行清单文件"""

    def _create(content: str) -> str:
        path = tmp_path / "execution-checklist.md"
        path.write_text(content, encoding="utf-8")
        return str(path)

    return _create


class TestValidExecutionChecklist:
    def test_valid_execution_checklist(self, tmp_execution_plan):
        content = """\
# 订单管理测试执行清单

## 输入材料

- 结构化测试用例：`cases.md`
- reference-pack：`reference-packs/`

## TC-001 账号查询命中订单

### 前置条件
- 已存在账号为 `acct_001` 的订单

### 测试步骤
1. 进入订单管理页面
2. 输入账号 `acct_001`
3. 点击查询

### 预期结果
- 返回目标订单

### 测试数据

#### 表：`supplier_order_m4x_task`

| trade_order_code | purchase_site_id |
| --- | --- |
| ORD-001 | acct_001 |

#### 表：`orders`

| orders_code | site_id | orders_status |
| --- | --- | --- |
| ORD-001 | acct_001 | OP |

### 说明
- `supplier_order_m4x_task.trade_order_code = orders.orders_code`

### 待确认项
- 无
"""
        result = validate(tmp_execution_plan(content))
        assert result["issues"] == []
        assert result["has_cases"] is True


class TestMissingFields:
    def test_old_data_checklist_format_is_rejected(self, tmp_execution_plan):
        content = """\
# 订单管理测试数据清单

## 一、基础记录池

### A1 账号查询基础池

#### 表：`supplier_order_m4x_task`

| trade_order_code | purchase_site_id |
| --- | --- |
| ORDER_001 | SITE_001 |

## 二、测试用例清单

## TC-001 账号查询命中订单

### 引用基础记录
- `A1` 中 `ORDER_001`

### 验证点
- 输入账号后可命中该订单
"""
        result = validate(tmp_execution_plan(content))
        assert result["has_cases"] is False
        assert any("测试执行清单" in issue for issue in result["issues"])

    def test_missing_preconditions_section(self, tmp_execution_plan):
        content = """\
# 订单管理测试执行清单

## TC-001 账号查询命中订单

### 测试步骤
1. 输入账号

### 预期结果
- 命中订单

### 测试数据

#### 表：`orders`

| orders_code |
| --- |
| ORD-001 |

### 说明
- 无

### 待确认项
- 无
"""
        result = validate(tmp_execution_plan(content))
        assert any("前置条件" in issue for issue in result["issues"])

    def test_missing_test_data_section(self, tmp_execution_plan):
        content = """\
# 订单管理测试执行清单

## TC-001 账号查询命中订单

### 前置条件
- 已存在订单

### 测试步骤
1. 输入账号

### 预期结果
- 命中订单

### 说明
- 无

### 待确认项
- 无
"""
        result = validate(tmp_execution_plan(content))
        assert any("测试数据" in issue for issue in result["issues"])

    def test_missing_case_sections(self, tmp_execution_plan):
        content = """\
# 订单管理测试执行清单

## 输入材料

- 结构化测试用例：`cases.md`
"""
        result = validate(tmp_execution_plan(content))
        assert result["has_cases"] is False
        assert any("至少包含一条" in issue for issue in result["issues"])

    def test_rejects_when_title_is_not_execution_checklist(self, tmp_execution_plan):
        content = """\
# 订单管理执行稿

这里提到测试执行清单，但标题不是正式名称。

## TC-001 账号查询命中订单

### 前置条件
- 已存在订单

### 测试步骤
1. 输入账号

### 预期结果
- 命中订单

### 测试数据

#### 表：`orders`

| orders_code |
| --- |
| ORD-001 |

### 说明
- 无

### 待确认项
- 无
"""
        result = validate(tmp_execution_plan(content))
        assert result["has_cases"] is False
        assert any("标题" in issue for issue in result["issues"])

    def test_rejects_when_test_data_has_no_table(self, tmp_execution_plan):
        content = """\
# 订单管理测试执行清单

## TC-001 账号查询命中订单

### 前置条件
- 已存在订单

### 测试步骤
1. 输入账号

### 预期结果
- 命中订单

### 测试数据

#### 表：`orders`

- 只有表标题，没有 Markdown 表格

### 说明
- 无

### 待确认项
- 无
"""
        result = validate(tmp_execution_plan(content))
        assert any("Markdown 表格" in issue for issue in result["issues"])


class TestFileErrors:
    def test_file_not_found(self):
        with pytest.raises(SystemExit) as exc_info:
            validate("/nonexistent/path/execution-checklist.md")
        assert exc_info.value.code == 2

    def test_main_rejects_extra_argument(self, monkeypatch, capsys, tmp_execution_plan):
        path = tmp_execution_plan("# demo")
        monkeypatch.setattr("sys.argv", ["validate_test_data.py", path, "extra.md"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        captured = capsys.readouterr()
        assert exc_info.value.code == 1
        assert "用法" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

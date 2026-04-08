#!/usr/bin/env python3
"""validate_test_data.py 的单元测试"""

import pytest

from validate_test_data import main, validate


@pytest.fixture
def tmp_data_plan(tmp_path):
    """创建临时测试数据设计文件"""

    def _create(content: str) -> str:
        path = tmp_path / "data-plan.md"
        path.write_text(content, encoding="utf-8")
        return str(path)

    return _create


class TestValidDataPlan:
    def test_valid_checklist_document(self, tmp_data_plan):
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

## TC-002 状态查询命中订单

### 引用基础记录
- `A1` 中 `ORDER_001`

### 验证点
- 选择状态后可命中该订单

## 三、待确认项

- 无
"""
        result = validate(tmp_data_plan(content))
        assert result["issues"] == []
        assert result["has_cases"] is True

class TestMissingFields:
    def test_old_table_format_is_rejected(self, tmp_data_plan):
        content = """\
# 订单管理测试数据设计

## 测试数据设计

| 编号 | 测试用例编号 | 数据目标 | 涉及表 | 关键字段 | 建议取值/样例来源 | 数据操作 | 关联关系 | 备注/待确认项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TD-001 | TC-001 | 构造可按账号筛选的订单 | supplier_order_m4x_task, orders | trade_order_code, purchase_site_id | 参考样例数据 | 预置 | 任务表关联订单表 | 无 |
"""
        result = validate(tmp_data_plan(content))
        assert result["has_cases"] is False
        assert any("仅支持" in issue for issue in result["issues"])

    def test_checklist_missing_base_pool_section(self, tmp_data_plan):
        content = """\
# 订单管理测试数据清单

## 二、测试用例清单

## TC-001 账号查询命中订单

### 引用基础记录
- `A1` 中 `ORDER_001`

### 验证点
- 输入账号后可命中该订单

## 三、待确认项

- 无
"""
        result = validate(tmp_data_plan(content))
        assert any("基础记录池" in issue for issue in result["issues"])

    def test_checklist_missing_reference_section(self, tmp_data_plan):
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

### 验证点
- 输入账号后可命中该订单

## 三、待确认项

- 无
"""
        result = validate(tmp_data_plan(content))
        assert any("引用基础记录" in issue for issue in result["issues"])

class TestFileErrors:
    def test_file_not_found(self):
        with pytest.raises(SystemExit) as exc_info:
            validate("/nonexistent/path/data-plan.md")
        assert exc_info.value.code == 2

    def test_main_rejects_extra_csv_argument(self, monkeypatch, capsys, tmp_data_plan):
        path = tmp_data_plan("# demo")
        monkeypatch.setattr("sys.argv", ["validate_test_data.py", path, "data-checklist.csv"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        captured = capsys.readouterr()
        assert exc_info.value.code == 1
        assert "用法" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

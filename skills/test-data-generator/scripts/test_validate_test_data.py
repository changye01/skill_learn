#!/usr/bin/env python3
"""validate_test_data.py 的单元测试"""

import pytest

from validate_test_data import validate


@pytest.fixture
def tmp_data_plan(tmp_path):
    """创建临时测试数据设计文件"""

    def _create(content: str) -> str:
        path = tmp_path / "data-plan.md"
        path.write_text(content, encoding="utf-8")
        return str(path)

    return _create


class TestValidDataPlan:
    def test_valid_document(self, tmp_data_plan):
        content = """\
# 订单管理测试数据设计

## 测试数据设计

| 编号 | 测试用例编号 | 数据目标 | 涉及表 | 关键字段 | 建议取值/样例来源 | 数据操作 | 关联关系 | 备注/待确认项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TD-001 | TC-001 | 构造可按账号筛选的订单 | supplier_order_m4x_task, orders | trade_order_code, purchase_site_id, site_id | 参考 `table_samples/supplier_order_m4x_task.csv` 与 `table_samples/orders.csv` | 预置 | `supplier_order_m4x_task.trade_order_code -> orders.orders_code` | 无 |
"""
        result = validate(tmp_data_plan(content))
        assert result["issues"] == []
        assert result["has_cases"] is True


class TestMissingFields:
    def test_missing_key_field_column(self, tmp_data_plan):
        content = """\
| 编号 | 测试用例编号 | 数据目标 | 涉及表 | 建议取值/样例来源 | 数据操作 | 关联关系 | 备注/待确认项 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TD-001 | TC-001 | 构造可按账号筛选的订单 | supplier_order_m4x_task, orders | 参考样例数据 | 预置 | 任务表关联订单表 | 无 |
"""
        result = validate(tmp_data_plan(content))
        assert any("关键字段" in issue for issue in result["issues"])

    def test_missing_relation_and_todo_section(self, tmp_data_plan):
        content = """\
| 编号 | 测试用例编号 | 数据目标 | 涉及表 | 关键字段 | 建议取值/样例来源 | 数据操作 |
| --- | --- | --- | --- | --- | --- | --- |
| TD-001 | TC-001 | 构造可按账号筛选的订单 | supplier_order_m4x_task, orders | trade_order_code, purchase_site_id | 参考样例数据 | 预置 |
"""
        result = validate(tmp_data_plan(content))
        assert any("关联关系" in issue for issue in result["issues"])
        assert any("备注/待确认项" in issue for issue in result["issues"])

    def test_missing_table_rows(self, tmp_data_plan):
        content = """\
# 订单管理测试数据设计

## 测试数据设计

| 编号 | 测试用例编号 | 数据目标 | 涉及表 | 关键字段 | 建议取值/样例来源 | 数据操作 | 关联关系 | 备注/待确认项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
"""
        result = validate(tmp_data_plan(content))
        assert result["has_cases"] is False
        assert any("至少一条" in issue for issue in result["issues"])


class TestFileErrors:
    def test_file_not_found(self):
        with pytest.raises(SystemExit) as exc_info:
            validate("/nonexistent/path/data-plan.md")
        assert exc_info.value.code == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

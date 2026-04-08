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


@pytest.fixture
def tmp_data_bundle(tmp_path):
    """创建临时测试数据设计 Markdown + CSV 清单"""

    def _create(md_content: str, csv_content: str | None = None) -> tuple[str, str]:
        md_path = tmp_path / "data-plan.md"
        csv_path = tmp_path / "data-checklist.csv"
        md_path.write_text(md_content, encoding="utf-8")
        if csv_content is not None:
            csv_path.write_text(csv_content, encoding="utf-8")
        return str(md_path), str(csv_path)

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

    def test_valid_document_with_matching_csv(self, tmp_data_bundle):
        md_content = """\
# 订单管理测试数据设计

## 测试数据设计

| 编号 | 测试用例编号 | 数据目标 | 涉及表 | 关键字段 | 建议取值/样例来源 | 数据操作 | 关联关系 | 备注/待确认项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TD-001 | TC-001 | 构造可按账号筛选的订单 | supplier_order_m4x_task, orders | trade_order_code, purchase_site_id, site_id | 参考 `table_samples/supplier_order_m4x_task.csv` 与 `table_samples/orders.csv` | 预置 | `supplier_order_m4x_task.trade_order_code -> orders.orders_code` | 无 |
"""
        csv_content = """\
测试用例编号,测试功能点,数据目标,涉及表,关键字段,建议数据值,样例来源,数据准备方式,验证方式,备注/待确认项
TC-001,账号查询,构造可按账号筛选的订单,"supplier_order_m4x_task, orders","trade_order_code, purchase_site_id, site_id",purchase_site_id=SITE_001,table_samples/orders.csv: ORDER_001,直接复用,列表按账号查询应命中该记录,无
"""
        md_path, csv_path = tmp_data_bundle(md_content, csv_content)
        result = validate(md_path, csv_path)
        assert result["issues"] == []
        assert result["has_matching_csv"] is True

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

    def test_valid_checklist_document_with_matching_csv(self, tmp_data_bundle):
        md_content = """\
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
        csv_content = """\
测试用例编号,测试功能点,数据目标,涉及表,关键字段,建议数据值,样例来源,数据准备方式,验证方式,备注/待确认项
TC-001,账号查询,构造可按账号筛选的订单,supplier_order_m4x_task,purchase_site_id,purchase_site_id=SITE_001,table_samples/supplier_order_m4x_task.csv: ORDER_001,直接复用,列表按账号查询应命中该记录,无
TC-002,状态查询,构造状态可筛选的订单,orders,orders_status,orders_status=OP,table_samples/orders.csv: ORDER_001,直接复用,列表按状态查询应命中该记录,无
"""
        md_path, csv_path = tmp_data_bundle(md_content, csv_content)
        result = validate(md_path, csv_path)
        assert result["issues"] == []
        assert result["has_matching_csv"] is True


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

    def test_csv_header_mismatch(self, tmp_data_bundle):
        md_content = """\
# 订单管理测试数据设计

## 测试数据设计

| 编号 | 测试用例编号 | 数据目标 | 涉及表 | 关键字段 | 建议取值/样例来源 | 数据操作 | 关联关系 | 备注/待确认项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TD-001 | TC-001 | 构造可按账号筛选的订单 | supplier_order_m4x_task, orders | trade_order_code, purchase_site_id, site_id | 参考 `table_samples/supplier_order_m4x_task.csv` 与 `table_samples/orders.csv` | 预置 | `supplier_order_m4x_task.trade_order_code -> orders.orders_code` | 无 |
"""
        csv_content = """\
测试用例编号,测试功能点,涉及表,关键字段,建议数据值,样例来源,数据准备方式,验证方式,备注/待确认项
TC-001,账号查询,"supplier_order_m4x_task, orders","trade_order_code, purchase_site_id, site_id",purchase_site_id=SITE_001,table_samples/orders.csv: ORDER_001,直接复用,列表按账号查询应命中该记录,无
"""
        md_path, csv_path = tmp_data_bundle(md_content, csv_content)
        result = validate(md_path, csv_path)
        assert any("CSV" in issue and "列头" in issue for issue in result["issues"])

    def test_csv_case_id_mismatch(self, tmp_data_bundle):
        md_content = """\
# 订单管理测试数据设计

## 测试数据设计

| 编号 | 测试用例编号 | 数据目标 | 涉及表 | 关键字段 | 建议取值/样例来源 | 数据操作 | 关联关系 | 备注/待确认项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TD-001 | TC-001 | 构造可按账号筛选的订单 | supplier_order_m4x_task, orders | trade_order_code, purchase_site_id, site_id | 参考 `table_samples/supplier_order_m4x_task.csv` 与 `table_samples/orders.csv` | 预置 | `supplier_order_m4x_task.trade_order_code -> orders.orders_code` | 无 |
"""
        csv_content = """\
测试用例编号,测试功能点,数据目标,涉及表,关键字段,建议数据值,样例来源,数据准备方式,验证方式,备注/待确认项
TC-002,账号查询,构造可按账号筛选的订单,"supplier_order_m4x_task, orders","trade_order_code, purchase_site_id, site_id",purchase_site_id=SITE_001,table_samples/orders.csv: ORDER_001,直接复用,列表按账号查询应命中该记录,无
"""
        md_path, csv_path = tmp_data_bundle(md_content, csv_content)
        result = validate(md_path, csv_path)
        assert any("测试用例编号集合" in issue for issue in result["issues"])

    def test_csv_missing_validation_column(self, tmp_data_bundle):
        md_content = """\
# 订单管理测试数据设计

## 测试数据设计

| 编号 | 测试用例编号 | 数据目标 | 涉及表 | 关键字段 | 建议取值/样例来源 | 数据操作 | 关联关系 | 备注/待确认项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TD-001 | TC-001 | 构造可按账号筛选的订单 | supplier_order_m4x_task, orders | trade_order_code, purchase_site_id, site_id | 参考 `table_samples/supplier_order_m4x_task.csv` 与 `table_samples/orders.csv` | 预置 | `supplier_order_m4x_task.trade_order_code -> orders.orders_code` | 无 |
"""
        csv_content = """\
测试用例编号,测试功能点,数据目标,涉及表,关键字段,建议数据值,样例来源,数据准备方式,备注/待确认项
TC-001,账号查询,构造可按账号筛选的订单,"supplier_order_m4x_task, orders","trade_order_code, purchase_site_id, site_id",purchase_site_id=SITE_001,table_samples/orders.csv: ORDER_001,直接复用,无
"""
        md_path, csv_path = tmp_data_bundle(md_content, csv_content)
        result = validate(md_path, csv_path)
        assert any("验证方式" in issue for issue in result["issues"])


class TestFileErrors:
    def test_file_not_found(self):
        with pytest.raises(SystemExit) as exc_info:
            validate("/nonexistent/path/data-plan.md")
        assert exc_info.value.code == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

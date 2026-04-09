#!/usr/bin/env python3
"""validate_cases.py 的单元测试"""

import pytest

from validate_cases import validate


@pytest.fixture
def tmp_cases(tmp_path):
    """创建临时测试用例文件"""

    def _create(content: str) -> str:
        path = tmp_path / "cases.md"
        path.write_text(content, encoding="utf-8")
        return str(path)

    return _create


class TestValidCases:
    """结构完整的测试用例文档"""

    def test_valid_document(self, tmp_cases):
        content = """\
# 订单管理测试用例

## 结构化测试用例

| 编号 | 测试功能点 | 前置条件 | 测试步骤 | 预期结果 |
| --- | --- | --- | --- | --- |
| TC-001 | 综合场景：完整流程验证 | 存在可操作订单 | 进入列表并修改采购员 | 修改成功且日志正确 |
"""
        result = validate(tmp_cases(content))
        assert result["issues"] == []
        assert result["has_e2e"]

    def test_valid_grouped_document(self, tmp_cases):
        content = """\
# 订单管理测试用例

## 场景组1：查询条件

| 编号 | 测试功能点 | 前置条件 | 测试步骤 | 预期结果 |
| --- | --- | --- | --- | --- |
| TC-001 | 账号查询命中 | 已存在账号订单 | 输入账号并查询 | 返回匹配订单 |

## 场景组2：综合场景

| 编号 | 测试功能点 | 前置条件 | 测试步骤 | 预期结果 |
| --- | --- | --- | --- | --- |
| TC-002 | 综合场景：完整流程验证 | 存在可操作订单 | 查询后分配采购员并校验日志 | 修改成功且日志正确 |
"""
        result = validate(tmp_cases(content))
        assert result["issues"] == []
        assert result["has_e2e"] is True


class TestMissingFields:
    """缺少关键字段"""

    def test_missing_expected_result(self, tmp_cases):
        content = """\
| 编号 | 测试功能点 | 前置条件 | 测试步骤 |
| --- | --- | --- | --- |
| TC-001 | 综合场景：查询条件 | 已存在测试数据 | 输入账号搜索 |
"""
        result = validate(tmp_cases(content))
        assert any("预期结果" in issue for issue in result["issues"])

    def test_missing_end_to_end_group(self, tmp_cases):
        content = """\
| 编号 | 测试功能点 | 前置条件 | 测试步骤 | 预期结果 |
| --- | --- | --- | --- | --- |
| TC-001 | 查询条件 | 已存在测试数据 | 输入账号搜索 | 返回匹配数据 |
"""
        result = validate(tmp_cases(content))
        assert result["has_e2e"] is False
        assert any("综合场景" in issue or "端到端" in issue for issue in result["issues"])

    def test_e2e_keyword_only_in_body_text_does_not_count(self, tmp_cases):
        content = """\
# 订单管理测试用例

## 结构化测试用例

综合场景说明：这里仅是背景描述，不代表真正存在综合场景用例。

| 编号 | 测试功能点 | 前置条件 | 测试步骤 | 预期结果 |
| --- | --- | --- | --- | --- |
| TC-001 | 查询条件 | 已存在测试数据 | 输入账号搜索 | 返回匹配数据 |
"""
        result = validate(tmp_cases(content))
        assert result["has_e2e"] is False
        assert any("综合场景" in issue or "端到端" in issue for issue in result["issues"])


class TestFileErrors:
    """文件异常场景"""

    def test_file_not_found(self):
        with pytest.raises(SystemExit) as exc_info:
            validate("/nonexistent/path/cases.md")
        assert exc_info.value.code == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

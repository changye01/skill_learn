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


@pytest.fixture
def tmp_case_bundle(tmp_path):
    """创建 Markdown + CSV 配套输出"""

    def _create(md_content: str, csv_content: str | None = None) -> tuple[str, str]:
        md_path = tmp_path / "cases.md"
        csv_path = tmp_path / "cases.csv"
        md_path.write_text(md_content, encoding="utf-8")
        if csv_content is not None:
            csv_path.write_text(csv_content, encoding="utf-8")
        return str(md_path), str(csv_path)

    return _create


class TestValidCases:
    """结构完整的测试用例文档"""

    def test_valid_document(self, tmp_case_bundle):
        md_content = """\
# 订单管理测试用例

## 结构化测试用例

| 编号 | 测试功能点 | 前置条件 | 测试步骤 | 预期结果 |
| --- | --- | --- | --- | --- |
| TC-001 | 综合场景：完整流程验证 | 存在可操作订单 | 进入列表并修改采购员 | 修改成功且日志正确 |
"""
        csv_content = """\
编号,测试功能点,前置条件,测试步骤,预期结果
TC-001,综合场景：完整流程验证,存在可操作订单,进入列表并修改采购员,修改成功且日志正确
"""
        md_path, _ = tmp_case_bundle(md_content, csv_content)
        result = validate(md_path)
        assert result["issues"] == []
        assert result["has_e2e"]
        assert result["has_matching_csv"] is True

    def test_valid_document_with_matching_csv(self, tmp_case_bundle):
        md_content = """\
# 订单管理测试用例

## 结构化测试用例

| 编号 | 测试功能点 | 前置条件 | 测试步骤 | 预期结果 |
| --- | --- | --- | --- | --- |
| TC-001 | 综合场景：完整流程验证 | 存在可操作订单 | 进入列表并修改采购员 | 修改成功且日志正确 |
"""
        csv_content = """\
编号,测试功能点,前置条件,测试步骤,预期结果
TC-001,综合场景：完整流程验证,存在可操作订单,进入列表并修改采购员,修改成功且日志正确
"""
        md_path, csv_path = tmp_case_bundle(md_content, csv_content)
        result = validate(md_path, csv_path)
        assert result["issues"] == []
        assert result["has_matching_csv"] is True

    def test_valid_document_with_utf8_bom_csv(self, tmp_case_bundle):
        md_content = """\
# 订单管理测试用例

## 结构化测试用例

| 编号 | 测试功能点 | 前置条件 | 测试步骤 | 预期结果 |
| --- | --- | --- | --- | --- |
| TC-001 | 综合场景：完整流程验证 | 存在可操作订单 | 进入列表并修改采购员 | 修改成功且日志正确 |
"""
        csv_content = "\ufeff编号,测试功能点,前置条件,测试步骤,预期结果\nTC-001,综合场景：完整流程验证,存在可操作订单,进入列表并修改采购员,修改成功且日志正确\n"
        md_path, csv_path = tmp_case_bundle(md_content, csv_content)
        result = validate(md_path, csv_path)
        assert result["issues"] == []
        assert result["has_matching_csv"] is True

    def test_valid_document_with_default_biaogeban_csv_name(self, tmp_path):
        md_path = tmp_path / "订单管理_结构化测试用例.md"
        csv_path = tmp_path / "订单管理_表格版用例.csv"
        md_path.write_text(
            """\
# 订单管理测试用例

## 结构化测试用例

| 编号 | 测试功能点 | 前置条件 | 测试步骤 | 预期结果 |
| --- | --- | --- | --- | --- |
| TC-001 | 综合场景：完整流程验证 | 存在可操作订单 | 进入列表并修改采购员 | 修改成功且日志正确 |
""",
            encoding="utf-8",
        )
        csv_path.write_text(
            """\
编号,测试功能点,前置条件,测试步骤,预期结果
TC-001,综合场景：完整流程验证,存在可操作订单,进入列表并修改采购员,修改成功且日志正确
""",
            encoding="utf-8",
        )

        result = validate(str(md_path))
        assert result["issues"] == []
        assert result["has_matching_csv"] is True

    def test_valid_grouped_document(self, tmp_case_bundle):
        md_content = """\
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
        csv_content = """\
编号,测试功能点,前置条件,测试步骤,预期结果
TC-001,账号查询命中,已存在账号订单,输入账号并查询,返回匹配订单
TC-002,综合场景：完整流程验证,存在可操作订单,查询后分配采购员并校验日志,修改成功且日志正确
"""
        md_path, csv_path = tmp_case_bundle(md_content, csv_content)
        result = validate(md_path, csv_path)
        assert result["issues"] == []
        assert result["has_e2e"] is True
        assert result["has_matching_csv"] is True


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

    def test_e2e_keyword_only_in_body_text_does_not_count(self, tmp_case_bundle):
        md_content = """\
# 订单管理测试用例

## 结构化测试用例

综合场景说明：这里仅是背景描述，不代表真正存在综合场景用例。

| 编号 | 测试功能点 | 前置条件 | 测试步骤 | 预期结果 |
| --- | --- | --- | --- | --- |
| TC-001 | 查询条件 | 已存在测试数据 | 输入账号搜索 | 返回匹配数据 |
"""
        csv_content = """\
编号,测试功能点,前置条件,测试步骤,预期结果
TC-001,查询条件,已存在测试数据,输入账号搜索,返回匹配数据
"""
        md_path, csv_path = tmp_case_bundle(md_content, csv_content)
        result = validate(md_path, csv_path)
        assert result["has_e2e"] is False
        assert any("综合场景" in issue or "端到端" in issue for issue in result["issues"])

    def test_csv_header_mismatch(self, tmp_case_bundle):
        md_content = """\
# 订单管理测试用例

## 结构化测试用例

| 编号 | 测试功能点 | 前置条件 | 测试步骤 | 预期结果 |
| --- | --- | --- | --- | --- |
| TC-001 | 综合场景：完整流程验证 | 存在可操作订单 | 进入列表并修改采购员 | 修改成功且日志正确 |
"""
        csv_content = """\
编号,测试功能点,测试步骤,预期结果
TC-001,综合场景：完整流程验证,进入列表并修改采购员,修改成功且日志正确
"""
        md_path, csv_path = tmp_case_bundle(md_content, csv_content)
        result = validate(md_path, csv_path)
        assert any("CSV" in issue and "列头" in issue for issue in result["issues"])

    def test_csv_case_id_mismatch(self, tmp_case_bundle):
        md_content = """\
# 订单管理测试用例

## 结构化测试用例

| 编号 | 测试功能点 | 前置条件 | 测试步骤 | 预期结果 |
| --- | --- | --- | --- | --- |
| TC-001 | 综合场景：完整流程验证 | 存在可操作订单 | 进入列表并修改采购员 | 修改成功且日志正确 |
"""
        csv_content = """\
编号,测试功能点,前置条件,测试步骤,预期结果
TC-002,综合场景：完整流程验证,存在可操作订单,进入列表并修改采购员,修改成功且日志正确
"""
        md_path, csv_path = tmp_case_bundle(md_content, csv_content)
        result = validate(md_path, csv_path)
        assert any("编号集合" in issue for issue in result["issues"])

    def test_requires_matching_csv_when_markdown_exists_alone(self, tmp_cases):
        content = """\
# 订单管理测试用例

## 结构化测试用例

| 编号 | 测试功能点 | 前置条件 | 测试步骤 | 预期结果 |
| --- | --- | --- | --- | --- |
| TC-001 | 综合场景：完整流程验证 | 存在可操作订单 | 进入列表并修改采购员 | 修改成功且日志正确 |
"""
        result = validate(tmp_cases(content))
        assert any("CSV" in issue for issue in result["issues"])


class TestFileErrors:
    """文件异常场景"""

    def test_file_not_found(self):
        with pytest.raises(SystemExit) as exc_info:
            validate("/nonexistent/path/cases.md")
        assert exc_info.value.code == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

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

需求名称: M4X 订单管理需求 26668

## 结构化测试用例

### TC-001
- 用例编号: TC-001
- 模块: 订单管理
- 场景组: 综合场景
- 用例标题: 完整流程验证
- 关联需求点: 分配采购员
- 前置条件: 存在可操作订单
- 测试步骤: 进入列表并修改采购员
- 预期结果: 修改成功且日志正确
- 优先级: P1
"""
        result = validate(tmp_cases(content))
        assert result["issues"] == []
        assert result["has_e2e"]


class TestMissingFields:
    """缺少关键字段"""

    def test_missing_expected_result(self, tmp_cases):
        content = """\
需求名称: 示例需求
- 场景组: 综合场景
- 关联需求点: 查询条件
- 测试步骤: 输入账号搜索
- 优先级: P1
"""
        result = validate(tmp_cases(content))
        assert any("预期结果" in issue for issue in result["issues"])

    def test_missing_end_to_end_group(self, tmp_cases):
        content = """\
需求名称: 示例需求
- 场景组: 查询条件
- 关联需求点: 查询条件
- 测试步骤: 输入账号搜索
- 预期结果: 返回匹配数据
- 优先级: P1
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

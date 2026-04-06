#!/usr/bin/env python3
"""检查测试数据设计文档的结构完整性。"""

import sys


REQUIRED_KEYWORDS = [
    "编号",
    "测试用例编号",
    "数据目标",
    "涉及表",
    "关键字段",
    "建议取值/样例来源",
    "数据操作",
    "关联关系",
    "备注/待确认项",
]


def _read_markdown(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误：文件不存在 - {filepath}")
        sys.exit(2)


def _extract_plan_ids(content: str) -> list[str]:
    data_ids = []

    for line in content.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if "---" in stripped:
            continue

        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or cells[0] in {"编号", "{{DATA_ID}}", ""}:
            continue
        data_ids.append(cells[0])

    return data_ids


def validate(filepath: str) -> dict:
    """验证测试数据设计文档，返回统计信息和问题列表。"""
    content = _read_markdown(filepath)
    issues = []

    for keyword in REQUIRED_KEYWORDS:
        if keyword not in content:
            issues.append(f"缺少必填字段：{keyword}")

    plan_ids = _extract_plan_ids(content)
    has_cases = bool(plan_ids)
    if not has_cases:
        issues.append("测试数据设计至少一条数据设计记录")

    return {
        "issues": issues,
        "has_cases": has_cases,
    }


def main():
    if len(sys.argv) != 2:
        print("用法: python validate_test_data.py <测试数据设计文件路径>")
        print("示例: python validate_test_data.py data-plan.md")
        sys.exit(1)

    filepath = sys.argv[1]
    result = validate(filepath)

    if result["issues"]:
        print("发现以下问题：")
        for issue in result["issues"]:
            print(f"- {issue}")
        sys.exit(1)

    print("✅ 测试数据设计文档结构完整")
    sys.exit(0)


if __name__ == "__main__":
    main()

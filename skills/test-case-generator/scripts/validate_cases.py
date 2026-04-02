#!/usr/bin/env python3
"""检查结构化测试用例文档的完整性。"""

import sys


REQUIRED_KEYWORDS = [
    "需求名称",
    "场景组",
    "关联需求点",
    "测试步骤",
    "预期结果",
    "优先级",
]

E2E_KEYWORDS = [
    "综合场景",
    "端到端",
]


def validate(filepath: str) -> dict:
    """验证测试用例文档，返回统计信息和问题列表。"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"错误：文件不存在 - {filepath}")
        sys.exit(2)

    issues = []

    for keyword in REQUIRED_KEYWORDS:
        if keyword not in content:
            issues.append(f"缺少必填字段：{keyword}")

    has_e2e = any(keyword in content for keyword in E2E_KEYWORDS)
    if not has_e2e:
        issues.append("缺少综合场景或端到端场景")

    return {
        "issues": issues,
        "has_e2e": has_e2e,
    }


def main():
    if len(sys.argv) != 2:
        print("用法: python validate_cases.py <测试用例文件路径>")
        print("示例: python validate_cases.py cases.md")
        sys.exit(1)

    filepath = sys.argv[1]
    result = validate(filepath)

    if result["issues"]:
        print("发现以下问题：")
        for issue in result["issues"]:
            print(f"- {issue}")
        sys.exit(1)

    print("✅ 测试用例文档结构完整")
    sys.exit(0)


if __name__ == "__main__":
    main()

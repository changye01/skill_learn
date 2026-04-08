#!/usr/bin/env python3
"""检查测试数据清单 Markdown 的结构完整性。"""

import re
import sys


CHECKLIST_REQUIRED_KEYWORDS = [
    "基础记录池",
    "测试用例清单",
    "引用基础记录",
    "验证点",
    "待确认项",
]

def _read_markdown(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误：文件不存在 - {filepath}")
        sys.exit(2)


def _extract_case_ids_from_checklist(content: str) -> list[str]:
    return re.findall(r"^##\s+(TC-[^\s]+)", content, flags=re.MULTILINE)


def _split_checklist_case_blocks(content: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^##\s+(TC-[^\s]+).*$", content, flags=re.MULTILINE))
    blocks = []

    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        blocks.append((match.group(1), content[start:end]))

    return blocks


def _validate_checklist_format(content: str, issues: list[str]) -> tuple[bool, list[str]]:
    for keyword in CHECKLIST_REQUIRED_KEYWORDS:
        if keyword not in content:
            issues.append(f"缺少必填字段：{keyword}")

    case_blocks = _split_checklist_case_blocks(content)
    case_ids = [case_id for case_id, _ in case_blocks]
    has_cases = bool(case_ids)
    if not has_cases:
        issues.append("测试数据清单至少包含一条测试用例记录")
        return has_cases, case_ids

    for case_id, block in case_blocks:
        if "### 引用基础记录" not in block:
            issues.append(f"{case_id} 缺少“引用基础记录”小节")
        if "### 验证点" not in block:
            issues.append(f"{case_id} 缺少“验证点”小节")

    return has_cases, case_ids


def validate(filepath: str) -> dict:
    """验证测试数据清单 Markdown，返回统计信息和问题列表。"""
    content = _read_markdown(filepath)
    issues = []

    if "测试数据清单" not in content:
        issues.append("当前仅支持新版《测试数据清单.md》格式，不再支持旧版表格稿")
        return {
            "issues": issues,
            "has_cases": False,
        }

    has_cases, case_ids = _validate_checklist_format(content, issues)

    return {
        "issues": issues,
        "has_cases": has_cases,
    }


def main():
    if len(sys.argv) != 2:
        print("用法: python validate_test_data.py <测试数据Markdown路径>")
        print("示例: python validate_test_data.py data-checklist.md")
        sys.exit(1)

    filepath = sys.argv[1]
    result = validate(filepath)

    if result["issues"]:
        print("发现以下问题：")
        for issue in result["issues"]:
            print(f"- {issue}")
        sys.exit(1)

    print("✅ 测试数据清单 Markdown 结构完整")
    sys.exit(0)


if __name__ == "__main__":
    main()

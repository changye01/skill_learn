#!/usr/bin/env python3
"""检查结构化测试用例文档的完整性。"""

import sys


REQUIRED_KEYWORDS = [
    "编号",
    "测试功能点",
    "前置条件",
    "测试步骤",
    "预期结果",
]

E2E_KEYWORDS = [
    "综合场景",
    "端到端",
]


def _read_markdown(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误：文件不存在 - {filepath}")
        sys.exit(2)


def _extract_markdown_case_ids(content: str) -> list[str]:
    return [row["编号"] for row in _extract_markdown_case_rows(content)]


def _parse_markdown_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _is_markdown_separator(line: str) -> bool:
    cells = _parse_markdown_cells(line)
    return bool(cells) and all(cell and set(cell) <= {":", "-"} for cell in cells)


def _extract_markdown_case_rows(content: str) -> list[dict[str, str]]:
    rows = []
    lines = content.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index].strip()
        if _parse_markdown_cells(line) != REQUIRED_KEYWORDS:
            index += 1
            continue

        if index + 1 >= len(lines) or not _is_markdown_separator(lines[index + 1].strip()):
            index += 1
            continue

        index += 2
        while index < len(lines):
            stripped = lines[index].strip()
            if not stripped.startswith("|"):
                break

            cells = _parse_markdown_cells(stripped)
            if len(cells) != len(REQUIRED_KEYWORDS):
                break

            if cells[0] not in {"编号", "{{CASE_ID}}", ""}:
                rows.append(dict(zip(REQUIRED_KEYWORDS, cells, strict=False)))
            index += 1

    return rows


def validate(filepath: str) -> dict:
    """验证测试用例文档，返回统计信息和问题列表。"""
    content = _read_markdown(filepath)
    issues = []

    for keyword in REQUIRED_KEYWORDS:
        if keyword not in content:
            issues.append(f"缺少必填字段：{keyword}")

    markdown_case_rows = _extract_markdown_case_rows(content)
    markdown_case_ids = [row["编号"] for row in markdown_case_rows]
    has_e2e = any(
        any(keyword in row["测试功能点"] for keyword in E2E_KEYWORDS)
        for row in markdown_case_rows
    )
    if not has_e2e:
        issues.append("缺少综合场景或端到端场景")

    return {
        "issues": issues,
        "has_e2e": has_e2e,
        "case_count": len(markdown_case_ids),
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

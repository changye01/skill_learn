#!/usr/bin/env python3
"""检查结构化测试用例文档的完整性。"""

import csv
import sys
from pathlib import Path


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
    case_ids = []

    for line in content.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if "---" in stripped:
            continue

        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or cells[0] in {"编号", "{{CASE_ID}}", ""}:
            continue
        case_ids.append(cells[0])

    return case_ids


def _resolve_csv_path(markdown_path: str, csv_path: str | None) -> str | None:
    if csv_path:
        return csv_path

    inferred = Path(markdown_path).with_suffix(".csv")
    if inferred.exists():
        return str(inferred)

    return None


def _read_csv_rows(filepath: str) -> tuple[list[str], list[dict[str, str]]]:
    try:
        with open(filepath, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            rows = list(reader)
            return headers, rows
    except FileNotFoundError:
        return [], []


def validate(filepath: str, csv_filepath: str | None = None) -> dict:
    """验证测试用例文档，返回统计信息和问题列表。"""
    content = _read_markdown(filepath)
    issues = []

    for keyword in REQUIRED_KEYWORDS:
        if keyword not in content:
            issues.append(f"缺少必填字段：{keyword}")

    markdown_case_ids = _extract_markdown_case_ids(content)
    has_e2e = any(keyword in content for keyword in E2E_KEYWORDS)
    if not has_e2e:
        issues.append("缺少综合场景或端到端场景")

    resolved_csv = _resolve_csv_path(filepath, csv_filepath)
    has_matching_csv = False

    if resolved_csv:
        csv_headers, csv_rows = _read_csv_rows(resolved_csv)
        if not csv_headers and not csv_rows:
            issues.append(f"CSV 文件不存在：{resolved_csv}")
        else:
            if csv_headers != REQUIRED_KEYWORDS:
                issues.append(
                    "CSV 列头不匹配，应为："
                    + " / ".join(REQUIRED_KEYWORDS)
                )

            csv_case_ids = [row.get("编号", "").strip() for row in csv_rows if row.get("编号")]
            if markdown_case_ids != csv_case_ids:
                issues.append("CSV 与 Markdown 的编号集合或顺序不一致")

            if csv_headers == REQUIRED_KEYWORDS and markdown_case_ids == csv_case_ids:
                has_matching_csv = True

    return {
        "issues": issues,
        "has_e2e": has_e2e,
        "has_matching_csv": has_matching_csv,
    }


def main():
    if len(sys.argv) not in {2, 3}:
        print("用法: python validate_cases.py <测试用例文件路径> [CSV 文件路径]")
        print("示例: python validate_cases.py cases.md")
        print("示例: python validate_cases.py cases.md cases.csv")
        sys.exit(1)

    filepath = sys.argv[1]
    csv_filepath = sys.argv[2] if len(sys.argv) == 3 else None
    result = validate(filepath, csv_filepath)

    if result["issues"]:
        print("发现以下问题：")
        for issue in result["issues"]:
            print(f"- {issue}")
        sys.exit(1)

    if result["has_matching_csv"]:
        print("✅ 测试用例文档结构完整，且 CSV 与 Markdown 一致")
    else:
        print("✅ 测试用例文档结构完整")
    sys.exit(0)


if __name__ == "__main__":
    main()

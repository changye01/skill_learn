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


def _candidate_csv_paths(markdown_path: str) -> list[Path]:
    path = Path(markdown_path)
    candidates = [path.with_suffix(".csv")]

    if "结构化测试用例" in path.stem:
        alt_name = f"{path.stem.replace('结构化测试用例', '表格版用例')}.csv"
        alt_path = path.with_name(alt_name)
        if alt_path not in candidates:
            candidates.append(alt_path)

    return candidates


def _resolve_csv_path(markdown_path: str, csv_path: str | None) -> str | None:
    if csv_path:
        return csv_path

    for candidate in _candidate_csv_paths(markdown_path):
        if candidate.exists():
            return str(candidate)

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

    markdown_case_rows = _extract_markdown_case_rows(content)
    markdown_case_ids = [row["编号"] for row in markdown_case_rows]
    has_e2e = any(
        any(keyword in row["测试功能点"] for keyword in E2E_KEYWORDS)
        for row in markdown_case_rows
    )
    if not has_e2e:
        issues.append("缺少综合场景或端到端场景")

    resolved_csv = _resolve_csv_path(filepath, csv_filepath)
    has_matching_csv = False

    if not resolved_csv:
        candidates = " / ".join(str(path) for path in _candidate_csv_paths(filepath))
        issues.append(f"缺少配套 CSV 文件：{candidates}")
    else:
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
        print("示例: python validate_cases.py cases.md  # 默认检查同名 .csv，并兼容 <需求名称>_表格版用例.csv")
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

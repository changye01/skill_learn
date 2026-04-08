#!/usr/bin/env python3
"""检查测试数据设计文档或测试数据清单的结构完整性。"""

import csv
import re
import sys


TABLE_REQUIRED_KEYWORDS = [
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

CHECKLIST_REQUIRED_KEYWORDS = [
    "基础记录池",
    "测试用例清单",
    "引用基础记录",
    "验证点",
    "待确认项",
]

CSV_HEADERS = [
    "测试用例编号",
    "测试功能点",
    "数据目标",
    "涉及表",
    "关键字段",
    "建议数据值",
    "样例来源",
    "数据准备方式",
    "验证方式",
    "备注/待确认项",
]


def _read_markdown(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误：文件不存在 - {filepath}")
        sys.exit(2)


def _read_csv_rows(filepath: str) -> tuple[list[str] | None, list[dict[str, str]]]:
    try:
        with open(filepath, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            return reader.fieldnames, list(reader)
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


def _extract_case_ids_from_table(content: str) -> list[str]:
    case_ids = []

    for line in content.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if "---" in stripped:
            continue

        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 2 or cells[1] in {"测试用例编号", "{{CASE_ID}}", ""}:
            continue
        case_ids.append(cells[1])

    return case_ids


def _extract_case_ids_from_checklist(content: str) -> list[str]:
    return re.findall(r"^##\s+(TC-[^\s]+)", content, flags=re.MULTILINE)


def _is_checklist_format(content: str) -> bool:
    return bool(_extract_case_ids_from_checklist(content))


def _validate_table_format(content: str, issues: list[str]) -> tuple[bool, list[str]]:
    for keyword in TABLE_REQUIRED_KEYWORDS:
        if keyword not in content:
            issues.append(f"缺少必填字段：{keyword}")

    plan_ids = _extract_plan_ids(content)
    case_ids = _extract_case_ids_from_table(content)
    has_cases = bool(plan_ids)
    if not has_cases:
        issues.append("测试数据设计至少一条数据设计记录")

    return has_cases, case_ids


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


def validate(filepath: str, csv_filepath: str | None = None) -> dict:
    """验证测试数据设计文档，返回统计信息和问题列表。"""
    content = _read_markdown(filepath)
    issues = []

    if _is_checklist_format(content):
        has_cases, case_ids = _validate_checklist_format(content, issues)
    else:
        has_cases, case_ids = _validate_table_format(content, issues)

    has_matching_csv = None
    if csv_filepath:
        fieldnames, rows = _read_csv_rows(csv_filepath)
        if fieldnames != CSV_HEADERS:
            missing_headers = [header for header in CSV_HEADERS if header not in (fieldnames or [])]
            if missing_headers:
                issues.append(f"CSV 列头缺少字段：{', '.join(missing_headers)}")
            else:
                issues.append("CSV 列头不符合测试数据清单规范")
            has_matching_csv = False
        else:
            csv_case_ids = [row["测试用例编号"].strip() for row in rows]
            if csv_case_ids != case_ids:
                issues.append("CSV 测试用例编号集合或顺序与 Markdown 不一致")
                has_matching_csv = False
            else:
                has_matching_csv = True

    return {
        "issues": issues,
        "has_cases": has_cases,
        "has_matching_csv": has_matching_csv,
    }


def main():
    if len(sys.argv) not in {2, 3}:
        print("用法: python validate_test_data.py <测试数据设计文件路径> [测试数据清单CSV路径]")
        print("示例: python validate_test_data.py data-plan.md data-checklist.csv")
        sys.exit(1)

    filepath = sys.argv[1]
    csv_filepath = sys.argv[2] if len(sys.argv) == 3 else None
    result = validate(filepath, csv_filepath)

    if result["issues"]:
        print("发现以下问题：")
        for issue in result["issues"]:
            print(f"- {issue}")
        sys.exit(1)

    print("✅ 测试数据设计文档结构完整")
    sys.exit(0)


if __name__ == "__main__":
    main()

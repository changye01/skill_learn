#!/usr/bin/env python3
"""检查测试执行清单 Markdown 的结构完整性。"""

import re
import sys


LEGACY_CASE_REQUIRED_SECTIONS = [
    "前置条件",
    "测试步骤",
    "预期结果",
]
DETAIL_REQUIRED_SECTIONS = [
    "输入数据",
    "说明",
    "待确认项",
]
CASE_TABLE_HEADERS = ["编号", "测试功能点", "前置条件", "测试步骤", "预期结果"]

TITLE_PATTERN = re.compile(r"^#\s+.*测试执行清单\s*$", flags=re.MULTILINE)
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
CASE_HEADING_PATTERN = re.compile(r"^(#{2,6})\s+(TC-[^\s]+).*$")

def _read_markdown(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误：文件不存在 - {filepath}")
        sys.exit(2)


def _parse_heading(line: str) -> tuple[int, str] | None:
    match = HEADING_PATTERN.match(line.strip())
    if not match:
        return None

    return len(match.group(1)), match.group(2).strip()


def _split_case_blocks(content: str) -> list[tuple[str, int, str]]:
    lines = content.splitlines()
    matches: list[tuple[int, int, str]] = []

    for index, line in enumerate(lines):
        match = CASE_HEADING_PATTERN.match(line.strip())
        if match:
            matches.append((index, len(match.group(1)), match.group(2)))

    blocks = []
    for start_index, case_level, case_id in matches:
        end_index = len(lines)

        for next_index in range(start_index + 1, len(lines)):
            heading = _parse_heading(lines[next_index])
            if heading and heading[0] <= case_level:
                end_index = next_index
                break

        block = "\n".join(lines[start_index:end_index])
        if end_index < len(lines):
            block += "\n"
        blocks.append((case_id, case_level, block))

    return blocks


def _validate_execution_checklist(content: str, issues: list[str]) -> bool:
    case_blocks = _split_case_blocks(content)
    has_cases = bool(case_blocks)
    if not has_cases:
        issues.append("测试执行清单至少包含一条测试用例记录")
        return has_cases

    for case_id, case_level, block in case_blocks:
        has_case_table = _has_case_table(block, case_id)

        for section in DETAIL_REQUIRED_SECTIONS:
            if not _extract_section(block, section, case_level):
                issues.append(f"{case_id} 缺少“{section}”小节")

        if not has_case_table:
            for section in LEGACY_CASE_REQUIRED_SECTIONS:
                if not _extract_section(block, section, case_level):
                    issues.append(f"{case_id} 缺少“{section}”小节")

        input_data_section = _extract_section(block, "输入数据", case_level)
        if input_data_section:
            if "表：" not in input_data_section:
                issues.append(f"{case_id} 的“输入数据”小节缺少按表分块内容")
            else:
                _validate_table_blocks(case_id, input_data_section, issues)

    return has_cases


def _extract_section(block: str, section_name: str, case_level: int) -> str:
    section_level = case_level + 1
    lines = block.splitlines()
    start_index = None

    for index, line in enumerate(lines):
        heading = _parse_heading(line)
        if heading == (section_level, section_name):
            start_index = index + 1
            break

    if start_index is None:
        return ""

    end_index = len(lines)
    for index in range(start_index, len(lines)):
        heading = _parse_heading(lines[index])
        if heading and heading[0] <= section_level:
            end_index = index
            break

    section_lines = lines[start_index:end_index]
    return "\n".join(section_lines).strip()


def _validate_table_blocks(case_id: str, input_data_section: str, issues: list[str]) -> None:
    table_headers = list(re.finditer(r"^#{1,6}\s+表：.+$", input_data_section, flags=re.MULTILINE))

    for index, header in enumerate(table_headers):
        start = header.end()
        end = table_headers[index + 1].start() if index + 1 < len(table_headers) else len(input_data_section)
        block = input_data_section[start:end]
        table_lines = [line.strip() for line in block.splitlines() if line.strip().startswith("|")]

        if len(table_lines) < 3 or not _is_markdown_separator(table_lines[1]):
            issues.append(f"{case_id} 的“输入数据”小节中，{header.group(0)} 后缺少有效 Markdown 表格")


def _has_case_table(block: str, case_id: str) -> bool:
    table = _extract_case_table(block)
    if not table:
        return False

    headers, rows = table
    if headers != CASE_TABLE_HEADERS:
        return False

    first_row_case_id = rows[0][0].strip()
    return first_row_case_id == case_id


def _extract_case_table(block: str) -> tuple[list[str], list[list[str]]] | None:
    lines = [line.rstrip() for line in block.splitlines()]

    for index in range(len(lines) - 2):
        header_line = lines[index].strip()
        separator_line = lines[index + 1].strip()
        row_line = lines[index + 2].strip()

        if not (header_line.startswith("|") and separator_line.startswith("|") and row_line.startswith("|")):
            continue

        headers = _split_markdown_row(header_line)
        if headers != CASE_TABLE_HEADERS or not _is_markdown_separator(separator_line):
            continue

        rows: list[list[str]] = []
        for row_index in range(index + 2, len(lines)):
            current_line = lines[row_index].strip()
            if not current_line.startswith("|"):
                break
            rows.append(_split_markdown_row(current_line))

        if rows:
            return headers, rows

    return None


def _split_markdown_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _is_markdown_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def validate(filepath: str) -> dict:
    """验证测试执行清单 Markdown，返回统计信息和问题列表。"""
    content = _read_markdown(filepath)
    issues = []

    if not TITLE_PATTERN.search(content):
        issues.append("文档标题必须包含“测试执行清单”")
        return {
            "issues": issues,
            "has_cases": False,
        }

    has_cases = _validate_execution_checklist(content, issues)

    return {
        "issues": issues,
        "has_cases": has_cases,
    }


def main():
    if len(sys.argv) != 2:
        print("用法: python validate_test_data.py <测试执行清单Markdown路径>")
        print("示例: python validate_test_data.py execution-checklist.md")
        sys.exit(1)

    filepath = sys.argv[1]
    result = validate(filepath)

    if result["issues"]:
        print("发现以下问题：")
        for issue in result["issues"]:
            print(f"- {issue}")
        sys.exit(1)

    print("✅ 测试执行清单 Markdown 结构完整")
    sys.exit(0)


if __name__ == "__main__":
    main()

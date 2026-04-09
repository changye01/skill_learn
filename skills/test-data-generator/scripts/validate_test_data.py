#!/usr/bin/env python3
"""检查测试执行清单 Markdown 的结构完整性。"""

import re
import sys


CASE_REQUIRED_SECTIONS = [
    "前置条件",
    "测试步骤",
    "预期结果",
    "输入数据",
    "说明",
    "待确认项",
]

TITLE_PATTERN = re.compile(r"^#\s+.*测试执行清单\s*$", flags=re.MULTILINE)

def _read_markdown(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误：文件不存在 - {filepath}")
        sys.exit(2)


def _split_case_blocks(content: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^##\s+(TC-[^\s]+).*$", content, flags=re.MULTILINE))
    blocks = []

    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        blocks.append((match.group(1), content[start:end]))

    return blocks


def _validate_execution_checklist(content: str, issues: list[str]) -> bool:
    case_blocks = _split_case_blocks(content)
    has_cases = bool(case_blocks)
    if not has_cases:
        issues.append("测试执行清单至少包含一条测试用例记录")
        return has_cases

    for case_id, block in case_blocks:
        for section in CASE_REQUIRED_SECTIONS:
            if f"### {section}" not in block:
                issues.append(f"{case_id} 缺少“{section}”小节")

        input_data_section = _extract_section(block, "输入数据")
        if input_data_section and "#### 表：" not in input_data_section:
            issues.append(f"{case_id} 的“输入数据”小节缺少按表分块内容")
        elif input_data_section:
            _validate_table_blocks(case_id, input_data_section, issues)

    return has_cases


def _extract_section(block: str, section_name: str) -> str:
    pattern = rf"^###\s+{re.escape(section_name)}\s*$"
    match = re.search(pattern, block, flags=re.MULTILINE)
    if not match:
        return ""

    start = match.end()
    next_section = re.search(r"^###\s+.+$", block[start:], flags=re.MULTILINE)
    end = start + next_section.start() if next_section else len(block)
    return block[start:end]


def _validate_table_blocks(case_id: str, input_data_section: str, issues: list[str]) -> None:
    table_headers = list(re.finditer(r"^####\s+表：.+$", input_data_section, flags=re.MULTILINE))

    for index, header in enumerate(table_headers):
        start = header.end()
        end = table_headers[index + 1].start() if index + 1 < len(table_headers) else len(input_data_section)
        block = input_data_section[start:end]
        table_lines = [line.strip() for line in block.splitlines() if line.strip().startswith("|")]

        if len(table_lines) < 3 or not _is_markdown_separator(table_lines[1]):
            issues.append(f"{case_id} 的“输入数据”小节中，{header.group(0)} 后缺少有效 Markdown 表格")


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

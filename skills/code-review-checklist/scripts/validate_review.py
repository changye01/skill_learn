#!/usr/bin/env python3
"""检查 Code Review 清单的完整性"""

import sys
import re


def validate(filepath: str) -> dict:
    """验证审查清单，返回统计信息和问题列表"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"错误：文件不存在 - {filepath}")
        sys.exit(2)

    lines = content.split('\n')
    issues = []
    total = 0
    checked = 0
    failed = 0

    for i, line in enumerate(lines, 1):
        # 匹配清单项: - [ ] 或 - [x] 或 - [!]
        match = re.match(r'^- \[([ x!])\] ', line)
        if not match:
            continue

        total += 1
        mark = match.group(1)

        if mark == ' ':
            issues.append(f"  第 {i} 行：未审查 - {line.strip()}")
        elif mark == 'x':
            checked += 1
        elif mark == '!':
            failed += 1
            # 检查下一行是否有备注
            next_line = lines[i] if i < len(lines) else ''
            if not next_line.strip().startswith('>'):
                issues.append(f"  第 {i} 行：标记为不通过但缺少备注 - {line.strip()}")

    return {
        'total': total,
        'checked': checked,
        'failed': failed,
        'unchecked': total - checked - failed,
        'issues': issues,
    }


def main():
    if len(sys.argv) != 2:
        print("用法: python validate_review.py <清单文件路径>")
        print("示例: python validate_review.py code-review-2026-03-03.md")
        sys.exit(1)

    filepath = sys.argv[1]
    result = validate(filepath)

    print(f"审查项统计：共 {result['total']} 项")
    print(f"  ✅ 通过: {result['checked']}")
    print(f"  ❌ 不通过: {result['failed']}")
    print(f"  ⬜ 未审查: {result['unchecked']}")

    if result['issues']:
        print(f"\n问题：")
        for issue in result['issues']:
            print(issue)
        sys.exit(1)
    else:
        print(f"\n✅ 审查清单已完整填写")
        sys.exit(0)


if __name__ == "__main__":
    main()

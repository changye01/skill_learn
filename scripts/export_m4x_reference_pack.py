#!/usr/bin/env python3
"""一次性导出 M4X 订单管理需求的 reference-pack 样例。"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path("/Users/changye/changye_workspace/changye/skill_learn")
DEFAULT_ENV_FILE = Path(
    "/Users/changye/changye_workspace/vue-msf/purchase-service/Code/Backend/.env"
)
DEFAULT_OUTPUT_DIR = ROOT / "reference-packs/m4x-order-list-query-fields"

TABLE_FIELDS = OrderedDict(
    {
        "supplier_order_m4x_task": [
            "somt_id",
            "trade_order_code",
            "purchase_site_id",
        ],
        "supplier_order_m4x_task_detail": [
            "somt_id",
            "product_id",
        ],
        "orders": [
            "orders_code",
            "site_id",
            "orders_status",
        ],
        "product": [
            "product_id",
            "product_source_type",
        ],
        "supplier_order_dbs_task": [
            "trade_order_code",
            "purchase_site_id",
        ],
    }
)

RELATIONS = [
    (
        "supplier_order_m4x_task.trade_order_code",
        "orders.orders_code",
        "用于列表接口获取订单状态 `orders_status`，以及历史数据修复时回填账号 `site_id`。",
    ),
    (
        "supplier_order_m4x_task.somt_id",
        "supplier_order_m4x_task_detail.somt_id",
        "用于从任务关联到详情行，拿到 `product_id`。",
    ),
    (
        "supplier_order_m4x_task_detail.product_id",
        "product.product_id",
        "用于根据 `product_source_type` 派生 `product_source_tag`（M4X/M4L）。",
    ),
]

RELATION_HEADERS = [
    "source_table",
    "source_field",
    "target_table",
    "target_field",
    "relation_type",
    "usage",
]

DICTIONARY_HEADERS = [
    "table_name",
    "field_name",
    "field_type",
    "nullable",
    "key_type",
    "default_value",
    "field_comment",
    "is_required_for_skill",
    "business_note",
]

REPAIR_SQL = """-- 修复 M4X 历史数据
UPDATE supplier_order_m4x_task t
INNER JOIN orders o ON o.orders_code = t.trade_order_code
SET t.purchase_site_id = o.site_id
WHERE (t.purchase_site_id = '' OR t.purchase_site_id IS NULL);

-- 修复 DBS 历史数据
UPDATE supplier_order_dbs_task t
INNER JOIN orders o ON o.orders_code = t.trade_order_code
SET t.purchase_site_id = o.site_id
WHERE (t.purchase_site_id = '' OR t.purchase_site_id IS NULL);
"""

SAFE_SQL_PREFIXES = ("SELECT", "SHOW", "SET", "START", "DESCRIBE", "EXPLAIN")
FORBIDDEN_SQL_PATTERNS = (
    r"\bINSERT\b",
    r"\bUPDATE\b",
    r"\bDELETE\b",
    r"\bREPLACE\b",
    r"\bALTER\b",
    r"\bDROP\b",
    r"\bTRUNCATE\b",
    r"\bCREATE\b",
    r"\bRENAME\b",
    r"\bGRANT\b",
    r"\bREVOKE\b",
    r"\bMERGE\b",
)


class StableMasker:
    """保持关联关系的一致脱敏。"""

    def __init__(self) -> None:
        self._maps: dict[str, dict[Any, Any]] = {}

    def _mask_token(self, group: str, raw_value: Any, prefix: str) -> Any:
        if raw_value in (None, "", 0, "0"):
            return raw_value
        mapping = self._maps.setdefault(group, {})
        if raw_value not in mapping:
            mapping[raw_value] = f"{prefix}{len(mapping) + 1:03d}"
        return mapping[raw_value]

    def mask(self, column: str, value: Any) -> Any:
        if value in (None, ""):
            return value

        if column in {"trade_order_code", "orders_code"}:
            return self._mask_token("order_code", value, "ORDER_")
        if column in {"purchase_site_id", "site_id"}:
            return self._mask_token("site_id", value, "SITE_")
        if column == "somt_id":
            return self._mask_token("somt_id", value, "SOMT_")
        if column == "product_id":
            return self._mask_token("product_id", value, "PRODUCT_")
        if column == "so_id":
            return self._mask_token("so_id", value, "SOID_")
        if column == "so_code":
            return self._mask_token("so_code", value, "SO_")
        if column == "job_number":
            return self._mask_token("job_number", value, "JOB_")

        return value


def parse_env_file(env_file: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    pattern = re.compile(r"^([A-Z0-9_]+)=(.*)$")
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = pattern.match(line)
        if not match:
            continue
        key, value = match.groups()
        env[key] = value.strip().strip("'").strip('"')
    return env


def connect(env_cfg: dict[str, str]):
    try:
        import pymysql
        from pymysql.cursors import DictCursor
    except ImportError as exc:  # pragma: no cover - runtime guard
        raise SystemExit(
            "缺少依赖 pymysql，请先在当前 Python 环境安装：pip install pymysql"
        ) from exc

    return pymysql.connect(
        host=env_cfg["DB_HOST"],
        port=int(env_cfg.get("DB_PORT", "3306")),
        user=env_cfg["DB_USERNAME"],
        password=env_cfg["DB_PASSWORD"],
        database=env_cfg["DB_DATABASE"],
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=False,
    )


def assert_read_only_sql(sql: str) -> None:
    normalized = sql.strip().upper()
    if not normalized.startswith(SAFE_SQL_PREFIXES):
        raise RuntimeError(f"检测到非只读 SQL，已拒绝执行: {sql.strip()[:80]}")
    if normalized.startswith("SHOW CREATE"):
        return
    for pattern in FORBIDDEN_SQL_PATTERNS:
        if re.search(pattern, normalized):
            raise RuntimeError(f"检测到写操作 SQL 关键字，已拒绝执行: {sql.strip()[:80]}")


def exec_sql(cursor, sql: str, params: tuple[Any, ...] = ()) -> None:
    assert_read_only_sql(sql)
    cursor.execute(sql, params)


def fetchall(cursor, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    exec_sql(cursor, sql, params)
    return list(cursor.fetchall())


def show_create_table(cursor, table: str) -> str:
    exec_sql(cursor, f"SHOW CREATE TABLE `{table}`")
    row = cursor.fetchone()
    return row["Create Table"]


def get_columns_meta(cursor, database: str, table: str) -> list[dict[str, Any]]:
    sql = """
    SELECT
      COLUMN_NAME,
      COLUMN_TYPE,
      IS_NULLABLE,
      COLUMN_DEFAULT,
      COLUMN_KEY,
      COLUMN_COMMENT
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
    ORDER BY ORDINAL_POSITION
    """
    return fetchall(cursor, sql, (database, table))


def build_in_clause(items: list[Any]) -> tuple[str, tuple[Any, ...]]:
    placeholders = ", ".join(["%s"] * len(items))
    return placeholders, tuple(items)


def pick_task_samples(cursor, limit: int) -> list[dict[str, Any]]:
    primary_limit = max(3, limit // 2)
    missing_limit = max(2, limit - primary_limit)

    sql_primary = """
    SELECT t.somt_id, t.trade_order_code, t.purchase_site_id
    FROM supplier_order_m4x_task t
    INNER JOIN orders o ON o.orders_code = t.trade_order_code
    WHERE t.task_type IN (1, 2)
      AND t.is_delete = 0
      AND purchase_site_id IS NOT NULL
      AND purchase_site_id <> ''
    ORDER BY t.somt_id DESC
    LIMIT %s
    """
    sql_missing = """
    SELECT t.somt_id, t.trade_order_code, t.purchase_site_id
    FROM supplier_order_m4x_task t
    INNER JOIN orders o ON o.orders_code = t.trade_order_code
    WHERE t.task_type IN (1, 2)
      AND t.is_delete = 0
      AND (purchase_site_id IS NULL OR purchase_site_id = '')
    ORDER BY t.somt_id DESC
    LIMIT %s
    """

    rows = fetchall(cursor, sql_primary, (primary_limit,))
    rows.extend(fetchall(cursor, sql_missing, (missing_limit,)))

    if len(rows) < limit:
        sql_fallback = """
        SELECT t.somt_id, t.trade_order_code, t.purchase_site_id
        FROM supplier_order_m4x_task t
        INNER JOIN orders o ON o.orders_code = t.trade_order_code
        WHERE t.task_type IN (1, 2)
          AND t.is_delete = 0
        ORDER BY t.somt_id DESC
        LIMIT %s
        """
        rows.extend(fetchall(cursor, sql_fallback, (limit,)))

    if len(rows) < limit:
        sql_last_resort = """
        SELECT somt_id, trade_order_code, purchase_site_id
        FROM supplier_order_m4x_task
        WHERE task_type IN (1, 2)
          AND is_delete = 0
        ORDER BY somt_id DESC
        LIMIT %s
        """
        rows.extend(fetchall(cursor, sql_last_resort, (limit,)))

    unique: OrderedDict[Any, dict[str, Any]] = OrderedDict()
    for row in rows:
        unique.setdefault(row["somt_id"], row)
        if len(unique) >= limit:
            break
    return list(unique.values())


def fetch_related_rows(cursor, table: str, key: str, ids: list[Any], columns: list[str]) -> list[dict[str, Any]]:
    if not ids:
        return []
    placeholders, params = build_in_clause(ids)
    sql = f"SELECT {', '.join(columns)} FROM `{table}` WHERE `{key}` IN ({placeholders})"
    return fetchall(cursor, sql, params)


def fetch_dbs_samples(cursor, limit: int) -> list[dict[str, Any]]:
    sql = """
    SELECT trade_order_code, purchase_site_id
    FROM supplier_order_dbs_task
    WHERE purchase_site_id IS NULL OR purchase_site_id = ''
    ORDER BY trade_order_code DESC
    LIMIT %s
    """
    return fetchall(cursor, sql, (limit,))


def mask_rows(rows: list[dict[str, Any]], masker: StableMasker) -> list[dict[str, Any]]:
    result = []
    for row in rows:
        result.append({key: masker.mask(key, value) for key, value in row.items()})
    return result


def write_csv(path: Path, rows: list[dict[str, Any]], headers: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({header: row.get(header, "") for header in headers})


def write_schema_files(cursor, output_dir: Path, table_fields: OrderedDict[str, list[str]]) -> None:
    tables_dir = output_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    for table in table_fields:
        ddl = show_create_table(cursor, table)
        (tables_dir / f"{table}.sql").write_text(f"{ddl};\n", encoding="utf-8")


def build_relations_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for left, right, note in RELATIONS:
        source_table, source_field = left.split(".", 1)
        target_table, target_field = right.split(".", 1)
        rows.append(
            {
                "source_table": source_table,
                "source_field": source_field,
                "target_table": target_table,
                "target_field": target_field,
                "relation_type": "join",
                "usage": note,
            }
        )

    rows.extend(
        [
            {
                "source_table": "supplier_order_m4x_task",
                "source_field": "purchase_site_id",
                "target_table": "",
                "target_field": "",
                "relation_type": "derived",
                "usage": "列表接口返回字段 `purchase_site_id` 直接来源于任务表该字段；`get-purchase-site-list` 的候选账号来自该字段去重结果。",
            },
            {
                "source_table": "orders",
                "source_field": "orders_status",
                "target_table": "api/m4x-order/get-order-status-map",
                "target_field": "value/label",
                "relation_type": "mapping",
                "usage": "订单状态原始值来源于 `orders.orders_status`，前端文案通过静态状态映射接口展示。",
            },
            {
                "source_table": "product",
                "source_field": "product_source_type",
                "target_table": "api/m4x-order/list",
                "target_field": "product_source_tag",
                "relation_type": "derived",
                "usage": "`31 -> M4X`，`28 -> M4L`，其他为空字符串。",
            },
        ]
    )
    return rows


def write_relations_csv(output_dir: Path) -> None:
    write_csv(output_dir / "relations.csv", build_relations_rows(), RELATION_HEADERS)


def build_dictionary_rows(columns_by_table: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    focus_fields = {
        "supplier_order_m4x_task": {
            "somt_id": "主任务主键；用于关联详情表。",
            "trade_order_code": "销售订单号；用于关联 `orders.orders_code`。",
            "purchase_site_id": "销售订单账号；功能一新增展示字段，也是账号筛选候选值来源。",
        },
        "supplier_order_m4x_task_detail": {
            "somt_id": "任务表主键；用于关联主任务。",
            "product_id": "产品 ID；用于查询 `product_source_type`。",
        },
        "orders": {
            "orders_code": "订单编码；用于和任务表做关联。",
            "site_id": "订单来源账号；用于历史数据修复回填 `purchase_site_id`。",
            "orders_status": "订单状态原始值；用于列表筛选和状态展示。",
        },
        "product": {
            "product_id": "产品主键；用于和详情表关联。",
            "product_source_type": "产品来源类型；当前需求只需关注 28(M4L) 与 31(M4X)。",
        },
        "supplier_order_dbs_task": {
            "trade_order_code": "DBS 订单号；用于历史修复时关联 orders。",
            "purchase_site_id": "销售订单账号；历史缺失值通过 `orders.site_id` 回填。",
        },
    }

    rows: list[dict[str, str]] = []
    for table, columns in columns_by_table.items():
        focus_map = focus_fields.get(table, {})
        for col in columns:
            field_name = col["COLUMN_NAME"]
            if field_name not in focus_map:
                continue
            rows.append(
                {
                    "table_name": table,
                    "field_name": field_name,
                    "field_type": col["COLUMN_TYPE"],
                    "nullable": col["IS_NULLABLE"],
                    "key_type": col["COLUMN_KEY"] or "",
                    "default_value": "" if col["COLUMN_DEFAULT"] is None else str(col["COLUMN_DEFAULT"]),
                    "field_comment": col["COLUMN_COMMENT"] or "",
                    "is_required_for_skill": "Y",
                    "business_note": focus_map[field_name],
                }
            )
    return rows


def write_dictionary_csv(cursor, database: str, output_dir: Path) -> None:
    columns_by_table = {
        table: get_columns_meta(cursor, database, table)
        for table in TABLE_FIELDS
    }
    write_csv(
        output_dir / "data_dictionary.csv",
        build_dictionary_rows(columns_by_table),
        DICTIONARY_HEADERS,
    )


def write_readme(output_dir: Path, sample_counts: dict[str, int]) -> None:
    lines = [
        "# M4X 功能一 Reference Pack",
        "",
        "该 reference-pack 由一次性脚本从数据库读取并生成，只覆盖当前需求的功能一：",
        "",
        "- 列表新增账号字段",
        "- 产品来源标识（M4X / M4L）",
        "- 新增账号和订单状态查询条件",
        "- 历史账号数据修复",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 包含内容",
        "",
        "- `tables/*.sql`：单表 DDL，方便后续逐表补充",
        "- `relations.csv`：表关系、派生字段和映射关系",
        "- `data_dictionary.csv`：核心字段字典，便于非研发补充业务含义",
        "- `repair_sql.sql`：历史数据修复 SQL",
        "- `table_samples/*.csv`：脱敏样例数据",
        "",
        "## 最小范围说明",
        "",
        "- 该包已按后续 skill 使用场景收紧，只保留功能一必需表和字段。",
        "- 未导出采购员、PO、日志、拍单链接等与功能一无直接关系的数据。",
        "- `supplier_order_m4x_task_detail` 仅保留 `somt_id/product_id`，用于支撑产品来源标识推导。",
        "",
        "## 样例数量",
        "",
    ]
    for table, count in sample_counts.items():
        lines.append(f"- `{table}`: {count} 行")
    lines.extend(
        [
            "",
            "## 脱敏说明",
            "",
            "- `trade_order_code/orders_code` 已做稳定映射脱敏",
            "- `purchase_site_id/site_id` 已做稳定映射脱敏",
            "- `somt_id/product_id/so_id/so_code/job_number` 已做稳定映射脱敏",
            "- 状态值、来源类型等业务枚举保留原值，便于后续 skill 参考",
        ]
    )
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def export_reference_pack(env_file: Path, output_dir: Path, sample_limit: int) -> None:
    env_cfg = parse_env_file(env_file)
    required = ["DB_HOST", "DB_PORT", "DB_DATABASE", "DB_USERNAME", "DB_PASSWORD"]
    missing = [key for key in required if key not in env_cfg or env_cfg[key] == ""]
    if missing:
        raise RuntimeError(f"数据库配置不完整，缺少: {', '.join(missing)}")

    output_dir.mkdir(parents=True, exist_ok=True)
    samples_dir = output_dir / "table_samples"
    samples_dir.mkdir(parents=True, exist_ok=True)

    sample_counts: dict[str, int] = {}
    masker = StableMasker()

    with connect(env_cfg) as conn:
        with conn.cursor() as cursor:
            exec_sql(cursor, "SET SESSION TRANSACTION READ ONLY")
            exec_sql(cursor, "START TRANSACTION READ ONLY")
            write_schema_files(cursor, output_dir, TABLE_FIELDS)
            write_relations_csv(output_dir)
            write_dictionary_csv(cursor, env_cfg["DB_DATABASE"], output_dir)

            tasks = pick_task_samples(cursor, sample_limit)
            task_rows = mask_rows(tasks, masker)
            write_csv(samples_dir / "supplier_order_m4x_task.csv", task_rows, TABLE_FIELDS["supplier_order_m4x_task"])
            sample_counts["supplier_order_m4x_task"] = len(task_rows)

            somt_ids = [row["somt_id"] for row in tasks]
            detail_rows_raw = fetch_related_rows(
                cursor,
                "supplier_order_m4x_task_detail",
                "somt_id",
                somt_ids,
                TABLE_FIELDS["supplier_order_m4x_task_detail"],
            )
            detail_rows = mask_rows(detail_rows_raw, masker)
            write_csv(
                samples_dir / "supplier_order_m4x_task_detail.csv",
                detail_rows,
                TABLE_FIELDS["supplier_order_m4x_task_detail"],
            )
            sample_counts["supplier_order_m4x_task_detail"] = len(detail_rows)

            order_codes = list(OrderedDict.fromkeys(row["trade_order_code"] for row in tasks if row["trade_order_code"]))
            order_rows_raw = fetch_related_rows(cursor, "orders", "orders_code", order_codes, TABLE_FIELDS["orders"])
            order_rows = mask_rows(order_rows_raw, masker)
            write_csv(samples_dir / "orders.csv", order_rows, TABLE_FIELDS["orders"])
            sample_counts["orders"] = len(order_rows)

            product_ids = list(
                OrderedDict.fromkeys(row["product_id"] for row in detail_rows_raw if row["product_id"] not in (None, ""))
            )
            product_rows_raw = fetch_related_rows(cursor, "product", "product_id", product_ids, TABLE_FIELDS["product"])
            product_rows = mask_rows(product_rows_raw, masker)
            write_csv(samples_dir / "product.csv", product_rows, TABLE_FIELDS["product"])
            sample_counts["product"] = len(product_rows)

            dbs_rows_raw = fetch_dbs_samples(cursor, sample_limit)
            dbs_rows = mask_rows(dbs_rows_raw, masker)
            write_csv(samples_dir / "supplier_order_dbs_task.csv", dbs_rows, TABLE_FIELDS["supplier_order_dbs_task"])
            sample_counts["supplier_order_dbs_task"] = len(dbs_rows)
        conn.rollback()

    (output_dir / "repair_sql.sql").write_text(REPAIR_SQL, encoding="utf-8")
    write_readme(output_dir, sample_counts)


def main() -> int:
    parser = argparse.ArgumentParser(description="导出当前需求的 reference-pack 样例")
    parser.add_argument("--env-file", type=Path, default=DEFAULT_ENV_FILE, help="purchase-service 的 .env 文件")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="reference-pack 输出目录")
    parser.add_argument("--sample-limit", type=int, default=12, help="主任务样例导出上限")
    args = parser.parse_args()

    export_reference_pack(args.env_file, args.output_dir, args.sample_limit)
    print(f"reference-pack 已生成: {args.output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

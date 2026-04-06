import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_m4x_reference_pack import (
    DICTIONARY_HEADERS,
    RELATION_HEADERS,
    assert_read_only_sql,
    build_dictionary_rows,
    build_relations_rows,
    write_schema_files,
)


class ReadOnlySqlTest(unittest.TestCase):
    def test_allows_select_show_and_set(self) -> None:
        assert_read_only_sql("SELECT * FROM orders LIMIT 1")
        assert_read_only_sql("SHOW CREATE TABLE `orders`")
        assert_read_only_sql("SET SESSION TRANSACTION READ ONLY")
        assert_read_only_sql("START TRANSACTION READ ONLY")

    def test_rejects_write_sql(self) -> None:
        with self.assertRaises(RuntimeError):
            assert_read_only_sql("UPDATE orders SET site_id = 'x'")

        with self.assertRaises(RuntimeError):
            assert_read_only_sql("DELETE FROM supplier_order_m4x_task")

    def test_rejects_unknown_prefix(self) -> None:
        with self.assertRaises(RuntimeError):
            assert_read_only_sql("WITH cte AS (SELECT 1) SELECT * FROM cte")


class OutputStructureTest(unittest.TestCase):
    def test_build_relations_rows_uses_csv_headers(self) -> None:
        rows = build_relations_rows()
        self.assertGreater(len(rows), 0)
        self.assertEqual(set(rows[0].keys()), set(RELATION_HEADERS))

    def test_build_dictionary_rows_uses_csv_headers(self) -> None:
        columns_by_table = {
            "orders": [
                {
                    "COLUMN_NAME": "orders_code",
                    "COLUMN_TYPE": "varchar(32)",
                    "IS_NULLABLE": "NO",
                    "COLUMN_KEY": "MUL",
                    "COLUMN_DEFAULT": None,
                    "COLUMN_COMMENT": "订单编码",
                }
            ]
        }
        rows = build_dictionary_rows(columns_by_table)
        self.assertGreater(len(rows), 0)
        self.assertEqual(set(rows[0].keys()), set(DICTIONARY_HEADERS))

    def test_write_schema_files_splits_into_single_table_sql(self) -> None:
        class FakeCursor:
            def __init__(self) -> None:
                self.current_table = ""

            def execute(self, sql: str, params=()) -> None:
                self.current_table = sql.split("`")[1]

            def fetchone(self):
                return {"Create Table": f"CREATE TABLE `{self.current_table}` (`id` int(11))"}

        with TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            write_schema_files(FakeCursor(), output_dir, {"foo": ["id"], "bar": ["id"]})
            self.assertTrue((output_dir / "tables" / "foo.sql").exists())
            self.assertTrue((output_dir / "tables" / "bar.sql").exists())


if __name__ == "__main__":
    unittest.main()

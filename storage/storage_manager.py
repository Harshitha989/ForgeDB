
import json
import re
from pathlib import Path


class StorageManager:
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _table_path(self, table_name):
        if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", table_name):
            raise ValueError("Invalid table name")

        return self.data_dir / f"{table_name.lower()}.json"

    def read_rows(self, table_name):
        path = self._table_path(table_name)

        if not path.exists():
            return []

        return json.loads(path.read_text(encoding="utf-8"))

    def write_rows(self, table_name, rows):
        path = self._table_path(table_name)
        path.write_text(
            json.dumps(rows, indent=4),
            encoding="utf-8"
        )

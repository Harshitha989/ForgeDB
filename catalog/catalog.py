
import json
from pathlib import Path

from catalog.schema import TableSchema


class Catalog:
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.data_dir / "catalog.json"
        self.tables = {}

        if self.file_path.exists():
            self.tables = json.loads(
                self.file_path.read_text(encoding="utf-8")
            )

    def save(self):
        self.file_path.write_text(
            json.dumps(self.tables, indent=4),
            encoding="utf-8"
        )

    def create_table(self, name, columns):
        name = name.lower()

        if name in self.tables:
            raise ValueError(f"Table '{name}' already exists")

        if not columns:
            raise ValueError("A table must have at least one column")

        for column, column_type in columns.items():
            if column_type not in ("INT", "TEXT"):
                raise ValueError(f"Unsupported type: {column_type}")

        self.tables[name] = columns
        self.save()

    def get_schema(self, name):
        name = name.lower()

        if name not in self.tables:
            raise ValueError(f"Table '{name}' does not exist")

        return TableSchema(name, self.tables[name])

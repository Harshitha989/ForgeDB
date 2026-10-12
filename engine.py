
from pathlib import Path

from catalog.catalog import Catalog
from storage.storage_manager import StorageManager
from parser.sql_parser import parse_sql
from executor.query_executor import QueryExecutor


class ForgeDB:
    def __init__(self, data_dir=None):
        if data_dir is None:
            data_dir = Path(__file__).parent / "data"

        self.catalog = Catalog(data_dir)
        self.storage = StorageManager(data_dir)
        self.executor = QueryExecutor(self.catalog, self.storage)

    def execute(self, sql):
        command = parse_sql(sql)
        return self.executor.execute(command)

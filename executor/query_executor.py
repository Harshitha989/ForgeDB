
class QueryExecutor:
    def __init__(self, catalog, storage):
        self.catalog = catalog
        self.storage = storage

    def matches(self, row, condition):
        if condition is None:
            return True

        column = condition["column"]

        if column not in row:
            raise ValueError(f"Unknown column: {column}")

        left = row[column]
        right = condition["value"]
        operator = condition["operator"]

        if type(left) is not type(right):
            raise ValueError("WHERE value has the wrong type")

        operations = {
            "=": lambda: left == right,
            "!=": lambda: left != right,
            ">": lambda: left > right,
            "<": lambda: left < right,
            ">=": lambda: left >= right,
            "<=": lambda: left <= right
        }

        return operations[operator]()

    def execute(self, command):
        action = command["action"]
        table = command["table"]

        if action == "create":
            self.catalog.create_table(table, command["columns"])
            return f"Table '{table}' created successfully."

        schema = self.catalog.get_schema(table)
        rows = self.storage.read_rows(table)

        if action == "insert":
            row = schema.validate_row(command["values"])
            rows.append(row)
            self.storage.write_rows(table, rows)
            return "1 row inserted."

        condition = command.get("condition")

        if action == "select":
            columns = command["columns"]

            if columns == ["*"]:
                columns = list(schema.columns)

            for column in columns:
                if column not in schema.columns:
                    raise ValueError(f"Unknown column: {column}")

            result = [
                {column: row[column] for column in columns}
                for row in rows if self.matches(row, condition)
            ]
            return result

        if action == "update":
            assignments = command["assignments"]

            for column in assignments:
                if column not in schema.columns:
                    raise ValueError(f"Unknown column: {column}")

            updated = 0

            for row in rows:
                if self.matches(row, condition):
                    candidate = dict(row)

                    for column, value in assignments.items():
                        candidate[column] = value

                    validated = schema.validate_row(
                        [candidate[column] for column in schema.columns]
                    )
                    row.update(validated)
                    updated += 1

            self.storage.write_rows(table, rows)
            return f"{updated} row(s) updated."

        if action == "delete":
            remaining = [
                row for row in rows
                if not self.matches(row, condition)
            ]
            deleted = len(rows) - len(remaining)
            self.storage.write_rows(table, remaining)
            return f"{deleted} row(s) deleted."

        raise ValueError("Unsupported operation")


class TableSchema:
    def __init__(self, table_name, columns):
        self.table_name = table_name
        self.columns = columns

    def validate_row(self, row):
        if len(row) != len(self.columns):
            raise ValueError(
                f"Expected {len(self.columns)} values, got {len(row)}"
            )

        result = {}

        for (column_name, column_type), value in zip(
            self.columns.items(), row
        ):
            if column_type == "INT":
                if isinstance(value, bool) or not isinstance(value, int):
                    raise ValueError(
                        f"Column '{column_name}' must be an integer"
                    )

            elif column_type == "TEXT":
                if not isinstance(value, str):
                    raise ValueError(
                        f"Column '{column_name}' must be text"
                    )

            result[column_name] = value

        return result

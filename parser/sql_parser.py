
import re


def split_csv(text):
    """Split comma-separated values without splitting inside quotes."""
    parts = []
    current = []
    quote = None

    for char in text:
        if quote:
            current.append(char)
            if char == quote:
                quote = None
        elif char in ("'", '"'):
            quote = char
            current.append(char)
        elif char == ",":
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)

    if quote:
        raise ValueError("Unclosed quote in SQL")

    parts.append("".join(current).strip())
    return parts


def parse_value(text):
    text = text.strip()

    if re.fullmatch(r"-?\d+", text):
        return int(text)

    if len(text) >= 2 and text[0] in ("'", '"') and text[-1] == text[0]:
        return text[1:-1].replace(text[0] * 2, text[0])

    raise ValueError(f"Invalid value: {text}")


def parse_condition(text):
    match = re.fullmatch(
        r"\s*([A-Za-z_]\w*)\s*(>=|<=|!=|=|>|<)\s*(.*?)\s*",
        text
    )

    if not match:
        raise ValueError("Invalid WHERE condition")

    column, operator, raw_value = match.groups()

    return {
        "column": column.lower(),
        "operator": operator,
        "value": parse_value(raw_value)
    }


def parse_sql(sql):
    sql = sql.strip().rstrip(";").strip()

    match = re.fullmatch(
        r"CREATE\s+TABLE\s+([A-Za-z_]\w*)\s*\((.*)\)",
        sql, re.IGNORECASE | re.DOTALL
    )
    if match:
        name, body = match.groups()
        columns = {}

        for item in split_csv(body):
            pieces = item.split()
            if len(pieces) != 2:
                raise ValueError("Use column_name INT or column_name TEXT")

            column, column_type = pieces
            column = column.lower()
            column_type = column_type.upper()

            if column in columns:
                raise ValueError(f"Duplicate column: {column}")

            columns[column] = column_type

        return {"action": "create", "table": name.lower(),
                "columns": columns}

    match = re.fullmatch(
        r"INSERT\s+INTO\s+([A-Za-z_]\w*)\s+VALUES\s*\((.*)\)",
        sql, re.IGNORECASE | re.DOTALL
    )
    if match:
        name, body = match.groups()
        values = [parse_value(v) for v in split_csv(body)]
        return {"action": "insert", "table": name.lower(),
                "values": values}

    match = re.fullmatch(
        r"SELECT\s+(.+?)\s+FROM\s+([A-Za-z_]\w*)"
        r"(?:\s+WHERE\s+(.+))?",
        sql, re.IGNORECASE | re.DOTALL
    )
    if match:
        fields, name, condition = match.groups()
        fields = [f.strip().lower() for f in fields.split(",")]

        return {
            "action": "select",
            "table": name.lower(),
            "columns": fields,
            "condition": parse_condition(condition) if condition else None
        }

    match = re.fullmatch(
        r"UPDATE\s+([A-Za-z_]\w*)\s+SET\s+(.+?)"
        r"(?:\s+WHERE\s+(.+))?",
        sql, re.IGNORECASE | re.DOTALL
    )
    if match:
        name, assignments_text, condition = match.groups()
        assignments = {}

        for item in split_csv(assignments_text):
            pieces = item.split("=", 1)
            if len(pieces) != 2:
                raise ValueError("Use column = value in SET")

            column, value = pieces
            assignments[column.strip().lower()] = parse_value(value)

        return {
            "action": "update",
            "table": name.lower(),
            "assignments": assignments,
            "condition": parse_condition(condition) if condition else None
        }

    match = re.fullmatch(
        r"DELETE\s+FROM\s+([A-Za-z_]\w*)"
        r"(?:\s+WHERE\s+(.+))?",
        sql, re.IGNORECASE | re.DOTALL
    )
    if match:
        name, condition = match.groups()
        return {
            "action": "delete",
            "table": name.lower(),
            "condition": parse_condition(condition) if condition else None
        }

    raise ValueError("Unsupported SQL command or invalid syntax")

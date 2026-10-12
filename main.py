
from engine import ForgeDB


def display_result(result):
    if isinstance(result, list):
        if not result:
            print("(0 rows)")
            return

        columns = list(result[0].keys())
        widths = {
            column: max(
                len(column),
                *(len(str(row[column])) for row in result)
            )
            for column in columns
        }

        border = "+" + "+".join(
            "-" * (widths[column] + 2) for column in columns
        ) + "+"

        print(border)
        print("|" + "|".join(
            f" {column:<{widths[column]}} " for column in columns
        ) + "|")
        print(border)

        for row in result:
            print("|" + "|".join(
                f" {str(row[column]):<{widths[column]}} "
                for column in columns
            ) + "|")

        print(border)
        print(f"{len(result)} row(s) returned.")
    else:
        print(result)


def main():
    db = ForgeDB()

    print("=" * 38)
    print("          ForgeDB v0.1")
    print("   Your Python Database Engine")
    print("Type EXIT to quit.")
    print("=" * 38)

    while True:
        try:
            sql = input("ForgeDB> ").strip()

            if sql.upper() in ("EXIT", "QUIT"):
                print("ForgeDB closed.")
                break

            if not sql:
                continue

            result = db.execute(sql)
            display_result(result)

        except (ValueError, OSError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()

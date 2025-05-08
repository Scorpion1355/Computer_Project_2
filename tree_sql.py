""" Tree SQL """

import argparse
import shlex
from data_manager import DataManager

class TreeSQL:

    def __init__(self):

        self.data_manager = DataManager()

    def parse_command(self, command):

        tokens = shlex.split(command)
        if not tokens:
            return "Пуста команда"

        cmd = tokens[0].lower()

        if cmd == "create":
            if len(tokens) >= 2 and tokens[1].lower() == "database":
                return self.data_manager.create_database(tokens[2])
            if len(tokens) >= 2 and tokens[1].lower() == "table":
                return self.create_table_command(tokens[2:])
        if cmd == "use":
            return self.data_manager.use_database(tokens[1])
        if cmd == "insert":
            return self.insert_command(tokens)
        if cmd == "select":
            return self.select_command(tokens)
        if cmd == "update":
            return self.update_command(tokens)
        if cmd == "delete":
            return self.delete_command(tokens)
        return "Невідома команда"

    def create_table_command(self, tokens):

        table_name = tokens[0]
        tree_type = "avl"

        if "using" in [t.lower() for t in tokens]:
            idx = tokens.index("USING") if "USING" in tokens else tokens.index("using")
            tree_type = tokens[idx + 1]

        col_start = tokens.index("(")
        col_end = tokens.index(")")
        columns_str = ' '.join(tokens[col_start + 1: col_end])
        columns = [col.strip() for col in columns_str.split(",")]

        return self.data_manager.create_table(table_name, columns, tree_type)

    def insert_command(self, tokens):

        try:
            table_name = tokens[2]
            values_index = tokens.index("VALUES")
            values_str = ' '.join(tokens[values_index + 1:])
            values_str = values_str.strip("()")
            raw_values = [v.strip() for v in values_str.split(",")]
            parsed_values = [self._parse_value(v) for v in raw_values]
            return self.data_manager.insert(table_name, parsed_values)

        except Exception as e:
            return f"Помилка вставки: {e}"

    def select_command(self, tokens):

        try:
            from_index = tokens.index("FROM")
            table_name = tokens[from_index + 1]

            condition = None
            if "WHERE" in [t.upper() for t in tokens]:
                where_index = tokens.index("WHERE")
                condition = ' '.join(tokens[where_index + 1:])

            result = self.data_manager.select(table_name, condition)
            return "\n".join(str(r) for r in result)

        except Exception as e:
            return f"Помилка SELECT: {e}"

    def update_command(self, tokens):

        try:
            table_name = tokens[1]
            set_index = tokens.index("SET")
            where_index = tokens.index("WHERE") if "WHERE" in tokens else len(tokens)

            update_tokens = tokens[set_index + 1: where_index]
            updates = {}
            for item in ' '.join(update_tokens).split(','):
                field, value = item.split('=')
                updates[field.strip()] = value.strip().strip("'\"")

            condition = ' '.join(tokens[where_index + 1:]) if "WHERE" in tokens else None

            return self.data_manager.update(table_name, updates, condition)

        except Exception as e:
            return f"Помилка UPDATE: {e}"

    def delete_command(self, tokens):

        try:
            table_name = tokens[2]
            condition = None
            if "WHERE" in [t.upper() for t in tokens]:
                where_index = tokens.index("WHERE")
                condition = ' '.join(tokens[where_index + 1:])

            return self.data_manager.delete(table_name, condition)

        except Exception as e:
            return f"Помилка DELETE: {e}"

    def _parse_value(self, value):

        if value.startswith("'") and value.endswith("'"):
            return value.strip("'")
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value

def main():

    parser = argparse.ArgumentParser(description="Інтерфейс команд для роботи з TreeSQL")
    parser.add_argument("--cmd", type=str, help="SQL-подібна команда")
    args = parser.parse_args()

    sql = TreeSQL()

    if args.cmd:
        result = sql.parse_command(args.cmd)
        print(result)
    else:
        print("Введіть команду або 'exit'):")
        while True:
            try:
                command = input(">>> ")
                if command.strip().lower() in ["exit", "quit"]:
                    break
                result = sql.parse_command(command)
                print(result)
            except KeyboardInterrupt:
                print("\nВихід.")
                break

if __name__ == "__main__":
    main()

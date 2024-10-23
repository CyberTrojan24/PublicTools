class SQLShell:
    def __init__(self):
        self.running = True
        self.data = {}  # Simple in-memory storage
        self.commands = {
            'create': self.create_table,
            'insert': self.insert_data,
            'select': self.select_data,
            'help': self.show_help,
            'exit': self.exit_shell,
            'show': self.show_tables
        }

    def create_table(self, args):
        # CREATE table_name (col1, col2, col3)
        if len(args) < 3 or '(' not in ' '.join(args) or ')' not in ' '.join(args):
            print("Syntax: CREATE table_name (column1, column2, ...)")
            return

        table_name = args[0]
        # Extract columns between parentheses
        cols_str = ' '.join(args[1:]).split('(')[1].split(')')[0]
        columns = [col.strip() for col in cols_str.split(',')]

        self.data[table_name] = {
            'columns': columns,
            'rows': []
        }
        print(f"Table {table_name} created with columns: {', '.join(columns)}")

    def insert_data(self, args):
        # INSERT table_name VALUES (val1, val2, val3)
        if len(args) < 3 or 'values' not in ' '.join(args).lower():
            print("Syntax: INSERT table_name VALUES (value1, value2, ...)")
            return

        table_name = args[0]
        if table_name not in self.data:
            print(f"Table {table_name} does not exist")
            return

        # Extract values between parentheses
        values_str = ' '.join(args[2:]).split('(')[1].split(')')[0]
        values = [val.strip() for val in values_str.split(',')]

        if len(values) != len(self.data[table_name]['columns']):
            print("Number of values doesn't match number of columns")
            return

        self.data[table_name]['rows'].append(values)
        print("Data inserted successfully")

    def select_data(self, args):
        # SELECT * FROM table_name
        if len(args) < 3 or 'from' not in ' '.join(args).lower():
            print("Syntax: SELECT * FROM table_name")
            return

        table_name = args[-1]
        if table_name not in self.data:
            print(f"Table {table_name} does not exist")
            return

        # Print columns
        columns = self.data[table_name]['columns']
        print(' | '.join(columns))
        print('-' * (len(' | '.join(columns)) + 2))

        # Print rows
        for row in self.data[table_name]['rows']:
            print(' | '.join(row))

    def show_tables(self, args):
        if not self.data:
            print("No tables exist")
            return
        print("\nAvailable tables:")
        for table in self.data:
            print(f"- {table}")
            print(f"  Columns: {', '.join(self.data[table]['columns'])}")
            print(f"  Rows: {len(self.data[table]['rows'])}\n")

    def show_help(self, args):
        print("\nAvailable commands:")
        print("  CREATE table_name (col1, col2, ...)  - Create a new table")
        print("  INSERT table_name VALUES (val1, ...) - Insert data into table")
        print("  SELECT * FROM table_name             - Display table contents")
        print("  SHOW TABLES                          - List all tables")
        print("  EXIT                                 - Exit the shell")
        print("  HELP                                 - Show this help message\n")

    def exit_shell(self, args):
        self.running = False
        print("Goodbye!")

    def run(self):
        print("Welcome to SQLShell! Type 'help' for available commands.")
        while self.running:
            try:
                user_input = input("sql> ")
                if not user_input.strip():
                    continue

                # Parse command and arguments
                parts = user_input.strip().split()
                command = parts[0].lower()
                args = parts[1:]

                if command in self.commands:
                    self.commands[command](args)
                else:
                    print(f"Unknown command: {command}")
                    print("Type 'help' for available commands")

            except KeyboardInterrupt:
                print("\nUse 'exit' to quit the shell")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    shell = SQLShell()
    shell.run()

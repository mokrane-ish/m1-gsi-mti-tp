import sqlite3


class DatabaseConnectionSingleton:
    _instance = None

    def __new__(cls, db_name=":memory:"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db_name = db_name
            cls._instance.connection = sqlite3.connect(db_name)
            print(f"Database connection opened ({db_name}).")
        return cls._instance

    def execute_query(self, query, params=()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            DatabaseConnectionSingleton._instance = None
            print("Database connection closed.")


if __name__ == "__main__":
    db1 = DatabaseConnectionSingleton()
    db2 = DatabaseConnectionSingleton()

    assert db1 is db2
    print("Same DB connection instance:", db1 is db2)

    # Create a table and insert a record via db1
    db1.execute_query("CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT)")
    db1.execute_query("INSERT INTO students (name) VALUES (?)", ("Amine",))

    # Query the same in-memory database via db2
    rows = db2.execute_query("SELECT * FROM students").fetchall()
    print("Rows retrieved from db2:", rows)

    db1.close()
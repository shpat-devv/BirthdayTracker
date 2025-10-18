import sqlite3

class Database:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.connection = None
        self.cursor = None

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_url, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
        else: 
            print("You're already connected, please disconnect first")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
        else: 
            print("No connection")

    def find(self, id, table):
        if not self.connection:
            print("Not connected to any database.")
            return
        
        query = f"SELECT * FROM {table} WHERE user_id = ?"
        res = self.cursor.execute(query, (id,))
        rows = res.fetchall()

        if len(rows) == 0:
            print(f"{table} entry with user_id {id} not found")
        else:
            print(f"{table} found: {rows}")

    def insert(self, table, data): # data should be a dictionary
        if not self.connection:
            print("Not connected to any database.")
            return

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = tuple(data.values())

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.connection.commit()
        print(f"Inserted into {table}: {data}")

    def delete(self, id, table):
        if not self.connection:
            print("Not connected to any database.")
            return

        query = f"DELETE FROM {table} WHERE user_id = ?"
        self.cursor.execute(query, (id,))
        self.connection.commit()

        if self.cursor.rowcount == 0:
            print(f"No record with user_id {id} found in {table}")
        else:
            print(f"Deleted record with user_id {id} from {table}")

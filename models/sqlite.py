import sqlite3

class SQLiteManager:
    def __init__(self, db_name="productos.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()

    def fetch_data(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    def close_connection(self):
        print("Closing connection...")
        self.conn.close()

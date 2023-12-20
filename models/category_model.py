from models.sqlite import SQLiteManager

class CategoryManager:
    def __init__(self):
        self.db = SQLiteManager()

    def insert_categoria(self, codigo, descripcion):
        insert_query = "INSERT INTO categorias (codigo, descripcion) VALUES (?, ?)"
        self.db.execute_query(insert_query, (codigo, descripcion))

    def get_all_categories(self):
        select_all_query = "SELECT codigo, descripcion FROM categorias"
        return self.db.fetch_data(select_all_query)

    def close_connection(self):
        self.db.close_connection()

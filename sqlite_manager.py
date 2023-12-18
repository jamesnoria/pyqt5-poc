import sqlite3


class SQLiteManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        # columns format example: "id INTEGER PRIMARY KEY, name TEXT, age INTEGER"
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert_data(self, table_name, data):
        # data format example: ("John Doe", 30)
        # avoid id column if you want to use autoincrement
        insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['?']*len(data))})"
        self.cursor.execute(insert_query, data)
        self.conn.commit()

    def insert_categoria(self, table_name, codigo, descripcion):
        # data format example: ("John Doe", 30)
        insert_query = f"INSERT INTO {table_name} (codigo, descripcion) VALUES('{codigo}', '{descripcion}');"
        print(insert_query)
        self.cursor.execute(insert_query)
        self.conn.commit()
    
    def insert_producto(self, table_name, producto, codigo, categoria, descripcion, precioCompra, precioVenta, stock, fechaRegistro):
        # data format example: ("John Doe", 30)
        insert_query = f"INSERT INTO {table_name} (producto, codigo, categoria, descripcion, precioCompra, precioVenta, stock, fechaRegistro) VALUES('{producto}', '{codigo}', '{categoria}', '{descripcion}', '{precioCompra}', '{precioVenta}', '{stock}', '{fechaRegistro}');"
        print(insert_query)
        self.cursor.execute(insert_query)
        self.conn.commit()

    def get_all_data(self, table_name):
        select_all_query = f"SELECT producto, codigo, categoria, descripcion, precioCompra, precioVenta, stock, fechaRegistro FROM {table_name}"
        self.cursor.execute(select_all_query)
        rows = self.cursor.fetchall()
        print(rows)
        return rows
    
    def get_categoria(self, table_name):
        select_all_query = f"SELECT codigo, descripcion from {table_name}"
        self.cursor.execute(select_all_query)
        rows = self.cursor.fetchall()
        return rows
    
    def get_products_by_category(self, table_name, categoria):
        select_all_query = f"SELECT producto, codigo, categoria, descripcion, precioCompra, precioVenta, stock, fechaRegistro FROM {table_name} WHERE categoria = '{categoria}'"
        print(select_all_query)
        self.cursor.execute(select_all_query)
        rows = self.cursor.fetchall()
        print(rows)
        return rows
    
    def login(self, table_name, usuario, password):
        select_all_query = f"SELECT username, password, perfil FROM {table_name} WHERE username = '{usuario}' AND password = '{password}'"
        self.cursor.execute(select_all_query)
        rows = self.cursor.fetchall()
        print(rows)
        return rows
    
    def get_user_profile(self, table_name, usuario):
        select_all_query = f"SELECT perfil FROM {table_name} WHERE username = '{usuario}'"
        self.cursor.execute(select_all_query)
        rows = self.cursor.fetchall()
        print(rows)
        return rows
    
    def get_product_by_name(self, table_name, producto):
        select_all_query = f"SELECT producto, codigo, categoria, descripcion, precioCompra, precioVenta, stock, fechaRegistro FROM {table_name} WHERE producto LIKE '%{producto}%'"
        print(select_all_query)
        self.cursor.execute(select_all_query)
        rows = self.cursor.fetchall()
        print(rows)
        return rows

    def update_data(self, table_name, set_clause, condition):
        # set_clause example: "name = 'Jane Doe', age = 25"
        # condition example: "id = 1"
        update_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        self.cursor.execute(update_query)
        self.conn.commit()

    def delete_data(self, table_name, condition):
        # condition example: "id = 1"
        delete_query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(delete_query)
        self.conn.commit()

    def close_connection(self):
        print("Closing connection...")
        self.conn.close()


# Example usage:
if __name__ == "__main__":
    db_name = "./productos.db"
    manager = SQLiteManager(db_name)

    # avoid id column if you want to use autoincrement

    manager.get_all_data("productos")

    manager.close_connection()

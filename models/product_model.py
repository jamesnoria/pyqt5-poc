from models.sqlite import SQLiteManager

class ProductManager:
    def __init__(self):
        self.db = SQLiteManager()

    def insert_producto(self, producto, codigo, categoria, descripcion, precioCompra, precioVenta, stock, fechaRegistro):
        insert_query = "INSERT INTO productos (producto, codigo, categoria, descripcion, precioCompra, precioVenta, stock, fechaRegistro) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        self.db.execute_query(insert_query, (producto, codigo, categoria, descripcion, precioCompra, precioVenta, stock, fechaRegistro))

    def get_all_products(self):
        select_all_query = "SELECT producto, codigo, categoria, descripcion, precioCompra, precioVenta, stock, fechaRegistro FROM productos"
        return self.db.fetch_data(select_all_query)

    def get_products_by_category(self, categoria):
        select_by_category_query = "SELECT producto, codigo, categoria, descripcion, precioCompra, precioVenta, stock, fechaRegistro FROM productos WHERE categoria = ?"
        return self.db.fetch_data(select_by_category_query, (categoria,))

    def get_product_by_name(self, producto):
        select_by_name_query = "SELECT producto, codigo, categoria, descripcion, precioCompra, precioVenta, stock, fechaRegistro FROM productos WHERE producto LIKE ?"
        return self.db.fetch_data(select_by_name_query, (f'%{producto}%',))

    def close_connection(self):
        self.db.close_connection()

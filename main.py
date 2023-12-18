import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QWidget, QHBoxLayout, QComboBox, QTextEdit, QMessageBox, QDateEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QDialog,
)
from PyQt5.QtCore import pyqtSignal, QDate

from sqlite_manager import SQLiteManager

import pandas as pd

manager_productos = SQLiteManager("./productos.db")


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")

        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.authenticate)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_edit)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_edit)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        # Apply styles
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
            }
            QLineEdit, QPushButton {
                font-size: 14px;
                padding: 6px;
                border-radius: 4px;
                border: 1px solid #cccccc;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #367c39;
            }
        """)

    def authenticate(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        usuario = manager_productos.login("usuarios", username, password)

        if usuario:
            # Return the user's profile upon successful authentication
            self.accept()
            print(usuario[0][2])
            # Assuming 'profile' is a key in your user data
            return usuario[0][2]
        else:
            QMessageBox.warning(
                self, "Error", "Usuario o contraseña incorrectos")
            return None


class AddCategoryDialog(QDialog):

    category_added = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Categoría")

        self.label_codigo_categoria = QLabel("Código de Categoría:")
        self.edit_codigo_categoria = QLineEdit()

        self.label_descripcion_categoria = QLabel("Descripción de Categoría:")
        self.edit_descripcion_categoria = QLineEdit()

        self.btn_guardar = QPushButton("Guardar")
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_salir = QPushButton("Salir")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_guardar)
        button_layout.addWidget(self.btn_limpiar)
        button_layout.addWidget(self.btn_salir)

        layout = QVBoxLayout()
        layout.addWidget(self.label_codigo_categoria)
        layout.addWidget(self.edit_codigo_categoria)
        layout.addWidget(self.label_descripcion_categoria)
        layout.addWidget(self.edit_descripcion_categoria)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.btn_guardar.clicked.connect(self.save_category)
        self.btn_limpiar.clicked.connect(self.clear_fields)
        self.btn_salir.clicked.connect(self.close)

    def save_category(self):
        codigo = self.edit_codigo_categoria.text()
        descripcion = self.edit_descripcion_categoria.text()
        # insert categoria to database
        manager_productos.insert_categoria("categorias", codigo, descripcion)
        new_category = f"{codigo} - {descripcion}"
        # Emit the signal with the new category data
        self.category_added.emit(new_category)
        QMessageBox.information(self, "Categoría Guardada", new_category)
        self.close()

    def clear_fields(self):
        self.edit_codigo_categoria.clear()
        self.edit_descripcion_categoria.clear()


class SearchDialog(QDialog):
    def __init__(self, categories, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Buscar por Categoría")
        self.resize(600, 400)

        self.combo_categoria = QComboBox()
        self.combo_categoria.addItems(categories)
        self.combo_categoria.currentIndexChanged.connect(self.load_data)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["Producto", "Código", "Categoría", "Descripción", "Precio Compra", "Precio Venta", "Stock"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.export_excel_btn = QPushButton("Exportar Excel")
        self.export_excel_btn.clicked.connect(self.export_to_excel)

        self.btn_buscar_nombre = QPushButton("Buscar por Nombre")
        self.btn_buscar_nombre.clicked.connect(self.search_by_name)

        self.exit_btn = QPushButton("Salir")
        self.exit_btn.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.export_excel_btn)
        button_layout.addWidget(self.btn_buscar_nombre)
        button_layout.addStretch()
        button_layout.addWidget(self.exit_btn)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Seleccione una categoría:"))
        layout.addWidget(self.combo_categoria)
        layout.addWidget(self.table)
        layout.addLayout(button_layout)  # Use the button_layout here

        self.setLayout(layout)

        # Load data for the initially selected category
        # Select the first category initially
        self.combo_categoria.setCurrentIndex(0)
        self.load_data()

    def export_to_excel(self):
        pandas_pd = pd.DataFrame()
        db_data = manager_productos.get_products_by_category(
            "productos", self.combo_categoria.currentText())
        pandas_pd = pd.DataFrame(db_data)
        pandas_pd.columns = ["Producto", "Código", "Categoría", "Descripción",
                             "Precio Compra", "Precio Venta", "Stock", "Fecha Registro"]
        pandas_pd.to_excel("productos.xlsx", index=False)
        QMessageBox.information(self, "Exportar a Excel",
                                "Datos exportados a productos.xlsx")
        # close the dialog
        self.close()

    def load_data(self):
        selected_category = self.combo_categoria.currentText()

        # Populate the table with the retrieved data for the initially selected category
        rows = manager_productos.get_products_by_category(
            "productos", selected_category)
        self.table.setRowCount(len(rows))
        for row in range(len(rows)):
            for col in range(7):
                self.table.setItem(
                    row, col, QTableWidgetItem(str(rows[row][col])))

    def search_by_name(self):
        self.close()  # Close the current dialog
        name_dialog = NameSearchDialog(self)
        name_dialog.exec_()  # Open the new dialog for searching by name


class NameSearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Buscar por Nombre")
        self.resize(600, 400)

        self.edit_nombre = QLineEdit()
        self.btn_buscar = QPushButton("Buscar")
        self.btn_exportar_excel = QPushButton("Exportar a Excel")
        self.btn_salir = QPushButton("Salir")

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["Producto", "Código", "Categoría", "Descripción", "Precio Compra", "Precio Venta", "Stock"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ingrese el nombre a buscar:"))
        layout.addWidget(self.edit_nombre)
        layout.addWidget(self.btn_buscar)
        # Add the Excel export button
        layout.addWidget(self.btn_exportar_excel)
        layout.addWidget(self.table)
        layout.addWidget(self.btn_salir)

        self.setLayout(layout)

        self.btn_buscar.clicked.connect(self.search)
        self.btn_salir.clicked.connect(self.close)
        self.btn_exportar_excel.clicked.connect(self.export_to_excel)

    def search(self):
        name_to_search = self.edit_nombre.text()
        rows = manager_productos.get_product_by_name(
            "productos", name_to_search)
        self.table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(
                    row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def export_to_excel(self):
        pandas_pd = pd.DataFrame()
        db_data = manager_productos.get_product_by_name(
            "productos", self.edit_nombre.text())
        pandas_pd = pd.DataFrame(db_data)
        pandas_pd.columns = ["Producto", "Código", "Categoría", "Descripción",
                             "Precio Compra", "Precio Venta", "Stock", "Fecha Registro"]
        pandas_pd.to_excel("productos.xlsx", index=False)
        QMessageBox.information(self, "Exportar a Excel",
                                "Datos exportados a productos.xlsx")
        # close the dialog
        self.close()


class MainWindow(QMainWindow):

    database_about_to_close = pyqtSignal()

    def __init__(self, user_profile):
        super().__init__()

        self.setWindowTitle("Registro de Productos")
        self.showMaximized()  # Maximize the window
        # Set minimum size to current size (maximized)
        self.setMinimumSize(self.size())
        self.setMaximumSize(self.size())

        self.category_dialog = AddCategoryDialog()
        self.category_dialog.category_added.connect(self.add_new_category)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.load_styles()
        self.create_layout()
        self.create_table()

        # Depending on the user's profile, enable/disable features
        if user_profile == "vendedor":
            self.disable_admin_features()

    def disable_admin_features(self):
        # Disable features that are not allowed for "vendedor" profile
        self.btn_nuevo.setEnabled(False)
        self.btn_guardar.setEnabled(False)
        # Disable other admin features as needed
        # ...

        # Disable input fields for "vendedor" profile
        self.edit_producto.setEnabled(False)
        self.edit_codigo.setEnabled(False)
        self.edit_descripcion.setEnabled(False)
        self.edit_precio_compra.setEnabled(False)
        self.edit_precio_venta.setEnabled(False)
        self.edit_stock.setEnabled(False)

        # Change styles for disabled input fields (grayed out)
        disabled_style = "background-color: #f0f0f0; color: #808080;"
        self.edit_producto.setStyleSheet(disabled_style)
        self.edit_codigo.setStyleSheet(disabled_style)
        self.edit_descripcion.setStyleSheet(disabled_style)
        self.edit_precio_compra.setStyleSheet(disabled_style)
        self.edit_precio_venta.setStyleSheet(disabled_style)
        self.edit_stock.setStyleSheet(disabled_style)

        # Connect only "Buscar" button for "vendedor" profile
        self.btn_buscar.clicked.connect(self.show_search_dialog)

    def closeEvent(self, event):
        # Emit signal when the window is closed
        self.database_about_to_close.emit()
        event.accept()

    def show_add_category_dialog(self):
        print("Combo box index:", self.combo_categoria.currentIndex())
        if self.combo_categoria.currentText() == "Agregar Categoría":
            print("Showing dialog")
            self.category_dialog.show()

    def add_new_category(self, new_category):
        # Remove "Agregar Categoría" item if present
        current_index = self.combo_categoria.findText("Agregar Categoría")
        if current_index != -1:
            self.combo_categoria.removeItem(current_index)

        # Add the new category to the combo box
        self.combo_categoria.addItem(new_category)

        # Add "Agregar Categoría" item at the end
        self.combo_categoria.addItem("Agregar Categoría")

    def load_styles(self):
        self.setStyleSheet("""
            /* Estilos para QLineEdit */
            QLineEdit {
                border: 1px solid #ccc;
                padding: 8px;
                border-radius: 3px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }

            /* Estilos para QPushButton */
            QPushButton {
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #367c39;
            }

            /* Estilos para QComboBox */
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 5px;
                background-color: white;
            }
            QComboBox:editable {
                background-color: white;
            }

            /* Estilos para QDateEdit */
            QDateEdit {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 5px;
                background-color: white;
            }
        """)

    def create_layout(self):
        form_layout = QVBoxLayout()

        self.label_producto = QLabel("Registrar Producto:")
        self.edit_producto = QLineEdit()

        self.label_codigo = QLabel("Código Producto:")
        self.edit_codigo = QLineEdit()

        self.label_categoria = QLabel("Categoría:")
        self.combo_categoria = QComboBox()
        # add categoria from database
        categoria = manager_productos.get_categoria("categorias")
        for i in categoria:
            self.combo_categoria.addItem(f"{i[0]} - {i[1]}")
        self.combo_categoria.addItem("Agregar Categoría")

        self.label_descripcion = QLabel("Descripción del Producto:")
        self.edit_descripcion = QTextEdit()

        self.label_precio_compra = QLabel("Precio de Compra:")
        self.edit_precio_compra = QLineEdit()

        self.label_precio_venta = QLabel("Precio de Venta:")
        self.edit_precio_venta = QLineEdit()

        self.label_stock = QLabel("Stock:")
        self.edit_stock = QLineEdit()

        self.label_fecha = QLabel("Fecha de Registro:")
        # Create QDate object with the current date
        current_date = QDate.currentDate()

        # Create QDateEdit and set it to the current date
        self.date_fecha = QDateEdit(current_date)
        self.date_fecha.setCalendarPopup(True)

        self.btn_nuevo = QPushButton("Nuevo")
        self.btn_guardar = QPushButton("Guardar")
        self.btn_buscar = QPushButton("Buscar")
        self.btn_salir = QPushButton("Salir")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_nuevo)
        button_layout.addWidget(self.btn_guardar)
        button_layout.addWidget(self.btn_buscar)
        button_layout.addWidget(self.btn_salir)

        form_layout.addWidget(self.label_producto)
        form_layout.addWidget(self.edit_producto)
        form_layout.addWidget(self.label_codigo)
        form_layout.addWidget(self.edit_codigo)
        form_layout.addWidget(self.label_categoria)
        form_layout.addWidget(self.combo_categoria)
        form_layout.addWidget(self.label_descripcion)
        form_layout.addWidget(self.edit_descripcion)
        form_layout.addWidget(self.label_precio_compra)
        form_layout.addWidget(self.edit_precio_compra)
        form_layout.addWidget(self.label_precio_venta)
        form_layout.addWidget(self.edit_precio_venta)
        form_layout.addWidget(self.label_stock)
        form_layout.addWidget(self.edit_stock)
        form_layout.addWidget(self.label_fecha)
        form_layout.addWidget(self.date_fecha)
        form_layout.addLayout(button_layout)

        self.form_widget = QWidget()  # Widget to contain the form layout
        self.form_widget.setLayout(form_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["Producto", "Código", "Categoría", "Descripción",
                "Precio Compra", "Precio Venta", "Stock", "Fecha Registro"]
        )
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        table_layout = QVBoxLayout()
        table_layout.addWidget(self.table)

        self.table_widget = QWidget()  # Widget to contain the table layout
        self.table_widget.setLayout(table_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.form_widget)
        main_layout.addWidget(self.table_widget)

        self.central_widget.setLayout(main_layout)

        # Connect buttons to functions
        self.btn_nuevo.clicked.connect(self.clear_fields)
        self.btn_guardar.clicked.connect(self.save_data)
        self.btn_salir.clicked.connect(self.close)
        self.combo_categoria.activated.connect(self.show_add_category_dialog)
        self.btn_buscar.clicked.connect(self.show_search_dialog)

    def show_search_dialog(self):
        categories = [self.combo_categoria.itemText(
            i) for i in range(self.combo_categoria.count())]
        search_dialog = SearchDialog(categories)
        search_dialog.exec_()

    def create_table(self):
        rows = manager_productos.get_all_data("productos")
        self.table.setRowCount(len(rows))
        for row in range(len(rows)):
            for col in range(8):
                item = rows[row][col]
                if isinstance(item, float):
                    item = str(item)
                self.table.setItem(row, col, QTableWidgetItem(str(item)))

    def clear_fields(self):
        self.edit_producto.clear()
        self.edit_codigo.clear()
        self.combo_categoria.setCurrentIndex(0)
        self.edit_descripcion.clear()
        self.edit_precio_compra.clear()
        self.edit_precio_venta.clear()
        self.edit_stock.clear()
        self.date_fecha.setDate(self.date_fecha.minimumDate())

    def save_data(self):
        # Get product data from input fields
        producto = self.edit_producto.text()
        codigo = self.edit_codigo.text()
        categoria = self.combo_categoria.currentText()
        descripcion = self.edit_descripcion.toPlainText()
        precio_compra = self.edit_precio_compra.text()
        precio_venta = self.edit_precio_venta.text()
        stock = self.edit_stock.text()
        fecha = self.date_fecha.text()

        # Check for empty required fields
        if not all([producto, codigo, categoria, descripcion, precio_compra, precio_venta, stock, fecha]):
            QMessageBox.warning(self, "Campos faltantes",
                                "Por favor, complete todos los campos.")
            return  # Stop execution if any field is empty

        try:
            # Convert precio_compra, precio_venta, and stock to float values
            precio_compra = float(precio_compra)
            precio_venta = float(precio_venta)
            stock = int(stock)
        except ValueError:
            QMessageBox.warning(
                self, "Error de entrada", "Por favor, ingrese valores numéricos en Precio Compra, Precio Venta y Stock.")
            return  # Stop execution if non-numeric values are entered

        # insert producto to database
        manager_productos.insert_producto(
            "productos", producto, codigo, categoria, descripcion, precio_compra, precio_venta, stock, fecha)

        # Add product data to the table
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(producto))
        self.table.setItem(row_position, 1, QTableWidgetItem(codigo))
        self.table.setItem(row_position, 2, QTableWidgetItem(categoria))
        self.table.setItem(row_position, 3, QTableWidgetItem(descripcion))
        self.table.setItem(
            row_position, 4, QTableWidgetItem(str(precio_compra)))
        self.table.setItem(
            row_position, 5, QTableWidgetItem(str(precio_venta)))
        self.table.setItem(row_position, 6, QTableWidgetItem(str(stock)))
        self.table.setItem(row_position, 7, QTableWidgetItem(fecha))

        # Clear input fields after saving
        self.clear_fields()

        QMessageBox.information(self, "Datos Guardados",
                                "Producto guardado en la tabla")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Login Dialog
    login_dialog = LoginDialog()
    user_profile = None
    while user_profile is None:  # Loop until a valid profile is retrieved
        if login_dialog.exec_() == QDialog.Accepted:
            user_profile = login_dialog.authenticate()

    # User Profile Handling
    window = None
    if user_profile == "admin":
        window = MainWindow("admin")
    elif user_profile == "vendedor":
        window = MainWindow("vendedor")

    if window:
        window.database_about_to_close.connect(
            manager_productos.close_connection)
        window.show()
        sys.exit(app.exec_())

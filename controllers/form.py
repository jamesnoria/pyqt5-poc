import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QWidget, QHBoxLayout, QComboBox, QTextEdit, QMessageBox, QDateEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QDialog,
)
from PyQt5.QtCore import pyqtSignal, QDate
import os

def convert_css_to_qt(css):
    # Split the CSS file content into individual rules
    css_rules = css.split('}')

    # Create a dictionary to store CSS properties for each selector
    css_dict = {}
    for rule in css_rules:
        parts = rule.split('{')
        if len(parts) == 2:
            selector = parts[0].strip()
            properties = parts[1].strip()
            css_dict[selector] = properties

    # Convert CSS rules to PyQt5 style
    qt_styles = ''
    for selector, properties in css_dict.items():
        qt_styles += f"{selector} {{ {properties} }}\n"

    return qt_styles

# Vista
form_view = "form_view.css"
form_estilos = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir, "views", form_view))


from models.category_model import CategoryManager
db_category = CategoryManager()

from models.product_model import ProductManager
db_product = ProductManager()

# controllers
from controllers.add_category_controller import AddCategoryDialog
from controllers.search_controller import SearchDialog


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

        # Load CSS
        with open(form_estilos, 'r') as file:
            css_content = file.read()
        qt_style = convert_css_to_qt(css_content)
        self.setStyleSheet(qt_style)

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

    def create_layout(self):
        form_layout = QVBoxLayout()

        self.label_producto = QLabel("Registrar Producto:")
        self.edit_producto = QLineEdit()

        self.label_codigo = QLabel("Código Producto:")
        self.edit_codigo = QLineEdit()

        self.label_categoria = QLabel("Categoría:")
        self.combo_categoria = QComboBox()
        # add categoria from database
        categoria = db_category.get_all_categories()
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
        rows = db_product.get_all_products()
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
        self.date_fecha.setDate(QDate.currentDate())

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
        db_product.insert_producto(
            producto, codigo, categoria, descripcion, precio_compra, precio_venta, stock, fecha)

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


# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     # Login Dialog
#     login_dialog = LoginDialog()
#     user_profile = None
#     while user_profile is None:  # Loop until a valid profile is retrieved
#         if login_dialog.exec_() == QDialog.Accepted:
#             user_profile = login_dialog.authenticate()

#     # User Profile Handling
#     window = None
#     if user_profile == "admin":
#         window = MainWindow("admin")
#     elif user_profile == "vendedor":
#         window = MainWindow("vendedor")

#     if window:
#         window.database_about_to_close.connect(
#             manager_productos.close_connection)
#         window.show()
#         sys.exit(app.exec_())

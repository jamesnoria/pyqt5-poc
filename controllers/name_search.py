from models.product_model import ProductManager
import pandas as pd
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QTableWidget, QHeaderView, QHBoxLayout, \
    QPushButton, QMessageBox, QLineEdit, QTableWidgetItem
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
name_search_view = "name_search_view.css"
name_search_styles = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir, "views", name_search_view))

db = ProductManager()


class NameSearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Buscar por Nombre")
        self.resize(1000, 400)

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

        # Load CSS
        with open(name_search_styles, 'r') as file:
            css_content = file.read()
        qt_style = convert_css_to_qt(css_content)
        self.setStyleSheet(qt_style)

        self.setLayout(layout)

        self.btn_buscar.clicked.connect(self.search)
        self.btn_salir.clicked.connect(self.close)
        self.btn_exportar_excel.clicked.connect(self.export_to_excel)

    def search(self):
        name_to_search = self.edit_nombre.text()
        rows = db.get_product_by_name(name_to_search)
        self.table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(
                    row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def export_to_excel(self):
        pandas_pd = pd.DataFrame()
        db_data = db.get_product_by_name(self.edit_nombre.text())
        pandas_pd = pd.DataFrame(db_data)
        pandas_pd.columns = ["Producto", "Código", "Categoría", "Descripción",
                             "Precio Compra", "Precio Venta", "Stock", "Fecha Registro"]
        pandas_pd.to_excel("productos.xlsx", index=False)
        QMessageBox.information(self, "Exportar a Excel",
                                "Datos exportados a productos.xlsx")
        # close the dialog
        self.close()

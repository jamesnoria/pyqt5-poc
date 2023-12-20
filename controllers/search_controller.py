
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
import os

from controllers.name_search import NameSearchDialog
import pandas as pd

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
search_view = "search_view.css"
search_styles = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir, "views", search_view))


from models.product_model import ProductManager
db = ProductManager()


class SearchDialog(QDialog):
    def __init__(self, categories, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Buscar por Categoría")
        self.resize(1000, 400)

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

        # Load CSS
        with open(search_styles, 'r') as file:
            css_content = file.read()
        qt_style = convert_css_to_qt(css_content)
        self.setStyleSheet(qt_style)

        # Load data for the initially selected category
        # Select the first category initially
        self.combo_categoria.setCurrentIndex(0)
        self.load_data()

    def export_to_excel(self):
        pandas_pd = pd.DataFrame()
        db_data = db.get_products_by_category(
            self.combo_categoria.currentText())
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
        rows = db.get_products_by_category(selected_category)
        self.table.setRowCount(len(rows))
        for row in range(len(rows)):
            for col in range(7):
                self.table.setItem(
                    row, col, QTableWidgetItem(str(rows[row][col])))

    def search_by_name(self):
        self.close()  # Close the current dialog
        name_dialog = NameSearchDialog(self)
        name_dialog.exec_()  # Open the new dialog for searching by name

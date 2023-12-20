
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal
import os

from models.category_model import CategoryManager
db = CategoryManager()

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
category_view = "category_view.css"
category_styles = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir, "views", category_view))

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

        # Load CSS
        with open(category_styles, 'r') as file:
            css_content = file.read()
        qt_style = convert_css_to_qt(css_content)
        self.setStyleSheet(qt_style)

        self.setLayout(layout)

        self.btn_guardar.clicked.connect(self.save_category)
        self.btn_limpiar.clicked.connect(self.clear_fields)
        self.btn_salir.clicked.connect(self.close)

    def save_category(self):
        codigo = self.edit_codigo_categoria.text()
        descripcion = self.edit_descripcion_categoria.text()
        # insert categoria to database
        db.insert_categoria(codigo, descripcion)
        new_category = f"{codigo} - {descripcion}"
        # Emit the signal with the new category data
        self.category_added.emit(new_category)
        QMessageBox.information(self, "Categoría Guardada", new_category)
        # self.close()

    def clear_fields(self):
        self.edit_codigo_categoria.clear()
        self.edit_descripcion_categoria.clear()
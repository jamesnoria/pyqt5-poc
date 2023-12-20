from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
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
login_view = "login_view.css"
login_estilos = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir, "views", login_view))

# Modelo
from models.login_model import LoginManager
db = LoginManager()

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

        # Load CSS
        with open(login_estilos, 'r') as file:
            css_content = file.read()
        qt_style = convert_css_to_qt(css_content)
        self.setStyleSheet(qt_style)

    def authenticate(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        usuario = db.login(username, password)

        if usuario:
            # Return the user's profile upon successful authentication
            self.accept()
            # Assuming 'profile' is a key in your user data
            return usuario[0][2]
        else:
            QMessageBox.warning(
                self, "Error", "Usuario o contraseña incorrectos")
            return None

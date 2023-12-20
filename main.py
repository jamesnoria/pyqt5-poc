import sys
from PyQt5.QtWidgets import QApplication, QDialog

# Controllers
from controllers.login_controller import LoginDialog
from controllers.form import MainWindow

# Models
from models.sqlite import SQLiteManager
db = SQLiteManager()

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
            db.close_connection)
        window.show()
        sys.exit(app.exec_())

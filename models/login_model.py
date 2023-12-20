from models.sqlite import SQLiteManager

class LoginManager:
    def __init__(self):
        self.db = SQLiteManager()

    def login(self, usuario, password):
        login_query = "SELECT username, password, perfil FROM usuarios WHERE username = ? AND password = ?"
        print(login_query)
        return self.db.fetch_data(login_query, (usuario, password))

    def get_user_profile(self, usuario):
        profile_query = "SELECT perfil FROM usuarios WHERE username = ?"
        return self.db.fetch_data(profile_query, (usuario,))

    def close_connection(self):
        self.db.close_connection()
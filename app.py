from flask import Flask
from flask_login import LoginManager
from funcs.sqlite_manager import SQLManger

# flask initation
app = Flask(__name__)
""" Reading secret key from config/secret_key.txt"""
with open("config/secret_key.txt", "r") as secret_:
    app.secret_key = secret_.read()

# sqlite3 initation
sql__ = SQLManger("mivro.db")
sql__.create_table()

""" Importing views """
from views.public_views import *
from views.login_views import *
from views.admin_views import *

if __name__ == "__main__":
    app.run(debug=True)

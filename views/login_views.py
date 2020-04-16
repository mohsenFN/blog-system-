from app import app
from random import choice
from funcs.sqlite_manager import SQLManger
from flask import request, redirect, url_for ,render_template 
from flask_login import login_user, logout_user, login_required, LoginManager, UserMixin
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address as GRA

sql__ = SQLManger("mivro.db")
sql__.create_table()

login_manager = LoginManager()
login_manager.init_app(app)

admins = {"user_name":{"password":"password"}}
limiter = Limiter(app, key_func=GRA, default_limits=["200 per day", "50 per hour"])

headers_list = ['/static/headers/header1.png',
                '/static/headers/header2.png', 
                '/static/headers/header3.png']

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(user__):
    if user__ not in admins:
        return

    user = User()
    user.id = user__
    return user

@login_manager.request_loader
def request_loader(request):
    user__ = request.form.get('user')
    if user__ not in admins:
        return

    user = User()
    user.id = user__
    user.is_authenticated = request.form['password'] == admins[user__]['password']
    return user

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5/minute")
def login():
    if request.method == 'GET':
        return render_template("admin/login.html", header=choice(headers_list))
        
    user__ = request.form['user']
    try:
        if request.form['password'] == admins[user__]['password']:
            user = User()
            user.id = user__
            login_user(user)
            print("22222222222222")
            return redirect(url_for('dashboard'))
            print("1111111")
    except KeyError:
        return render_template("errors/auth_error.html")
    except TypeError:
        print("typo")

    return 'Bad login'

@app.errorhandler(401)
def custom_401(error):
    return render_template("errors/auth_error.html")

@app.route("/signout")
@app.route('/logout')
def logout__():
    logout_user()
    return render_template("admin/logout.html")
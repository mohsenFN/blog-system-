from app import app
from flask import render_template, flash, request
from flask_login import login_required
from funcs.sqlite_manager import SQLManger
from sqlite3 import IntegrityError
from datetime import datetime

sql__ = SQLManger("mivro.db")
sql__.create_table

@app.route("/dashboard")
@app.route("/panel")
@app.route('/admin')
@login_required
def dashboard():
    return render_template("admin/dashboard.html")

@app.route("/new", methods=["GET", "POST"])
@login_required
def new_post__():
    if request.method == "POST":
        form_data = request.form
        try:
            sql__.new_row(form_data["post_title"], form_data["post_subtitle"], form_data["post_id"], form_data["post_category"], form_data["post_subcategory"], datetime.now().strftime("%d %B %Y"), form_data["post_content"])
            flash('post added')
        except IntegrityError:
            flash("choose another post name")  

    return render_template("admin/post.html")

@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove_post__():
    if request.method == "POST":
        rm_post = request.form.get("rm_post")
        if rm_post == "Select":
            flash("No posts is selected !")
        else:
            sql__.delete_post(rm_post)
            flash("Removed0")

    post_list = [post[0] for post in sql__.get_posts()]
    return render_template("admin/remove.html", ll=post_list)

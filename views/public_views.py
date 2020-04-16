from app import app
from random import choice
from itertools import chain
from flask import render_template
from funcs.sqlite_manager import SQLManger


sql__ = SQLManger("mivro.db")
sql__.create_table()

headers_list = ['/static/headers/header1.png',
                '/static/headers/header2.png', 
                '/static/headers/header3.png']

                
@app.route("/home")
@app.route("/")
def index__():    
    """ chaining categories and removing repeated items """
    raw_categs = (list(chain.from_iterable(sql__.list_all_categs())))
    categs = list(dict.fromkeys(raw_categs))

    return render_template("public/index.html", posts=sql__.get_posts(), header=choice(headers_list), categs=categs)

@app.route("/post/<post_id>")
def posts__(post_id):
    post = sql__.get_post_by_id(post_id)
    if len(post) == 1:
        return render_template("public/post.html", post=post[0], header=choice(headers_list))
    else:
        return render_template("errors/post404.html", header=choice(headers_list))

@app.route("/category/<categ>")
@app.route("/categ/<categ>")
def by_categ(categ):
	posts = sql__.get_all_by_categ(str(categ))
	print(len(posts))
	if len(posts) > 0 :
		return render_template("public/category_post.html",posts=posts, category_name=str(categ), header=choice(headers_list))
	else:
		return render_template("errors/category404.html", category_name=categ, header=choice(headers_list))

@app.route("/me")
@app.route("/about")
def about__():
    return render_template("public/about.html", header=choice(headers_list))



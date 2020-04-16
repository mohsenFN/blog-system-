import sqlite3

class SQLManger:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.c = self.conn.cursor()
    
    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS posts(
            title TEXT NOT NULL,
            subtitle TEXT,
			id TEXT NOT NULL PRIMARY KEY,
            category TEXT NOT NULL,
			sub_category TEXT NOT NULL,
			date TEXT NOT NULL,
            content TEXT NOT NULL
        )""")
        self.conn.commit()

    def new_row(self, title_, subtitle_, id_, category_, sub_category, date_, content_):
        self.c.execute("INSERT INTO posts (title, subtitle, id, category, sub_category, date, content) VALUES (?, ?, ?, ?, ?, ?, ?)", (title_, subtitle_, id_, category_, sub_category,date_, content_,))
        self.conn.commit()

    def get_posts(self):
        self.c.execute("SELECT * FROM posts ORDER BY date DESC")
        return self.c.fetchall()
    
    def delete_post(self, post_name):
        self.c.execute("DELETE FROM posts WHERE title=?", (post_name,))
        self.conn.commit()

    def get_post_by_id(self, post_id):
        self.c.execute("SELECT * FROM posts WHERE id=?", (post_id,))
        return self.c.fetchall()

    def get_all_by_categ(self, categ):
        self.c.execute("SELECT * FROM posts WHERE category=? OR sub_category=? ORDER BY date DESC", (categ,categ,))
        return self.c.fetchall()

    def list_all_categs(self):
        self.c.execute("SELECT category, sub_category FROM posts")
        return self.c.fetchall()

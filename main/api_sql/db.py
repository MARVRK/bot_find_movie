import sqlite3
import os

from reportlab.lib.colors import thistle


class DataBase():

    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "databse.db"))
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                date_of_release INTEGER,
                category TEXT,
                movie_code INTEGER,
                image BLOB
                )
            """)
        self.conn.commit()

    def upload_data(self, name, date_of_release, category, movie_code, image):
        self.cursor.execute('INSERT INTO movies(name,date_of_release, category, movie_code, image) values(?,?,?,?,?)',
                            (name, date_of_release, category, movie_code, image))
        self.conn.commit()

    # def get_all_movies(self):
    #     movie_list = []
    #     self.cursor.execute('SELECT id, name from movies')
    #     self.conn.commit()
    #     this = self.cursor.fetchall()
    #     for id, name in this:
    #         movie_list.append((id, name))
    #     return movie_list

    def fetch_all_data(self, movie_code):
        self.cursor.execute('SELECT * from movies WHERE movie_code = ?',
                            (movie_code,))
        self.conn.commit()
        return self.cursor.fetchone()


    def delete_movie(self, name):
        self.cursor.execute('DELETE from movies WHERE name = ?',
                            (name,))
        self.conn.commit()


db = DataBase()
#db.create_table()
# db.get_all_movies()
# db.fetch_all_data(1)

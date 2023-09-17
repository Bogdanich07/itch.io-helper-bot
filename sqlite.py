import sqlite3 as sq
import json

def create_table():
    """Create a "users" table in "data.db" if it doesn't exist"""

    with sq.connect("data.db") as db:
        cursor = db.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id PRIMARY KEY,
                user_name TEXT,
                games_user_follows TEXT
            )
        """
        )
        db.commit()


def read_table():
    with sq.connect("data.db") as db:
        cursor = db.cursor()
        cursor.execute("""SELECT * from users""")
        users = cursor.fetchall()
        table = {}
        for user in users:
            try:
                table[user[0]] = json.loads(user[2])
            except:
                continue
            
        return table

def insert_user(user_id, user_name, games_user_follows=None):
    with sq.connect("data.db") as db:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (user_id, user_name, games_user_follows) VALUES (?, ?, ?)",
            (user_id, user_name, games_user_follows),
        )
        db.commit()


def update_user_name(user_id, user_name):
    """Connect to "data.db" and update the username of a user based on their ID"""
    with sq.connect("data.db") as db:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE users SET user_name = ? WHERE user_id = ?", (user_name, user_id)
        )
        db.commit()


def update_follows(user_id, games_user_follows):
    with sq.connect("data.db") as db:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE users SET games_user_follows = ? WHERE user_id = ?",
            (games_user_follows, user_id),
        )
        db.commit()


def check_user_existence(user_id):
    with sq.connect("data.db") as db:
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()

    return result

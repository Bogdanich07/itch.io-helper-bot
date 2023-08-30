import sqlite3 as sq


def create_table():
    db = sq.connect("data.db")
    cursor = db.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            user_name TEXT
            games_user_follows TEXT
        )
    """
    )

    db.commit()
    db.close()


def insert_user(user_id, user_name):
    db = sq.connect("data.db")
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO users (user_id, user_name) VALUES (?, ?)", (user_id, user_name)
    )

    db.commit()
    db.close()

def update_user_name(user_id, user_name):
    db = sq.connect("data.db")
    cursor = db.cursor()

    cursor.execute(
        "UPDATE users SET user_name = ? WHERE user_id = ?", (user_name, user_id)
    )
    db.commit()


def check_user_existence(user_id):
    conn = sq.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    conn.close()

    return result is not None

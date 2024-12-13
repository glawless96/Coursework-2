import sqlite3
import hashlib


db_file = "user_data.db"

def setup_database():
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            level INTEGER DEFAULT 1
        )
    ''')
    connection.commit()
    connection.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO players (username, password) VALUES (?, ?)', (username, hash_password(password)))
        connection.commit()
        connection.close()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM players WHERE username = ? AND password = ?', (username, hash_password(password)))
    user = cursor.fetchone()
    connection.close()
    return user
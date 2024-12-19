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

def setup_operations_table():
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_operations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            operation TEXT NOT NULL,
            question TEXT NOT NULL,
            difficulty INTEGER NOT NULL,
            level INTEGER NOT NULL,
            correctly_answered INTEGER NOT NULL,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES players (id)
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
        # Insert the new user into the database
        cursor.execute(
            'INSERT INTO players (username, password) VALUES (?, ?)', 
            (username, hash_password(password))
        )
        connection.commit()

        # Retrieve the newly created user's details
        cursor.execute('SELECT * FROM players WHERE username = ?', (username,))
        user_data = cursor.fetchone()
        connection.close()

        if user_data:
            return User(user_data[0], user_data[1])
        else:
            return "User not created. Please try again."
        
    except sqlite3.IntegrityError:
        return None


def login_user(username, password):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM players WHERE username = ? AND password = ?', (username, hash_password(password)))
    user_data = cursor.fetchone()

    if user_data:
        connection.close()
        return User(user_data[0], user_data[1])
    else:
        cursor.execute('SELECT * FROM players WHERE username = ?', (username,))
        user = cursor.fetchone()
        connection.close()
        if user:
            return "Wrong Password"
        else:
            return "Invalid User"

def get_operations_by_user(user_id):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM user_operations
        WHERE user_id = ?
        ORDER BY created DESC
    ''', (user_id,))
    operations = cursor.fetchall()
    connection.close()

    # Return structured data
    return [
        {
            "id": op[0],
            "user_id": op[1],
            "operation": op[2],
            "question": op[3],
            "difficulty": op[4],
            "level": op[5],
            "correctly_answered": bool(op[6]),
            "created": op[7] 
        } for op in operations
    ]

def log_operation(user_id, operation, question, difficulty, level, correctly_answered):
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO user_operations (user_id, operation, question, difficulty, level, correctly_answered)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, operation, question, difficulty, level, int(correctly_answered)))
        
        connection.commit()
        last_row_id = cursor.lastrowid
        connection.close()

        return last_row_id
    except sqlite3.Error as e:
        print(f"Error logging operation: {e}")
        return 'False'

def update_operation(operation_id, correctly_answered):
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE user_operations
            SET correctly_answered = ?
            WHERE id = ?
        ''', (int(correctly_answered), operation_id))
        connection.commit()
        connection.close()
        return True
    except sqlite3.Error as e:
        print(f"Error updating operation: {e}")
        return False

class User:
    def __init__(self, id=None, username =None, level=1, difficulty=1, total_question=0, right_question=0, wrong_question=0):
        self.id = id
        self.username = username
        self.level = level
        self.difficulty = difficulty
        self.total_question = total_question
        self.right_question = right_question
        self.wrong_question = wrong_question
        
    def update_user_details(self, id=None, username =None, level=1, difficulty=1, total_question=0, right_question=0, wrong_question=0):
        self.id = id
        self.username = username
        self.level = level
        self.difficulty = difficulty
        self.total_question = total_question
        self.right_question = right_question
        self.wrong_question = wrong_question
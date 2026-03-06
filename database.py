import sqlite3
import os

DB_PATH = 'science_questions.db'

def get_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def init_db():
    """Initialize the database with the questions table."""
    conn = get_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_name TEXT NOT NULL,
                    question_text TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()

def add_question(student_name, question_text):
    """Add a new question to the database."""
    conn = get_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO questions (student_name, question_text)
                VALUES (?, ?)
            ''', (student_name, question_text))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding question: {e}")
            return False
        finally:
            conn.close()
    return False

def get_all_questions():
    """Retrieve all questions from the database."""
    conn = get_connection()
    questions = []
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT id, student_name, question_text, timestamp FROM questions ORDER BY timestamp DESC')
            rows = cursor.fetchall()
            for row in rows:
                questions.append({
                    'id': row[0],
                    'student_name': row[1],
                    'question_text': row[2],
                    'timestamp': row[3]
                })
        except sqlite3.Error as e:
            print(f"Error fetching questions: {e}")
        finally:
            conn.close()
    return questions

def delete_all_questions():
    """Delete all questions (useful for testing/resetting)."""
    conn = get_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM questions')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting questions: {e}")
        finally:
            conn.close()

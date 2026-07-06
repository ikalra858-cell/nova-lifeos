import sqlite3
import os

DB_NAME = "nova.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        message TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def save_message(role, message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    "INSERT INTO chat_history(role, message) VALUES(?, ?)",
    (role, message)
)

    conn.commit()
    conn.close()

def load_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT role, message FROM chat_history ORDER BY id")

    rows = cursor.fetchall()

    conn.close()

    return rows

def init_tasks_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    
def add_task(task):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks(task) VALUES(?)", (task,))

    conn.commit()
    conn.close()


def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, task FROM tasks")

    rows = cursor.fetchall()

    conn.close()

    return rows 

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))

    conn.commit()
    conn.close()
    
def delete_task_by_name(task_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE LOWER(task)=LOWER(?)",
        (task_name,)
    )

    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted

def delete_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks")

    conn.commit()
    conn.close()

    
def init_notes_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        note TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    

def add_note(note):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes(note) VALUES(?)",
        (note,)
    )

    conn.commit()
    conn.close()


def get_notes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, note FROM notes")

    rows = cursor.fetchall()

    conn.close()

    return rows

def delete_note(note_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE id=?",
        (note_id,)
    )

    conn.commit()
    conn.close()
    
def delete_note_by_name(note_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE LOWER(note)=LOWER(?)",
        (note_name,)
    )

    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted
    
def delete_all_notes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM notes")

    conn.commit()
    conn.close()
    
def init_events_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_event(event):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO events(event) VALUES(?)",
        (event,)
    )

    conn.commit()
    conn.close()
    
def get_events():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM events"
    )

    events = cursor.fetchall()

    conn.close()

    return events

def delete_event(event_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM events WHERE id=?",
        (event_id,)
    )

    conn.commit()
    conn.close()
    
def delete_event_by_name(event_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM events WHERE LOWER(event)=LOWER(?)",
        (event_name,)
    )

    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted
    
def delete_all_events():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM events")

    conn.commit()
    conn.close()


def init_goals_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_goal(goal):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO goals(goal) VALUES(?)",
        (goal,)
    )

    conn.commit()
    conn.close()


def get_goals():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM goals")

    goals = cursor.fetchall()

    conn.close()

    return goals

def delete_goal(goal_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM goals WHERE id=?",
        (goal_id,)
    )

    conn.commit()
    conn.close()
    
def delete_goal_by_name(goal_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM goals WHERE LOWER(goal)=LOWER(?)",
        (goal_name,)
    )

    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted
    
def delete_all_goals():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM goals")

    conn.commit()
    conn.close()
    
def init_memory_table():
    print("DATABASE PATH:", os.path.abspath("nova.db"))
    conn = sqlite3.connect("nova.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS memory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE,
        value TEXT
    )
    """)

    conn.commit()
    conn.close()
    
def save_memory(key, value):

    conn = sqlite3.connect("nova.db")
    c = conn.cursor()

    c.execute("""
    INSERT OR REPLACE INTO memory(key,value)
    VALUES(?,?)
    """,(key,value))

    conn.commit()
    conn.close()
    
def get_memory(key):

    conn = sqlite3.connect("nova.db")
    c = conn.cursor()

    c.execute("""
    SELECT value
    FROM memory
    WHERE key=?
    """,(key,))

    row = c.fetchone()

    conn.close()

    if row:
        return row[0]

    return None

def total_tasks():
    return len(get_tasks())


def total_notes():
    return len(get_notes())


def total_events():
    return len(get_events())


def total_goals():
    return len(get_goals())

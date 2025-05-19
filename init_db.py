import sqlite3

conn = sqlite3.connect('notes.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    note TEXT NOT NULL,
    FOREIGN KEY(username) REFERENCES users(username)
)
''')

conn.commit()
conn.close()

print("Database initialized with tables.")

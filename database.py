# database.py

import sqlite3
import hashlib

# Connect & Create Table
conn = sqlite3.connect("login_app.db")
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
""")
conn.commit()
conn.close()

# Hashing Function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Add New User
def add_user(username, password):
    try:
        hashed = hash_password(password)
        conn = sqlite3.connect("login_app.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO users VALUES (?, ?)", (username, hashed))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# Verify User
def verify_user(username, password):
    hashed = hash_password(password)
    conn = sqlite3.connect("login_app.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
    result = cur.fetchone()
    conn.close()
    return result is not None

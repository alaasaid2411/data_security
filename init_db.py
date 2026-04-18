import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

cursor.execute("DELETE FROM users")

admin_password = hash_password("admin123")
user_password = hash_password("user123")

cursor.execute(
    "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
    ("admin", admin_password, "admin")
)

cursor.execute(
    "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
    ("alaa", user_password, "user")
)

conn.commit()
conn.close()

print("Database created!")
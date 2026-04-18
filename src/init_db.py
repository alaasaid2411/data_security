import sqlite3
import hashlib
#calss to intilize the database and create the table and insert data into it

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS users")

cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

admin_password = hash_password("admin123")
user_password = hash_password("user123")

# Insert initial admin into the database
cursor.execute(
    "INSERT INTO users (username, password_hash, role, status) VALUES (?, ?, ?, ?)",
    ("admin", admin_password, "admin", "logged_out")
)
# Insert initial user into the database
cursor.execute(
    "INSERT INTO users (username, password_hash, role, status) VALUES (?, ?, ?, ?)",
    ("alaa", user_password, "user", "logged_out")
)

conn.commit()
conn.close()

print("Database created successfully!")
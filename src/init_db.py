import sqlite3

try:
    from src.database import DATABASE_PATH
    from src.security import PasswordHasher
except ModuleNotFoundError:
    from database import DATABASE_PATH
    from security import PasswordHasher


# Initialize the database and insert the first admin and standard user.
password_hasher = PasswordHasher()
conn = sqlite3.connect(DATABASE_PATH)
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

admin_password = password_hasher.hash("admin123")
user_password = password_hasher.hash("user123")

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

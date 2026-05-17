import sqlite3
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = ROOT_DIR / "users.db"


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def get_user_by_username(username):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, password_hash, role, status FROM users WHERE username = ?",
            (username,),
        )
        return cursor.fetchone()


def create_user(username, password_hash, role="user"):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash, role, status) VALUES (?, ?, ?, ?)",
            (username, password_hash, role, "logged_out"),
        )
        conn.commit()


def update_password(username, new_password_hash):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password_hash = ? WHERE username = ?",
            (new_password_hash, username),
        )
        conn.commit()


def update_user_status(username, new_status):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET status = ? WHERE username = ?",
            (new_status, username),
        )
        conn.commit()

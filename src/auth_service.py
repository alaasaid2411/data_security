from src.database import create_user, get_user_by_username, update_password, update_user_status
from src.security import PasswordHasher


password_hasher = PasswordHasher()


def authenticate_user(username, password):
    user = get_user_by_username(username)

    if not user:
        return None, "User not found"

    user_id, db_username, db_password_hash, role, status = user

    if password_hasher.hash(password) != db_password_hash:
        return None, "Wrong password"

    update_user_status(db_username, "logged_in")

    return {
        "id": user_id,
        "username": db_username,
        "role": role,
        "status": "logged_in",
    }, ""


def username_exists(username):
    return get_user_by_username(username) is not None


def register_user(username, password):
    if username_exists(username):
        return False, "Username already exists"

    hashed_password = password_hasher.hash(password)
    create_user(username, hashed_password)
    return True, ""


def reset_user_password(username, new_password):
    hashed_password = password_hasher.hash(new_password)
    update_password(username, hashed_password)


def logout_user(username):
    if username:
        update_user_status(username, "logged_out")

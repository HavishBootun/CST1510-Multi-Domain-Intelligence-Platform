import bcrypt
from app.data.users import get_user_by_username, insert_user
from pathlib import Path


def register_user(username, password, role='user'):
    """
    Registers a user by hashing their password, then storing it securely.
    """
    # Hash password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Insert user
    insert_user(username, hashed, role)

    return True, f"User '{username}' registered successfully."


def login_user(username, password):
    """Verifies a user's password via bcrypt hash comparison."""
    user = get_user_by_username(username)

    if not user:
        return False, "User not found."

    stored_hash = user[2]

    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, "Login successful."

    return False, "Incorrect password."

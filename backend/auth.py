from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from database.classes import User
from database.report import Report

ph = PasswordHasher()

def signup_username_valid(name: str) -> Report:
    if len(name) < 3:
        return Report(True, "Username must be at least 3 characters long.")
    if len(name) > 20:
        return Report(True, "Username must be at most 20 characters long.")
    if not name.isalnum():
        return Report(True, "Username must be alphanumeric.")
    return Report(False, "Username is valid.")

def signup_password_valid(password: str) -> Report:
    if len(password) < 6:
        return Report(True, "Password must be at least 6 characters long.")
    if len(password) > 50:
        return Report(True, "Password must be at most 50 characters long.")
    return Report(False, "Password is valid.")

def login_valid(user: User, password: str) -> bool:
    try:
        ph.verify(user.passwordhash, password)
        return True
    except VerifyMismatchError:
        return False
    
def hash_password(password: str) -> str:
    return ph.hash(password)
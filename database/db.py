from database.report import Report
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.exc import IntegrityError
#from sqlalchemy.orm

from database.dbclasses import User, init

global SessionLocal

ph = PasswordHasher()

def ensure_db():
    global SessionLocal
    SessionLocal = init()

def username_correct(name: str) -> Report:
    if len(name) < 3:
        return Report(True, "Username must be at least 3 characters long.")
    if len(name) > 20:
        return Report(True, "Username must be at most 20 characters long.")
    if not name.isalnum():
        return Report(True, "Username must be alphanumeric.")
    return Report(False, "Username is valid.")

def password_correct(password: str) -> Report:
    if len(password) < 6:
        return Report(True, "Password must be at least 6 characters long.")
    if len(password) > 50:
        return Report(True, "Password must be at most 50 characters long.")
    return Report(False, "Password is valid.")

def create_user(name: str, password: str) -> Report:
    name = name.strip().lower()
    
    username_report = username_correct(name)
    if username_report.is_error:
        return username_report

    password_report = password_correct(password)
    if password_report.is_error:
        return password_report

    passwordhash = ph.hash(password)

    with SessionLocal() as session:
        user = User(name=name, passwordhash=passwordhash)
        session.add(user)

        try:
            session.commit()
            print(user.id)
            return Report(False, "User created successfully.")
        except IntegrityError:
            session.rollback()
            return Report(True, "User already exists.")

def is_valid_user(name: str, password: str) -> bool:
    name = name.strip().lower()

    with SessionLocal() as session:
        user = session.query(User).filter_by(name=name).first()

        if user is None:
            return False

        try:
            ph.verify(user.passwordhash, password)
            return True
        except VerifyMismatchError:
            return False
        
def list_users() -> list[str]:
    with SessionLocal() as session:
        return [
            name
            for (name,) in session.query(User.name).all()
        ]
    
def delete_user(name: str) -> None:
    with SessionLocal() as session:
        session.query(User).filter_by(name=name).delete()
        session.commit()

def delete_user_with_id(id: int) -> None:
    with SessionLocal() as session:
        session.query(User).filter_by(id=id).delete()
        session.commit()
## Administrative functions for the database, such as
## creating users, logins etc.

from database.report import Report
from sqlalchemy.exc import IntegrityError

import backend.auth as auth
from database.classes import User, init

global SessionLocal

def ensure_db():
    global SessionLocal
    SessionLocal = init()

def create_user(name: str, password: str) -> Report:
    name = name.strip().lower()
    
    username_report = auth.signup_username_valid(name)
    if username_report.is_error:
        return username_report

    password_report = auth.signup_password_valid(password)
    if password_report.is_error:
        return password_report

    passwordhash = auth.hash_password(password)

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

## Used for authentication
## returns True if login is successful
def is_valid_user(name: str, password: str) -> bool:
    name = name.strip().lower()

    with SessionLocal() as session:
        user = session.query(User).filter_by(name=name).first()

        if user is None:
            return False
        
        return auth.login_valid(user, password)
        
def list_users() -> list[str]:
    with SessionLocal() as session:
        return [
            name
            for (name,) in session.query(User.name).all()
        ]
    
def get_uid_by_name(name: str) -> int:
    name = name.strip().lower()

    with SessionLocal() as session:
        user = session.query(User).filter_by(name=name).first()

        if user is None:
            return -1
        
        return user.id

def get_user_by_uid(id: int) -> User:
    with SessionLocal() as session:
        user = session.get(id)
        return user

def get_username_by_uid(id: int) -> str:
    user: User = get_user_by_uid(id)

    if user is None:
        return ""
    
    return user.name

def delete_user(name: str) -> None:
    with SessionLocal() as session:
        session.query(User).filter_by(name=name).delete()
        session.commit()

def delete_user_with_id(id: int) -> None:
    with SessionLocal() as session:
        session.query(User).filter_by(id=id).delete()
        session.commit()
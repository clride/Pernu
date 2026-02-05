import getpass
import sys

sys.path.append('..')
from database import db as db

def main():
    db.ensure_db()

    print("Current users:", db.list_users())

    login_success = False

    while not login_success:
        login_name = input("Login - Enter username: ")
        login_password = getpass.getpass("Login - Enter password: ")
        if db.is_valid_user(login_name, login_password):
            print("Login successful!")  
            login_success = True
        else:
            print("Invalid username or password. Please try again.")

if __name__ == "__main__":
    main()
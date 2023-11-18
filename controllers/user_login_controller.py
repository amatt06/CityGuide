from db.user_table import email_exists
from db.user_table import match_password


def authenticate(email, password):
    if email_exists(email):
        if match_password(email, password):
            return True
    return False


def login():
    print("Logged In")

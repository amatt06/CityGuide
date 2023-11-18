from db.user_table import email_exists
from db.user_table import match_password
from flask import flash


def authenticate(email, password):
    if email_exists(email):
        if match_password(email, password):
            login(email)
            return True
        else:
            flash("Incorrect password. Please try again.", 'error')
            return False
    else:
        flash("Account not found. Please register.", 'error')
    return False


def login(email):
    print(f"Logged In : {email}")

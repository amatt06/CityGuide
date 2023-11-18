from db.user_table import email_exists
from db.user_table import match_password
from flask import flash, session


def authenticate(email, password):
    if email_exists(email):
        if match_password(email, password):
            session_start(email)
            return True
        else:
            flash("Incorrect password. Please try again.", 'error')
            return False
    else:
        flash("Account not found. Please register.", 'error')
    return False


def session_start(email):
    session['user_email'] = email
    print(f"Logged In : {email}")


def logout():
    # Perform any logout-related tasks here
    session.pop('user_email', None)
    print("Logged Out")

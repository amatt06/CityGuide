from flask import redirect, url_for, session


def login_required(view_func):
    def wrapper(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('login'))
        return view_func(*args, **kwargs)

    return wrapper


def logout_required(view_func):
    def wrapper(*args, **kwargs):
        if 'user_email' in session:
            return redirect(url_for('logout_route'))
        return view_func(*args, **kwargs)

    return wrapper

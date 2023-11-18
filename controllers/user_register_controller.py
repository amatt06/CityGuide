import bcrypt
from db.user_table import email_exists, table


def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


def register_user(email, password):
    if email_exists(email):
        return None

    hashed_password = hash_password(password)

    table.put_item(
        Item={
            'Email': email,
            'Password': hashed_password,
        }
    )
    return email

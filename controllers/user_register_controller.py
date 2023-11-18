import bcrypt
from db.city_guide_user import dynamodb
from db.city_guide_user import email_exists


def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


def register_user(email, password):
    if email_exists(email):
        return None

    hashed_password = hash_password(password)

    table_name = 'CityGuideUsers'
    table = dynamodb.Table(table_name)

    table.put_item(
        Item={
            'Email': email,
            'Password': hashed_password,
        }
    )
    return email

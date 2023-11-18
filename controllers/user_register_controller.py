import bcrypt
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')


def is_email_unique(email):
    table = dynamodb.Table('CityGuideUsers')

    try:
        response = table.get_item(
            Key={
                'Email': email
            }
        )
    except ClientError as e:
        print(f"Error checking email uniqueness: {e}")
        return False

    return 'Item' not in response


def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


def register_user(email, password):
    if not is_email_unique(email):
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

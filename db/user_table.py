import bcrypt
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
table = dynamodb.Table('CityGuideUsers')


def email_exists(email):
    try:
        response = table.get_item(
            Key={
                'Email': email
            }
        )
    except ClientError as e:
        print(f"Error checking email : {e}")
        return False

    return 'Item' in response


def match_password(email, password):
    try:
        response = table.get_item(
            Key={
                'Email': email
            }
        )
    except ClientError as e:
        print(f"Error checking password: {e}")
        return False

    if 'Item' not in response:
        return False

    hashed_password = response['Item'].get('Password')

    hashed_password = bytes(hashed_password)

    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

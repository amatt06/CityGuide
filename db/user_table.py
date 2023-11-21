import bcrypt
import boto3

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
table = dynamodb.Table('CityGuideUsers')


def email_exists(email):
    response = table.get_item(
        Key={
            'Email': email
        }
    )

    return 'Item' in response


def match_password(email, password):
    response = table.get_item(
        Key={
            'Email': email
        }
    )

    hashed_password = response['Item'].get('Password')

    hashed_password = bytes(hashed_password)

    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

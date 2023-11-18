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
        print(f"Error checking email uniqueness: {e}")
        return False

    return 'Item' in response

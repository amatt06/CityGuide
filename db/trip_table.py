import boto3
import json

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
trips_table = dynamodb.Table('CityGuideTrips')
trip_data_bucket = 'city-guide-trip-data'


def save_trip(user_email, trip_id, trip_name, trip_notes, s3_url):
    response = trips_table.put_item(
        Item={
            'Email': user_email,
            'TripID': trip_id,
            'TripName': trip_name,
            'TripNotes': trip_notes,
            'S3URL': s3_url,
        }
    )
    print("Save trip successful:", response)
    return True


def get_user_trips(user_email):
    response = trips_table.query(
        KeyConditionExpression='Email = :email',
        ExpressionAttributeValues={':email': user_email}
    )
    return response.get('Items', [])


def get_trip_details(email, trip_id):
    response = trips_table.get_item(
        Key={
            'Email': email,
            'TripID': trip_id,
        }
    )
    item = response.get('Item')
    if item:
        s3_url = item.get('S3URL')
        trip_data = get_trip_data_from_s3(s3_url)
        return trip_data


def get_trip_data_from_s3(s3_url):
    bucket, key = get_bucket(s3_url)

    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')

    trip_data = json.loads(content)

    return trip_data


def get_bucket(s3_url):
    parts = s3_url[5:].split('/', 1)
    bucket = parts[0]
    key = parts[1] if len(parts) > 1 else ''
    return bucket, key

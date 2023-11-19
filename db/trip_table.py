import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
trips_table = dynamodb.Table('CityGuideTrips')
trip_data_bucket = 'city-guide-trip-data'


def save_trip(user_email, trip_id, trip_name, trip_notes, s3_url):
    try:
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
    except ClientError as e:
        print("Error saving trip:", e)
        return False

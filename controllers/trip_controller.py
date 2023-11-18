import json
from uuid import uuid4
from db.trip_table import s3, trips_table, trip_data_bucket


class TripController:
    @staticmethod
    def generate_trip_id():
        return str(uuid4())

    @staticmethod
    def save_to_s3(email, trip_id, title, trip_data):
        s3_key = f"{email}/{trip_id}.{title}.json"
        s3.put_object(
            Bucket=trip_data_bucket,
            Key=s3_key,
            Body=json.dumps(trip_data),
            ContentType='application/json'
        )
        return s3_key

    @staticmethod
    def save_to_dynamodb(trip_id, email, title, notes, s3_key):
        trips_table.put_item(
            Item={
                'TripID': trip_id,
                'Email': email,
                'Title': title,
                'Notes': notes,
                'S3Key': s3_key
            }
        )

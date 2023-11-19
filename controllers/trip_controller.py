import json
import uuid
from db.trip_table import save_trip, s3, trip_data_bucket


def generate_trip_id(user_email, trip_name):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{user_email}_{trip_name}"))


def save_to_s3(user_email, trip_id, trip_data):
    s3_key = f"{user_email}/{trip_id}.json"
    s3_object_url = f"s3://{trip_data_bucket}/{s3_key}"

    trip_json = json.dumps(trip_data)

    s3.put_object(Bucket=trip_data_bucket, Key=s3_key, Body=trip_json)

    return s3_object_url


def save_trip_to_db(user_email, trip_id, trip_name, trip_notes, s3_url):
    save_trip(user_email, trip_id, trip_name, trip_notes, s3_url)

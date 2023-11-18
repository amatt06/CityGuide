import boto3

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
trips_table = dynamodb.Table('CityGuideTrips')
trip_data_bucket = 'city-guide-trip-data'

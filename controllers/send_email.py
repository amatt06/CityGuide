import json

import boto3


def invoke_lambda(user_email, trip_name, google_maps_data):
    lambda_client = boto3.client('lambda', region_name='sp-southeast-2')

    payload = {'email': user_email, 'trip_name': trip_name, 'google_maps_data': google_maps_data}

    try:
        response = lambda_client.invoke(
            FunctionName='CityGuideEmail',
            InvocationType='Event',
            Payload=json.dumps(payload)
        )
        print("Lambda Invocation Response:", response)
    except Exception as e:
        print("Error invoking Lambda function:", e)

import requests

import json


def invoke_lambda_api_gateway(user_email, trip_name, google_maps_data):
    api_gateway_url = "https://cnzkyo3xkl.execute-api.ap-southeast-2.amazonaws.com/save_trip"

    payload = {'email': user_email, 'trip_name': trip_name, 'google_maps_data': google_maps_data}

    requests.post(api_gateway_url, json=payload)

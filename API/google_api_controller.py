import os
import requests
from dotenv import load_dotenv

load_dotenv()


def sort_places(places, sorting_option):
    if sorting_option == 'rating':
        places.sort(key=lambda x: x['rating'], reverse=True)
    elif sorting_option == 'reviews':
        places.sort(key=lambda x: x['user_ratings_total'], reverse=True)


def parse_google_maps_data(api_response, num_results):
    places = []
    for result in api_response.get('results', []):
        if len(places) >= num_results:
            break

        place_name = result.get('name', 'N/A')
        rating = result.get('rating', 'N/A')
        formatted_address = result.get('formatted_address', 'N/A')
        user_ratings_total = result.get('user_ratings_total', 'N/A')

        price_level = result.get('price_level', 'N/A')
        price_level_str = 'N/A' if price_level == 'N/A' else '$' * price_level

        place_info = {
            'name': place_name,
            'rating': rating,
            'formatted_address': formatted_address,
            'user_ratings_total': user_ratings_total,
            'price_level': price_level_str,
        }

        places.append(place_info)

    return places


class GoogleMapsAPIController:
    def __init__(self):
        self.base_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
        self.api_key = os.getenv('GOOGLE_API_KEY')

    def get_google_maps_data(self, city, sorting_option='rating', num_results=20, place_type='all'):
        place_types = []
        if place_type.lower() == 'restaurants' or place_type.lower() == 'all':
            place_types.append('restaurant')
        if place_type.lower() == 'attractions' or place_type.lower() == 'all':
            place_types.append('tourist_attraction')

        all_places = []

        for pt in place_types:
            params = {
                'query': f'{city} {pt}',
                'key': self.api_key,
            }

            if pt:
                params['type'] = pt

            response = requests.get(self.base_url, params=params)
            data = response.json()

            places_data = parse_google_maps_data(data, num_results)
            all_places.extend(places_data)

            if len(all_places) >= num_results:
                break

        sort_places(all_places, sorting_option)

        return all_places

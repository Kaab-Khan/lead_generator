import time

from typing import List, Dict
import requests
from src.infrastructure.config.settings import Settings

settings = Settings()

class PlacesSearchService:
    """
    Service to interact with Google Places API
    """

    BASE_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def search_places(self, lat: float, lng: float, radius: int, max_results: int) -> List[Dict]:
        """
        Calls Google Places API to search for businesses around (lat, lng)
        """
        places = []
        params = {
            "location": f"{lat},{lng}",
            "radius": radius,
            "key": self.api_key
        }

        while True:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if data['status'] != 'OK' and data['status'] != 'ZERO_RESULTS':
                raise ValueError(f"Places API error: {data.get('status')}")

            places.extend(data.get('results', []))

            if 'next_page_token' in data and len(places) < max_results:
                params['pagetoken'] = data['next_page_token']
                time.sleep(2)  # Wait for token to become valid
            else:
                break

        return places[:max_results]
    

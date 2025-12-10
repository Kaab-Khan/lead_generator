from typing import Tuple
import requests
from src.infrastructure.config.settings import Settings
settings = Settings()

class GeocodeService:
    """
    Service to interact with Google Geocoding API
    """

    BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def geocode(self, area_name: str) -> Tuple[float, float]:
        """
        Calls Google Geocoding API to convert area → (lat, lng)
        """
        params = {
            "address": area_name,
            "key": self.api_key
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data['status'] != 'OK' or not data['results']:
            raise ValueError(f"Geocoding API error: {data.get('status')}")

        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']

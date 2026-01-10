from typing import Tuple, Optional

import requests

from src.infrastructure.config.settings import settings
from src.infrastructure.monitoring import RateLimiter, APICostTracker


class GeocodeService:
    BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

    def __init__(
        self, 
        api_key: str | None = None,
        rate_limiter: Optional[RateLimiter] = None,
        cost_tracker: Optional[APICostTracker] = None,
    ) -> None:
        self.api_key = api_key or settings.google_maps_api_key
        self.rate_limiter = rate_limiter
        self.cost_tracker = cost_tracker

    def geocode_area(self, area_name: str) -> Tuple[float, float]:
        """
        Convert an area name (e.g. 'Luton, UK') into (lat, lng) using Google Geocoding API.
        """
        if self.rate_limiter:
            self.rate_limiter.wait_if_needed()
        
        params = {
            "address": area_name,
            "key": self.api_key,
        }
        resp = requests.get(self.BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        if self.cost_tracker:
            self.cost_tracker.track_geocoding()

        status = data.get("status")
        if status != "OK" or not data.get("results"):
            raise ValueError(f"Geocoding failed for area='{area_name}', status={status}, data={data}")

        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]

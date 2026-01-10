import time
from typing import Any, Dict, Optional

import requests

from src.infrastructure.config.settings import settings
from src.infrastructure.monitoring import RateLimiter, APICostTracker


class PlaceDetailsService:
    BASE_URL = "https://maps.googleapis.com/maps/api/place/details/json"

    def __init__(
        self, 
        api_key: str | None = None,
        rate_limiter: Optional[RateLimiter] = None,
        cost_tracker: Optional[APICostTracker] = None,
    ) -> None:
        self.api_key = api_key or settings.google_maps_api_key
        self.sleep_between_calls = settings.details_sleep_seconds
        self.rate_limiter = rate_limiter
        self.cost_tracker = cost_tracker

    def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        if self.rate_limiter:
            self.rate_limiter.wait_if_needed()
        
        fields = [
            "name",
            "formatted_address",
            "formatted_phone_number",
            "website",
            "rating",
            "user_ratings_total",
            "url",
        ]

        params = {
            "place_id": place_id,
            "fields": ",".join(fields),
            "key": self.api_key,
        }

        resp = requests.get(self.BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        if self.cost_tracker:
            self.cost_tracker.track_place_details()

        status = data.get("status")
        if status != "OK":
            return None

        time.sleep(self.sleep_between_calls)
        return data.get("result") or None

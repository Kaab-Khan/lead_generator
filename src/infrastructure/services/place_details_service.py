import time
from typing import Any, Dict, Optional

import requests

from src.infrastructure.config.settings import settings


class PlaceDetailsService:
    BASE_URL = "https://maps.googleapis.com/maps/api/place/details/json"

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or settings.google_maps_api_key
        self.sleep_between_calls = settings.details_sleep_seconds

    def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch detailed info for a single place_id using Google Place Details API.
        Returns a dict or None on non-OK status.
        """
        fields = [
            "name",
            "formatted_address",
            "formatted_phone_number",
            "website",
            "rating",
            "user_ratings_total",
            "url",  # Google Maps business URL
        ]

        params = {
            "place_id": place_id,
            "fields": ",".join(fields),
            "key": self.api_key,
        }

        resp = requests.get(self.BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        status = data.get("status")
        if status != "OK":
            # Could be NOT_FOUND, INVALID_REQUEST, etc. — just skip.
            return None

        # small delay to be gentle with rate limits
        time.sleep(self.sleep_between_calls)
        return data.get("result") or None


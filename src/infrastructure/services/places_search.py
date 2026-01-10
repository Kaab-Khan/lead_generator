import time
from typing import Any, Dict, List, Optional

import requests

from src.infrastructure.config.settings import settings
from src.infrastructure.monitoring import RateLimiter, APICostTracker


class PlacesSearchService:
    BASE_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    def __init__(
        self, 
        api_key: str | None = None,
        rate_limiter: Optional[RateLimiter] = None,
        cost_tracker: Optional[APICostTracker] = None,
    ) -> None:
        self.api_key = api_key or settings.google_maps_api_key
        self.next_page_sleep = settings.next_page_sleep_seconds
        self.rate_limiter = rate_limiter
        self.cost_tracker = cost_tracker

    def search_places(
        self,
        lat: float,
        lng: float,
        keyword: str,
        radius: int | None = None,
        max_results: int | None = None,
    ) -> List[Dict[str, Any]]:
        radius = radius or settings.default_radius
        max_results = max_results or settings.default_max_results

        params: Dict[str, Any] = {
            "key": self.api_key,
            "location": f"{lat},{lng}",
            "radius": radius,
            "query": keyword,
        }

        all_results: List[Dict[str, Any]] = []

        while True:
            if self.rate_limiter:
                self.rate_limiter.wait_if_needed()
            
            resp = requests.get(self.BASE_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            if self.cost_tracker:
                self.cost_tracker.track_places_search()

            status = data.get("status")
            if status not in ("OK", "ZERO_RESULTS"):
                raise RuntimeError(f"Places search error: status={status}, data={data}")

            results = data.get("results", [])
            all_results.extend(results)

            if len(all_results) >= max_results:
                break

            next_page_token = data.get("next_page_token")
            if not next_page_token:
                break

            time.sleep(self.next_page_sleep)
            params = {"pagetoken": next_page_token, "key": self.api_key}

        return all_results[:max_results]

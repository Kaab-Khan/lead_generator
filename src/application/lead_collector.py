from typing import List, Optional

from src.domain.models import BusinessLead
from src.infrastructure.services.geocode import GeocodeService
from src.infrastructure.services.places_search import PlacesSearchService
from src.infrastructure.services.place_details_service import PlaceDetailsService
from src.infrastructure.config.settings import settings
from src.infrastructure.monitoring import RateLimiter, RateLimitConfig, APICostTracker


class LeadCollector:
    def __init__(
        self,
        geocode_service: Optional[GeocodeService] = None,
        places_search_service: Optional[PlacesSearchService] = None,
        place_details_service: Optional[PlaceDetailsService] = None,
    ) -> None:
        # Initialize rate limiter and cost tracker if enabled
        self.rate_limiter = None
        self.cost_tracker = None
        
        if settings.enable_rate_limiting:
            rate_config = RateLimitConfig(
                requests_per_minute=settings.rate_limit_requests_per_minute,
                requests_per_day=settings.rate_limit_requests_per_day,
            )
            self.rate_limiter = RateLimiter(rate_config)
        
        if settings.enable_cost_tracking:
            self.cost_tracker = APICostTracker()
        
        # Initialize services with rate limiter and cost tracker
        self.geocode_service = geocode_service or GeocodeService(
            rate_limiter=self.rate_limiter,
            cost_tracker=self.cost_tracker,
        )
        self.places_search_service = places_search_service or PlacesSearchService(
            rate_limiter=self.rate_limiter,
            cost_tracker=self.cost_tracker,
        )
        self.place_details_service = place_details_service or PlaceDetailsService(
            rate_limiter=self.rate_limiter,
            cost_tracker=self.cost_tracker,
        )

    def collect_leads(
        self,
        area_name: str,
        keyword: str,
        radius: Optional[int] = None,
        max_results: Optional[int] = None,
    ) -> List[BusinessLead]:
        radius = radius or settings.default_radius
        max_results = max_results or settings.default_max_results

        lat, lng = self.geocode_service.geocode_area(area_name)

        raw_places = self.places_search_service.search_places(
            lat=lat,
            lng=lng,
            keyword=keyword,
            radius=radius,
            max_results=max_results,
        )

        leads: List[BusinessLead] = []

        for place in raw_places:
            place_id = place.get("place_id")
            if not place_id:
                continue

            details = self.place_details_service.get_place_details(place_id)
            if not details:
                continue

            lead = BusinessLead(
                name=details.get("name", ""),
                address=details.get("formatted_address", ""),
                phone=details.get("formatted_phone_number"),
                website=details.get("website"),
                google_maps_url=details.get("url"),
                rating=details.get("rating"),
                user_ratings_total=details.get("user_ratings_total"),
                place_id=place_id,
            )
            leads.append(lead)

        return leads
    
    def get_cost_summary(self):
        """Get the cost tracking summary"""
        if self.cost_tracker:
            return self.cost_tracker.get_summary()
        return None
    
    def print_cost_summary(self):
        """Print the cost tracking summary"""
        if self.cost_tracker:
            self.cost_tracker.print_summary()

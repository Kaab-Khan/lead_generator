from typing import List, Optional

from src.domain.models import BusinessLead
from src.infrastructure.services.geocode import GeocodeService
from src.infrastructure.services.places_search import PlacesSearchService
from src.infrastructure.services.place_details_service import PlaceDetailsService
from src.infrastructure.config.settings import settings


class LeadCollector:
    """
    Orchestrates lead collection using various services
    """

    def __init__(
        self,
        geocode_service: Optional[GeocodeService] = None,
        places_search_service: Optional[PlacesSearchService] = None,
        place_details_service: Optional[PlaceDetailsService] = None,
    ) -> None:
        self.geocode_service = geocode_service or GeocodeService()
        self.places_search_service = places_search_service or PlacesSearchService()
        self.place_details_service = place_details_service or PlaceDetailsService()

    def collect_leads(
        self,
        area_name: str,
        keyword: str,
        radius: Optional[int] = None,
        max_results: Optional[int] = None,
    ) -> List[BusinessLead]:
        """
        Orchestrates:
        - geocode area
        - search places by keyword
        - fetch details per place
        - convert into BusinessLead objects
        """
        radius = radius or settings.default_radius
        max_results = max_results or settings.default_max_results

        # 1. geocode
        lat, lng = self.geocode_service.geocode_area(area_name)

        # 2. search places
        raw_places = self.places_search_service.search_places(
            lat=lat,
            lng=lng,
            keyword=keyword,
            radius=radius,
            max_results=max_results,
        )

        leads: List[BusinessLead] = []

        # 3. details → BusinessLead
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

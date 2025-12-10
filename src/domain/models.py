from dataclasses import dataclass

@dataclass
class BusinessLead:
    name: str
    address: str
    phone: str | None
    website: str | None
    google_maps_url: str | None
    rating: float | None
    user_ratings_total: int | None
    place_id: str | None

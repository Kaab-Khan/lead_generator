from dataclasses import dataclass, field
from typing import Dict
from datetime import datetime


@dataclass
class APICostConfig:
    """
    Google Maps API Pricing (as of 2024)
    Prices are in USD per 1000 requests
    """
    geocoding_per_1000: float = 5.00
    places_text_search_per_1000: float = 32.00
    place_details_per_1000: float = 17.00


@dataclass
class APICallStats:
    """Statistics for API calls"""
    geocoding_calls: int = 0
    places_search_calls: int = 0
    place_details_calls: int = 0
    total_cost: float = 0.0
    started_at: datetime = field(default_factory=datetime.now)
    
    def add_geocoding_call(self, cost_config: APICostConfig) -> None:
        """Record a geocoding API call"""
        self.geocoding_calls += 1
        self.total_cost += cost_config.geocoding_per_1000 / 1000
    
    def add_places_search_call(self, cost_config: APICostConfig) -> None:
        """Record a places search API call"""
        self.places_search_calls += 1
        self.total_cost += cost_config.places_text_search_per_1000 / 1000
    
    def add_place_details_call(self, cost_config: APICostConfig) -> None:
        """Record a place details API call"""
        self.place_details_calls += 1
        self.total_cost += cost_config.place_details_per_1000 / 1000
    
    def get_summary(self) -> Dict[str, any]:
        """Get a summary of API usage and costs"""
        elapsed = datetime.now() - self.started_at
        return {
            "geocoding_calls": self.geocoding_calls,
            "places_search_calls": self.places_search_calls,
            "place_details_calls": self.place_details_calls,
            "total_calls": (
                self.geocoding_calls + 
                self.places_search_calls + 
                self.place_details_calls
            ),
            "total_cost_usd": round(self.total_cost, 4),
            "elapsed_seconds": int(elapsed.total_seconds()),
        }


class APICostTracker:
    """
    Tracks API calls and calculates costs for Google Maps API usage
    """
    
    def __init__(self, cost_config: APICostConfig | None = None) -> None:
        self.cost_config = cost_config or APICostConfig()
        self.stats = APICallStats()
    
    def track_geocoding(self) -> None:
        """Track a geocoding API call"""
        self.stats.add_geocoding_call(self.cost_config)
    
    def track_places_search(self) -> None:
        """Track a places search API call"""
        self.stats.add_places_search_call(self.cost_config)
    
    def track_place_details(self) -> None:
        """Track a place details API call"""
        self.stats.add_place_details_call(self.cost_config)
    
    def get_stats(self) -> APICallStats:
        """Get current statistics"""
        return self.stats
    
    def get_summary(self) -> Dict[str, any]:
        """Get summary of API usage"""
        return self.stats.get_summary()
    
    def print_summary(self) -> None:
        """Print a formatted summary of API usage and costs"""
        summary = self.get_summary()
        print("\n" + "="*50)
        print("API USAGE & COST SUMMARY")
        print("="*50)
        print(f"Geocoding calls:      {summary['geocoding_calls']:>6}")
        print(f"Places search calls:  {summary['places_search_calls']:>6}")
        print(f"Place details calls:  {summary['place_details_calls']:>6}")
        print(f"{'─'*50}")
        print(f"Total API calls:      {summary['total_calls']:>6}")
        print(f"Total cost (USD):     ${summary['total_cost_usd']:>6.4f}")
        print(f"Elapsed time (sec):   {summary['elapsed_seconds']:>6}")
        print("="*50 + "\n")

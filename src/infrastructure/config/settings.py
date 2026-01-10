import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    google_maps_api_key: str
    default_radius: int = 3000
    default_max_results: int = 60
    details_sleep_seconds: float = 0.15
    next_page_sleep_seconds: float = 2.5
    
    # Rate limiting
    enable_rate_limiting: bool = True
    rate_limit_requests_per_minute: int = 60
    rate_limit_requests_per_day: int = 5000
    
    # Cost tracking
    enable_cost_tracking: bool = True

    @classmethod
    def from_env(cls) -> "Settings":
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GOOGLE_MAPS_API_KEY is not set. "
                "Add it to your .env file or environment variables."
            )
        return cls(google_maps_api_key=api_key)


# ✅ this is the missing instantiation
settings = Settings.from_env()

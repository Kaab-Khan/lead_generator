import time
from dataclasses import dataclass
from collections import deque
from typing import Deque


@dataclass
class RateLimitConfig:
    """
    Configuration for API rate limiting
    
    Google Maps API has the following default limits:
    - 1000 requests per minute per API
    - 100,000 requests per day (free tier: $200 credit = ~4000 requests)
    """
    requests_per_minute: int = 60  # Conservative: 60 req/min (1 per second)
    requests_per_day: int = 5000  # Conservative daily limit
    min_delay_seconds: float = 0.1  # Minimum delay between requests


class RateLimiter:
    """
    Rate limiter to prevent exceeding Google Maps API quotas
    Uses a sliding window approach
    """
    
    def __init__(self, config: RateLimitConfig | None = None) -> None:
        self.config = config or RateLimitConfig()
        self.minute_window: Deque[float] = deque()
        self.day_window: Deque[float] = deque()
        self.last_request_time: float = 0.0
    
    def _clean_old_timestamps(self, window: Deque[float], max_age: float) -> None:
        """Remove timestamps older than max_age seconds"""
        current_time = time.time()
        while window and (current_time - window[0]) > max_age:
            window.popleft()
    
    def wait_if_needed(self) -> None:
        """
        Wait if necessary to respect rate limits
        Checks both per-minute and per-day limits
        """
        current_time = time.time()
        
        # Clean old timestamps
        self._clean_old_timestamps(self.minute_window, 60)
        self._clean_old_timestamps(self.day_window, 86400)  # 24 hours
        
        # Check per-minute limit
        if len(self.minute_window) >= self.config.requests_per_minute:
            oldest_in_minute = self.minute_window[0]
            wait_time = 60 - (current_time - oldest_in_minute)
            if wait_time > 0:
                print(f"[RateLimiter] Per-minute limit reached. Waiting {wait_time:.2f}s...")
                time.sleep(wait_time)
                current_time = time.time()
        
        # Check per-day limit
        if len(self.day_window) >= self.config.requests_per_day:
            raise RuntimeError(
                f"Daily API limit reached ({self.config.requests_per_day} requests). "
                "Please wait 24 hours or increase your quota."
            )
        
        # Enforce minimum delay between requests
        if self.last_request_time > 0:
            time_since_last = current_time - self.last_request_time
            if time_since_last < self.config.min_delay_seconds:
                sleep_time = self.config.min_delay_seconds - time_since_last
                time.sleep(sleep_time)
                current_time = time.time()
        
        # Record this request
        self.minute_window.append(current_time)
        self.day_window.append(current_time)
        self.last_request_time = current_time
    
    def get_current_usage(self) -> dict:
        """Get current rate limit usage statistics"""
        self._clean_old_timestamps(self.minute_window, 60)
        self._clean_old_timestamps(self.day_window, 86400)
        
        return {
            "requests_last_minute": len(self.minute_window),
            "requests_today": len(self.day_window),
            "minute_limit": self.config.requests_per_minute,
            "day_limit": self.config.requests_per_day,
            "minute_usage_percent": (len(self.minute_window) / self.config.requests_per_minute) * 100,
            "day_usage_percent": (len(self.day_window) / self.config.requests_per_day) * 100,
        }

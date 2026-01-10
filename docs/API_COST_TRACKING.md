# API Cost Tracking & Rate Limiting Documentation

## Overview

This project includes built-in cost tracking and rate limiting features to help you:
1. **Monitor costs** - Track exactly how much each lead generation run costs
2. **Prevent overages** - Stay within Google Maps API quotas
3. **Optimize usage** - Make informed decisions about API usage

---

## Google Maps API Pricing (2024)

### Cost per 1,000 requests:
- **Geocoding API**: $5.00
- **Places Text Search API**: $32.00
- **Place Details API**: $17.00

### Example Cost Calculation:
For a typical lead generation run:
- 1 Geocoding call (area lookup)
- 1-3 Places Search calls (depends on pagination)
- 60 Place Details calls (one per business)

**Estimated cost**: 
- Geocoding: 1 × $0.005 = $0.005
- Places Search: 2 × $0.032 = $0.064
- Place Details: 60 × $0.017 = $1.020
- **Total**: ~$1.09 per run

---

## Features

### 1. **Cost Tracking**

The `APICostTracker` automatically tracks all API calls and calculates costs in real-time.

**Tracked metrics:**
- Number of Geocoding API calls
- Number of Places Search API calls  
- Number of Place Details API calls
- Total cost in USD
- Elapsed time

**Usage:**
Cost tracking is enabled by default. At the end of each run, you'll see:

```
==================================================
API USAGE & COST SUMMARY
==================================================
Geocoding calls:           1
Places search calls:       2
Place details calls:      60
──────────────────────────────────────────────────
Total API calls:          63
Total cost (USD):     $1.0890
Elapsed time (sec):      127
==================================================
```

**Configuration:**
In `.env` or settings:
```python
ENABLE_COST_TRACKING=true  # Set to false to disable
```

---

### 2. **Rate Limiting**

The `RateLimiter` prevents exceeding Google Maps API quotas using a sliding window approach.

**Default limits:**
- **Per minute**: 60 requests (1 per second - conservative)
- **Per day**: 5,000 requests (conservative for free tier)
- **Minimum delay**: 0.1 seconds between requests

**Behavior:**
- Automatically waits when approaching per-minute limit
- Raises error if daily limit reached
- Enforces minimum delay between requests

**Configuration:**
In `.env`:
```bash
ENABLE_RATE_LIMITING=true
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_REQUESTS_PER_DAY=5000
```

Or in `settings.py`:
```python
enable_rate_limiting: bool = True
rate_limit_requests_per_minute: int = 60
rate_limit_requests_per_day: int = 5000
```

**Example Output:**
```
[RateLimiter] Per-minute limit reached. Waiting 15.32s...
```

---

## Configuration

### Settings Location
File: `src/infrastructure/config/settings.py`

### Available Settings

```python
@dataclass
class Settings:
    # API Configuration
    google_maps_api_key: str
    
    # Search Configuration
    default_radius: int = 3000
    default_max_results: int = 60
    
    # Timing Configuration
    details_sleep_seconds: float = 0.15
    next_page_sleep_seconds: float = 2.5
    
    # Rate Limiting
    enable_rate_limiting: bool = True
    rate_limit_requests_per_minute: int = 60
    rate_limit_requests_per_day: int = 5000
    
    # Cost Tracking
    enable_cost_tracking: bool = True
```

### Environment Variables
File: `.env`

```bash
# Required
GOOGLE_MAPS_API_KEY=your_api_key_here

# Optional (uses defaults if not set)
ENABLE_RATE_LIMITING=true
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_REQUESTS_PER_DAY=5000
ENABLE_COST_TRACKING=true
```

---

## Google Maps API Quotas

### Free Tier
- **Monthly credit**: $200
- **Estimated requests**: ~4,000 Place Details + 12,500 Geocoding + 6,250 Places Search
- **Daily quota**: 100,000 requests per day (across all APIs)

### Paid Tier
- Pay-as-you-go after $200 credit
- No daily limits (unless manually set)
- Can set billing alerts

### Recommendations
1. **Start conservative**: Use default settings (60 req/min, 5,000/day)
2. **Monitor costs**: Check the summary after each run
3. **Adjust as needed**: Increase limits if you have a paid account
4. **Set billing alerts**: In Google Cloud Console

---

## Advanced Usage

### Programmatic Access

```python
from src.application.lead_collector import LeadCollector

collector = LeadCollector()
leads = collector.collect_leads("London, UK", "restaurants")

# Get cost summary as dict
summary = collector.get_cost_summary()
print(f"Total cost: ${summary['total_cost_usd']}")
print(f"Total calls: {summary['total_calls']}")

# Or print formatted summary
collector.print_cost_summary()
```

### Custom Configuration

```python
from src.infrastructure.monitoring import RateLimiter, RateLimitConfig, APICostTracker
from src.application.lead_collector import LeadCollector
from src.infrastructure.services.geocode import GeocodeService

# Custom rate limiting
rate_config = RateLimitConfig(
    requests_per_minute=120,  # Higher limit for paid accounts
    requests_per_day=10000,
    min_delay_seconds=0.05,
)
rate_limiter = RateLimiter(rate_config)

# Custom cost tracker
cost_tracker = APICostTracker()

# Use in services
geocode_service = GeocodeService(
    rate_limiter=rate_limiter,
    cost_tracker=cost_tracker,
)
```

### Disabling Features

To disable cost tracking or rate limiting:

**Option 1: Environment variables**
```bash
ENABLE_COST_TRACKING=false
ENABLE_RATE_LIMITING=false
```

**Option 2: Code**
```python
# In settings.py
enable_cost_tracking: bool = False
enable_rate_limiting: bool = False
```

---

## Troubleshooting

### Issue: "Daily API limit reached"
**Solution**: 
- Wait 24 hours for the limit to reset
- Or increase `rate_limit_requests_per_day` in settings
- Or disable rate limiting (not recommended for free tier)

### Issue: Slow performance
**Solution**:
- Rate limiting adds delays to respect quotas
- If you have a paid account, increase `rate_limit_requests_per_minute`
- Reduce `details_sleep_seconds` (currently 0.15s)

### Issue: Cost tracking shows $0.00
**Solution**:
- Check if `enable_cost_tracking` is set to `true`
- Verify the cost tracker is initialized in LeadCollector

---

## API Cost Optimization Tips

1. **Reduce max_results**: Fetch only what you need
   ```python
   collector.collect_leads("London, UK", "pizza", max_results=20)
   ```

2. **Use specific areas**: Smaller radius = fewer results
   ```python
   collector.collect_leads("London, UK", "pizza", radius=1500)
   ```

3. **Batch processing**: Process multiple keywords in one session to reuse geocoding

4. **Cache results**: Store leads in database to avoid re-fetching

5. **Monitor regularly**: Check cost summaries and adjust strategy

---

## Resources

- [Google Maps Platform Pricing](https://developers.google.com/maps/billing/gmp-billing)
- [API Usage Limits](https://developers.google.com/maps/documentation/places/web-service/usage-and-billing)
- [Billing Alerts Setup](https://cloud.google.com/billing/docs/how-to/budgets)

---

**Last Updated**: 2024-12-13

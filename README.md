# Lead Generator 🎯

A scalable business lead generation tool that leverages the Google Maps Places API to discover and collect business information based on location and keywords. Built with clean architecture principles for maintainability and extensibility.

## 📋 Overview

Lead Generator automates the process of finding potential business leads by:
- Searching for businesses in specific geographic areas
- Collecting detailed business information (name, address, phone, website, ratings)
- Classifying leads by website availability
- Exporting results to CSV files for easy analysis
- Tracking API usage and costs in real-time

## ✨ Features

- **Geographic Search**: Search businesses by city, region, or country
- **Keyword Targeting**: Find businesses by specific industry keywords (e.g., "eyelash extensions", "restaurants")
- **Detailed Business Data**: Collect comprehensive information including:
  - Business name and address
  - Phone numbers
  - Websites
  - Google ratings and review counts
  - Google Maps URLs
- **Lead Classification**: Automatically separate leads with/without websites
- **Cost Tracking**: Monitor Google Maps API usage and estimated costs
- **Rate Limiting**: Built-in protection against API quota exhaustion
- **CSV Export**: Easy-to-use exports for CRM integration

## 🏗️ Architecture

The project follows clean architecture with clear separation of concerns:

```
src/
├── application/              # Application services & use cases
│   ├── lead_collector.py     # Main lead collection orchestration
│   └── lead_classifier.py    # Lead classification logic
│
├── domain/                   # Core business logic
│   ├── models.py             # Business entities (BusinessLead)
│   └── lead_rules.py         # Business rules & validation
│
├── infrastructure/           # External integrations
│   ├── config/
│   │   └── settings.py       # Configuration management
│   ├── services/
│   │   ├── geocode.py        # Google Geocoding API
│   │   ├── places_search.py  # Google Places Search API
│   │   └── place_details_service.py  # Place Details API
│   ├── monitoring/
│   │   ├── rate_limiter.py   # API rate limiting
│   │   └── api_cost_tracker.py  # Cost tracking
│   └── external/
│       └── csv_exporter.py   # CSV file export
│
├── cli.py                    # Command-line interface
└── main.py                   # Application entry point
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Google Maps API key with Places API enabled
- Make (optional, for using Makefile commands)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd lead_generator-1
   ```

2. **Set up virtual environment**
   ```bash
   # Using Make
   make ensure-venv
   make requirements

   # Or manually
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   GOOGLE_MAPS_API_KEY=your_api_key_here
   ```

   To obtain a Google Maps API key:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable Places API, Geocoding API, and Place Details API
   - Create credentials (API Key)
   - Set up billing (required for API usage)

### Usage

**Interactive CLI Mode:**
```bash
# Using Make
make run

# Or manually
source venv/bin/activate
python src/main.py
```

You'll be prompted for:
- **Area**: Geographic location (e.g., "Luton, UK", "New York, USA")
- **Keyword**: Business type or industry (e.g., "eyelash extensions", "coffee shop")

**Example:**
```
Area (e.g. 'Luton, UK'): Manchester, UK
Keyword (e.g. 'eyelash extensions'): nail salon

[INFO] Collecting leads for area='Manchester, UK', keyword='nail salon'...
[INFO] Total leads: 45
[INFO] With website: 28
[INFO] Without website: 17
[INFO] Lead collection and export completed.

==================================================
API USAGE & COST SUMMARY
==================================================
Geocoding calls:           1
Places search calls:       3
Place details calls:      45
──────────────────────────────────────────────────
Total API calls:          49
Total cost (USD):     $0.7810
Elapsed time (sec):      78
==================================================
```

**Output Files:**

CSV files are saved in the `output/` directory:
- `{area}_{keyword}_with_website.csv` - Leads that have websites
- `{area}_{keyword}_without_website.csv` - Leads without websites

### CSV Merger Tool

Merge multiple CSV files and remove duplicates based on `place_id`. Useful when businesses appear in overlapping categories (e.g., a business listed as both "beautician" and "hairdresser").

**Merge by pattern:**
```bash
# Merge all hairdressers in LU postcodes
python3 scripts/merge_csv.py --pattern "lu*_hairdresser_*.csv" \
    --output output/master_hairdressers_luton.csv
```

**Merge by categories:**
```bash
# Merge overlapping beauty service categories
python3 scripts/merge_csv.py \
    --categories hairdresser beautician ladies_hairdresser eyelash_extension \
    --postcodes lu1 lu2 lu3 lu4 lu5 \
    --output output/master_beauty_luton.csv
```

**Merge specific files:**
```bash
python3 scripts/merge_csv.py \
    --files output/file1.csv output/file2.csv output/file3.csv \
    --output output/merged.csv
```

**Features:**
- ✅ Automatic deduplication by `place_id`
- ✅ Pattern matching with glob support
- ✅ Category-based merging across postcodes
- ✅ Detailed merge statistics
- ✅ Preserves data integrity

**Documentation:**
- Full guide: [docs/CSV_MERGER.md](docs/CSV_MERGER.md)
- Quick reference: [docs/CSV_MERGER_QUICK_REFERENCE.md](docs/CSV_MERGER_QUICK_REFERENCE.md)
- Code examples: [examples/csv_merger_examples.py](examples/csv_merger_examples.py)

## ⚙️ Configuration

Edit `src/infrastructure/config/settings.py` or set environment variables:

| Setting | Default | Description |
|---------|---------|-------------|
| `GOOGLE_MAPS_API_KEY` | Required | Your Google Maps API key |
| `default_radius` | 3000 | Search radius in meters |
| `default_max_results` | 60 | Maximum leads to collect |
| `enable_rate_limiting` | True | Enable API rate limiting |
| `rate_limit_requests_per_minute` | 60 | Max requests per minute |
| `rate_limit_requests_per_day` | 5000 | Max requests per day |
| `enable_cost_tracking` | True | Track API costs |
| `details_sleep_seconds` | 0.15 | Delay between detail requests |
| `next_page_sleep_seconds` | 2.5 | Delay for pagination |

## 💰 API Costs

Google Maps API pricing (as of 2024):
- Geocoding: $5.00 per 1,000 requests
- Places Text Search: $32.00 per 1,000 requests
- Place Details: $17.00 per 1,000 requests

**Estimated cost per search:**
- 1 location = ~$0.50-$2.00 (depending on result count)
- 60 results = ~$1.00-$1.50

The tool includes built-in cost tracking to monitor your usage in real-time.

## 🧪 Development

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Run tests
make test
```

### Project Structure

- `src/` - Source code
- `tests/` - Test files
- `docs/` - Additional documentation
- `output/` - Generated CSV files
- `scripts/` - Utility scripts

### Makefile Commands

```bash
make help              # Show all available commands
make ensure-venv       # Create/verify virtual environment
make requirements      # Install runtime dependencies
make requirements-dev  # Install dev dependencies
make run              # Run the application
make format           # Format code with Black
make lint             # Lint code with Pylint
make test             # Run tests with Pytest
make clean            # Remove cache files
make clean-all        # Remove cache + venv
```

## 📚 Dependencies

Core dependencies:
- `fastapi==0.104.1` - Web framework (for future API endpoints)
- `googlemaps==4.10.0` - Google Maps API client
- `requests==2.31.0` - HTTP requests
- `python-dotenv==1.0.0` - Environment variable management
- `openpyxl==3.1.2` - Excel file support
- `pandas==2.1.4` - Data manipulation and CSV handling

Development dependencies:
- `pytest==7.4.2` - Testing framework
- `black==24.10.0` - Code formatting
- `flake8==6.1.0` - Linting

See `requirements.txt` for complete list.

## 🎯 Use Cases

- **Sales Teams**: Generate prospect lists for outbound campaigns
- **Market Research**: Analyze business density in specific areas
- **Competitive Analysis**: Identify competitors in target markets
- **Digital Marketing**: Find businesses without websites for web design services
- **Data Collection**: Build databases for specific industries

## 🔐 Security Notes

- Never commit your `.env` file or API keys to version control
- Keep your Google Cloud API key secure
- Set up API key restrictions in Google Cloud Console
- Monitor API usage to prevent unexpected charges
- Consider setting up billing alerts in Google Cloud

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is provided as-is for educational and commercial use.

## 📞 Support

For issues, questions, or contributions, please open an issue in the repository.

---

**Last Updated:** 2026-01-03

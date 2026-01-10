# CSV Merger - Quick Reference

## Quick Start Examples

### Example 1: Merge All Hairdressers in Luton
```bash
python3 scripts/merge_csv.py --pattern "lu*_hairdresser_*.csv" \
    --output output/master_hairdressers_luton.csv
```
**Result**: Merges regular hairdressers + ladies hairdressers across all LU postcodes

### Example 2: Merge Multiple Categories (Avoid Duplicates)
```bash
python3 scripts/merge_csv.py \
    --categories hairdresser beautician eyelash_extension ladies_hairdresser \
    --postcodes lu1 lu2 lu3 lu4 lu5 \
    --output output/master_beauty_services_luton.csv
```
**Result**: Merges overlapping beauty categories, removing duplicate businesses

### Example 3: Merge Specific Postcode (All Categories)
```bash
python3 scripts/merge_csv.py --pattern "lu1_*.csv" \
    --output output/master_lu1_all_businesses.csv
```
**Result**: All businesses in LU1 postcode across all categories

### Example 4: Merge Specific Files
```bash
python3 scripts/merge_csv.py \
    --files output/lu1_hairdresser_with_website.csv \
            output/lu1_hairdresser_without_website.csv \
    --output output/merged_lu1_hairdressers.csv
```

## Pattern Syntax

- `*` = Match any characters
- `lu*_hairdresser_*.csv` = All hairdresser files in any LU postcode
- `*_beautician_*.csv` = All beautician files regardless of location
- `lu1_*.csv` = All categories in LU1 postcode

## How Deduplication Works

The tool uses **place_id** (Google's unique business identifier) to remove duplicates:

1. Reads all matching CSV files
2. For each row, checks if the place_id has been seen before
3. If new → adds to output
4. If duplicate → skips
5. **First occurrence wins** - if a business appears in multiple files, only the first one is kept

## Why This Matters

Businesses often appear in multiple categories:
- A salon might be listed as "hairdresser", "beautician", AND "ladies_hairdresser"
- Without deduplication, you'd contact the same business 3 times
- With deduplication, you get 1 master list with each business appearing once

## Output Statistics

After running, you'll see:
```
Files processed: 18
Total rows read: 540
Unique rows written: 201
Duplicates removed: 339
```

**339 duplicates removed** means you avoided 339 redundant entries!

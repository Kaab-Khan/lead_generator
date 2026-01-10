# CSV Merger Documentation

## Overview

The CSV Merger tool allows you to merge multiple CSV files from the lead generator and automatically remove duplicates based on `place_id`. This is particularly useful when businesses appear in multiple categories (e.g., a business might be listed as both "beautician" and "hairdresser").

## Features

- **Automatic Deduplication**: Uses `place_id` to ensure each business appears only once
- **Pattern Matching**: Merge files using glob patterns
- **Category-Based Merging**: Merge specific categories across multiple postcodes
- **Statistics Reporting**: Shows how many rows were processed and duplicates removed

## Usage Methods

### 1. Command Line Interface (Recommended)

#### Merge by Pattern

Merge all files matching a pattern:

```bash
# Merge all hairdresser files in LU postcodes
python scripts/merge_csv.py --pattern "lu*_hairdresser_*.csv" \
                             --output output/merged_lu_hairdressers.csv

# Merge all beautician files
python scripts/merge_csv.py --pattern "*_beautician_*.csv" \
                             --output output/merged_all_beauticians.csv
```

#### Merge by Categories and Postcodes

Merge specific categories across specific postcodes:

```bash
# Merge hairdressers, beauticians, and ladies_hairdressers in LU1-LU5
python scripts/merge_csv.py --categories hairdresser beautician ladies_hairdresser \
                             --postcodes lu1 lu2 lu3 lu4 lu5 \
                             --output output/merged_beauty_services_luton.csv

# Merge eyelash extensions in all LU postcodes
python scripts/merge_csv.py --categories eyelash_extension \
                             --postcodes lu1 lu2 lu3 lu4 lu5 lu6 \
                             --output output/merged_eyelash_luton.csv
```

#### Merge Specific Files

Merge explicitly listed files:

```bash
python scripts/merge_csv.py --files output/lu1_hairdresser_with_website.csv \
                                     output/lu1_hairdresser_without_website.csv \
                                     output/lu1_beautician_with_website.csv \
                             --output output/merged_lu1_beauty.csv
```

### 2. Programmatic API

Use the merger in your Python code:

```python
from src.infrastructure.external.csv_merger import CsvMerger

merger = CsvMerger()

# Method 1: Merge by pattern
stats = merger.merge_by_pattern(
    pattern="lu*_hairdresser_*.csv",
    output_file="output/merged_lu_hairdressers.csv",
    base_dir="output"
)

# Method 2: Merge by categories and postcodes
stats = merger.merge_categories(
    categories=['hairdresser', 'beautician', 'ladies_hairdresser'],
    postcodes=['lu1', 'lu2', 'lu3', 'lu4', 'lu5'],
    output_file="output/merged_beauty_luton.csv"
)

# Method 3: Merge specific files
stats = merger.merge_files(
    input_files=[
        "output/lu1_hairdresser_with_website.csv",
        "output/lu1_hairdresser_without_website.csv"
    ],
    output_file="output/merged_lu1.csv"
)

# Check statistics
print(f"Unique rows: {stats['unique_rows_written']}")
print(f"Duplicates removed: {stats['duplicates_removed']}")
```

## Common Use Cases

### Case 1: Merge All Hairdressers in Luton

This includes regular hairdressers, ladies hairdressers, and unisex salons:

```bash
python scripts/merge_csv.py --pattern "lu*_*hairdresser_*.csv" \
                             --output output/master_hairdressers_luton.csv
```

### Case 2: Merge Beauty Services (Overlapping Categories)

Merge beauticians, hairdressers, and eyelash extensions (categories that often overlap):

```bash
python scripts/merge_csv.py --categories hairdresser beautician ladies_hairdresser eyelash_extension \
                             --postcodes lu1 lu2 lu3 lu4 lu5 \
                             --output output/master_beauty_luton.csv
```

### Case 3: Merge by Postcode (All Categories)

Get all businesses in a specific postcode:

```bash
python scripts/merge_csv.py --pattern "lu1_*.csv" \
                             --output output/master_lu1_all_categories.csv
```

### Case 4: Merge With and Without Website Files

Combine both website and non-website versions for a category:

```bash
python scripts/merge_csv.py --pattern "lu*_hairdresser_*.csv" \
                             --output output/master_hairdressers_all.csv
```

## Output Format

The merged CSV will have the same format as the input files:

```csv
name,address,phone,website,google_maps_url,rating,user_ratings_total,place_id
Lucia Hair & Beauty,"90 High Town Rd, Luton LU2 0DQ, UK",01582 459991,http://www.luciahairandbeauty.co.uk/,...
```

## Deduplication Logic

- **Primary Key**: `place_id` (Google Places unique identifier)
- **Strategy**: First occurrence wins - if a business appears in multiple files, only the first occurrence is kept
- **Why place_id**: It's the most reliable unique identifier for businesses across Google Places API results

## Statistics Output

After merging, you'll see statistics like:

```
[CsvMerger] Merge Complete:
  Files processed: 10
  Total rows read: 523
  Unique rows written: 387
  Duplicates removed: 136
  Output: output/merged_beauty_luton.csv
```

## Advanced Options

### Custom Deduplication Field

By default, deduplication uses `place_id`, but you can specify a different field:

```bash
python scripts/merge_csv.py --pattern "lu*_hairdresser_*.csv" \
                             --output output/merged.csv \
                             --dedupe-field phone
```

### Custom Base Directory

Change the directory where input files are searched:

```bash
python scripts/merge_csv.py --pattern "*.csv" \
                             --output merged.csv \
                             --base-dir /path/to/custom/directory
```

## Tips

1. **Check for Overlaps**: Before merging, consider which categories might have overlapping businesses
2. **Use Patterns Wisely**: The `*` wildcard helps match multiple files efficiently
3. **Inspect Output**: Always check the statistics to ensure the merge worked as expected
4. **Keep Originals**: The merger doesn't modify input files, so your original data is safe

## Troubleshooting

**No files found matching pattern**
- Check that the pattern is correct
- Verify files exist in the base directory
- Use quotes around patterns with wildcards

**Fewer rows than expected**
- This is normal - duplicates are being removed
- Check the "Duplicates removed" statistic

**Missing columns in output**
- All input files must have the same column structure
- Ensure all files were generated by the same exporter version

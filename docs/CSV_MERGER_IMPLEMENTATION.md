# CSV Merger Implementation Summary

## Overview

Created a comprehensive CSV merger tool to consolidate lead generation results and eliminate duplicates based on `place_id`. This solves the problem of businesses appearing in multiple categories (e.g., beautician, hairdresser, ladies hairdresser).

## Files Created

1. **`src/infrastructure/external/csv_merger.py`** - Core merger library
2. **`scripts/merge_csv.py`** - CLI tool for easy command-line usage
3. **`docs/CSV_MERGER.md`** - Complete documentation
4. **`docs/CSV_MERGER_QUICK_REFERENCE.md`** - Quick reference guide
5. **`examples/csv_merger_examples.py`** - Code examples

## Key Features

### 1. **Smart Deduplication**
- Uses `place_id` (Google's unique business identifier)
- First occurrence wins - preserves the first seen entry
- Automatically handles overlapping categories

### 2. **Three Merge Methods**

#### Pattern-Based Merging
```bash
python3 scripts/merge_csv.py --pattern "lu*_hairdresser_*.csv" \
    --output output/merged_hairdressers.csv
```
Matches files using glob patterns

#### Category-Based Merging
```bash
python3 scripts/merge_csv.py \
    --categories hairdresser beautician ladies_hairdresser \
    --postcodes lu1 lu2 lu3 lu4 lu5 \
    --output output/merged_beauty.csv
```
Combines specific categories across postcodes

#### Explicit File Merging
```bash
python3 scripts/merge_csv.py \
    --files file1.csv file2.csv file3.csv \
    --output output/merged.csv
```
Merges explicitly listed files

### 3. **Detailed Statistics**
After each merge, shows:
- Files processed
- Total rows read
- Unique rows written
- Duplicates removed
- Output file location

## Real-World Test Results

Test run on hairdresser data:
```
Files processed: 18
Total rows read: 540
Unique rows written: 201
Duplicates removed: 339
```

**Result**: 62.8% duplicate rate! This shows how critical deduplication is when dealing with overlapping business categories.

## Use Cases

### Use Case 1: Master Hairdresser List
Get all hairdressers in Luton without duplicates:
```bash
python3 scripts/merge_csv.py --pattern "lu*_hairdresser_*.csv" \
    --output output/master_hairdressers_luton.csv
```

### Use Case 2: Beauty Services Master List
Merge overlapping beauty categories:
```bash
python3 scripts/merge_csv.py \
    --categories hairdresser beautician eyelash_extension ladies_hairdresser \
    --postcodes lu1 lu2 lu3 lu4 lu5 \
    --output output/master_beauty_luton.csv
```

### Use Case 3: Single Postcode All Categories
Get everything in one postcode:
```bash
python3 scripts/merge_csv.py --pattern "lu1_*.csv" \
    --output output/master_lu1_all.csv
```

### Use Case 4: Combine With/Without Website
Merge both website and non-website versions:
```bash
python3 scripts/merge_csv.py --pattern "lu*_electrician_*.csv" \
    --output output/master_electricians.csv
```

## Why This Matters

**Problem**: Businesses often appear in multiple categories
- A salon might be: hairdresser, beautician, AND ladies_hairdresser
- Without deduplication: contact same business 3 times
- With deduplication: clean master list, contact once

**Solution**: The merger automatically:
1. Identifies duplicates via place_id
2. Keeps only unique businesses
3. Provides statistics on duplicates removed

## Integration Options

### Option 1: Command Line (Simplest)
```bash
python3 scripts/merge_csv.py --pattern "pattern" --output "file.csv"
```

### Option 2: Python API
```python
from src.infrastructure.external.csv_merger import CsvMerger

merger = CsvMerger()
stats = merger.merge_by_pattern("lu*_hairdresser_*.csv", "output.csv")
```

### Option 3: Examples Script
```bash
python3 examples/csv_merger_examples.py
```

## Technical Details

**Deduplication Field**: `place_id` (default, configurable)
**Strategy**: First-seen-first-kept
**File Format**: Standard CSV with headers
**Encoding**: UTF-8
**Memory**: Efficient - processes files sequentially

## Future Enhancements

Potential additions:
1. Custom merge strategies (newest wins, rating-based, etc.)
2. Conflict resolution rules
3. Merge reports (which files contributed which rows)
4. Field mapping/transformation during merge
5. Excel output format support

## Getting Started

1. **Quick test**:
   ```bash
   python3 scripts/merge_csv.py --pattern "lu1_*.csv" \
       --output output/test_merge.csv
   ```

2. **Check documentation**:
   - Full docs: `docs/CSV_MERGER.md`
   - Quick ref: `docs/CSV_MERGER_QUICK_REFERENCE.md`

3. **Run examples**:
   ```bash
   python3 examples/csv_merger_examples.py
   ```

## Success Metrics

✅ Successfully merges multiple CSV files
✅ Removes duplicates based on place_id
✅ Preserves data integrity
✅ Provides detailed statistics
✅ Multiple interface options (CLI, API, examples)
✅ Comprehensive documentation
✅ Tested with real data (62.8% duplicate rate found)

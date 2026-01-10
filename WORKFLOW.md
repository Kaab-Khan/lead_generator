# Lead Generation Workflow

## Step 1: Collect Leads

Run the lead generator:
```bash
make run
```

When prompted:
- **Area**: Enter postcode (e.g., "LU1, UK" or "Luton, UK")
- **Keyword**: Enter business type (e.g., "hairdresser", "beautician", "eyelash extensions")

The tool will create CSV files in the `output/` directory.

---

## Step 2: Merge Results (Remove Duplicates)

### Merge LU Postcodes - Hairdressers (without website only)

```bash
python3 scripts/merge_csv.py --pattern "lu*_*hairdresser_without_website.csv" \
    --output output/merged/merged_lu_hairdressers_no_website.csv
```

This merges:
- All LU postcodes (lu1, lu2, lu3, etc.)
- All hairdresser types (hairdresser, ladies_hairdresser, unisex_hairdresser)
- Only businesses WITHOUT websites

---

## Common Merge Commands

### All hairdressers in LU postcodes (with + without website)
```bash
python3 scripts/merge_csv.py --pattern "lu*_*hairdresser_*.csv" \
    --output output/merged/merged_lu_hairdressers_all.csv
```

### Only WITH website
```bash
python3 scripts/merge_csv.py --pattern "lu*_*hairdresser_with_website.csv" \
    --output output/merged/merged_lu_hairdressers_with_website.csv
```

### Multiple categories WITHOUT website
```bash
python3 scripts/merge_csv.py --pattern "lu*_*_without_website.csv" \
    --output output/merged/merged_lu_all_categories_no_website.csv
```

### Specific categories across multiple postcodes (with + without website)
```bash
python3 scripts/merge_csv.py \
    --categories hairdresser beautician eyelash_extension ladies_hairdresser \
    --postcodes lu1 lu2 lu3 lu4 lu5 \
    --output output/merged/merged_lu_beauty_services_all.csv
```

### Specific categories - WITH website only
```bash
python3 scripts/merge_csv.py \
    --categories hairdresser beautician eyelash_extension ladies_hairdresser \
    --postcodes lu1 lu2 lu3 lu4 lu5 \
    --website-filter with_website \
    --output output/merged/merged_lu_beauty_services_with_website.csv
```

### Specific categories - WITHOUT website only
```bash
python3 scripts/merge_csv.py \
    --categories hairdresser beautician eyelash_extension ladies_hairdresser \
    --postcodes lu1 lu2 lu3 lu4 lu5 \
    --website-filter without_website \
    --output output/merged/merged_lu_beauty_services_without_website.csv
```

---

## Quick Reference

**Collect**: `make run` → enter postcode + keyword
**Merge**: Copy command from above → Run in terminal
**Results**: Check `output/merged/` directory for merged CSV files

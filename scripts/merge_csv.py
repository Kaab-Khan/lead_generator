#!/usr/bin/env python3
"""
CSV Merger CLI - Merge and deduplicate CSV files from lead generation
"""
import argparse
import csv
import glob
import sys
from pathlib import Path


class CsvMerger:
    """
    Merges multiple CSV files and removes duplicates based on place_id.
    """
    
    def merge_files(self, input_files, output_file, dedupe_field="place_id"):
        seen_ids = set()
        merged_rows = []
        total_rows = 0
        files_processed = 0
        
        for file_path in input_files:
            file_path = Path(file_path)
            if not file_path.exists():
                print(f"[CsvMerger] Warning: File not found: {file_path}")
                continue
                
            try:
                with file_path.open('r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    fieldnames = reader.fieldnames
                    
                    for row in reader:
                        total_rows += 1
                        place_id = row.get(dedupe_field, '')
                        
                        if not place_id or place_id in seen_ids:
                            continue
                            
                        seen_ids.add(place_id)
                        merged_rows.append(row)
                        
                files_processed += 1
                print(f"[CsvMerger] Processed: {file_path.name}")
                
            except Exception as e:
                print(f"[CsvMerger] Error processing {file_path}: {e}")
                continue
        
        if merged_rows:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with output_path.open('w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(merged_rows)
                
            stats = {
                'files_processed': files_processed,
                'total_rows_read': total_rows,
                'unique_rows_written': len(merged_rows),
                'duplicates_removed': total_rows - len(merged_rows),
                'output_file': str(output_path)
            }
            
            print(f"\n[CsvMerger] Merge Complete:")
            print(f"  Files processed: {stats['files_processed']}")
            print(f"  Total rows read: {stats['total_rows_read']}")
            print(f"  Unique rows written: {stats['unique_rows_written']}")
            print(f"  Duplicates removed: {stats['duplicates_removed']}")
            print(f"  Output: {stats['output_file']}")
            
            return stats
        else:
            print("[CsvMerger] No data to merge.")
            return {'files_processed': files_processed, 'total_rows_read': 0,
                   'unique_rows_written': 0, 'duplicates_removed': 0, 'output_file': None}
    
    def merge_by_pattern(self, pattern, output_file, base_dir="output", dedupe_field="place_id"):
        base_path = Path(base_dir)
        search_pattern = str(base_path / pattern)
        matching_files = sorted(glob.glob(search_pattern))
        
        if not matching_files:
            print(f"[CsvMerger] No files found matching pattern: {pattern}")
            return {'files_processed': 0, 'total_rows_read': 0,
                   'unique_rows_written': 0, 'duplicates_removed': 0, 'output_file': None}
        
        print(f"[CsvMerger] Found {len(matching_files)} files matching pattern: {pattern}")
        for f in matching_files:
            print(f"  - {Path(f).name}")
        print()
        
        return self.merge_files(matching_files, output_file, dedupe_field)
    
    def merge_categories(self, categories, postcodes, output_file, 
                        base_dir="output", dedupe_field="place_id", website_filter=None):
        base_path = Path(base_dir)
        files_to_merge = []
        
        for postcode in postcodes:
            for category in categories:
                if website_filter:
                    # Match specific website filter
                    pattern = f"{postcode}_{category}_{website_filter}.csv"
                else:
                    # Match both with_website and without_website versions
                    pattern = f"{postcode}_{category}_*.csv"
                matches = glob.glob(str(base_path / pattern))
                files_to_merge.extend(matches)
        
        files_to_merge = sorted(list(set(files_to_merge)))
        
        if not files_to_merge:
            print(f"[CsvMerger] No files found for categories {categories} in postcodes {postcodes}")
            return {'files_processed': 0, 'total_rows_read': 0,
                   'unique_rows_written': 0, 'duplicates_removed': 0, 'output_file': None}
        
        print(f"[CsvMerger] Found {len(files_to_merge)} files to merge:")
        for f in files_to_merge:
            print(f"  - {Path(f).name}")
        print()
        
        return self.merge_files(files_to_merge, output_file, dedupe_field)


def main():
    parser = argparse.ArgumentParser(
        description="Merge CSV files and remove duplicates based on place_id",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Merge all hairdresser files in LU postcodes
  python scripts/merge_csv.py --pattern "lu*_hairdresser_*.csv" --output output/merged_lu_hairdressers.csv
  
  # Merge specific categories across postcodes
  python scripts/merge_csv.py --categories hairdresser beautician ladies_hairdresser \\
                               --postcodes lu1 lu2 lu3 lu4 lu5 \\
                               --output output/merged_beauty_luton.csv
  
  # Merge specific files
  python scripts/merge_csv.py --files output/lu1_hairdresser_with_website.csv \\
                                        output/lu1_hairdresser_without_website.csv \\
                               --output output/merged_lu1_hairdresser.csv
        """
    )
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--pattern',
        help='Glob pattern to match files (e.g., "lu*_hairdresser_*.csv")'
    )
    input_group.add_argument(
        '--files',
        nargs='+',
        help='Specific files to merge'
    )
    input_group.add_argument(
        '--categories',
        nargs='+',
        help='Category names to merge (use with --postcodes)'
    )
    
    # Other arguments
    parser.add_argument(
        '--postcodes',
        nargs='+',
        help='Postcode prefixes (use with --categories)'
    )
    parser.add_argument(
        '--output',
        '-o',
        required=True,
        help='Output file path for merged CSV'
    )
    parser.add_argument(
        '--base-dir',
        default='output',
        help='Base directory for input files (default: output)'
    )
    parser.add_argument(
        '--dedupe-field',
        default='place_id',
        help='Field to use for deduplication (default: place_id)'
    )
    parser.add_argument(
        '--website-filter',
        choices=['with_website', 'without_website'],
        help='Filter by website status (use with --categories): with_website or without_website'
    )
    
    args = parser.parse_args()
    
    # Validate category/postcode combination
    if args.categories and not args.postcodes:
        parser.error("--categories requires --postcodes")
    if args.postcodes and not args.categories:
        parser.error("--postcodes requires --categories")
    
    # Create merger instance
    merger = CsvMerger()
    
    # Execute appropriate merge method
    try:
        if args.pattern:
            stats = merger.merge_by_pattern(
                pattern=args.pattern,
                output_file=args.output,
                base_dir=args.base_dir,
                dedupe_field=args.dedupe_field
            )
        elif args.categories:
            stats = merger.merge_categories(
                categories=args.categories,
                postcodes=args.postcodes,
                output_file=args.output,
                base_dir=args.base_dir,
                dedupe_field=args.dedupe_field,
                website_filter=args.website_filter
            )
        else:  # args.files
            stats = merger.merge_files(
                input_files=args.files,
                output_file=args.output,
                dedupe_field=args.dedupe_field
            )
        
        if stats['unique_rows_written'] > 0:
            print("\n✓ Merge completed successfully!")
            sys.exit(0)
        else:
            print("\n✗ No data was merged.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n✗ Error during merge: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

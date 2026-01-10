#!/usr/bin/env python3
"""
Example: Using CSV Merger programmatically in your code
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.infrastructure.external.csv_merger import CsvMerger


def example_1_merge_hairdressers_luton():
    """Example: Merge all hairdressers in Luton area"""
    print("=" * 60)
    print("Example 1: Merge all hairdressers in Luton")
    print("=" * 60)
    
    merger = CsvMerger()
    stats = merger.merge_by_pattern(
        pattern="lu*_hairdresser_*.csv",
        output_file="output/examples/merged_hairdressers_luton.csv",
        base_dir="output"
    )
    
    print(f"\n✓ Created master list with {stats['unique_rows_written']} unique businesses")
    print(f"✓ Removed {stats['duplicates_removed']} duplicates")
    

def example_2_merge_beauty_services():
    """Example: Merge overlapping beauty service categories"""
    print("\n" + "=" * 60)
    print("Example 2: Merge overlapping beauty categories")
    print("=" * 60)
    
    merger = CsvMerger()
    stats = merger.merge_categories(
        categories=['hairdresser', 'beautician', 'ladies_hairdresser', 'eyelash_extension'],
        postcodes=['lu1', 'lu2', 'lu3', 'lu4', 'lu5'],
        output_file="output/examples/merged_beauty_services_luton.csv"
    )
    
    print(f"\n✓ Merged {stats['files_processed']} files")
    print(f"✓ {stats['unique_rows_written']} unique businesses")
    print(f"✓ Avoided {stats['duplicates_removed']} duplicate contacts")


def example_3_merge_specific_files():
    """Example: Merge specific files"""
    print("\n" + "=" * 60)
    print("Example 3: Merge specific files")
    print("=" * 60)
    
    merger = CsvMerger()
    
    files_to_merge = [
        "output/lu1_hairdresser_with_website.csv",
        "output/lu1_hairdresser_without_website.csv",
        "output/lu1_beautician_with_website.csv",
        "output/lu1_beautician_without_website.csv"
    ]
    
    stats = merger.merge_files(
        input_files=files_to_merge,
        output_file="output/examples/merged_lu1_beauty.csv"
    )
    
    print(f"\n✓ Processed {len(files_to_merge)} files")
    print(f"✓ Result: {stats['unique_rows_written']} unique businesses")


def example_4_check_duplicate_rate():
    """Example: Check how many duplicates exist across categories"""
    print("\n" + "=" * 60)
    print("Example 4: Analyze duplicate rate")
    print("=" * 60)
    
    merger = CsvMerger()
    
    # Merge to see overlap between hairdressers and beauticians
    stats = merger.merge_categories(
        categories=['hairdresser', 'beautician'],
        postcodes=['lu1'],
        output_file="output/examples/analysis_lu1_overlap.csv"
    )
    
    if stats['total_rows_read'] > 0:
        duplicate_rate = (stats['duplicates_removed'] / stats['total_rows_read']) * 100
        print(f"\n✓ Total businesses found: {stats['total_rows_read']}")
        print(f"✓ Unique businesses: {stats['unique_rows_written']}")
        print(f"✓ Duplicates: {stats['duplicates_removed']}")
        print(f"✓ Duplicate rate: {duplicate_rate:.1f}%")
        print(f"\nThis means {duplicate_rate:.1f}% of businesses appear in multiple categories!")


if __name__ == "__main__":
    # Run all examples
    example_1_merge_hairdressers_luton()
    # example_2_merge_beauty_services()
    # example_3_merge_specific_files()
    # example_4_check_duplicate_rate()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)

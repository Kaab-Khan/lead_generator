import csv
from pathlib import Path
from typing import List, Union
import glob


class CsvMerger:
    """
    Merges multiple CSV files and removes duplicates based on place_id.
    Useful for consolidating business leads from overlapping categories.
    """
    
    def merge_files(
        self, 
        input_files: List[Union[str, Path]], 
        output_file: Union[str, Path],
        dedupe_field: str = "place_id"
    ) -> dict:
        """
        Merge multiple CSV files into one, removing duplicates based on dedupe_field.
        
        Args:
            input_files: List of CSV file paths to merge
            output_file: Output path for the merged CSV
            dedupe_field: Field name to use for deduplication (default: place_id)
            
        Returns:
            Dictionary with merge statistics
        """
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
                        
                        # Skip rows without the dedupe field or duplicates
                        if not place_id or place_id in seen_ids:
                            continue
                            
                        seen_ids.add(place_id)
                        merged_rows.append(row)
                        
                files_processed += 1
                print(f"[CsvMerger] Processed: {file_path.name}")
                
            except Exception as e:
                print(f"[CsvMerger] Error processing {file_path}: {e}")
                continue
        
        # Write merged results
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
            return {
                'files_processed': files_processed,
                'total_rows_read': 0,
                'unique_rows_written': 0,
                'duplicates_removed': 0,
                'output_file': None
            }
    
    def merge_by_pattern(
        self,
        pattern: str,
        output_file: Union[str, Path],
        base_dir: Union[str, Path] = "output",
        dedupe_field: str = "place_id"
    ) -> dict:
        """
        Merge CSV files matching a glob pattern.
        
        Args:
            pattern: Glob pattern to match files (e.g., "lu*_hairdresser_*.csv")
            output_file: Output path for the merged CSV
            base_dir: Base directory to search for files (default: output)
            dedupe_field: Field name to use for deduplication (default: place_id)
            
        Returns:
            Dictionary with merge statistics
            
        Example:
            # Merge all hairdresser files in LU postcodes
            merger.merge_by_pattern("lu*_hairdresser_*.csv", "output/merged_lu_hairdressers.csv")
        """
        base_path = Path(base_dir)
        search_pattern = str(base_path / pattern)
        
        matching_files = glob.glob(search_pattern)
        matching_files.sort()  # Sort for consistent ordering
        
        if not matching_files:
            print(f"[CsvMerger] No files found matching pattern: {pattern}")
            return {
                'files_processed': 0,
                'total_rows_read': 0,
                'unique_rows_written': 0,
                'duplicates_removed': 0,
                'output_file': None
            }
        
        print(f"[CsvMerger] Found {len(matching_files)} files matching pattern: {pattern}")
        for f in matching_files:
            print(f"  - {Path(f).name}")
        print()
        
        return self.merge_files(matching_files, output_file, dedupe_field)
    
    def merge_categories(
        self,
        categories: List[str],
        postcodes: List[str],
        output_file: Union[str, Path],
        base_dir: Union[str, Path] = "output",
        dedupe_field: str = "place_id",
        website_filter: str = None
    ) -> dict:
        """
        Merge specific categories across specific postcodes.
        
        Args:
            categories: List of category names (e.g., ['hairdresser', 'beautician'])
            postcodes: List of postcode prefixes (e.g., ['lu1', 'lu2', 'lu3'])
            output_file: Output path for the merged CSV
            base_dir: Base directory to search for files (default: output)
            dedupe_field: Field name to use for deduplication (default: place_id)
            website_filter: Filter by 'with_website', 'without_website', or None for both
            
        Returns:
            Dictionary with merge statistics
            
        Example:
            # Merge hairdressers and beauticians in LU1-LU5
            merger.merge_categories(
                ['hairdresser', 'beautician'], 
                ['lu1', 'lu2', 'lu3', 'lu4', 'lu5'],
                'output/merged_beauty_services_luton.csv'
            )
        """
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
        
        # Remove duplicates and sort
        files_to_merge = sorted(list(set(files_to_merge)))
        
        if not files_to_merge:
            print(f"[CsvMerger] No files found for categories {categories} in postcodes {postcodes}")
            return {
                'files_processed': 0,
                'total_rows_read': 0,
                'unique_rows_written': 0,
                'duplicates_removed': 0,
                'output_file': None
            }
        
        print(f"[CsvMerger] Found {len(files_to_merge)} files to merge:")
        for f in files_to_merge:
            print(f"  - {Path(f).name}")
        print()
        
        return self.merge_files(files_to_merge, output_file, dedupe_field)

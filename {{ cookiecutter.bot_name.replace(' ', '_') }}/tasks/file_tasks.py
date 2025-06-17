"""
File Processing Tasks

Handle file operations, conversions, and organization.
"""

import shutil
import csv
from pathlib import Path
from . import log_task_start, log_task_complete, log_task_error


def process_csv_files(logger, input_folder, output_folder):
    """
    Process all CSV files in the input folder.
    
    Args:
        logger: Logger instance
        input_folder: Path to input folder
        output_folder: Path to output folder
        
    Returns:
        int: Number of files processed
    """
    log_task_start(logger, "CSV Processing")
    
    try:
        input_path = Path(input_folder)
        output_path = Path(output_folder)
        
        processed_count = 0
        csv_files = list(input_path.glob("*.csv"))
        
        if not csv_files:
            logger.info("No CSV files found to process")
            return 0

        for csv_file in csv_files:
            logger.info(f"Processing: {csv_file.name}")
            
            # Read CSV and process (example: add a processed timestamp column)
            rows = []
            with open(csv_file, 'r', newline='', encoding='utf-8') as infile:
                reader = csv.DictReader(infile)
                fieldnames = reader.fieldnames + ['processed_timestamp']
                
                for row in reader:
                    row['processed_timestamp'] = str(Path().cwd())  # Example processing
                    rows.append(row)
            
            # Write processed CSV
            output_file = output_path / f"processed_{csv_file.name}"
            with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                if rows:
                    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
            
            processed_count += 1
        
        log_task_complete(logger, "CSV Processing", f"{processed_count} files processed")
        return processed_count
        
    except Exception as e:
        log_task_error(logger, "CSV Processing", str(e))
        raise


def organize_files_by_type(logger, source_folder):
    """
    Organize files in a folder by their type/extension.
    
    Args:
        logger: Logger instance
        source_folder: Path to folder to organize
        
    Returns:
        int: Number of files organized
    """
    log_task_start(logger, "File Organization")
    
    try:
        source_path = Path(source_folder)
        
        # Define file type categories
        file_types = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf'],
            'spreadsheets': ['.xlsx', '.xls', '.csv'],
            'presentations': ['.ppt', '.pptx'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
            'audio': ['.mp3', '.wav', '.flac', '.aac']
        }
        
        organized_count = 0
        
        # Process all files in the source folder
        for file_path in source_path.iterdir():
            if file_path.is_file():
                file_extension = file_path.suffix.lower()
                
                # Find the appropriate category
                category_found = False
                for category, extensions in file_types.items():
                    if file_extension in extensions:
                        # Create category folder if it doesn't exist
                        category_folder = source_path / category
                        category_folder.mkdir(exist_ok=True)
                        
                        # Move file to category folder
                        destination = category_folder / file_path.name
                        shutil.move(str(file_path), str(destination))
                        logger.info(f"Moved {file_path.name} to {category}/")
                        
                        organized_count += 1
                        category_found = True
                        break
                
                # If no category found, move to 'other' folder
                if not category_found:
                    other_folder = source_path / 'other'
                    other_folder.mkdir(exist_ok=True)
                    destination = other_folder / file_path.name
                    shutil.move(str(file_path), str(destination))
                    logger.info(f"Moved {file_path.name} to other/")
                    organized_count += 1
        
        log_task_complete(logger, "File Organization", f"{organized_count} files organized")
        return organized_count
        
    except Exception as e:
        log_task_error(logger, "File Organization", str(e))
        raise


def cleanup_old_files(logger, folder_path, days_old=7):
    """
    Clean up files older than specified days.
    
    Args:
        logger: Logger instance
        folder_path: Path to folder to clean
        days_old: Files older than this many days will be deleted
        
    Returns:
        int: Number of files deleted
    """
    log_task_start(logger, "File Cleanup")
    
    try:
        import time
        from datetime import datetime, timedelta
        
        folder = Path(folder_path)
        cutoff_time = time.time() - (days_old * 24 * 60 * 60)
        deleted_count = 0
        
        for file_path in folder.rglob('*'):
            if file_path.is_file():
                file_age = file_path.stat().st_mtime
                if file_age < cutoff_time:
                    logger.info(f"Deleting old file: {file_path.name}")
                    file_path.unlink()
                    deleted_count += 1
        
        log_task_complete(logger, "File Cleanup", f"{deleted_count} old files deleted")
        return deleted_count
        
    except Exception as e:
        log_task_error(logger, "File Cleanup", str(e))
        raise


def convert_text_files_to_uppercase(logger, input_folder, output_folder):
    """
    Convert all text files to uppercase.
    
    Args:
        logger: Logger instance
        input_folder: Path to input folder
        output_folder: Path to output folder
        
    Returns:
        int: Number of files converted
    """
    log_task_start(logger, "Text File Conversion")
    
    try:
        input_path = Path(input_folder)
        output_path = Path(output_folder)
        
        converted_count = 0
        text_files = list(input_path.glob("*.txt"))
        
        if not text_files:
            logger.info("No text files found to convert")
            return 0

        for text_file in text_files:
            logger.info(f"Converting: {text_file.name}")
            
            # Read file content
            with open(text_file, 'r', encoding='utf-8') as infile:
                content = infile.read()
            
            # Convert to uppercase
            uppercase_content = content.upper()
            
            # Write converted file
            output_file = output_path / f"uppercase_{text_file.name}"
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(uppercase_content)
            
            converted_count += 1
        
        log_task_complete(logger, "Text File Conversion", f"{converted_count} files converted")
        return converted_count
        
    except Exception as e:
        log_task_error(logger, "Text File Conversion", str(e))
        raise 
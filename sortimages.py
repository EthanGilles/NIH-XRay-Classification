import os
import csv
import shutil
from collections import defaultdict
import argparse

def sort_images(csv_path, source_dir, output_dir):
    """
    Sorts images into subfolders based on labels from a CSV file.
    Skips:
    1. Images where the label contains '|' (indicating multi-label)
    (Now allows duplicate entries in CSV - last label wins)
    
    Args:
        csv_path (str): Path to the CSV file (format: filename,label)
        source_dir (str): Directory containing images to sort
        output_dir (str): Base directory where labeled folders will be created
    """
    # Read CSV - last label for each filename wins (overwrites previous entries)
    label_map = {}
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 2:  # Skip rows with missing data
                continue
            filename, label = row[0].strip(), row[1].strip()
            if filename and label:  # Ignore empty entries
                label_map[filename] = label  # Last entry wins for duplicates

    # Process each image
    for filename, label in label_map.items():
        if '|' in label:  # Skip if label contains separator (multi-label)
            print(f"Skipping {filename}: label contains '|' (multi-label)")
            continue

        src_path = os.path.join(source_dir, filename)
        dest_folder = os.path.join(output_dir, label)
        dest_path = os.path.join(dest_folder, filename)

        if not os.path.exists(src_path):
            print(f"Warning: {filename} not found in source directory")
            continue

        os.makedirs(dest_folder, exist_ok=True)  # Create label folder if needed
        shutil.move(src_path, dest_path)
        print(f"Moved {filename} → {dest_folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sort images into folders by labels from a CSV.")
    parser.add_argument("--csv", required=True, help="Path to CSV file (format: filename,label)")
    parser.add_argument("--source", required=True, help="Directory containing images to sort")
    parser.add_argument("--output", required=True, help="Base directory for labeled folders")
    args = parser.parse_args()

    sort_images(args.csv, args.source, args.output)
    print("Done!")


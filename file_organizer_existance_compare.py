# It check and generate reports of followings
# 1. List of all files in source folder.
# 2. List of all files in destination folder.
# 3. Check all files of source are exist in destination or not then generate report.

import os
import csv
import hashlib
from pathlib import Path
from tqdm import tqdm

# =========================
# USER CONFIGURATION
# =========================
FOLDER1 = r"SOURCE_FOLDER" # Add source folder name/path to check all files of source are exist in destination or not
FOLDER2 = r"DESTINATION_FOLDER" # Add destination folder name/path
OUTPUT_DIR = r"E:\comparison_reports"

HASH_ALGO = "sha256"
BUFFER_SIZE = 1024 * 1024  # 1 MB chunks

# =========================
# UTILITY FUNCTIONS
# =========================
def compute_hash(file_path, algo="sha256"):
    h = hashlib.new(algo)
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(BUFFER_SIZE):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        return f"ERROR: {e}"

def scan_folder(folder_path):
    records = []
    folder_path = Path(folder_path)

    # Count total files for progress bar
    total_files = sum(len(files) for _, _, files in os.walk(folder_path))

    with tqdm(total=total_files, desc=f"Scanning {folder_path.name}", unit="file") as pbar:
        for root, _, files in os.walk(folder_path):
            for name in files:
                full_path = Path(root) / name
                relative_path = full_path.relative_to(folder_path)
                size = full_path.stat().st_size

                file_hash = compute_hash(full_path, HASH_ALGO)

                records.append({
                    "file_name": name,
                    "relative_path": str(relative_path),
                    "absolute_path": str(full_path),
                    "size_bytes": size,
                    "hash": file_hash
                })

                pbar.update(1)

    return records

def write_csv(file_path, records):
    if not records:
        return

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

# =========================
# MAIN LOGIC
# =========================
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Scanning FOLDER1...")
    folder1_files = scan_folder(FOLDER1)

    print("Scanning FOLDER2...")
    folder2_files = scan_folder(FOLDER2)

    # Write full reports
    folder1_csv = os.path.join(OUTPUT_DIR, "FOLDER1_all_files.csv")
    folder2_csv = os.path.join(OUTPUT_DIR, "FOLDER2_all_files.csv")

    write_csv(folder1_csv, folder1_files)
    write_csv(folder2_csv, folder2_files)

    print("CSV reports generated.")

    # Build hash set for FOLDER2
    folder2_hashes = set(
        f["hash"] for f in folder2_files if not f["hash"].startswith("ERROR")
    )

    # Find missing files
    missing_files = []
    for f in folder1_files:
        if f["hash"] not in folder2_hashes:
            missing_files.append(f)

    missing_csv = os.path.join(OUTPUT_DIR, "FOLDER1_missing_in_FOLDER2.csv")
    write_csv(missing_csv, missing_files)

    print("\nComparison complete.")
    print(f"Total files in FOLDER1: {len(folder1_files)}")
    print(f"Total files in FOLDER2: {len(folder2_files)}")
    print(f"Missing files: {len(missing_files)}")
    print(f"\nReports saved in: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()

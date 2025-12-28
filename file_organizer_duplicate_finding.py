# It create report of duplicate files from target directory

import hashlib
from pathlib import Path
from collections import defaultdict
import csv
from tqdm import tqdm

TARGET_DIR = Path("TARGET_FOLDER") # Please change the target folder name/path
REPORT_FILE = "duplicate_report.csv"
CHUNK_SIZE = 8192


def hash_file(path: Path) -> str | None:
    sha = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(CHUNK_SIZE):
                sha.update(chunk)
        return sha.hexdigest()
    except (PermissionError, OSError) as e:
        print(f"⚠️ Skipping {path}: {e}")
        return None


def main():
    size_map = defaultdict(list)

    files = [
        f for f in TARGET_DIR.rglob("*")
        if f.is_file() and not f.is_symlink()
    ]

    print(f"🔍 Scanning {len(files)} files...")

    for file in tqdm(files, desc="Grouping by size"):
        size_map[file.stat().st_size].append(file)

    duplicate_groups = []

    for same_size_files in tqdm(size_map.values(), desc="Hashing potential duplicates"):
        if len(same_size_files) < 2:
            continue

        same_size_files.sort()  # deterministic order
        hash_map = defaultdict(list)

        for file in same_size_files:
            file_hash = hash_file(file)
            if file_hash:
                hash_map[file_hash].append(file)

        for group in hash_map.values():
            if len(group) > 1:
                duplicate_groups.append(group)

    with open(REPORT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Group_ID", "File_Path"])
        for i, group in enumerate(duplicate_groups, start=1):
            for file in group:
                writer.writerow([i, str(file)])

    print("✅ Duplicate scan completed.")
    print(f"📄 Report saved as: {REPORT_FILE}")
    print(f"📦 Duplicate groups found: {len(duplicate_groups)}")


if __name__ == "__main__":
    main()

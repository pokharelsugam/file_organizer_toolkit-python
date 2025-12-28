# It move the duplicate files listed in duplicate_report.csv into new folder "DUPLICATE_QUARANTINE" for mannual review and deletion

import csv
from pathlib import Path
import shutil
from tqdm import tqdm

REPORT_FILE = "duplicate_report.csv"
QUARANTINE_DIR = Path("DUPLICATE_QUARANTINE")


def main():
    QUARANTINE_DIR.mkdir(exist_ok=True)

    groups: dict[str, list[Path]] = {}

    with open(REPORT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            path = Path(row["File_Path"])
            groups.setdefault(row["Group_ID"], []).append(path)

    moved = 0

    for files in tqdm(groups.values(), desc="Quarantining duplicates"):
        existing = [f for f in files if f.exists()]
        if len(existing) < 2:
            continue

        # ✅ Keep the newest file (change logic if you want)
        keep = max(existing, key=lambda f: f.stat().st_mtime)

        for duplicate in existing:
            if duplicate == keep:
                continue

            target = QUARANTINE_DIR / duplicate.name
            counter = 1
            while target.exists():
                target = QUARANTINE_DIR / f"{duplicate.stem}_{counter}{duplicate.suffix}"
                counter += 1

            shutil.move(str(duplicate), str(target))
            moved += 1

    print(f"✅ {moved} duplicate files moved to quarantine.")
    print(f"📁 Kept one copy per group in original location.")


if __name__ == "__main__":
    main()

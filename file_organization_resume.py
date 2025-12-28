# It resume file organization  if stopped or interrupt file_organization.py script.
# It check in source and destination folder by hashing (not only by file_name for accurate identification) to identify files are already copied or not.
# If files are already copied it skip this file and search for new files.
# If files are not already copied it make copy in destination.

# Please add source folder name/path before running.

import shutil
import hashlib
from pathlib import Path
from tqdm import tqdm

SOURCE_DIR = Path("SOURCE_FOLDER") #Add source folder name/path here
DEST_DIR = Path("ORGANIZED_FILES")

FILE_TYPES = {
    "Documents": [
        ".pdf", ".docx", ".doc", ".pptx", ".ppt", ".pub", ".odt"
    ],
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".heic"
    ],
    "Videos": [
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"
    ],
    "Audio": [
        ".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"
    ],
    "Archives": [
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"
    ],
    "Code": [
        ".py", ".ipynb", ".c", ".cpp", ".html", ".BAS", ".r", ".sh"
    ],
    "Design": [
        ".psd", ".ai", ".xd", ".fig", ".sketch",
        ".dwg", ".dxf", ".step", ".stp", ".iges", ".igs",
        ".blend", ".fbx", ".obj", ".3ds", ".max"
    ],
    "Softwares": [
        ".exe", ".msi", ".iso", ".img", ".dmg", ".apk"
    ],
    "Data": [
        ".xlsx", ".xls", ".xlsm", ".csv", ".tsv",
        ".txt", ".json", ".xml", ".db", ".sqlite",
        ".mdb", ".accdb"
    ]
}

def get_category(ext):
    for category, extensions in FILE_TYPES.items():
        if ext.lower() in extensions:
            return category
    return "Others"

def hash_file(path, chunk_size=8192):
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            sha.update(chunk)
    return sha.hexdigest()

def main():
    DEST_DIR.mkdir(exist_ok=True)
    copied = skipped = renamed = 0

    all_files = [p for p in SOURCE_DIR.rglob("*") if p.is_file()]

    for file_path in tqdm(all_files, desc="Organizing files", unit="file"):
        category = get_category(file_path.suffix)
        target_dir = DEST_DIR / category
        target_dir.mkdir(exist_ok=True)

        target_file = target_dir / file_path.name

        if target_file.exists():
            if hash_file(file_path) == hash_file(target_file):
                skipped += 1
                continue
            else:
                counter = 1
                new_target = target_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
                while new_target.exists():
                    counter += 1
                    new_target = target_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
                shutil.copy2(file_path, new_target)
                renamed += 1
        else:
            shutil.copy2(file_path, target_file)
            copied += 1

    print(
        f"✅ Completed | Copied: {copied} | Skipped (same): {skipped} | Renamed (diff): {renamed}"
    )

if __name__ == "__main__":
    main()

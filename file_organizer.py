# File copy paste safely in organised form with progress bar
# Reads files from "SOURCE_FOLDER" # Edit it
# Writes organized files into "ORGANIZED_FILES"
# Preserves original quality and metadata

import shutil
from pathlib import Path
from tqdm import tqdm

SOURCE_DIR = Path("SOURCE_FOLDER") # Add source folder name/path here
DEST_DIR = Path("ORGANIZED_FILES") 

FILE_TYPES = {
    "Documents": [
        ".pdf", ".docx", ".doc", ".pptx", ".ppt", ".pub", ".odt"
    ],

    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".heic"
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

def main():
    DEST_DIR.mkdir(exist_ok=True)

    # Collect all files first (for progress bar)
    all_files = [f for f in SOURCE_DIR.rglob("*") if f.is_file()]

    for file_path in tqdm(all_files, desc="📂 Organizing files", unit="file"):
        category = get_category(file_path.suffix)
        target_dir = DEST_DIR / category
        target_dir.mkdir(exist_ok=True)

        target_file = target_dir / file_path.name
        counter = 1

        # Handle same-name files safely
        while target_file.exists():
            target_file = target_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
            counter += 1

        shutil.copy2(file_path, target_file)

    print("\n✅ Organization completed safely with progress tracking.")

if __name__ == "__main__":
    main()

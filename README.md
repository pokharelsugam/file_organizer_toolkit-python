# 📁 File Organizer Toolkit

A **safe, resumable, and duplicate-aware Python file organization toolkit** designed for large file collections, backups, and long-running operations where **data integrity matters more than speed**.

This toolkit focuses on **zero data loss**, **no overwriting**, **resume after interruption**, and **full auditability** using cryptographic hashing.

---

## 🚀 Why This Toolkit?

Most file organizers:
- overwrite files silently ❌
- fail on interruption ❌
- delete duplicates automatically ❌

This toolkit is built with a **data-safety-first philosophy**, making it suitable for:
- External HDD / SSD / NAS backups
- Academic & research data
- Long-running file migrations
- Archival & forensic workflows

---

## ✨ Features

- ✅ Safe file copy (no overwrite)
- ✅ Preserves original file metadata
- ✅ Resume support after interruption (hash-based)
- ✅ Progress bars for long operations
- ✅ Accurate duplicate detection (size + SHA-256)
- ✅ Duplicate quarantine instead of deletion
- ✅ Source vs destination verification
- ✅ CSV-based audit and reporting
- ✅ Modular scripts (use only what you need)

---

## 📂 Repository Structure

---

## 📦 Script Overview

| Script | Purpose | Key Features | When to Use |
|--------|---------|--------------|-------------|
| **1. `file_organizer.py`** | Safe file organization | Organizes files from `SOURCE_FOLDER` into `ORGANIZED_FILES`<br>Categorizes by extension<br>Preserves metadata (`shutil.copy2`)<br>Avoids overwriting with auto-renaming<br>Progress bar (`tqdm`) | First-time organization |
| **2. `file_organization_resume.py`** | Resume-safe organizer | Resumes after interruption<br>SHA-256 hashing for comparison<br>Skips correctly copied files<br>Renames only if content differs | Previous run was interrupted |
| **3. `file_organizer_duplicate_finding.py`** | Duplicate detection (read-only) | Scans organized files<br>Groups by size first<br>SHA-256 for accuracy<br>Generates `duplicate_report.csv` | Identify duplicates safely |
| **4. `file_organizer_duplicate_quarantine.py`** | Duplicate quarantine (non-destructive) | Reads `duplicate_report.csv`<br>Keeps one copy per group<br>Moves extras to `DUPLICATE_QUARANTINE` | Clean duplicates with manual review |
| **5. `file_organizer_existance_compare.py`** | Source–destination verification | Generates CSV reports:<br>All source files<br>All destination files<br>Missing files (hash-based) | Validate backup completeness |

---
## Configuration
Edit the paths directly inside each script before running

PythonSOURCE_DIR = Path("SOURCE_FOLDER")
DEST_DIR = Path("ORGANIZED_FILES")

## Dependency
- Create virtual environment
'''
python -m venv fileenv
'''
- Activate virtual environment
'''
fileenv\Scripts\activate.bat
'''
- Install dependency
'''
pip install tqdm
'''

## 🔄 Recommended Workflow

For maximum safety and reliability:

1. **Organize files** 
'''
   python file_organizer.py
'''
2. **Resume if interrupted**
'''
   python file_organization_resume.py
'''
3. **Detect duplicates**
'''
   python file_organizer_duplicate_finding.py
'''
4. **Quarantine duplicates**
'''
   python file_organizer_duplicate_quarantine.py
'''
5. **Verify source vs destination**
'''
   python file_organizer_existance_compare.py
'''

## Safety Guarantee
 - ✔ No overwriting of files
 - ✔ SHA-256 content verification
 - ✔ Metadata preserved
 - ✔ No automatic deletion
 - ✔ Full CSV audit trail

## Generated Reports
 - duplicate_report.csv
 - FOLDER1_all_files.csv
 - FOLDER2_all_files.csv
 - FOLDER1_missing_in_FOLDER2.csv

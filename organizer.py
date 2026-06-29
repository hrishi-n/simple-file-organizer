"""
File Organizer CLI — sorts files in a directory into categorized subfolders.
"""

import os
import shutil
import argparse
from pathlib import Path

CATEGORIES = {
    "Images":    {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff"},
    "Videos":    {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"},
    "Audio":     {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"},
    "ISO":       {".iso"},
    "Documents": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".txt", ".rtf"},
    "Archives":  {".zip", ".tar", ".gz", ".rar", ".7z", ".bz2"},
    "Code":      {".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".go", ".rs", ".sh"},
    "Data":      {".csv", ".json", ".xml", ".yaml", ".yml", ".sql", ".db"},
}


def get_category(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Other"


def organize(directory: str, dry_run: bool = False) -> dict:
    target = Path(directory).resolve()

    if not target.is_dir():
        raise NotADirectoryError(f"'{directory}' is not a valid directory.")

    moved = {}
    skipped = []

    for item in target.iterdir():
        if item.is_dir():
            continue

        category = get_category(item)
        dest_folder = target / category
        dest_file = dest_folder / item.name

        # Handle name collisions
        counter = 1
        while dest_file.exists():
            dest_file = dest_folder / f"{item.stem}_{counter}{item.suffix}"
            counter += 1

        moved.setdefault(category, []).append((item.name, dest_file.name))

        if not dry_run:
            dest_folder.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest_file))

    return moved


def print_summary(moved: dict, dry_run: bool):
    if not moved:
        print("Nothing to organize — no files found.")
        return

    prefix = "[DRY RUN] " if dry_run else ""
    total = sum(len(files) for files in moved.values())

    print(f"\n{prefix}Organized {total} file(s):\n")
    for category, files in sorted(moved.items()):
        print(f"  {category}/ ({len(files)} file(s))")
        for original, saved_as in files:
            if original != saved_as:
                print(f"    • {original}  →  {saved_as}  (renamed to avoid conflict)")
            else:
                print(f"    • {original}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Organize files in a directory into categorized subfolders."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to organize (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would happen without moving any files",
    )

    args = parser.parse_args()

    try:
        moved = organize(args.directory, dry_run=args.dry_run)
        print_summary(moved, dry_run=args.dry_run)
    except NotADirectoryError as e:
        print(f"Error: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

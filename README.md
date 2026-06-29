# File Organizer

A simple CLI tool that sorts files in a directory into categorized subfolders.

## What it does

Scans a directory and moves files into subfolders based on type:

| Folder      | File types |
|-------------|------------|
| `Images/`   | jpg, png, gif, svg, webp, … |
| `Videos/`   | mp4, mov, avi, mkv, … |
| `Audio/`    | mp3, wav, flac, aac, … |
| `Documents/`| pdf, docx, xlsx, pptx, txt, … |
| `Archives/` | zip, tar, gz, rar, 7z, … |
| `Code/`     | py, js, ts, html, css, … |
| `Data/`     | csv, json, xml, yaml, sql, … |
| `Other/`    | everything else |

## Usage

```bash
# Organize the current directory
python organizer.py

# Organize a specific directory
python organizer.py ~/Downloads

# Preview what would happen (no files moved)
python organizer.py ~/Downloads --dry-run
```

## Setup

```bash
# Clone the repo
git clone https://github.com/your-username/file-organizer.git
cd file-organizer

# (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install test dependencies
pip install -r requirements.txt
```

## Running tests

```bash
pytest test_organizer.py -v
```

## Notes

- Subdirectories inside the target folder are never touched.
- If a file with the same name already exists in the destination, it is renamed (`file_1.jpg`, `file_2.jpg`, …).
- Use `--dry-run` to safely preview changes before committing to them.

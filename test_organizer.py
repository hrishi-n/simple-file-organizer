import pytest
import shutil
from pathlib import Path
from organizer import get_category, organize


@pytest.fixture
def tmp_dir(tmp_path):
    files = [
        "photo.jpg", "clip.mp4", "song.mp3", "report.pdf",
        "archive.zip", "script.py", "data.csv", "mystery.xyz",
    ]
    for name in files:
        (tmp_path / name).touch()
    return tmp_path


def test_get_category():
    assert get_category(Path("photo.jpg")) == "Images"
    assert get_category(Path("video.mp4")) == "Videos"
    assert get_category(Path("song.mp3")) == "Audio"
    assert get_category(Path("doc.pdf")) == "Documents"
    assert get_category(Path("archive.zip")) == "Archives"
    assert get_category(Path("script.py")) == "Code"
    assert get_category(Path("data.csv")) == "Data"
    assert get_category(Path("unknown.xyz")) == "Other"


def test_dry_run_moves_nothing(tmp_dir):
    moved = organize(str(tmp_dir), dry_run=True)
    assert moved  # something was reported
    # No subfolders created
    subfolders = [p for p in tmp_dir.iterdir() if p.is_dir()]
    assert subfolders == []


def test_organize_moves_files(tmp_dir):
    moved = organize(str(tmp_dir), dry_run=False)
    assert "Images" in moved
    assert "Videos" in moved
    assert (tmp_dir / "Images" / "photo.jpg").exists()
    assert (tmp_dir / "Videos" / "clip.mp4").exists()
    assert not (tmp_dir / "photo.jpg").exists()


def test_collision_handling(tmp_dir):
    (tmp_dir / "Images").mkdir()
    (tmp_dir / "Images" / "photo.jpg").touch()
    organize(str(tmp_dir), dry_run=False)
    assert (tmp_dir / "Images" / "photo_1.jpg").exists()


def test_invalid_directory():
    with pytest.raises(NotADirectoryError):
        organize("/nonexistent/path/abc123")

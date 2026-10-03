import re
from datetime import date
from pathlib import Path


def archive_directory(root: Path, title: str, recording_date: date | None = None) -> Path:
    clean = re.sub(r"[^\w.-]+", "_", title, flags=re.UNICODE).strip("_.") or "Untitled"
    return root / f"{recording_date or date.today():%Y-%m-%d}_{clean}"


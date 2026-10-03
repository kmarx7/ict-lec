import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class AppConfig(BaseModel):
    download_dir: Path = Field(default_factory=lambda: Path(os.environ.get("LECTURE_ARCHIVE_DOWNLOAD_DIR", "~/Downloads/LectureArchive")).expanduser())
    database_path: Path = Path("data/library.db")
    max_loops: int = 8
    chunk_size: int = 1024 * 1024

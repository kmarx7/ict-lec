from datetime import UTC, datetime
from pathlib import Path

from src.library.database import Database


class RecordingRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def add(self, *, source_url: str, title: str | None, strategy: str, directory: Path, files: list[Path]) -> int:
        now = datetime.now(UTC).isoformat()
        with self.database.connect() as db:
            cursor = db.execute(
                "INSERT INTO recordings(source,source_url,title,acquisition_strategy,verified,local_directory,status,created_at,updated_at) VALUES(?,?,?,?,1,?,'archived',?,?)",
                ("zoom", source_url, title, strategy, str(directory), now, now),
            )
            recording_id = int(cursor.lastrowid)
            db.executemany(
                "INSERT INTO recording_files(recording_id,file_type,filename,file_size,local_path,verified,status) VALUES(?,?,?,?,?,1,'archived')",
                [(recording_id, p.suffix.removeprefix(".").upper(), p.name, p.stat().st_size, str(p)) for p in files],
            )
            return recording_id

    def list_recordings(self):
        with self.database.connect() as db:
            return db.execute("SELECT * FROM recordings ORDER BY created_at DESC").fetchall()


import sqlite3
from pathlib import Path

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS recordings (
 id INTEGER PRIMARY KEY AUTOINCREMENT, source TEXT NOT NULL, source_url TEXT NOT NULL,
 title TEXT, recording_date TEXT, duration_seconds INTEGER, acquisition_strategy TEXT,
 verified INTEGER NOT NULL DEFAULT 0, local_directory TEXT, status TEXT NOT NULL,
 created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS recording_files (
 id INTEGER PRIMARY KEY AUTOINCREMENT, recording_id INTEGER NOT NULL, file_type TEXT,
 filename TEXT NOT NULL, file_size INTEGER, local_path TEXT, verified INTEGER NOT NULL DEFAULT 0,
 status TEXT NOT NULL, FOREIGN KEY(recording_id) REFERENCES recordings(id) ON DELETE CASCADE
);
"""


class Database:
    def __init__(self, path: Path) -> None:
        self.path = path

    def connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(SCHEMA)


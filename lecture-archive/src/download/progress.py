from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DownloadProgress:
    filename: str
    downloaded_bytes: int
    total_bytes: int | None
    speed_bytes_per_second: float
    eta_seconds: float | None
    strategy: str

    @property
    def percentage(self) -> float | None:
        return self.downloaded_bytes * 100 / self.total_bytes if self.total_bytes else None


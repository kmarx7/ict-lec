from pathlib import Path


def resume_headers(part_path: Path, accept_ranges: bool) -> tuple[dict[str, str], int]:
    if accept_ranges and part_path.exists():
        size = part_path.stat().st_size
        if size:
            return {"Range": f"bytes={size}-"}, size
    return {}, 0


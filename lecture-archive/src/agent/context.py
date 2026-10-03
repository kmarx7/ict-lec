from pathlib import Path

from pydantic import BaseModel, Field


class AgentContext(BaseModel):
    original_url: str
    canonical_url: str | None = None
    source_type: str = "zoom"
    recording_found: bool | None = None
    playback_available: bool | None = None
    download_allowed: bool | None = None
    login_required: bool = False
    passcode_required: bool = False
    api_available: bool = False
    browser_session_available: bool = False
    current_strategy: str | None = None
    attempted_strategies: list[str] = Field(default_factory=list)
    available_files: list[dict] = Field(default_factory=list)
    completed_files: list[Path] = Field(default_factory=list)
    failed_files: list[Path] = Field(default_factory=list)
    last_error_code: str | None = None
    last_error_message: str | None = None
    retry_counts: dict[str, int] = Field(default_factory=dict)
    loop_count: int = 0
    goal_reached: bool = False
    terminal_reason: str | None = None
    passcode: str | None = Field(default=None, exclude=True, repr=False)
    local_import_path: Path | None = None
    cancelled: bool = False


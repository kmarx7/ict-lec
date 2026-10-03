from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class ActionType(StrEnum):
    REQUEST_PASSCODE = "request_passcode"
    REQUEST_LOGIN = "request_login"
    ZOOM_API_DOWNLOAD = "zoom_api_download"
    DIRECT_DOWNLOAD = "direct_download"
    BROWSER_DOWNLOAD = "browser_download"
    LOCAL_IMPORT = "local_import"
    RETRY = "retry"
    STOP = "stop"


class Observation(BaseModel):
    url_valid: bool = False
    canonical_url: str | None = None
    recording_found: bool | None = None
    playback_available: bool | None = None
    download_allowed: bool | None = None
    login_required: bool = False
    passcode_required: bool = False
    api_available: bool = False
    direct_download_available: bool = False
    browser_download_available: bool = False
    browser_session_available: bool = False
    local_file_available: bool = False
    candidate_files: list[dict[str, Any]] = Field(default_factory=list)
    disk_free_bytes: int | None = None
    network_available: bool | None = None
    errors: list[str] = Field(default_factory=list)


class ActionPlan(BaseModel):
    action: ActionType
    strategy_name: str | None = None
    reason: str
    stop: bool = False


class ExecutionResult(BaseModel):
    success: bool
    strategy: str
    error_code: str | None = None
    message: str | None = None
    downloaded_files: list[Path] = Field(default_factory=list)
    retryable: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class EvaluationResult(BaseModel):
    success: bool
    goal_reached: bool = False
    retryable: bool = False
    error_category: str | None = None
    reason: str | None = None
    verified_files: list[Path] = Field(default_factory=list)


from typing import Any

from pydantic import BaseModel, Field


class ZoomRecordingFile(BaseModel):
    file_type: str
    file_name: str | None = None
    file_size: int | None = None
    download_url: str | None = Field(default=None, repr=False)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ZoomPageState(BaseModel):
    recording_found: bool | None = None
    playback_available: bool | None = None
    download_allowed: bool | None = None
    passcode_required: bool = False
    login_required: bool = False
    download_button_visible: bool = False
    title: str | None = None


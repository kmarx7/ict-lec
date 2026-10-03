from enum import StrEnum


class AppState(StrEnum):
    IDLE = "idle"
    ANALYZING = "analyzing"
    WAITING_FOR_PASSCODE = "waiting_for_passcode"
    WAITING_FOR_LOGIN = "waiting_for_login"
    EXECUTING = "executing"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"
    TERMINATED = "terminated"


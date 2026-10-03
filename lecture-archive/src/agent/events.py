from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class EventType(StrEnum):
    OBSERVATION = "OBSERVATION"
    PLAN_SELECTED = "PLAN_SELECTED"
    ACTION_STARTED = "ACTION_STARTED"
    ACTION_COMPLETED = "ACTION_COMPLETED"
    ACTION_FAILED = "ACTION_FAILED"
    EVALUATION = "EVALUATION"
    RETRY = "RETRY"
    GOAL_REACHED = "GOAL_REACHED"
    TERMINATED = "TERMINATED"


class AgentEvent(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    event_type: EventType
    message: str
    strategy: str | None = None
    error_code: str | None = None


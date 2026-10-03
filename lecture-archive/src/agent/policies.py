from dataclasses import dataclass

from src.utils.errors import ErrorCode


@dataclass(frozen=True, slots=True)
class RetryRule:
    retryable: bool
    max_attempts: int = 0
    base_delay_seconds: float = 0


RETRY_RULES = {
    ErrorCode.NETWORK_TIMEOUT: RetryRule(True, 3, 1),
    ErrorCode.CONNECTION_RESET: RetryRule(True, 3, 1),
    ErrorCode.SERVER_ERROR: RetryRule(True, 3, 2),
    ErrorCode.PARTIAL_DOWNLOAD: RetryRule(True, 3, 0),
    ErrorCode.DOWNLOAD_URL_EXPIRED: RetryRule(True, 1, 0),
}

TERMINAL_ERRORS = {
    ErrorCode.INVALID_URL,
    ErrorCode.RECORDING_NOT_FOUND,
    ErrorCode.DOWNLOAD_NOT_ALLOWED,
    ErrorCode.DISK_FULL,
    ErrorCode.USER_CANCELLED,
}


def retry_rule(code: str | None) -> RetryRule:
    try:
        return RETRY_RULES.get(ErrorCode(code), RetryRule(False))
    except (ValueError, TypeError):
        return RetryRule(False)


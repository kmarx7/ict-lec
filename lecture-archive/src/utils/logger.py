import logging
import re


class RedactingFilter(logging.Filter):
    PATTERNS = (re.compile(r"(?i)(passcode|authorization|access_token|cookie)\s*[:=]\s*\S+"), re.compile(r"([?&](?:pwd|token|signature)=[^&\s]+)", re.I))

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        for pattern in self.PATTERNS:
            message = pattern.sub("[REDACTED]", message)
        record.msg, record.args = message, ()
        return True


import re


def safe_filename(value: str, fallback: str = "recording") -> str:
    value = re.sub(r"[\\/:*?\"<>|\x00-\x1f]+", "_", value).strip(" ._")
    return value[:180] or fallback


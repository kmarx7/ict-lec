from dataclasses import dataclass
from urllib.parse import parse_qs, unquote, urlparse


@dataclass(frozen=True, slots=True)
class ParsedZoomURL:
    original_url: str
    canonical_url: str
    host: str
    kind: str


class ZoomURLParser:
    ALLOWED_PATH_PREFIXES = ("/rec/share/", "/rec/play/")

    def parse(self, value: str) -> ParsedZoomURL:
        raw = value.strip()
        parsed = urlparse(raw)
        if parsed.scheme != "https" or not self._valid_host(parsed.hostname):
            raise ValueError("URL must use HTTPS on zoom.us or a zoom.us subdomain")

        query = parse_qs(parsed.query)
        origin = query.get("originRequestUrl", [None])[0]
        if origin:
            return self.parse(unquote(origin))

        kind = next(
            (prefix.split("/")[2] for prefix in self.ALLOWED_PATH_PREFIXES if parsed.path.startswith(prefix)),
            None,
        )
        if kind is None:
            raise ValueError("Unsupported Zoom recording URL path")

        canonical = parsed._replace(fragment="").geturl()
        return ParsedZoomURL(raw, canonical, parsed.hostname or "", kind)

    @staticmethod
    def _valid_host(hostname: str | None) -> bool:
        if not hostname:
            return False
        host = hostname.rstrip(".").lower()
        return host == "zoom.us" or host.endswith(".zoom.us")


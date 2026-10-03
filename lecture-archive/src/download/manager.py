import asyncio
import time
from collections.abc import Callable
from pathlib import Path

import aiofiles
import httpx

from src.download.progress import DownloadProgress
from src.utils.errors import ErrorCode


class DownloadError(RuntimeError):
    def __init__(self, code: ErrorCode, message: str, retryable: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.retryable = retryable


class DownloadManager:
    def __init__(self, chunk_size: int = 1024 * 1024, timeout: float = 30) -> None:
        self.chunk_size = chunk_size
        self.timeout = timeout

    async def download(
        self,
        url: str,
        destination: Path,
        *,
        headers: dict[str, str] | None = None,
        strategy: str = "unknown",
        progress: Callable[[DownloadProgress], None] | None = None,
        cancelled: Callable[[], bool] | None = None,
    ) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        part = destination.with_suffix(destination.suffix + ".part")
        current = part.stat().st_size if part.exists() else 0
        request_headers = dict(headers or {})
        if current:
            request_headers["Range"] = f"bytes={current}-"
        try:
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                async with client.stream("GET", url, headers=request_headers) as response:
                    if response.status_code == 416 and current:
                        part.replace(destination)
                        return destination
                    if response.status_code in (401, 403, 404):
                        codes = {401: ErrorCode.HTTP_UNAUTHORIZED, 403: ErrorCode.HTTP_FORBIDDEN, 404: ErrorCode.HTTP_NOT_FOUND}
                        raise DownloadError(codes[response.status_code], f"HTTP {response.status_code}")
                    if response.status_code >= 500:
                        raise DownloadError(ErrorCode.SERVER_ERROR, f"HTTP {response.status_code}", True)
                    response.raise_for_status()
                    resumed = current > 0 and response.status_code == 206
                    if current and not resumed:
                        current = 0
                    total_header = response.headers.get("content-length")
                    total = (int(total_header) + current) if total_header else None
                    started = time.monotonic()
                    mode = "ab" if resumed else "wb"
                    async with aiofiles.open(part, mode) as stream:
                        async for chunk in response.aiter_bytes(self.chunk_size):
                            if cancelled and cancelled():
                                raise DownloadError(ErrorCode.USER_CANCELLED, "Cancelled by user")
                            await stream.write(chunk)
                            current += len(chunk)
                            elapsed = max(time.monotonic() - started, 0.001)
                            speed = current / elapsed
                            if progress:
                                progress(DownloadProgress(destination.name, current, total, speed, (total - current) / speed if total and speed else None, strategy))
            if total is not None and current != total:
                raise DownloadError(ErrorCode.PARTIAL_DOWNLOAD, "Response ended before expected size", True)
            return part
        except httpx.TimeoutException as exc:
            raise DownloadError(ErrorCode.NETWORK_TIMEOUT, str(exc), True) from exc
        except (httpx.NetworkError, asyncio.IncompleteReadError) as exc:
            raise DownloadError(ErrorCode.CONNECTION_RESET, str(exc), True) from exc


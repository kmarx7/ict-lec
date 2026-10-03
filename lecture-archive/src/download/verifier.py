import asyncio
import json
from pathlib import Path

from pydantic import BaseModel, Field


class VerificationReport(BaseModel):
    valid: bool
    reason: str
    duration_seconds: float | None = None
    streams: list[str] = Field(default_factory=list)


class FileVerifier:
    async def verify(self, path: Path, expected_size: int | None = None) -> VerificationReport:
        if not path.is_file() or path.stat().st_size == 0:
            return VerificationReport(valid=False, reason="파일이 없거나 비어 있습니다.")
        if expected_size is not None and path.stat().st_size != expected_size:
            return VerificationReport(valid=False, reason="파일 크기가 예상 크기와 다릅니다.")
        suffix = path.suffix.lower().removesuffix(".part")
        # A part file has two suffixes: recording.mp4.part.
        if path.suffix.lower() == ".part":
            suffix = Path(path.stem).suffix.lower()
        if suffix == ".vtt":
            header = (await asyncio.to_thread(path.read_bytes))[:256].decode("utf-8", "replace")
            return VerificationReport(valid=header.lstrip("\ufeff").startswith("WEBVTT"), reason="올바른 WebVTT 파일입니다." if header.lstrip("\ufeff").startswith("WEBVTT") else "WEBVTT 헤더가 없습니다.")
        if suffix not in {".mp4", ".m4a", ".mov"}:
            return VerificationReport(valid=True, reason="비어 있지 않은 파일입니다.")
        return await self._ffprobe(path)

    async def _ffprobe(self, path: Path) -> VerificationReport:
        try:
            process = await asyncio.create_subprocess_exec(
                "ffprobe", "-v", "error", "-show_entries", "format=duration", "-show_streams", "-of", "json", str(path),
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
            )
        except FileNotFoundError:
            return VerificationReport(valid=False, reason="미디어 검증에 ffprobe가 필요합니다.")
        stdout, stderr = await process.communicate()
        if process.returncode:
            return VerificationReport(valid=False, reason=f"ffprobe 검증 실패: {stderr.decode(errors='replace')[:200]}")
        try:
            data = json.loads(stdout)
            duration = float(data.get("format", {}).get("duration", 0))
            streams = [item.get("codec_type", "unknown") for item in data.get("streams", [])]
        except (ValueError, TypeError, json.JSONDecodeError):
            return VerificationReport(valid=False, reason="ffprobe 결과가 올바르지 않습니다.")
        valid = duration > 0 and bool({"video", "audio"}.intersection(streams))
        return VerificationReport(valid=valid, reason="올바른 미디어 파일입니다." if valid else "재생 가능한 미디어 스트림이 없습니다.", duration_seconds=duration, streams=streams)

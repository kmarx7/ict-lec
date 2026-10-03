
import pytest

from src.agent.context import AgentContext
from src.agent.evaluator import GoalEvaluator
from src.agent.models import ExecutionResult
from src.download.verifier import VerificationReport


class StubVerifier:
    def __init__(self, valid): self.valid = valid
    async def verify(self, path, expected_size=None): return VerificationReport(valid=self.valid, reason="ok" if self.valid else "bad")


@pytest.mark.asyncio
async def test_evaluator_requires_objective_verification(tmp_path):
    path = tmp_path / "video.mp4"
    path.write_bytes(b"not-real-but-verifier-isolated")
    result = ExecutionResult(success=True, strategy="test", downloaded_files=[path])
    assert not (await GoalEvaluator(StubVerifier(False)).evaluate(AgentContext(original_url="x"), result)).goal_reached
    assert (await GoalEvaluator(StubVerifier(True)).evaluate(AgentContext(original_url="x"), result)).goal_reached


@pytest.mark.asyncio
async def test_zero_byte_file_is_invalid(tmp_path):
    path = tmp_path / "empty.mp4"
    path.touch()
    result = await GoalEvaluator().verifier.verify(path)
    assert not result.valid


@pytest.mark.asyncio
async def test_html_saved_as_mp4_fails_ffprobe(tmp_path):
    path = tmp_path / "error.mp4"
    path.write_text("<html>error</html>")
    assert not (await GoalEvaluator().verifier.verify(path)).valid


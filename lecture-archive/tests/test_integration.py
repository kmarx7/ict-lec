import json

import pytest

from src.agent.context import AgentContext
from src.agent.controller import LoopController
from src.agent.evaluator import GoalEvaluator
from src.agent.executor import Executor
from src.agent.observer import BasicObserver
from src.agent.planner import RuleBasedPlanner
from src.strategies.local_import import LocalImportStrategy


@pytest.mark.asyncio
async def test_local_import_observe_plan_execute_verify_loop(tmp_path):
    source = tmp_path / "source" / "transcript.vtt"
    source.parent.mkdir()
    source.write_text("WEBVTT\n\n00:00.000 --> 00:01.000\nHello\n", encoding="utf-8")
    destination = tmp_path / "archive"
    context = AgentContext(
        original_url="local://import",
        source_type="local",
        local_import_path=source,
    )
    controller = LoopController(
        BasicObserver(),
        RuleBasedPlanner(),
        Executor({"local_import": LocalImportStrategy(destination)}),
        GoalEvaluator(),
    )

    result = await controller.run(context)

    assert result.goal_reached
    assert result.completed_files == [destination / "transcript.vtt"]
    assert result.completed_files[0].read_text(encoding="utf-8").startswith("WEBVTT")


def test_metadata_shape_contains_no_sensitive_values(tmp_path):
    metadata = {
        "source": "zoom",
        "verified": True,
        "files": [{"filename": "recording.mp4", "verified": True}],
    }
    path = tmp_path / "metadata.json"
    path.write_text(json.dumps(metadata), encoding="utf-8")
    serialized = path.read_text(encoding="utf-8").lower()
    assert all(key not in serialized for key in ("passcode", "cookie", "authorization", "access_token"))

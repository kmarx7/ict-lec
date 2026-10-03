from pathlib import Path

import pytest

from src.agent.context import AgentContext
from src.agent.controller import LoopController
from src.agent.models import ActionPlan, ActionType, EvaluationResult, ExecutionResult, Observation


class Observer:
    async def inspect(self, context): return Observation(url_valid=True)


class Planner:
    def decide(self, context, observation): return ActionPlan(action=ActionType.RETRY, strategy_name="fake", reason="try")


class Executor:
    def __init__(self): self.calls = 0
    async def execute(self, context, plan):
        self.calls += 1
        return ExecutionResult(success=self.calls == 2, strategy="fake", retryable=self.calls == 1, error_code="NETWORK_TIMEOUT", downloaded_files=[Path(__file__)] if self.calls == 2 else [])


class Evaluator:
    async def evaluate(self, context, result):
        return EvaluationResult(success=result.success, goal_reached=result.success, retryable=result.retryable, error_category=result.error_code, verified_files=result.downloaded_files)


@pytest.mark.asyncio
async def test_loop_replans_after_failure_then_succeeds():
    executor = Executor()
    context = await LoopController(Observer(), Planner(), executor, Evaluator(), max_loops=3).run(AgentContext(original_url="x"))
    assert context.goal_reached and context.loop_count == 2 and executor.calls == 2

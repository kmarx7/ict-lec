import asyncio
from collections.abc import Callable

from src.agent.context import AgentContext
from src.agent.events import AgentEvent, EventType
from src.agent.models import ActionType
from src.agent.policies import retry_rule


class LoopController:
    def __init__(self, observer, planner, executor, evaluator, *, max_loops: int = 8, event_sink: Callable[[AgentEvent], None] | None = None, human_handler=None) -> None:
        self.observer, self.planner, self.executor, self.evaluator = observer, planner, executor, evaluator
        self.max_loops, self.event_sink, self.human_handler = max_loops, event_sink, human_handler

    def emit(self, event_type: EventType, message: str, **kwargs) -> None:
        if self.event_sink:
            self.event_sink(AgentEvent(event_type=event_type, message=message, **kwargs))

    async def run(self, context: AgentContext) -> AgentContext:
        while not context.goal_reached and context.loop_count < self.max_loops:
            observation = await self.observer.inspect(context)
            self._apply_observation(context, observation)
            self.emit(EventType.OBSERVATION, "Environment observed")
            plan = self.planner.decide(context, observation)
            self.emit(EventType.PLAN_SELECTED, plan.reason, strategy=plan.strategy_name)
            if plan.stop:
                context.terminal_reason = plan.reason
                self.emit(EventType.TERMINATED, plan.reason)
                break
            if plan.action in {ActionType.REQUEST_PASSCODE, ActionType.REQUEST_LOGIN}:
                if not self.human_handler:
                    context.terminal_reason = plan.action.value
                    break
                await self.human_handler(context, plan)
                context.loop_count += 1
                continue
            context.current_strategy = plan.strategy_name
            context.attempted_strategies.append(plan.strategy_name or "")
            self.emit(EventType.ACTION_STARTED, plan.reason, strategy=plan.strategy_name)
            result = await self.executor.execute(context, plan)
            evaluation = await self.evaluator.evaluate(context, result)
            context.loop_count += 1
            if evaluation.goal_reached:
                context.goal_reached = True
                context.completed_files.extend(evaluation.verified_files)
                self.emit(EventType.GOAL_REACHED, evaluation.reason or "Goal reached", strategy=result.strategy)
                break
            context.last_error_code = evaluation.error_category
            context.last_error_message = evaluation.reason
            context.retry_counts[result.strategy] = context.retry_counts.get(result.strategy, 0) + 1
            self.emit(EventType.ACTION_FAILED, evaluation.reason or "Action failed", strategy=result.strategy, error_code=evaluation.error_category)
            rule = retry_rule(evaluation.error_category)
            if evaluation.retryable and rule.base_delay_seconds:
                await asyncio.sleep(rule.base_delay_seconds * (2 ** (context.retry_counts[result.strategy] - 1)))
        if not context.goal_reached and context.loop_count >= self.max_loops:
            context.terminal_reason = "max_loops_reached"
            self.emit(EventType.TERMINATED, "Maximum loop count reached")
        return context

    @staticmethod
    def _apply_observation(context, observation) -> None:
        context.canonical_url = observation.canonical_url or context.canonical_url
        context.recording_found = observation.recording_found
        context.playback_available = observation.playback_available
        context.download_allowed = observation.download_allowed
        context.login_required = observation.login_required
        context.passcode_required = observation.passcode_required
        context.api_available = observation.api_available
        context.browser_session_available = observation.browser_session_available
        if observation.candidate_files:
            context.available_files = observation.candidate_files


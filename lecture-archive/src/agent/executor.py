from src.agent.context import AgentContext
from src.agent.models import ActionPlan, ExecutionResult


class Executor:
    def __init__(self, strategies: dict[str, object]) -> None:
        self.strategies = strategies

    async def execute(self, context: AgentContext, plan: ActionPlan) -> ExecutionResult:
        if not plan.strategy_name or plan.strategy_name not in self.strategies:
            return ExecutionResult(success=False, strategy=plan.strategy_name or "none", error_code="UNKNOWN_ERROR", message="Strategy is not registered")
        strategy = self.strategies[plan.strategy_name]
        if not await strategy.can_handle(context):
            return ExecutionResult(success=False, strategy=plan.strategy_name, error_code="DOWNLOAD_NOT_ALLOWED", message="Strategy preconditions failed")
        return await strategy.execute(context)


from src.agent.context import AgentContext
from src.agent.models import EvaluationResult, ExecutionResult
from src.download.verifier import FileVerifier


class GoalEvaluator:
    def __init__(self, verifier: FileVerifier | None = None) -> None:
        self.verifier = verifier or FileVerifier()

    async def evaluate(self, context: AgentContext, result: ExecutionResult) -> EvaluationResult:
        if not result.success:
            return EvaluationResult(success=False, retryable=result.retryable, error_category=result.error_code, reason=result.message)
        if not result.downloaded_files:
            return EvaluationResult(success=False, error_category="INVALID_MEDIA", reason="No files were produced")
        verified = []
        for path in result.downloaded_files:
            report = await self.verifier.verify(path)
            if not report.valid:
                return EvaluationResult(success=False, error_category="INVALID_MEDIA", reason=report.reason, verified_files=verified)
            final = path
            if path.suffix == ".part":
                final = path.with_suffix("")
                path.replace(final)
            verified.append(final)
        return EvaluationResult(success=True, goal_reached=True, reason="All downloaded files verified", verified_files=verified)

    def is_complete(self, context: AgentContext) -> bool:
        return context.goal_reached and bool(context.completed_files) and all(path.is_file() for path in context.completed_files)


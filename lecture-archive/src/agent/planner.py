from src.agent.context import AgentContext
from src.agent.models import ActionPlan, ActionType, Observation
from src.agent.policies import retry_rule
from src.utils.errors import ErrorCode


class RuleBasedPlanner:
    def decide(self, context: AgentContext, observation: Observation) -> ActionPlan:
        if context.cancelled:
            return self._stop(ErrorCode.USER_CANCELLED, "Cancelled by user")
        if not observation.url_valid and not observation.local_file_available:
            return self._stop(ErrorCode.INVALID_URL, "Invalid or unsupported Zoom URL")
        if observation.recording_found is False:
            return self._stop(ErrorCode.RECORDING_NOT_FOUND, "Recording was not found")
        if observation.passcode_required:
            return ActionPlan(action=ActionType.REQUEST_PASSCODE, reason="Passcode is required")
        if observation.login_required:
            return ActionPlan(action=ActionType.REQUEST_LOGIN, reason="Zoom login is required")
        if observation.download_allowed is False:
            return self._stop(ErrorCode.DOWNLOAD_NOT_ALLOWED, "Download disabled by host")
        if observation.api_available and observation.download_allowed is True:
            return ActionPlan(action=ActionType.ZOOM_API_DOWNLOAD, strategy_name="zoom_api", reason="Official Zoom API is available")
        if observation.direct_download_available and observation.download_allowed is True:
            return ActionPlan(action=ActionType.DIRECT_DOWNLOAD, strategy_name="zoom_direct", reason="Official direct download is available")
        if observation.browser_download_available and observation.download_allowed is not False:
            return ActionPlan(action=ActionType.BROWSER_DOWNLOAD, strategy_name="zoom_browser", reason="Official browser download action is available")
        if observation.local_file_available:
            return ActionPlan(action=ActionType.LOCAL_IMPORT, strategy_name="local_import", reason="Local file is available")
        rule = retry_rule(context.last_error_code)
        attempts = context.retry_counts.get(context.current_strategy or "", 0)
        if rule.retryable and attempts < rule.max_attempts and context.current_strategy:
            return ActionPlan(action=ActionType.RETRY, strategy_name=context.current_strategy, reason=f"Retryable error: {context.last_error_code}")
        return self._stop(ErrorCode.UNKNOWN_ERROR, "No authorized acquisition strategy is available")

    @staticmethod
    def _stop(code: ErrorCode, reason: str) -> ActionPlan:
        return ActionPlan(action=ActionType.STOP, reason=f"{code.value}: {reason}", stop=True)


from src.agent.context import AgentContext
from src.agent.models import ActionPlan, ActionType, Observation
from src.agent.policies import retry_rule
from src.utils.errors import ErrorCode


class RuleBasedPlanner:
    def decide(self, context: AgentContext, observation: Observation) -> ActionPlan:
        if context.cancelled:
            return self._stop(ErrorCode.USER_CANCELLED, "사용자가 다운로드를 취소했습니다.")
        if not observation.url_valid and not observation.local_file_available:
            return self._stop(ErrorCode.INVALID_URL, "올바르거나 지원되는 Zoom 링크가 아닙니다.")
        if observation.recording_found is False:
            return self._stop(ErrorCode.RECORDING_NOT_FOUND, "녹화를 찾을 수 없습니다.")
        if observation.passcode_required:
            return ActionPlan(action=ActionType.REQUEST_PASSCODE, reason="녹화 암호가 필요합니다.")
        if observation.login_required:
            return ActionPlan(action=ActionType.REQUEST_LOGIN, reason="Zoom 로그인이 필요합니다.")
        if observation.download_allowed is False:
            return self._stop(ErrorCode.DOWNLOAD_NOT_ALLOWED, "호스트가 다운로드를 허용하지 않았습니다.")
        if observation.api_available and observation.download_allowed is True:
            return ActionPlan(action=ActionType.ZOOM_API_DOWNLOAD, strategy_name="zoom_api", reason="공식 Zoom API 다운로드를 사용합니다.")
        if observation.direct_download_available and observation.download_allowed is True:
            return ActionPlan(action=ActionType.DIRECT_DOWNLOAD, strategy_name="zoom_direct", reason="공식 직접 다운로드를 사용합니다.")
        if observation.browser_download_available and observation.download_allowed is not False:
            return ActionPlan(action=ActionType.BROWSER_DOWNLOAD, strategy_name="zoom_browser", reason="Zoom의 공식 다운로드 버튼을 사용합니다.")
        if observation.local_file_available:
            return ActionPlan(action=ActionType.LOCAL_IMPORT, strategy_name="local_import", reason="로컬 파일을 사용할 수 있습니다.")
        rule = retry_rule(context.last_error_code)
        attempts = context.retry_counts.get(context.current_strategy or "", 0)
        if rule.retryable and attempts < rule.max_attempts and context.current_strategy:
            return ActionPlan(action=ActionType.RETRY, strategy_name=context.current_strategy, reason=f"다시 시도할 수 있는 오류입니다: {context.last_error_code}")
        return ActionPlan(
            action=ActionType.STOP,
            reason=(
                "녹화는 재생할 수 있지만 호스트가 공식 다운로드 버튼을 제공하지 않았습니다. "
                "다운로드가 필요하면 녹화 호스트에게 허용을 요청해 주세요."
            ),
            stop=True,
        )

    @staticmethod
    def _stop(code: ErrorCode, reason: str) -> ActionPlan:
        return ActionPlan(action=ActionType.STOP, reason=f"{code.value}: {reason}", stop=True)

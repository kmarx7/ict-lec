from src.agent.context import AgentContext
from src.agent.models import ActionType, Observation
from src.agent.planner import RuleBasedPlanner


def decide(**kwargs):
    return RuleBasedPlanner().decide(AgentContext(original_url="https://zoom.us/rec/share/x"), Observation(url_valid=True, **kwargs))


def test_passcode_precedes_strategies():
    assert decide(passcode_required=True).action == ActionType.REQUEST_PASSCODE


def test_login_is_requested():
    assert decide(login_required=True).action == ActionType.REQUEST_LOGIN


def test_api_is_preferred():
    assert decide(api_available=True, download_allowed=True).action == ActionType.ZOOM_API_DOWNLOAD


def test_browser_action_is_selected():
    assert decide(browser_download_available=True).action == ActionType.BROWSER_DOWNLOAD


def test_explicit_denial_is_terminal():
    plan = decide(download_allowed=False)
    assert plan.stop and "DOWNLOAD_NOT_ALLOWED" in plan.reason


from src.agent.context import AgentContext


def test_context_has_independent_mutable_defaults():
    first = AgentContext(original_url="a")
    second = AgentContext(original_url="b")
    first.attempted_strategies.append("x")
    assert second.attempted_strategies == []


def test_passcode_is_excluded_from_serialization():
    context = AgentContext(original_url="x", passcode="secret")
    assert "passcode" not in context.model_dump()

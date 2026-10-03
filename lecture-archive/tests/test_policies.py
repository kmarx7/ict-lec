from src.agent.policies import retry_rule


def test_timeout_has_bounded_retry():
    rule = retry_rule("NETWORK_TIMEOUT")
    assert rule.retryable and rule.max_attempts == 3


def test_permission_denial_is_not_retryable():
    assert not retry_rule("DOWNLOAD_NOT_ALLOWED").retryable


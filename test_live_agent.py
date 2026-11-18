"""Explicitly gated provider test placeholder; local planner behavior is tested offline."""
import os
import pytest

pytestmark = pytest.mark.skipif(
    os.getenv("ASMA_RUN_EXTERNAL_PROVIDER_TESTS") != "1" or not os.getenv("DEEPSEEK_API_KEY"),
    reason="external provider checks require explicit opt-in and a configured key",
)

def test_remote_planner_is_not_enabled_by_default():
    pytest.skip("Remote planning is intentionally not part of the offline test suite.")

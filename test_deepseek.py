"""Opt-in connectivity check. Never sends provider traffic during normal pytest runs."""
import os
import pytest

pytestmark = pytest.mark.skipif(
    os.getenv("ASMA_RUN_EXTERNAL_PROVIDER_TESTS") != "1" or not os.getenv("DEEPSEEK_API_KEY"),
    reason="external provider checks require explicit opt-in and a configured key",
)

def test_deepseek_connectivity_is_explicitly_opted_in():
    pytest.skip("Use the provider's documented health check in a separately approved environment.")

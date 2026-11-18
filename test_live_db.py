"""Explicitly gated database connectivity placeholder."""
import os
import pytest

pytestmark = pytest.mark.skipif(
    os.getenv("ASMA_RUN_EXTERNAL_PROVIDER_TESTS") != "1" or not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"),
    reason="live database checks require explicit opt-in and external credentials",
)

def test_live_database_is_not_contacted_by_default():
    pytest.skip("Use an isolated test project after explicitly approving external access.")

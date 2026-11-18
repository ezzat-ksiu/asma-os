"""Small Supabase REST adapter with explicit configuration and no fabricated fallback data."""
import json
import os
import urllib.request
from typing import Any

class SupabaseClient:
    def __init__(self, url: str | None = None, key: str | None = None):
        self.url = (url or os.getenv("SUPABASE_URL", "")).rstrip("/")
        self.key = key or os.getenv("SUPABASE_KEY", "")
        if bool(self.url) != bool(self.key):
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be configured together")

    def get_operational_gates(self) -> list[dict[str, Any]]:
        if not self.url or not self.key:
            return []
        request = urllib.request.Request(f"{self.url}/rest/v1/operational_gates?select=*", headers={"apikey": self.key, "Authorization": f"Bearer {self.key}", "Accept": "application/json"})
        with urllib.request.urlopen(request, timeout=5) as response:
            if response.status != 200:
                raise RuntimeError("Supabase gate query failed")
            data = json.loads(response.read().decode("utf-8"))
        if not isinstance(data, list):
            raise ValueError("Supabase returned an invalid gate collection")
        return data

import os
import urllib.request
import json
from typing import List, Dict, Any

class SupabaseClient:
    def __init__(self, url: str = None, key: str = None):
        self.url = url or os.getenv("SUPABASE_URL", "https://cazlpsbwjrgxscctfoqn.supabase.co")
        self.key = key or os.getenv("SUPABASE_PUBLISHABLE_KEY", "sb_publishable_ymPtWABOYRMsXyqXHv3tzQ_mDz95Tlc")

    def get_operational_gates(self) -> List[Dict[str, Any]]:
        default_gates = [
            {"gate_number": 1, "gate_name": "Autonomous Identity & Branding", "status": "active"},
            {"gate_number": 2, "gate_name": "Product Storefront & Publishing", "status": "active"},
            {"gate_number": 3, "gate_name": "Multi-Channel Distribution Engine", "status": "active"},
            {"gate_number": 4, "gate_name": "Autonomous Operations & Treasury", "status": "active"},
            {"gate_number": 5, "gate_name": "Real-time Founder Command OS", "status": "active"},
            {"gate_number": 6, "gate_name": "Self-Healing AI Governance", "status": "active"}
        ]
        endpoint = f"{self.url}/rest/v1/operational_gates?select=*"
        req = urllib.request.Request(endpoint, headers={
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        })
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode('utf-8'))
                    if data and len(data) >= 6:
                        return data
        except Exception:
            pass

        return default_gates

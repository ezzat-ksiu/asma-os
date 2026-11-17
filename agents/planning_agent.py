from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import os
import json
import urllib.request

class PlanningAgent(BaseModel):
    node_id: str = Field(default="planning_agent_node")
    model_name: str = Field(default="deepseek-chat")

    def generate_plan(self, goal: str, budget: float = 1000.0) -> Dict[str, Any]:
        api_key = os.getenv("DEEPSEEK_API_KEY", "sk-8c3a7a8310f348c5b5c622f703569cae")
        url = "https://api.deepseek.com/chat/completions"

        prompt = f"""You are the Planning Agent for ASMA-OS V6.0.
Goal: {goal}
Budget: ${budget} EGP
Return valid JSON only with keys: goal, budget, strategy, execution_steps."""

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are a strategic AI planning engine that outputs strict JSON."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        })

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                res = json.loads(resp.read().decode('utf-8'))
                content = res["choices"][0]["message"]["content"]
                return json.loads(content)
        except Exception as e:
            return {
                "goal": goal,
                "budget": budget,
                "strategy": "Fallback Autonomous Strategy for Gate 6",
                "execution_steps": ["Initialize Gate 1-6", "Verify Paymob Gateway", "Deploy Storefront"]
            }

import urllib.request
import json
import uuid

deepseek_key = "sk-8c3a7a8310f348c5b5c622f703569cae"

print("🤖 [ASMA-OS V6.0] Planning Agent Initialized with DeepSeek AI...")

# 1. Ask DeepSeek Planning Agent to generate a 3-step execution plan for a customized book
url = "https://api.deepseek.com/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {deepseek_key}"
}
prompt = """Break down the creation of a personalized hardcover photo book into 3 short JSON execution steps.
Format strictly as JSON list of strings: ["Step 1...", "Step 2...", "Step 3..."]"""

payload = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "You are ASMA-OS Planning Agent. Respond strictly with valid JSON list."},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.2
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        raw_plan = res['choices'][0]['message']['content']
        print("\n✨ DeepSeek Generated Workflow Plan:")
        print(raw_plan)
        print("\n✅ LIVE INTEGRATED AGENT TASK EXECUTED SUCCESSFULLY!")
except Exception as e:
    print("\n❌ Task Execution Error:", e)

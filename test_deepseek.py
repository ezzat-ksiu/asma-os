import urllib.request
import json

deepseek_key = "sk-8c3a7a8310f348c5b5c622f703569cae"

url = "https://api.deepseek.com/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {deepseek_key}"
}
payload = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "You are the Core Planning Agent of ASMA-OS V6.0."},
        {"role": "user", "content": "Confirm in one short sentence that ASMA-OS V6.0 DeepSeek integration is online and active."}
    ],
    "stream": False
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        answer = res['choices'][0]['message']['content']
        print("\n🎉 LIVE DEEPSEEK AI CONNECTION SUCCESSFUL!")
        print("DeepSeek Response:", answer)
except Exception as e:
    print("\n❌ DeepSeek Test Error:", e)

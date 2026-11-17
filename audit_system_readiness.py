import os
import sys
import shutil
import urllib.request
import json
import subprocess

print("==========================================================")
print("🔍 ASMA-OS V6.0 COMPLETE SYSTEM READINESS AUDIT")
print("==========================================================")

# 1. Check Python Virtual Environment
print("\n1. PYTHON & CORE DEPENDENCIES:")
print(f"   - Python Executable: {sys.executable}")
print(f"   - Python Version: {sys.version.split()[0]}")

try:
    import pydantic
    import pytest
    import mcp
    import langgraph
    print("   - Core Packages (Pydantic, Pytest, MCP, LangGraph): ✅ ALL INSTALLED")
except ImportError as e:
    print(f"   - Core Packages: ❌ Missing package: {e}")

# 2. Check System Binaries (Node.js, npm, Typst, Git)
print("\n2. LOCAL SYSTEM BINARIES & TOOLING:")
tools = {
    "git": "Git Version Control",
    "node": "Node.js Environment (Required for Storefront & Founder Screen)",
    "npm": "NPM Package Manager",
    "typst": "Typst Printing & Document Compiler"
}

for tool, desc in tools.items():
    path = shutil.which(tool)
    if path:
        print(f"   - {tool.upper()} ({desc}): ✅ INSTALLED ({path})")
    else:
        print(f"   - {tool.upper()} ({desc}): ⚠️ NOT FOUND IN PATH")

# 3. Check Live Cloud Environment Variables (.env)
print("\n3. CLOUD INTEGRATIONS & API KEYS (.env):")
env_vars = {}
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip().strip('"')

keys_to_check = [
    ("SUPABASE_URL", "Supabase Live Database URL"),
    ("SUPABASE_KEY", "Supabase Live Anon Key"),
    ("DEEPSEEK_API_KEY", "DeepSeek AI Key"),
    ("GEMINI_API_KEY", "Google Gemini QA AI Key"),
    ("R2_ACCOUNT_ID", "Cloudflare R2 Storage Account"),
    ("GELATO_API_KEY", "Gelato Print-On-Demand Key"),
    ("PAYMOB_API_KEY", "Paymob Payment Gateway Key"),
    ("AUTH0_DOMAIN", "Auth0 Identity Domain")
]

for key, label in keys_to_check:
    val = env_vars.get(key, "")
    if val and not val.startswith("YOUR_") and not val.startswith("PASTE_"):
        print(f"   - {key} ({label}): ✅ CONFIGURED")
    else:
        print(f"   - {key} ({label}): ⚠️ MISSING OR PLACEHOLDER")

print("\n==========================================================")
print("AUDIT COMPLETE.")
print("==========================================================")

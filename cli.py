# -*- coding: utf-8 -*-
"""
LUMEYRA ASMA-OS V6.0 Founder Local Command Line Tool
"""
import sys
import os
import subprocess

def run_cmd(cmd):
    print(f"Executing: {cmd}")
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        print(f"Error executing: {cmd}")

def main():
    print("=" * 60)
    print("      LUMEYRA ASMA-OS V6.0 - FOUNDER CONTROL PANEL")
    print("=" * 60)
    print("1. Run E2E Gate Tests (Pytest)")
    print("2. Generate 30 SEO Articles")
    print("3. Check Git Status")
    print("4. Push Latest Code to GitHub")
    print("Q. Quit")
    print("-" * 60)
    
    choice = input("Select an option: ").strip().lower()
    if choice == '1':
        run_cmd("python -m pytest test_e2e_gates.py -v")
    elif choice == '2':
        run_cmd("python services/seo_engine.py")
    elif choice == '3':
        run_cmd("git status")
    elif choice == '4':
        run_cmd("git add . && git commit -m 'feat: update system assets' && git push origin main")
    elif choice == 'q':
        sys.exit(0)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
"""Local developer helper for safe, non-production project tasks."""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Sequence


def run_cmd(args: Sequence[str]) -> int:
    """Run a fixed argument vector without invoking a shell."""
    if not args or any(not isinstance(arg, str) for arg in args):
        raise ValueError("args must be a non-empty sequence of strings")
    result = subprocess.run(list(args), shell=False, check=False)
    return result.returncode


def main() -> None:
    print("=" * 60)
    print("FOLIAVERE (provisional) / ASMA-OS Local Developer Menu")
    print("No provider, payment, publishing, or Git push actions are available.")
    print("1. Run the full local test suite")
    print("2. Show Git status")
    print("Q. Quit")
    choice = input("Select an option: ").strip().lower()
    if choice == "1":
        raise SystemExit(run_cmd([sys.executable, "-m", "pytest", "-v"]))
    if choice == "2":
        raise SystemExit(run_cmd(["git", "status", "-sb"]))
    if choice != "q":
        print("Invalid choice.")


if __name__ == "__main__":
    main()

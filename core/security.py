"""Zero-trust token helpers, payload sanitization, and a lightweight source scan."""

from __future__ import annotations

import hashlib
import hmac
import math
import re
from pathlib import Path
from typing import Any
import unicodedata


class ZeroTrustSecurityManager:
    """Small standard-library security helpers with no hosted dependencies."""

    _dangerous_keys = {
        "__proto__", "prototype", "constructor", "__definegetter__", "__definesetter__",
        "__lookupgetter__", "__lookupsetter__", "tostring", "valueof", "hasownproperty",
        "isprototypeof", "propertyisenumerable", "tolocalestring",
    }
    _secret_assignment = re.compile(
        r"""(?i)\b(?:password|passwd|secret|api[_-]?key|access[_-]?token)\b\s*[:=]\s*['"][^'"]{6,}['"]"""
    )
    _dangerous_code = (
        (re.compile(r"\beval\s*\("), "dynamic eval call"),
        (re.compile(r"\bexec\s*\("), "dynamic exec call"),
        (re.compile(r"\bpickle\.loads\s*\("), "unsafe pickle deserialization"),
        (re.compile(r"\bshell\s*=" + r"\s*True\b"), "shell" + "=True process invocation"),
    )
    _source_extensions = {".py", ".js", ".jsx", ".ts", ".tsx"}
    _excluded_dirs = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache"}

    @staticmethod
    def generate_node_token(node_id: str, secret_key: str) -> str:
        if not isinstance(node_id, str) or not node_id.strip():
            raise ValueError("node_id must not be empty")
        if not isinstance(secret_key, str) or not secret_key:
            raise ValueError("secret_key must not be empty")
        return hmac.new(
            secret_key.encode("utf-8"),
            node_id.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    @classmethod
    def validate_node_token(cls, node_id: str, token: str, secret_key: str) -> bool:
        if not isinstance(token, str):
            return False
        try:
            expected = cls.generate_node_token(node_id, secret_key)
        except (TypeError, ValueError):
            return False
        return hmac.compare_digest(expected, token)

    @classmethod
    def sanitize_payload(cls, payload: dict) -> dict:
        """Return JSON-like payload data with unsafe keys and values removed."""
        if not isinstance(payload, dict):
            raise TypeError("payload must be a dictionary")
        budget = [0]
        exceeded_limits = [False]

        def clean(value: Any, depth: int = 0) -> Any:
            budget[0] += 1
            if depth > 32 or budget[0] > 10_000:
                exceeded_limits[0] = True
                return _DROP
            if isinstance(value, dict):
                safe: dict[str, Any] = {}
                for raw_key, raw_value in value.items():
                    if budget[0] >= 10_000:
                        break
                    if not isinstance(raw_key, str):
                        continue
                    key = unicodedata.normalize("NFC", raw_key).strip()
                    lowered = key.casefold()
                    if (
                        not key
                        or len(key) > 256
                        or lowered in cls._dangerous_keys
                        or lowered.startswith("__")
                        or "$" in key
                        or "." in key
                        or any(ord(char) < 32 or ord(char) == 127 for char in key)
                        or key in safe
                    ):
                        continue
                    value = clean(raw_value, depth + 1)
                    if value is not _DROP:
                        safe[key] = value
                return safe
            if isinstance(value, (list, tuple)):
                safe_items = []
                for raw_item in value:
                    if budget[0] >= 10_000:
                        break
                    item = clean(raw_item, depth + 1)
                    if item is not _DROP:
                        safe_items.append(item)
                return safe_items
            if value is None or isinstance(value, (str, bool, int)):
                return value
            if isinstance(value, float) and math.isfinite(value):
                return value
            return _DROP

        sanitized = clean(payload)
        if exceeded_limits[0]:
            return {}
        return sanitized if isinstance(sanitized, dict) else {}

    @classmethod
    def static_security_scan(cls, codebase_path: str) -> dict[str, Any]:
        """Heuristically scan source files for common risky patterns.

        This dependency-free check is suitable for local feedback; it is not a
        replacement for a dedicated SAST tool or a security review.
        """
        root = Path(codebase_path).expanduser()
        if not root.exists() or not root.is_dir():
            return {
                "status": "FAIL",
                "clean": False,
                "files_scanned": 0,
                "findings": [{"path": str(root), "line": 0, "rule": "invalid_path"}],
            }
        findings: list[dict[str, Any]] = []
        files_scanned = 0
        try:
            files = root.rglob("*")
            for path in files:
                if not path.is_file() or path.suffix.lower() not in cls._source_extensions:
                    continue
                relative = path.relative_to(root)
                if any(part in cls._excluded_dirs for part in relative.parts):
                    continue
                try:
                    if path.stat().st_size > 2_000_000:
                        continue
                    source = path.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    findings.append({"path": str(relative), "line": 0, "rule": "unreadable_source"})
                    continue
                files_scanned += 1
                for line_number, line in enumerate(source.splitlines(), start=1):
                    if cls._secret_assignment.search(line):
                        findings.append({
                            "path": str(relative), "line": line_number, "rule": "possible_hardcoded_secret",
                        })
                    for pattern, rule in cls._dangerous_code:
                        if pattern.search(line):
                            findings.append({"path": str(relative), "line": line_number, "rule": rule})
        except OSError:
            findings.append({"path": str(root), "line": 0, "rule": "scan_error"})
        return {
            "status": "PASS" if not findings else "FAIL",
            "clean": not findings,
            "files_scanned": files_scanned,
            "findings": findings,
        }


_DROP = object()

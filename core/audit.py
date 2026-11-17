"""Immutable, tamper-evident audit ledger using a SHA-256 hash chain."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import hmac
import json
from types import MappingProxyType
from typing import Any, Mapping


_GENESIS_HASH = "0" * 64


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


@dataclass(frozen=True, slots=True)
class AuditBlock:
    timestamp: str
    actor: str
    action: str
    details: Mapping[str, Any]
    previous_hash: str
    block_hash: str


class CryptoAuditLedger:
    """Append-only audit entries whose order and contents are hash-verifiable."""

    def __init__(self) -> None:
        self._blocks: list[AuditBlock] = []

    @property
    def blocks(self) -> tuple[AuditBlock, ...]:
        return tuple(self._blocks)

    @staticmethod
    def _hash_block(
        timestamp: str,
        actor: str,
        action: str,
        details: Mapping[str, Any],
        previous_hash: str,
    ) -> str:
        canonical = json.dumps(
            {
                "timestamp": timestamp,
                "actor": actor,
                "action": action,
                "details": _thaw(details),
                "previous_hash": previous_hash,
            },
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def append_entry(self, actor: str, action: str, details: dict) -> AuditBlock:
        if not isinstance(actor, str) or not actor.strip():
            raise ValueError("actor must not be empty")
        if not isinstance(action, str) or not action.strip():
            raise ValueError("action must not be empty")
        if not isinstance(details, dict):
            raise TypeError("details must be a dictionary")
        timestamp = datetime.now(timezone.utc).isoformat(timespec="microseconds")
        immutable_details = _freeze(details)
        previous_hash = self._blocks[-1].block_hash if self._blocks else _GENESIS_HASH
        block_hash = self._hash_block(timestamp, actor, action, immutable_details, previous_hash)
        block = AuditBlock(
            timestamp=timestamp,
            actor=actor,
            action=action,
            details=immutable_details,
            previous_hash=previous_hash,
            block_hash=block_hash,
        )
        self._blocks.append(block)
        return block

    def verify_integrity(self) -> bool:
        previous_hash = _GENESIS_HASH
        try:
            for block in self._blocks:
                if block.previous_hash != previous_hash:
                    return False
                expected = self._hash_block(
                    block.timestamp,
                    block.actor,
                    block.action,
                    block.details,
                    block.previous_hash,
                )
                if not hmac.compare_digest(expected, block.block_hash):
                    return False
                previous_hash = block.block_hash
        except (AttributeError, TypeError, ValueError, json.JSONDecodeError):
            return False
        return True

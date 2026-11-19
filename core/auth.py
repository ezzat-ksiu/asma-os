"""Fail-closed founder identity authorization for private API operations."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Protocol


class TokenVerifier(Protocol):
    def verify_token(self, token: str) -> dict[str, Any]: ...


class AuthenticationNotConfigured(RuntimeError):
    """Required identity-provider or founder allowlist settings are missing."""


class AuthenticationRejected(PermissionError):
    """A token is invalid or does not belong to an allowlisted founder subject."""


def authorize_founder_token(
    token: str,
    verifier: TokenVerifier,
    allowed_subjects: Iterable[str],
) -> dict[str, str]:
    """Validate a JWT then authorize its exact subject against a private allowlist.

    Only a minimal subject identity is returned. Email and arbitrary token claims
    are deliberately not copied into logs or response objects.
    """
    subjects = {subject.strip() for subject in allowed_subjects if subject.strip()}
    if not subjects:
        raise AuthenticationNotConfigured("Founder subject allowlist is not configured")
    if not token:
        raise AuthenticationRejected("Bearer token is required")
    try:
        claims = verifier.verify_token(token)
    except Exception as exc:
        raise AuthenticationRejected("Bearer token could not be verified") from exc
    subject = claims.get("sub") if isinstance(claims, dict) else None
    if not isinstance(subject, str) or subject not in subjects:
        raise AuthenticationRejected("Token subject is not authorized for founder access")
    return {"subject": subject}

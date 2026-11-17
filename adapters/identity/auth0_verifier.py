"""Auth0 JWT verification and machine-to-machine token acquisition."""
from __future__ import annotations

import os
import time
from urllib.parse import urlparse

from adapters.http import request_json


class Auth0Verifier:
    def __init__(self, domain: str | None = None, audience: str | None = None, *,
                 client_id: str | None = None, client_secret: str | None = None,
                 timeout: float = 10, clock=time.time):
        self.domain = (domain or os.getenv("AUTH0_DOMAIN", "")).strip().rstrip("/")
        if self.domain and not self.domain.startswith(("https://", "http://")):
            self.domain = "https://" + self.domain
        self.audience = audience or os.getenv("AUTH0_AUDIENCE")
        self.client_id = client_id or os.getenv("AUTH0_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("AUTH0_CLIENT_SECRET")
        self.timeout, self.clock, self._jwks_cache = timeout, clock, (0, [])
        if self.domain and urlparse(self.domain).scheme != "https":
            raise ValueError("Auth0 domain must use HTTPS")

    def _jwks(self) -> list[dict]:
        if self._jwks_cache[0] > self.clock():
            return self._jwks_cache[1]
        if not self.domain:
            raise ValueError("AUTH0_DOMAIN is required")
        keys = request_json("Auth0", f"{self.domain}/.well-known/jwks.json", timeout=self.timeout).get("keys", [])
        self._jwks_cache = (self.clock() + 300, keys)
        return keys

    def verify_token(self, token: str) -> dict:
        if not self.audience:
            raise ValueError("Auth0 audience is required")
        try:
            import jwt
        except ImportError as exc:
            raise RuntimeError("Install PyJWT[crypto] to verify Auth0 tokens") from exc
        header = jwt.get_unverified_header(token)
        if header.get("alg") != "RS256" or not header.get("kid"):
            raise ValueError("Only keyed RS256 Auth0 tokens are accepted")
        jwk = next((item for item in self._jwks() if item.get("kid") == header["kid"]), None)
        if not jwk:
            raise ValueError("No matching Auth0 signing key")
        key = jwt.algorithms.RSAAlgorithm.from_jwk(jwk)
        return jwt.decode(token, key, algorithms=["RS256"], audience=self.audience,
                          issuer=f"{self.domain}/", options={"require": ["exp", "iat", "sub"]})

    def get_machine_token(self, *, audience: str | None = None) -> dict:
        if not all((self.domain, self.client_id, self.client_secret, audience or self.audience)):
            raise ValueError("Auth0 domain, client credentials, and audience are required")
        return request_json("Auth0", f"{self.domain}/oauth/token", method="POST", timeout=self.timeout,
            payload={"client_id": self.client_id, "client_secret": self.client_secret,
                     "audience": audience or self.audience, "grant_type": "client_credentials"})


"""Small async PostgreSQL adapter wrapper; driver is injected by the application."""
from __future__ import annotations

from typing import Any, Optional


class PostgresAdapter:
    """Async pool wrapper compatible with asyncpg-style pools.

    No database driver is imported or started implicitly, keeping local setup
    free of paid services and allowing applications to inject their own pool.
    """

    def __init__(self, pool: Optional[Any] = None) -> None:
        self.pool = pool

    async def connect(self, dsn: str, **pool_options: Any) -> None:
        if self.pool is not None:
            return
        try:
            import asyncpg
        except ImportError as exc:
            raise RuntimeError("Install asyncpg to create a PostgreSQL connection pool") from exc
        self.pool = await asyncpg.create_pool(dsn=dsn, **pool_options)

    async def execute(self, query: str, *args: Any) -> Any:
        if self.pool is None:
            raise RuntimeError("PostgreSQL pool is not connected")
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def fetch(self, query: str, *args: Any) -> list[Any]:
        if self.pool is None:
            raise RuntimeError("PostgreSQL pool is not connected")
        async with self.pool.acquire() as connection:
            return list(await connection.fetch(query, *args))

    async def close(self) -> None:
        if self.pool is not None:
            await self.pool.close()
            self.pool = None

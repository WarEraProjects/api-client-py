import json
import sqlite3
import threading
from collections import OrderedDict
from typing import Any, Protocol


class CacheBackend(Protocol):
    def get(self, key: str) -> tuple[Any, float] | None:
        """Return (data, timestamp) if key exists, else None."""
        ...

    def set(self, key: str, data: Any, timestamp: float) -> None:
        """Store data with its fetch timestamp."""
        ...

    def delete(self, key: str) -> None:
        """Remove a key from the cache."""
        ...

    def clear(self) -> None:
        """Clear all keys from the cache."""
        ...

    def get_size(self) -> int:
        """Return the number of items in the cache."""
        ...

    def pop_oldest(self) -> None:
        """Remove the oldest item from the cache (for LRU eviction)."""
        ...


class MemoryCacheBackend:
    """Default SWR cache backend using an in-memory OrderedDict for true LRU eviction."""

    def __init__(self) -> None:
        self._cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()

    def get(self, key: str) -> tuple[Any, float] | None:
        val = self._cache.get(key)
        if val is not None:
            self._cache.move_to_end(key)
        return val

    def set(self, key: str, data: Any, timestamp: float) -> None:
        self._cache[key] = (data, timestamp)
        self._cache.move_to_end(key)

    def delete(self, key: str) -> None:
        self._cache.pop(key, None)

    def clear(self) -> None:
        self._cache.clear()

    def get_size(self) -> int:
        return len(self._cache)

    def pop_oldest(self) -> None:
        if self._cache:
            self._cache.popitem(last=False)


class SQLiteCacheBackend:
    """
    A persistent SWR cache backend backed by a local SQLite file.
    All disk I/O operations are protected by a thread lock, making it safe for
    use in highly concurrent background threads or asyncio workers.
    """

    def __init__(self, db_path: str = "warera_cache.sqlite") -> None:
        self._db_path = db_path
        self._lock = threading.Lock()
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        # SQLite objects created in a thread can only be used in that same thread.
        # So we create a short-lived connection per operation. Since we use a Lock,
        # concurrent writes are serialized anyway.
        return sqlite3.connect(self._db_path, timeout=10.0)

    def _init_db(self) -> None:
        with self._lock, self._get_connection() as conn:
            conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS swr_cache (
                        key TEXT PRIMARY KEY,
                        data TEXT,
                        timestamp REAL
                    )
                    """
            )

    def get(self, key: str) -> tuple[Any, float] | None:
        with self._lock, self._get_connection() as conn:
            cursor = conn.execute("SELECT data, timestamp FROM swr_cache WHERE key = ?", (key,))
            row = cursor.fetchone()
            if row:
                try:
                    return json.loads(row[0]), row[1]
                except json.JSONDecodeError:
                    return None
            return None

    def set(self, key: str, data: Any, timestamp: float) -> None:
        with self._lock, self._get_connection() as conn:
            # We serialize the data to JSON string to store in SQLite
            conn.execute(
                "INSERT OR REPLACE INTO swr_cache (key, data, timestamp) VALUES (?, ?, ?)",
                (key, json.dumps(data), timestamp),
            )

    def delete(self, key: str) -> None:
        with self._lock, self._get_connection() as conn:
            conn.execute("DELETE FROM swr_cache WHERE key = ?", (key,))

    def clear(self) -> None:
        with self._lock, self._get_connection() as conn:
            conn.execute("DELETE FROM swr_cache")

    def get_size(self) -> int:
        with self._lock, self._get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM swr_cache")
            row = cursor.fetchone()
            return row[0] if row else 0

    def pop_oldest(self) -> None:
        with self._lock, self._get_connection() as conn:
            conn.execute(
                """
                    DELETE FROM swr_cache
                    WHERE key = (
                        SELECT key FROM swr_cache ORDER BY timestamp ASC LIMIT 1
                    )
                    """
            )

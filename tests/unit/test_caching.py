import asyncio
from typing import Any

from warera.cache_backends import SQLiteCacheBackend


def test_sqlite_cache_backend_basic(tmp_path: Any) -> None:
    db_path = tmp_path / "cache.db"
    backend = SQLiteCacheBackend(db_path=str(db_path))

    # Set
    backend.set("my_key", {"foo": "bar"}, 1000)

    # Get
    val = backend.get("my_key")
    assert val is not None
    assert val[0] == {"foo": "bar"}
    assert val[1] == 1000

    # Delete
    backend.delete("my_key")
    assert backend.get("my_key") is None


def test_sqlite_cache_backend_concurrent(tmp_path: Any) -> None:
    db_path = tmp_path / "cache2.db"
    backend = SQLiteCacheBackend(db_path=str(db_path))

    async def worker(idx: int) -> None:
        key = f"key_{idx}"
        backend.set(key, {"idx": idx}, 2000)
        val = backend.get(key)
        assert val is not None
        assert val[0] == {"idx": idx}

    async def main() -> None:
        await asyncio.gather(*(worker(i) for i in range(50)))

    asyncio.run(main())


def test_sqlite_cache_backend_invalid_json(tmp_path: Any) -> None:
    db_path = tmp_path / "cache3.db"
    backend = SQLiteCacheBackend(db_path=str(db_path))

    # Manually insert bad JSON
    with backend._get_connection() as conn:
        conn.execute(
            "INSERT INTO swr_cache (key, data, timestamp) VALUES (?, ?, ?)",
            ("bad_key", "NOT_JSON", 1234),
        )

    # Should not crash, should return None
    assert backend.get("bad_key") is None

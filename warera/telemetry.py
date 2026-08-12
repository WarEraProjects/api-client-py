from typing import Protocol


class TelemetryHooks(Protocol):
    """
    Protocol for observability and telemetry instrumentation.
    Implement this protocol to attach your own Datadog/Prometheus/StatsD tracking.
    """

    def on_rate_limit_sleep(self, wait_seconds: float) -> None:
        """Called when the HTTP session sleeps due to exhausted rate limits."""
        ...

    def on_batch_flush(self, size: int, execution_time_ms: float) -> None:
        """Called when an auto-batch chunk is flushed to the network."""
        ...

    def on_cache_hit(self, key: str, is_stale: bool) -> None:
        """Called when a value is returned from the SWR Cache."""
        ...

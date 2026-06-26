# Advanced Usage

The Python client includes a suite of advanced features designed to maximize network throughput and handle extremely massive datasets safely. 

## High-Concurrency Pagination (`collect_all`)

The `collect_all()` engine is the most powerful feature of the wrapper. Unlike traditional pagination (where a client waits for page 1 to load before requesting page 2), `collect_all()` uses synthetic time-sliced cursors to split a timeline into chunks and requests them all concurrently.

```python
# Fetches thousands of transaction logs simultaneously.
# The `time_slice_days` parameter breaks the timeline into 0.2-day chunks (approx 5 hours).
# The `concurrency` parameter dictates how many HTTP chunks to fire at once.
logs = await warera.transaction.collect_all(
    oldest_date="2026-01-01T00:00:00Z",
    time_slice_days=0.2, 
    concurrency=500
)
```

> [!WARNING]
> **Rate Limit Note**: A `concurrency=500` will instantly saturate the API's global rate limit of 500 requests per minute. The library implements transparent 429 backoff protection via jitter, but hitting the API this hard may cause `502 Bad Gateway` errors from upstream load balancers if you are querying highly demanding databases. Dial down `concurrency` to 100 if you experience random disconnects.



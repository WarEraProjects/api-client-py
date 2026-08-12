# Frequently Asked Questions

This page contains answers to common questions and issues developers encounter when building scripts with the `warera-client`.

---

### Do I need an API key to use the library?

**No, but it is highly recommended.** 
If you don't provide an API key, the library works perfectly fine anonymously. However, WarEra enforces much stricter rate limits on anonymous IP addresses (e.g., 100 requests instead of 500). For anything beyond basic testing, [generate an API key in your game settings](https://warera.com/settings) and pass it to the client.

### What are these `_id` and `__v` fields on every model?

These are internal properties returned by the game's backend database (MongoDB / Mongoose). 
- `_id` is the primary key for a document. The library automatically aliases this to `.id` in Python for convenience!
- `__v` is the document version key used internally by the backend to track revisions. You can safely ignore it.

### Why does a specific field return `None` when I access it?

WarEra's backend is highly dynamic. If a user hasn't unlocked a specific feature, or if a country hasn't formed an alliance, the API will often omit that data entirely. 

To prevent parsing crashes, the Python client makes these fields `Optional` (which defaults to `None`). Always check if a field exists before attempting to access nested properties on it!

```python
# GOOD:
if user.party:
    print(user.party.name)

# BAD: (Will crash if the user is independent)
print(user.party.name)
```

### Can I use this library with Django, Flask, or other synchronous frameworks?

**Yes!** While the library is built around `asyncio`, we provide a robust synchronous wrapper specifically for this use case.

Just import `WareraClient` from the `sync` submodule instead of the root module:

```python
from warera.sync import WareraClient
client = WareraClient(api_key="your_key")
```

The sync wrapper spawns a daemon thread with an isolated event loop, ensuring it plays nicely with Django/Flask's threading models without sacrificing the auto-batching engine's performance.

### How do I handle Rate Limiting (`WareraRateLimitError`)?

**You usually don't have to!** The library automatically intercepts `429 Too Many Requests` responses, parses the `ratelimit-reset` header, silently sleeps your async task for the exact required duration, and transparently retries the request for you.

You only need to manually handle `WareraRateLimitError` if the library exhausts its automatic retries (which defaults to 3 attempts).

### What's the difference between `User` and `UserLite`?

Many endpoints return a "Lite" version of a model to save bandwidth.
- `UserLite` contains basic info (name, avatar, level, citizenship). It is returned by paginated endpoints like `get_by_country()` or search endpoints.
- `User` contains the *complete* profile (stats, inventory, achievements, etc.). It is only returned when fetching a specific user by ID.

### My IDE is complaining about `Pydantic` imports or validation?

Make sure you have `pydantic >= 2.0.0` installed. This library relies heavily on Pydantic V2's Rust core for high-speed JSON parsing. It is not compatible with Pydantic V1.

### How do I fetch ALL of the users / battles / articles in the game?

Do **not** manually loop over pages. Instead, use the built-in `collect_all()` method available on supported resources. 

`collect_all()` uses time-sliced synthetic cursors to divide the timeline into chunks and fires hundreds of requests concurrently, fetching massive datasets in seconds. See the [Advanced Usage](Advanced-Usage) page for a guide!

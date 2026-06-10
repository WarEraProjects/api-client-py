"""
Warera client exception hierarchy.

All exceptions inherit from WareraError so callers can catch everything
with a single broad clause, or be selective with the subclasses.
"""

from __future__ import annotations

from typing import Any


class WareraError(Exception):
    """Base class for all warera-client errors."""


class WareraHTTPError(WareraError):
    """Raised when the API returns a non-2xx HTTP status."""

    def __init__(self, status_code: int, message: str, response_body: Any = None) -> None:
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(f"HTTP {status_code}: {message}")


class WareraUnauthorizedError(WareraHTTPError):
    """
    HTTP 401 — missing or invalid X-API-Key.

    ``api_key_configured`` tells you which case you are in:
      • False — the request was sent without any API key (none configured).
      • True  — a key was sent but the server rejected it.
      • None  — unknown (error not raised by the HTTP layer).
    """

    def __init__(
        self, response_body: Any = None, api_key_configured: bool | None = None
    ) -> None:
        self.api_key_configured = api_key_configured
        if api_key_configured is False:
            message = (
                "Unauthorized — this endpoint requires authentication and no API key "
                "is configured. Set the WARERA_API_KEY environment variable, pass "
                "api_key=... to WareraClient, or call warera.set_api_key()."
            )
        elif api_key_configured:
            message = (
                "Unauthorized — the configured API key was rejected by the server. "
                "Verify it is correct and still active "
                "(you can check with `await warera.validate_api_key()`)."
            )
        else:
            message = "Unauthorized — check your X-API-Key"
        super().__init__(401, message, response_body)


class WareraForbiddenError(WareraHTTPError):
    """HTTP 403 — authenticated but not allowed."""

    def __init__(self, response_body: Any = None) -> None:
        super().__init__(
            403,
            "Forbidden — your API key does not grant access to this resource. "
            "Some endpoints (e.g. work stats, action logs) only return data "
            "for the key owner's own account.",
            response_body,
        )


class WareraNotFoundError(WareraHTTPError):
    """HTTP 404 — resource does not exist."""

    def __init__(self, response_body: Any = None) -> None:
        super().__init__(404, "Not Found", response_body)


class WareraRateLimitError(WareraHTTPError):
    """
    HTTP 429 — rate limit exceeded.
    The client will auto-retry with backoff; this is raised only after
    all retries are exhausted.
    """

    def __init__(self, retry_after: float | None = None, response_body: Any = None) -> None:
        self.retry_after = retry_after
        super().__init__(429, "Rate limit exceeded", response_body)


class WareraServerError(WareraHTTPError):
    """HTTP 5xx — server-side error, retried automatically."""

    def __init__(self, status_code: int, response_body: Any = None) -> None:
        super().__init__(status_code, f"Server error ({status_code})", response_body)


class WareraValidationError(WareraError):
    """
    Raised when an API response cannot be parsed into the expected Pydantic model.
    `raw` contains the original parsed JSON for debugging.
    """

    def __init__(self, message: str, raw: Any = None) -> None:
        self.raw = raw
        super().__init__(message)


class WareraBatchError(WareraError):
    """
    Raised when one or more items in a batch request fail.
    Inspect `.errors` (dict of index → WareraError) and
    `.results` (dict of index → parsed data) separately.
    """

    def __init__(
        self,
        errors: dict[int, WareraError],
        results: dict[int, Any],
    ) -> None:
        self.errors = errors
        self.results = results
        failed = list(errors.keys())
        super().__init__(f"Batch request had {len(failed)} failure(s) at indices: {failed}")


def _raise_for_status(
    status_code: int, response_body: Any, *, api_key_configured: bool | None = None
) -> None:
    """Convert an HTTP status code into the appropriate WareraHTTPError."""
    if status_code == 401:
        raise WareraUnauthorizedError(response_body, api_key_configured=api_key_configured)
    if status_code == 403:
        raise WareraForbiddenError(response_body)
    if status_code == 404:
        raise WareraNotFoundError(response_body)
    if status_code == 429:
        raise WareraRateLimitError(response_body=response_body)
    if status_code >= 500:
        raise WareraServerError(status_code, response_body)
    if status_code >= 400:
        raise WareraHTTPError(status_code, "Client error", response_body)

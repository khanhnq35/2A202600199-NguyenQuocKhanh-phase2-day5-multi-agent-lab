"""Tracing hooks.

This file intentionally avoids binding to one provider. Students can plug in LangSmith,
Langfuse, OpenTelemetry, or simple JSON traces.
"""

from collections.abc import Iterator
from contextlib import contextmanager
from time import perf_counter
from typing import Any


@contextmanager
def trace_span(name: str, attributes: dict[str, Any] | None = None) -> Iterator[dict[str, Any]]:
    """Create a local timing span for agent and workflow observability.

    The span stores attributes and duration for JSON trace export.
    """

    started = perf_counter()
    span: dict[str, Any] = {"name": name, "attributes": attributes or {}, "duration_seconds": None}
    try:
        yield span
    finally:
        span["duration_seconds"] = perf_counter() - started

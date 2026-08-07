"""Keep the default test run network-free.

Tests that need the real device or service are marked ``live`` and skipped
unless ``--run-live`` is passed (or ``SDK_TEMPLATE_LIVE=1`` is exported), so
cloning the repository and running ``uv run pytest`` never depends on hardware
being reachable or on credentials existing. Real credentials and captures taken
from a real device must not be committed as fixtures either way — anything in
the repository is published with every release.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Iterable

    from _pytest.config import Config
    from _pytest.config.argparsing import Parser
    from _pytest.nodes import Item

_LIVE_MARKER = "live"
_LIVE_ENVIRONMENT_VARIABLE = "SDK_TEMPLATE_LIVE"


def pytest_addoption(parser: Parser) -> None:
    """Register the opt-in flag for the live suite."""
    parser.addoption(
        "--run-live",
        action="store_true",
        default=False,
        help="Run tests that talk to the real device or service.",
    )


def pytest_configure(config: Config) -> None:
    """Declare the marker so --strict-markers does not reject it."""
    config.addinivalue_line(
        "markers",
        f"{_LIVE_MARKER}: talks to the real device; needs --run-live.",
    )


def pytest_collection_modifyitems(config: Config, items: Iterable[Item]) -> None:
    """Skip the live suite unless it was explicitly opted into."""
    opted_in = (
        config.getoption("--run-live")
        or os.environ.get(_LIVE_ENVIRONMENT_VARIABLE) == "1"
    )
    if opted_in:
        return
    skip = pytest.mark.skip(reason="live test; pass --run-live to enable")
    for item in items:
        if _LIVE_MARKER in item.keywords:
            item.add_marker(skip)

"""Typed shape of the credentials persisted on the config entry."""

from __future__ import annotations

from typing import TypedDict


class IntegrationBlueprintConfigData(TypedDict):
    """Shape of the credentials persisted on the config entry."""

    username: str
    password: str

"""Typed shape of a jsonplaceholder post response."""

from __future__ import annotations

from typing import TypedDict


class IntegrationBlueprintPost(TypedDict):
    """Shape of a /posts/{id} response from jsonplaceholder."""

    userId: int
    id: int
    title: str
    body: str

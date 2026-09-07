# CLAUDE.md

Guidance for Claude Code (claude.ai/code) agents working in this repository.

## Always read `CODE_STYLE.md` first

Before creating, renaming or restructuring any file/class/function, **read [`CODE_STYLE.md`](./CODE_STYLE.md)**. It is the single source of truth for conventions: language, file organisation, naming, typing, properties vs `__init__`, imports, docstrings, comments, coordinator pattern, repairs/diagnostics layout, translations, lint workflow.

For user-facing topics (what's included, how to fork, rename steps, layout diagram, useful commands, CI list), see [`README.md`](./README.md).

This file deliberately avoids restating those rules — it only adds:

1. The verification workflow agents must run after every change.
2. The architectural reasoning that is not obvious from `CODE_STYLE.md` alone.
3. What "based on this blueprint" means for downstream repos.

## Template relationship

This repo is the scaffold other `ha-*` integration repos are created from via GitHub's "Use this template" button (see `README.md` → How to use). That copy is **one-time and one-directional**: once a repo is generated, it has its own `CLAUDE.md`/`CODE_STYLE.md`/CI and diverges immediately — there is no sync mechanism pulling blueprint changes into existing forks. A fix or convention change made here (e.g. a new `CODE_STYLE.md` rule, a CI job bump) only reaches already-forked repos if someone manually ports it over; treat this repo and its forks as independent once generated, not as a shared-source relationship.

## Verification workflow

**After every code change, always run lint then tests, in that order, before declaring the task done. Either run `scripts/lint` (a thin wrapper that only chains the four commands) or run them directly:**

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy custom_components/integration_blueprint
uv run pytest
```

- Lint runs `ruff format`, `ruff check` and `mypy` — all configured in `pyproject.toml`. Fix any failure and re-run before moving on.
- `pytest` enforces a **90 % coverage gate** (`--cov-fail-under` in `pyproject.toml`).

Both gates mirror CI (`.github/workflows/ci.yml`). Skip this only when the change literally cannot affect lint or tests (e.g., README-only edits).

## Bumping the Home Assistant version

The Home Assistant version is pinned in two places and **must be updated together**, otherwise CI, HACS and the test harness drift apart:

1. `pyproject.toml` `[dependency-groups] dev` — `homeassistant==<X.Y.Z>` (runtime/CI lint + mypy) **and** `pytest-homeassistant-custom-component==<matching release>` (the test harness ships its own pinned `homeassistant`; the two pins must come from the same HA release, otherwise lint and tests resolve different cores).
2. `hacs.json` — `"homeassistant": "<X.Y.Z>"` (minimum HA core enforced by HACS).

Verify the pairing on PyPI before committing: the `requires_dist` of `pytest-homeassistant-custom-component` must list the same `homeassistant==<X.Y.Z>` you pinned in `pyproject.toml`.

## Conventions not obvious from the code

The integration follows the HA `DataUpdateCoordinator` pattern; the module-by-module layout is in `README.md`. A few choices are not evident from reading a single file:

- State lives on `entry.runtime_data` (auto-discarded on unload), **never** on `hass.data`.
- `data/__init__.py` holds the `type` aliases (`IntegrationBlueprintConfigEntry`, `Json*`) **and** re-exports every symbol from the sibling modules, so downstream code imports everything from `.data`.
- Reauth is wired to fire when the coordinator raises `ConfigEntryAuthFailed`. Register Repairs issues (see the sample helper in `repairs.py`) from the coordinator/setup when you detect a recoverable problem; issue strings live under `issues.<issue_id>` in the translation files.

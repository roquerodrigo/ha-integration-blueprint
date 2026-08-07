# Home Assistant Integration Blueprint

[![CI](https://github.com/roquerodrigo/ha-integration-blueprint/actions/workflows/ci.yml/badge.svg)](https://github.com/roquerodrigo/ha-integration-blueprint/actions/workflows/ci.yml)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

[![Open your Home Assistant instance and open the repository inside HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=roquerodrigo&repository=ha-integration-blueprint&category=integration)

---

Template for creating custom [Home Assistant](https://www.home-assistant.io/) integrations distributable via [HACS](https://hacs.xyz/).

Based on [ludeeus/integration_blueprint](https://github.com/ludeeus/integration_blueprint), with adaptations used in the [@roquerodrigo](https://github.com/roquerodrigo) integrations. Conventions for contributors live in [`CODE_STYLE.md`](./CODE_STYLE.md); architectural notes for AI agents in [`CLAUDE.md`](./CLAUDE.md).

## What's included

- **Full integration scaffold** with `DataUpdateCoordinator`, config flow, options flow, sample sensor and typed `runtime_data`.
- **Reauth + reconfigure flows** triggered automatically by `ConfigEntryAuthFailed` or by the user.
- **Options flow** with a configurable `scan_interval` plumbed through to the coordinator.
- **Diagnostics platform** with credential redaction (`diagnostics.py`).
- **Repairs platform** (`repairs.py`) wired into HA's Issue Registry, with sample issue + `ConfirmRepairFlow`.
- **CI**: ruff lint + format, mypy type-check, `hassfest`, HACS validation, CodeQL security scan.
- **Pre-commit hooks** (`.pre-commit-config.yaml`) mirroring the lint gates plus file hygiene checks.
- **Coverage gate** at 90 % enforced by `pyproject.toml` (`--cov-fail-under`).
- **Scripts** (`scripts/setup`, `scripts/develop`) built on `uv` — create the `.venv` and start HA in debug with the integration loaded.
- **Tests** with `pytest-homeassistant-custom-component` covering init, config + reauth + reconfigure flows, options flow, coordinator, API client, base entity, sensor, diagnostics, repairs and translation parity.
- **Issue templates**, **PR template**, **`.editorconfig`** and grouped Dependabot updates.
- **Translations** for English and Brazilian Portuguese (with parity test).

## How to use

1. Use this repository as a **template** on GitHub ("Use this template" button) or clone it manually.
2. Rename the domain throughout the codebase:
   - `custom_components/integration_blueprint/` → `custom_components/<your_domain>/`
   - `DOMAIN = "integration_blueprint"` in `const.py`; `domain` in `manifest.json`; `name` in `hacs.json`
   - `name`, `documentation`, `issue_tracker`, `codeowners` in `manifest.json`
   - Rename classes: `IntegrationBlueprint*` → `<YourDomain>*`
   - Run `grep -rn integration_blueprint .` to catch leftover imports (especially in `tests/`)
3. Replace the sample API in `api.py` with your real client and adjust `coordinator.py`, `config_flow.py`, `sensor.py` to match.
4. Update `translations/en.json` and `translations/pt-BR.json` (parity is enforced by tests).
5. Replace the brand assets in `custom_components/integration_blueprint/brand/` — the blueprint ships **obvious `TODO` placeholders**, not usable artwork (see [`brand/README.md`](./custom_components/integration_blueprint/brand/README.md)). Swap `icon.png`, `icon@2x.png`, `icon.svg`, `logo.png` and `logo@2x.png` for your own, then register the integration in [`home-assistant/brands`](https://github.com/home-assistant/brands).
6. Update `README.md` and `CLAUDE.md` for your integration.

## Useful commands

```bash
scripts/setup                                              # create .venv and install deps (uv sync)
scripts/develop                                            # start Home Assistant in debug mode with the integration loaded
uv run ruff format --check .                               # check formatting
uv run ruff check .                                        # lint
uv run mypy custom_components/integration_blueprint        # type-check
uv run pytest                                              # run tests with the 90 % coverage gate
```

Both scripts run through `uv`, which manages `./.venv` automatically — no `source .venv/bin/activate` needed. For ad-hoc commands, prefix with `uv run` (e.g. `uv run pytest`, `uv run ruff …`).

HA runs with config in `config/` and `PYTHONPATH` pointing at `custom_components/` — no symlinks. To recreate entity/device IDs during development:

```bash
rm config/.storage/core.entity_registry config/.storage/core.device_registry
```

## Layout

```
custom_components/integration_blueprint/
├── __init__.py        # async_setup_entry / unload / reload
├── api.py             # ApiClient (single class)
├── brand/             # brand assets — obvious TODO placeholders, replace per fork
│   ├── README.md      # what to add when forking
│   ├── icon.png       # square symbol (+ icon@2x.png)
│   ├── icon.svg       # vector version of the square icon
│   └── logo.png       # landscape wordmark (+ logo@2x.png)
├── config_flow.py     # user / reauth / reconfigure steps
├── const.py           # DOMAIN, LOGGER, URLs, ATTRIBUTION, scan-interval defaults
├── coordinator.py     # DataUpdateCoordinator (interval injected from options)
├── data/              # one TypedDict/dataclass per file; type aliases in __init__.py
│   ├── __init__.py    # type aliases (ConfigEntry, Json*) + re-exports
│   ├── config_data.py
│   ├── diagnostics_entry.py
│   ├── diagnostics_payload.py
│   ├── options_data.py
│   ├── post.py
│   └── runtime.py     # IntegrationBlueprintData dataclass
├── diagnostics.py     # downloadable diagnostics with credential redaction
├── entity.py          # base CoordinatorEntity
├── exceptions/        # one file per exception class
│   ├── __init__.py
│   ├── api_client_authentication_error.py
│   ├── api_client_communication_error.py
│   └── api_client_error.py
├── icons.json         # entity icons keyed by translation_key
├── manifest.json
├── options_flow.py    # OptionsFlow with scan_interval
├── repairs.py         # Repair platform: async_create_fix_flow + sample issue
├── sensor.py          # sample platform
└── translations/
    ├── en.json
    └── pt-BR.json
```

Layout convention (one top-level class per file; related classes grouped under a directory) is documented in [`CODE_STYLE.md`](./CODE_STYLE.md).

## Pre-commit hooks

Install once per clone (after `scripts/setup`):

```bash
pre-commit install
```

This wires ruff + basic file hygiene checks (`.pre-commit-config.yaml`) into every commit, mirroring the CI lint job.

## CI

All workflows call the reusable workflows in [`roquerodrigo/workflows`](https://github.com/roquerodrigo/workflows):

- **`ci.yml`** — ruff (check + format) + mypy, pytest with the coverage gate, and `hassfest` + HACS validation; push/PR to `main`
- **`codeql.yml`** — GitHub CodeQL security scan; push/PR to `main` and a weekly cron
- **`release.yml`** — release-please, gated on a green CI run on `main`
- **`auto-assign.yml`** — assigns new issues/PRs to the code owner

## Companion SDK

Integrations that wrap a device or cloud protocol keep that code in a separate
package, released to PyPI and pinned from `manifest.json`. [`sdk-template/`](./sdk-template)
scaffolds that repository — `src/` layout, `py.typed`, hatchling build,
network-free tests with an opt-in live suite, and the release-to-PyPI workflow.
Copy its contents into the SDK's own repository; it is not part of the
integration, so delete the directory in a fork that does not need one.

## License

[MIT](LICENSE)

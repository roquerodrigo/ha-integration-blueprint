# Integration Blueprint

<!-- ha-marketplace:exclude-start -->
[![CI](https://github.com/roquerodrigo/ha-integration-blueprint/actions/workflows/ci.yml/badge.svg)](https://github.com/roquerodrigo/ha-integration-blueprint/actions/workflows/ci.yml)
[![GitHub release](https://img.shields.io/github/v/release/roquerodrigo/ha-integration-blueprint)](https://github.com/roquerodrigo/ha-integration-blueprint/releases/latest)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-db61a2?logo=githubsponsors&logoColor=white)](https://github.com/sponsors/roquerodrigo)

[![Open your Home Assistant instance and open a repository in the Marketplace.](https://my.home-assistant.io/badges/marketplace_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=roquerodrigo&repository=ha-integration-blueprint&category=integration)
<!-- ha-marketplace:exclude-end -->

Start a new Home Assistant custom integration from one that already works.
This template is a small, complete integration that polls a sample web API
with a user name and password. It comes with tests, strict type checking, CI,
Marketplace validation and an automated release flow, so your new repository
starts with every check green and only the code for your device or service
left to write. A second template for the companion Python SDK lives in
[`sdk-template/`](sdk-template/README.md).

It started from
[ludeeus/integration_blueprint](https://github.com/ludeeus/integration_blueprint)
and is now the base of the integrations published by
[roquerodrigo](https://github.com/roquerodrigo).

## Features

- A setup form that checks the user name and password against the service
  before saving, and refuses to add the same account twice.
- Reauthentication: when the service rejects the saved credentials, Home
  Assistant asks the user for new ones and reloads the integration.
  **Reconfigure** lets the user change them at any time. Both refuse a
  different account.
- An options form with the polling interval, 300 seconds by default and at
  least 30. Saving it reloads the integration with the new interval.
- Short outages do not turn entities unavailable. When the service fails, the
  last values stay in place for up to five minutes before the entities go
  unavailable. A rejected password still asks for reauthentication at once.
- A diagnostics download with the user name and password removed.
- A Repairs issue with a **Fix** button, ready to copy for problems the user
  can solve.
- Devices the account no longer provides can be deleted from the device page.
- Errors from the API client have URL query strings removed before they
  reach the log, so an API key or session id in a request URL does not leak.
- Strict typing: mypy rejects untyped functions and `Any`, and every payload
  has its own `TypedDict`. Ruff runs with every rule enabled.
- Tests with `pytest-homeassistant-custom-component` for every module, and a
  coverage gate at 90 %. Further tests check that every locale has the same
  keys and that every icon belongs to a translated entity.
- English and Brazilian Portuguese translations.
- Placeholder brand images that are impossible to mistake for real artwork.
- CI on every pull request: lint, type check, tests, Home Assistant
  Marketplace validation and a CodeQL scan. Pull request branches are rebased
  onto `main` when they fall behind, and new issues and pull requests are
  assigned to the maintainer.
- Automated releases: after every green CI run on `main`, a release pull
  request collects the changes, with the next version and release notes
  written from the commit messages. Merging it tags the release and attaches
  the integration zip that HACS and the Marketplace install.
- Weekly grouped Dependabot updates for Python packages and GitHub Actions.
  Home Assistant and its test harness are left out, because they move
  together by hand.

## Requirements

- Python 3.14.2 or newer and [uv](https://docs.astral.sh/uv/).
- Home Assistant 2026.7.2 or newer, the version pinned in `hacs.json` and in
  the development dependencies.
- For the release flow, two repository secrets: `RELEASE_TOKEN`, a token with
  write access to contents and pull requests (so the release pull request it
  opens runs CI), and `ANTHROPIC_API_KEY`, used to write the release notes.

## Starting a new integration

1. Select **Use this template** on GitHub and create your repository.
2. Rename the sample everywhere. Replace these four forms in every file of
   the repository, then rename the `custom_components/integration_blueprint/`
   directory to match:

   | Replace                    | With                    | Example       |
   |----------------------------|-------------------------|---------------|
   | `integration_blueprint`    | your domain             | `my_device`   |
   | `IntegrationBlueprint`     | your class prefix       | `MyDevice`    |
   | `Integration Blueprint`    | the product name        | `My Device`   |
   | `ha-integration-blueprint` | your repository name    | `ha-my-device`|

   Run `git grep -niE 'integration.?blueprint'` afterwards to catch what is
   left, such as the zip name in `hacs.json`, the `--cov` target in
   `pyproject.toml`, `scripts/lint` and the IDE files in `.idea/` (delete
   that directory if you do not use it).
3. Reset the release history: empty `CHANGELOG.md` down to its heading and set
   `version` to `0.1.0` in `manifest.json` and `pyproject.toml`. A repository
   with no tags gets `1.0.0` as its first release, so add a
   `.release-autopilot.yml` with `initial_version: 0.1.0` to start below 1.0.
4. Fill in `manifest.json`: `codeowners`, `documentation`, `issue_tracker`,
   `iot_class` and `integration_type` (`device` for one physical device,
   `hub` for a gateway with several, `service` for an account on a cloud
   service).
5. Add `"country": ["BR"]` (or your country codes) to `hacs.json` only when
   the device or service exists in specific countries. Users who filter HACS
   by another country stop seeing the repository. With `country` set, every
   piece of prose in the repository is written in that country's language,
   as described under "Language" in [CODE_STYLE.md](CODE_STYLE.md).
6. Replace the sample client in `api.py` with your own, or with your SDK pinned
   exactly in the `requirements` of `manifest.json`. Then adapt
   `coordinator.py`, `config_flow.py`, `sensor.py` and the payload types in
   `data/`.
7. Delete what your integration does not use, together with its tests:
   `repairs.py` if it raises no issues, the reauthentication and reconfigure
   steps if it has no credentials, and `sdk-template/` with
   `tests/test_sdk_template.py`.
8. Update `translations/en.json` and `translations/pt-BR.json` together. The
   tests fail when their keys differ.
9. Replace every image in `brand/` with the real brand of the device or
   service, as listed in
   [brand/README.md](custom_components/integration_blueprint/brand/README.md).
10. Write the README for the people who will use the integration, following
    the [README standard](docs/readme-standard.md). Rewrite `CLAUDE.md` and
    `CODE_STYLE.md` wherever they describe behaviour you removed.
11. Add the `RELEASE_TOKEN` and `ANTHROPIC_API_KEY` secrets, then run
    `scripts/setup` and `scripts/lint`. Everything must pass before the
    first commit.

The template and the repositories made from it are independent after the
copy. A later change here does not reach an existing integration unless
someone ports it by hand.

## Project layout

Inside `custom_components/integration_blueprint/`:

| Path                          | Holds                                                           |
|-------------------------------|-----------------------------------------------------------------|
| `__init__.py`                 | Setup, unload, reload and device removal                        |
| `api.py`                      | The sample API client, to replace                               |
| `coordinator.py`              | Polling, error handling and the five minute grace period        |
| `config_flow.py`              | Setup, reauthentication and reconfigure forms                   |
| `options_flow.py`             | The polling interval option                                     |
| `entity.py`, `sensor.py`      | The base entity and the sample **Title** sensor                 |
| `diagnostics.py`              | The diagnostics download and the keys it redacts                |
| `repairs.py`                  | The sample Repairs issue and its fix flow                       |
| `data/`                       | One `TypedDict` or dataclass per file, type aliases in `__init__.py` |
| `exceptions/`                 | One exception class per file                                    |
| `icons.json`, `translations/` | Entity icons, English and Portuguese strings                    |
| `brand/`                      | Placeholder icon and logo images                                |

At the repository root:

| Path            | Holds                                     |
|-----------------|-------------------------------------------|
| `tests/`        | One test module per production module     |
| `scripts/`      | `setup`, `develop` and `lint`             |
| `config/`       | The Home Assistant configuration used by `scripts/develop` |
| `docs/`         | The README standard for new integrations  |
| `sdk-template/` | The companion SDK template                |

The conventions behind this layout are in [CODE_STYLE.md](CODE_STYLE.md), and
the development commands are in [CONTRIBUTING.md](CONTRIBUTING.md).

## Companion SDK

An integration that wraps a device or cloud protocol keeps that code in a
separate Python package, released to PyPI and pinned from `manifest.json`.
[`sdk-template/`](sdk-template/README.md) starts that repository: `src`
layout, type information shipped with the package, tests that run without the
network, an opt-in suite against the real device and a release flow that
publishes to PyPI. Copy its contents into the SDK's own repository.

## Support

This template is built and maintained on personal time. If it is useful to
you, consider [sponsoring the work](https://github.com/sponsors/roquerodrigo).
It keeps the fixes, the testing and the releases coming.

Bugs and requests go to the
[issue tracker](https://github.com/roquerodrigo/ha-integration-blueprint/issues).

<!-- ha-marketplace:exclude-start -->
## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development setup and
workflow, and [CODE_STYLE.md](CODE_STYLE.md) for the code conventions.

## License

[MIT](LICENSE)
<!-- ha-marketplace:exclude-end -->

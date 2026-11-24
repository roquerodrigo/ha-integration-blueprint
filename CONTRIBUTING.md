# Contributing

Bug reports, ideas and pull requests are welcome. A change here reaches new
integrations made from the template. Integrations that already exist do not
pick it up.

## Reporting a bug

Open an [issue](https://github.com/roquerodrigo/ha-integration-blueprint/issues/new/choose)
with:

- the Home Assistant version and the template version;
- what you did, what you expected and what happened;
- the relevant log lines and, if the sample integration was running, its
  diagnostics (the user name and password are redacted).

## Development setup

The project uses [uv](https://docs.astral.sh/uv/), which manages `.venv` on
its own. Prefix ad hoc commands with `uv run`.

```bash
scripts/setup      # install the dependencies into .venv
scripts/develop    # run Home Assistant at http://localhost:8123 with this integration loaded
```

`scripts/develop` uses the configuration in [`config/`](config/), with debug
logging for the integration. It loads the integration straight from
`custom_components/`, so there is nothing to link or copy. To start again with
new entity and device ids, delete `config/.storage/core.entity_registry` and
`config/.storage/core.device_registry`.

## Checks

Run these before opening a pull request. CI runs the same ones, and
`scripts/lint` runs all four in this order.

```bash
uv run ruff format --check .                          # formatting
uv run ruff check .                                   # lint
uv run mypy custom_components/integration_blueprint   # type check
uv run pytest                                         # tests, coverage must stay at 90 % or more
```

`pre-commit install` adds a hook that formats, lints and type checks every
commit with the same tool versions, along with basic file checks.

Read [CODE_STYLE.md](CODE_STYLE.md) before adding or restructuring code.

## Updating Home Assistant

Home Assistant is pinned three times, and the three move together:
`homeassistant` and `pytest-homeassistant-custom-component` in
`pyproject.toml`, and `homeassistant` in `hacs.json`. Pick the harness release
that pins the same Home Assistant version. Dependabot leaves both packages
alone for this reason.

## Pull requests

1. Fork the repository and branch from `main`.
2. Write commit messages as [Conventional Commits](https://www.conventionalcommits.org/).
   Releases and their notes are generated from them. Mark breaking changes
   with `!` or a `BREAKING CHANGE:` footer.
3. Update `translations/en.json` and `translations/pt-BR.json` together when
   you change user-facing strings.
4. Update the README when what the template provides or how to start from it
   changes, and [docs/readme-standard.md](docs/readme-standard.md) when the
   README rules change.
5. Fill in the pull request template.

## License

Contributions are released under the project's [MIT License](LICENSE).

# Companion SDK template

Scaffold for the **standalone Python package** that wraps a device or cloud API
and is consumed by a Home Assistant integration through the `requirements` key
of its `manifest.json`. It is not part of the integration and never ships to
Home Assistant.

The SDK lives in its own repository, releases to PyPI, and knows nothing about
Home Assistant: entities, coordinators and config-entry plumbing stay on the
integration side. Keeping the two apart is what lets the protocol work be
tested, versioned and released without an HA test harness.

## Using it

1. Create the SDK repository and copy the **contents** of this directory into
   its root (including the dotfiles: `.github/`, `.gitignore`,
   `.pre-commit-config.yaml`).
2. Rename the placeholders:
   - directory `src/sdk_template/` → `src/<your_package>/`
   - `name` in `pyproject.toml`, `[tool.hatch.build.targets.wheel] packages`,
     the `--cov` target and the `package` input of the publish job in
     `.github/workflows/release.yml`
   - class prefix `SdkTemplate*` → `<YourPackage>*`
   - `grep -rn sdk_template .` and `grep -rn sdk-template .` catch the rest
3. Replace `client.py` with the real client and its tests.
4. Add the repository secrets the release flow needs: `RELEASE_TOKEN` (a token
   with contents and pull-requests write access, so the release pull request it
   opens runs CI), `ANTHROPIC_API_KEY` (for the release notes) and
   `PYPI_API_TOKEN`.

In a fork of the integration blueprint this whole directory is dead weight —
delete it.

## What it settles

- **`src/` layout.** The package is importable only after an (editable)
  install, which keeps the test suite honest about what actually gets packaged.
- **`py.typed`.** Ships the type information; without it every consumer sees
  `Any`. It is force-included in the wheel because hatchling does not pick up
  non-Python files on its own.
- **Runtime dependencies are never pinned and never capped.** Home Assistant
  pins its own transitive dependencies exactly, so an SDK that pins — or caps —
  a library HA also ships will eventually contradict HA's pin and the
  integration fails to install. Use a `>=` floor only. Exact pins belong in the
  dependency groups and the lock file, which never reach the consumer. The
  integration side is the mirror image: its `manifest.json` pins the SDK
  exactly, so what runs inside HA only ever moves through a bump pull request.
- **`mypy strict`.** An SDK owns its entire type surface; there is no framework
  boundary to relax for, unlike the integration.
- **Network-free tests by default.** The live-hardware suite is opt-in through
  `--run-live` (or `SDK_TEMPLATE_LIVE=1`), so cloning and running `pytest`
  never depends on the device being reachable — and never depends on real
  credentials, which must not be committed as fixtures either way.
- **Release flow.** After a green CI run on `main`,
  [Release Autopilot](https://github.com/marketplace/actions/release-autopilot)
  keeps a release pull request up to date: it picks the next version from the
  conventional commits, writes it into `project.version` in `pyproject.toml`
  and into `uv.lock`, and writes the release notes and `CHANGELOG.md`. Merging
  that pull request tags `vX.Y.Z` and creates the GitHub release, and the
  shared `publish-pypi` reusable then publishes the tag to PyPI. The version
  files are detected on their own; `.release-autopilot.yml` only sets
  `initial_version`, so the first release is `0.1.0` rather than `1.0.0`. Running the workflow by hand with a `tag` republishes an
  existing tag to PyPI.

## Releasing a fix that has to reach Home Assistant

1. Pull request on the SDK (fix plus tests), merged; merging the release pull
   request kept by Release Autopilot tags the release and it publishes to PyPI.
2. Bump pull request on the integration: the `==` pin in `manifest.json` and
   the matching pin in the integration's dev dependency group, plus whatever
   code the new version needs.
3. Merge the bump; the integration's own release follows.

Before merging the SDK release, validate the change against a locally built
wheel (`uv build`, then install the artefact into the environment that runs the
integration) — the first real execution of a change should never be the
published version.

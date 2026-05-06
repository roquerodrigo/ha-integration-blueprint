# Code Style Guide

Style conventions for the `ha-integration-blueprint` project. Run `scripts/lint`
before committing — it executes `ruff format`, `ruff check --fix` and `mypy`,
and must exit cleanly. `pytest` (with the 95 % coverage gate) follows.

**Always read this file before adding or restructuring code.**

## Language

- All code is written in **English**: file names, class names, function names,
  variable names, dictionary keys, identifier strings.
- The conversation language with the user can be Portuguese or anything else;
  what is committed to disk stays English.
- User-facing strings live in `custom_components/integration_blueprint/translations/{en,pt-BR}.json`
  only — do not hardcode them in Python.

## File organization

- **One top-level class per file.** Multiple semantically related classes (e.g.
  exception families) get grouped into a package directory with one class per
  submodule and an `__init__.py` re-exporting the public symbols.
  - Example: `exceptions/` contains `api_client_error.py`,
    `api_client_communication_error.py`,
    `api_client_authentication_error.py`, plus `__init__.py`.
- **TypedDicts and `type` aliases do not count as "classes"** for this rule —
  they live alongside related code (typically in `data.py`) and do not need
  their own file.
- **Helper functions** may live in the same file as the single class that uses
  them (e.g. `_verify_response_or_raise` in `api.py`).
- **`__init__.py` of the integration package** wires `async_setup_entry`,
  `async_unload_entry`, `async_reload_entry` and nothing else.

## Naming

- Public classes are prefixed with `IntegrationBlueprint` (rename to
  `<YourDomain>` when forking).
- Concrete platform entities end with the entity type: `IntegrationBlueprintSensor`.
- Exception classes end with `Error`: `IntegrationBlueprintApiClientError`,
  `…CommunicationError`, `…AuthenticationError`.
- Private attributes / functions are prefixed with `_`.

## Typing

**Strict typing. No generics, no `Any`.** Mypy on `scripts/lint` enforces this.

Banned: `typing.Any`, `object` as a value type, bare `dict` / `list` / `tuple` /
`set`, `dict[str, Any]`, `Mapping[str, Any]`.

Required:

- `TypedDict` for known dict / JSON shapes (see `data.py` for the canonical
  examples: `IntegrationBlueprintPost`, `IntegrationBlueprintConfigData`,
  `IntegrationBlueprintOptionsData`, `IntegrationBlueprintDiagnosticsPayload`).
- `@dataclass` for structured records (`IntegrationBlueprintData`).
- Named `type` aliases for recursive / shared shapes — `JsonPrimitive`,
  `JsonValue`, `JsonObject` in `data.py`.
- `frozenset[str]` / `tuple[str, ...]` for fixed string collections.
- `cast("TypedDictName", value)` at HA framework boundaries that hand us a
  permissive type (e.g. `entry.data` is `MappingProxyType[str, Any]`).

When narrowing an HA-provided callback signature (e.g. `async_step_user`),
mypy reports `[override]` (Liskov violation). Add `# type: ignore[override]`
with a one-line comment explaining the deliberate narrowing — see
`config_flow.py` for the canonical example.

## Properties and `__init__`

- **Always prefer `@property`** over assigning `_attr_*` values in `__init__`.
  Properties are computed lazily from backing fields stored on the parent class
  (e.g. `self.coordinator`, `self.entity_description`).
- When the body of `__init__` would only call `super().__init__(...)`, omit
  `__init__` entirely and let Python inherit the parent.
- Class-level constants like `_attr_attribution = ATTRIBUTION` and
  `_attr_has_entity_name = True` are fine — they don't depend on instance
  state.

## Imports

- Always start every module with `from __future__ import annotations` so type
  hints become lazy strings and the runtime cost of `if TYPE_CHECKING` imports
  is zero.
- Same-package relative imports (`from .module import …`) are the default.
- Move type-only imports into a `TYPE_CHECKING` block (Ruff `TC001`/`TC003`):

  ```python
  from __future__ import annotations
  from typing import TYPE_CHECKING

  if TYPE_CHECKING:
      from collections.abc import Mapping
      from .data import IntegrationBlueprintConfigData
  ```

- `noqa` comments are reserved for unavoidable framework constraints (e.g.
  `# noqa: ARG001` for HA-framework callback parameters that must exist but go
  unused). Document the reason inline if non-obvious. Never silence to "make
  ruff happy" — fix the underlying code.

## Docstrings

- Every public class, function, method (including `@property`) and `__init__`
  has a docstring. Ruff enforces this via `D102`/`D107`.
- A single sentence is usually enough. Describe the *contract* or the *why*,
  not the obvious implementation.
- Module-level docstring at the top of every `.py` file.
- Avoid restating the type — the signature already does that.

## Comments

- Default to **no comments**. Add one only when the *why* is not obvious from
  the code: a hidden constraint, a workaround, a subtle invariant, or a
  deliberate type-system override.
- Never describe *what* the code does — well-named identifiers handle that.
- **No section dividers** like `# --- API payloads ---` to group related
  declarations. If a file has so many sections that you feel the need for
  visual separators, split it into multiple files instead.

## Coordinator and runtime data

- All API state flows through `entry.runtime_data: IntegrationBlueprintData`
  (`data.py`). Never store integration state in `hass.data`.
- The coordinator is typed as `DataUpdateCoordinator[IntegrationBlueprintPost]`
  (or whatever your real payload TypedDict is). `_async_update_data` returns
  the typed payload; client errors map to `UpdateFailed`,
  authentication errors to `ConfigEntryAuthFailed` (which triggers reauth).

## Config / options / repairs / diagnostics

- `config_flow.py` carries `user`, `reauth`, `reauth_confirm` and `reconfigure`
  steps, all sharing one `_validate` helper and one `_credentials_schema`
  builder.
- `options_flow.py` holds the single `IntegrationBlueprintOptionsFlow`
  class. New options keys go into the `IntegrationBlueprintOptionsData`
  TypedDict in `data.py`.
- `repairs.py` exposes `async_create_fix_flow`. Sample helpers like
  `async_raise_deprecated_api_issue` show how to register issues from anywhere
  in the integration.
- `diagnostics.py` returns `IntegrationBlueprintDiagnosticsPayload`. Sensitive
  keys go into the `TO_REDACT: frozenset[str]` constant.

## Translations

- Two locales: `en.json` and `pt-BR.json`. `tests/test_translations.py`
  parametrizes over every locale and fails if their nested key sets diverge.
- Issue strings live under `issues.<issue_id>`; options strings under
  `options.step.init.data`; flow strings under `config.step.<step_id>`.

## Linting and verification

- Ruff configuration lives in `.ruff.toml` with `select = ["ALL"]`.
- Mypy configuration lives in `mypy.ini`. Both run from `scripts/lint`.
- After every change run `scripts/lint && pytest`. Both gates mirror CI
  (`.github/workflows/lint.yml`).
- Tests live in `tests/`, mirroring the production layout. The 95 % coverage
  gate (`pytest.ini`) prevents untested code from sneaking in. When a test
  exercises a state that is impossible under the new types, update or remove
  it — never weaken the type to satisfy the test.

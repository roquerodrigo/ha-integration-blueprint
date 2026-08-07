from __future__ import annotations

import json
from pathlib import Path

COMPONENT_DIR = (
    Path(__file__).parent.parent / "custom_components" / "integration_blueprint"
)


def _entity_keys(section: dict) -> set[tuple[str, str]]:
    return {(platform, key) for platform, block in section.items() for key in block}


def _icons() -> dict:
    return json.loads((COMPONENT_DIR / "icons.json").read_text(encoding="utf-8"))


def test_icons_file_exists():
    assert (COMPONENT_DIR / "icons.json").exists()


def test_icon_entity_keys_are_translated():
    translations = json.loads(
        (COMPONENT_DIR / "translations" / "en.json").read_text(encoding="utf-8"),
    )
    orphans = _entity_keys(_icons()["entity"]) - _entity_keys(translations["entity"])
    assert not orphans, f"icons.json styles entities en.json does not know: {orphans}"


def test_icon_values_use_mdi_prefix():
    for platform, block in _icons()["entity"].items():
        for key, icons in block.items():
            assert icons["default"].startswith("mdi:"), (platform, key)

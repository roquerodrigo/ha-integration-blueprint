from __future__ import annotations

import tomllib
from pathlib import Path

import pytest
import yaml

SDK_TEMPLATE = Path(__file__).parent.parent / "sdk-template"
PYPROJECT = tomllib.loads((SDK_TEMPLATE / "pyproject.toml").read_text())
RELEASE_WORKFLOW = yaml.safe_load(
    (SDK_TEMPLATE / ".github" / "workflows" / "release.yml").read_text()
)


def test_template_ships_a_license():
    assert (SDK_TEMPLATE / "LICENSE").read_text().startswith("MIT License")


def test_template_uses_the_hatchling_build_backend():
    assert PYPROJECT["build-system"]["build-backend"] == "hatchling.build"


def test_template_uses_the_src_layout():
    packages = PYPROJECT["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"]
    assert packages == ["src/sdk_template"]
    assert (SDK_TEMPLATE / "src" / "sdk_template" / "__init__.py").is_file()


def test_template_ships_the_typing_marker():
    marker = SDK_TEMPLATE / "src" / "sdk_template" / "py.typed"
    assert marker.is_file()
    force_include = PYPROJECT["tool"]["hatch"]["build"]["targets"]["wheel"][
        "force-include"
    ]
    assert force_include["src/sdk_template/py.typed"] == "sdk_template/py.typed"


@pytest.mark.parametrize("requirement", PYPROJECT["project"]["dependencies"])
def test_runtime_dependencies_are_neither_pinned_nor_capped(requirement):
    """
    Runtime pins and upper bounds break the consuming integration.

    Home Assistant pins its own transitive dependencies exactly, so an SDK that
    contradicts one of those pins simply fails to install inside HA. Exact
    versions belong in the dependency groups and the lock file.
    """
    assert "==" not in requirement
    assert "<" not in requirement


def test_template_release_is_cut_by_release_autopilot():
    release_job = RELEASE_WORKFLOW["jobs"]["release"]
    release_step = next(
        step for step in release_job["steps"] if step.get("id") == "release"
    )
    assert release_step["uses"] == "roquerodrigo/release-autopilot@latest"
    assert release_step["with"] == {
        "token": "${{ secrets.RELEASE_TOKEN }}",
        "anthropic-api-key": "${{ secrets.ANTHROPIC_API_KEY }}",
    }
    assert release_job["outputs"] == {
        "released": "${{ steps.release.outputs.released }}",
        "tag": "${{ steps.release.outputs.tag }}",
    }
    assert release_job["permissions"] == {
        "contents": "write",
        "pull-requests": "write",
    }
    assert RELEASE_WORKFLOW["concurrency"] == {
        "group": "release",
        "cancel-in-progress": False,
    }


def test_template_release_publishes_the_released_tag_to_pypi():
    publish_job = RELEASE_WORKFLOW["jobs"]["publish"]
    assert publish_job["needs"] == "release"
    assert publish_job["uses"].endswith("/publish-pypi.yml@main")
    assert "needs.release.outputs.released == 'true'" in publish_job["if"]
    assert "needs.release.outputs.tag" in publish_job["with"]["ref"]
    assert publish_job["with"]["package"] == PYPROJECT["project"]["name"]


@pytest.mark.parametrize(
    "leftover", ["release-please-config.json", ".release-please-manifest.json"]
)
def test_template_carries_no_release_please_configuration(leftover):
    assert not (SDK_TEMPLATE / leftover).exists()


def test_template_test_suite_is_network_free_by_default():
    conftest = (SDK_TEMPLATE / "tests" / "conftest.py").read_text()
    assert "--run-live" in conftest

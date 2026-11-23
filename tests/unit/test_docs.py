"""Tests for the documentation generation helpers in ``tasks.docs``."""

import pytest

from tasks.docs import _escape_mdx_braces, _escape_mdx_structure


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        pytest.param("no braces here", "no braces here", id="untouched"),
        pytest.param(
            "e.g. 'Ethernet{module}/1'.",
            "e.g. 'Ethernet\\{module\\}/1'.",
            id="bare-braces-escaped",
        ),
        pytest.param(
            "e.g. `Ethernet{module}/1`.",
            "e.g. `Ethernet{module}/1`.",
            id="inline-code-left-alone",
        ),
        pytest.param(
            "{a} then `{b}` then {c}",
            "\\{a\\} then `{b}` then \\{c\\}",
            id="mixed-inside-and-outside",
        ),
        pytest.param(
            "``a ` b {c}``",
            "``a ` b {c}``",
            id="double-backtick-span-with-embedded-backtick",
        ),
        pytest.param(
            "{{ device__name__value }}",
            "\\{\\{ device__name__value \\}\\}",
            id="jinja-style-double-braces",
        ),
        pytest.param(
            "unterminated `code {x}",
            "unterminated `code \\{x\\}",
            id="unclosed-span-still-escaped",
        ),
    ],
)
def test_escape_mdx_braces(text: str, expected: str) -> None:
    assert _escape_mdx_braces(text) == expected


@pytest.mark.parametrize("value", [None, 42, True])
def test_escape_mdx_braces_passes_through_non_strings(value: object) -> None:
    assert _escape_mdx_braces(value) is value  # type: ignore[arg-type]


def test_escape_mdx_structure_walks_nested_containers() -> None:
    payload = {
        "description": "a {token}",
        "nodes": [
            {"name": "Node", "attributes": [{"description": "b {token}"}]},
            {"name": "Safe", "attributes": [{"description": "c `{token}`"}]},
        ],
        "optional": True,
        "order_weight": 1000,
    }

    result = _escape_mdx_structure(payload)

    assert result["description"] == "a \\{token\\}"
    assert result["nodes"][0]["attributes"][0]["description"] == "b \\{token\\}"
    # Inline code spans survive the walk unchanged.
    assert result["nodes"][1]["attributes"][0]["description"] == "c `{token}`"
    # Non-string scalars are preserved, not stringified.
    assert result["optional"] is True
    assert result["order_weight"] == 1000


def test_escape_mdx_structure_does_not_mutate_input() -> None:
    payload = {"description": "a {token}"}

    _escape_mdx_structure(payload)

    assert payload["description"] == "a {token}"

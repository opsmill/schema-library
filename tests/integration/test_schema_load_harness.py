"""Exercise the schema-load harness without starting Docker."""

import subprocess
from unittest.mock import Mock

import pytest

from .test_schema_load import TestSchemaLoad as SchemaLoadCase


def test_failed_convergence_is_not_hidden_by_a_noop_reload() -> None:
    case = SchemaLoadCase()
    case.failed = set()
    ctl = Mock(
        side_effect=[
            subprocess.CompletedProcess(
                args="load",
                returncode=1,
                stdout="schema 'base' loaded successfully",
                stderr="Schema is still not in sync",
            ),
            subprocess.CompletedProcess(
                args="load",
                returncode=0,
                stdout="The schema in Infrahub was already up to date",
                stderr="",
            ),
        ]
    )

    with pytest.raises(AssertionError, match="Schema is still not in sync"):
        case.test_load(ctl, "base")

    ctl.assert_called_once()
    assert "--wait 60" in ctl.call_args.args[0]
    assert "base" in case.failed

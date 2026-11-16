"""Load every non-experimental schema into one Infrahub instance, in dependency order."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

import pytest
import yaml

from tasks.schemas import METADATA_FILE, load_order

from .conftest import TestSchemaLibrary

# The `infrahubctl` installed next to the running interpreter, whatever the PATH holds.
INFRAHUBCTL = Path(sys.executable).parent / "infrahubctl"
LOADED_MARKER = "loaded successfully"
WAIT_RETRIES = 2
ORDER = load_order()
METADATA = yaml.safe_load(METADATA_FILE.read_text(encoding="utf-8"))


def _dependencies(path: str) -> list[str]:
    """Return the schema paths this entry depends on, as listed in `.metadata.yml`."""
    return list(METADATA.get(path, {}).get("dependencies", []))


class TestSchemaLoad(TestSchemaLibrary):
    # Paths whose load failed, so that entries depending on them are skipped
    # instead of reporting a second failure with the same root cause.
    failed: set[str] = set()

    @pytest.mark.parametrize("path", ORDER, ids=ORDER)
    def test_load(self, ctl: Callable, path: str) -> None:
        broken = [
            dependency
            for dependency in _dependencies(path)
            if dependency in self.failed
        ]
        if broken:
            pytest.skip(f"Dependency failed to load: {', '.join(broken)}")

        command = f"{INFRAHUBCTL} schema load {path} --wait 60"
        result = ctl(command)
        # The schema is stored before `--wait` polls the instance. When that poll fails, for example on a
        # cache timeout inside Infrahub, the command exits 1 although the load succeeded. Loading the same
        # schema again changes nothing, so retry that case instead of reporting a failed load.
        for _ in range(WAIT_RETRIES):
            if result.returncode == 0 or LOADED_MARKER not in result.stdout:
                break
            result = ctl(command)
        if result.returncode != 0:
            self.failed.add(path)
        assert result.returncode == 0, (
            f"`infrahubctl schema load {path}` exited with {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

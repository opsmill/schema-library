"""Fixtures for the tests that run against a real Infrahub instance in Docker."""

# Without the `integration` dependency group a plain `pytest` run skips this directory
# instead of failing at collection.
import pytest

pytest.importorskip("infrahub_testcontainers")

# pylint: disable=wrong-import-position
import subprocess  # noqa: E402

from infrahub_testcontainers.helpers import TestInfrahubDocker  # type: ignore[import-untyped]  # noqa: E402


class TestSchemaLibrary(TestInfrahubDocker):
    """Base class: one Infrahub instance per test class, driven through `infrahubctl`."""

    @pytest.fixture(scope="class")
    def infrahub_address(self, infrahub_port: int) -> str:
        return f"http://localhost:{infrahub_port}"

    @pytest.fixture(scope="class")
    def ctl(self, infrahub_address: str):
        """Return a function that runs a shell command against the test instance."""

        def _run(command: str) -> subprocess.CompletedProcess[str]:
            return self.execute_command(command, infrahub_address)

        return _run

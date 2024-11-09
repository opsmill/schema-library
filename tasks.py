import os
from pathlib import Path

from invoke import Context, task  # type: ignore

# If no version is indicated, we will take the latest
VERSION = os.getenv("INFRAHUB_VERSION", None)
DOCKER_PROJECT = os.getenv("INFRAHUB_BUILD_NAME", "schema-library-ci")
COMPOSE_COMMAND = f"curl https://infrahub.opsmill.io/{VERSION if VERSION else ''} | sed 's/8000:8000/0:8000/' | docker compose -p {DOCKER_PROJECT} -f -"


@task
def start(context: Context) -> None:
    context.run(f"{COMPOSE_COMMAND} up -d --wait")


@task
def load_schema_base(context: Context, schema: Path = Path("./base/*.yml")) -> None:
    context.run(f"infrahubctl schema load {schema}")


@task
def load_schema_experimental(
    context: Context, schema: Path = Path("./experimental/**/*.yml")
) -> None:
    Base = Path("./base/*.yml")
    context.run(f"infrahubctl schema load {Base}")
    context.run(f"infrahubctl schema load {schema}")


@task
def destroy(context: Context) -> None:
    context.run(f"{COMPOSE_COMMAND} down -v")


@task
def stop(context: Context) -> None:
    context.run(f"{COMPOSE_COMMAND} down")


@task
def restart(context: Context, component: str = "") -> None:
    if component:
        context.run(f"{COMPOSE_COMMAND} restart {component}")
        return

    context.run(f"{COMPOSE_COMMAND} restart")

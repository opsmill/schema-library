import os
from pathlib import Path

from invoke import Context, task  # type: ignore

# If no version is indicated, we will take the latest
VERSION = os.getenv("INFRAHUB_VERSION", None)
DOCKER_PROJECT = os.getenv("INFRAHUB_BUILD_NAME", "schema-library-ci")
COMPOSE_COMMAND = f"curl https://infrahub.opsmill.io/{VERSION if VERSION else ''} | sed 's/8000:8000/0:8000/' | docker compose -p {DOCKER_PROJECT} -f -"


def _parse_and_load_extensions(
    context: Context, extensions_path: Path, allowed_to_fail: bool
) -> None:
    # Looping over all entries in extensions dir
    for entry in os.listdir(extensions_path):
        # Make sure it's a dir
        # TODO: here if in extensions folder we have a dir without schema it will fail
        if os.path.isdir(extensions_path / entry):
            print(f"Loading `{entry}`")

            # Load extensions
            # TODO: Maybe improve what we return here...
            context.run(
                f"infrahubctl schema load {extensions_path / entry}",
                warn=allowed_to_fail,
            )


@task
def start(context: Context) -> None:
    context.run(f"{COMPOSE_COMMAND} up -d --wait")


@task
def load_schema_base(context: Context) -> None:
    base_path = Path("./base")
    context.run(f"infrahubctl schema load {base_path}")


@task
def load_schema_extensions(context: Context) -> None:
    extensions_path = Path("./extensions")

    # First loop: here we allow to fail so it will load as much as it can
    print("Loading all extensions once ...")
    _parse_and_load_extensions(context, extensions_path, True)

    # First loop: all the dependencies are loaded it MUST work
    print("Loading all extensions second time ...")
    _parse_and_load_extensions(context, extensions_path, False)

    # FIXME: If we have 3 degrees of dependencies it won't work
    print("All good!")


@task
def destroy(context: Context) -> None:
    context.run(f"{COMPOSE_COMMAND} down -v")


@task
def stop(context: Context) -> None:
    context.run(f"{COMPOSE_COMMAND} down")

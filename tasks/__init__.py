import os

from invoke import Collection, Context, task

from . import docs, linter, schemas

VERSION = os.getenv("INFRAHUB_VERSION", None)
DOCKER_PROJECT = os.getenv("INFRAHUB_BUILD_NAME", "schema-library-ci")
COMPOSE_COMMAND = f"curl https://infrahub.opsmill.io/{VERSION if VERSION else ''} | sed 's/8000:8000/0:8000/' | docker compose -p {DOCKER_PROJECT} -f -"  # noqa: line-too-long

ns = Collection()

ns.add_collection(Collection.from_module(linter))
ns.add_collection(Collection.from_module(schemas))
ns.add_collection(Collection.from_module(docs))


@task(name="start")
def start(context: Context) -> None:
    """Start local instance of Infrahub for test purposes."""
    context.run(f"{COMPOSE_COMMAND} up -d --wait")


@task(name="destroy")
def destroy(context: Context) -> None:
    """Destroy local instance of Infrahub for test purposes."""
    context.run(f"{COMPOSE_COMMAND} down -v --remove-orphans --rmi local")


ns.add_task(start)
ns.add_task(destroy)

from invoke import Collection, Context, task  # type: ignore

from . import docusaurus, linter, schemas

ns = Collection()

ns.add_collection(Collection.from_module(linter))
ns.add_collection(Collection.from_module(docusaurus))
ns.add_collection(Collection.from_module(schemas))


@task(name="lint")
def lint_all(context: Context) -> None:
    linter.lint_all(context)


@task(name="format")
def format(context: Context) -> None:
    linter.format(context)


ns.add_task(lint_all)
ns.add_task(format)

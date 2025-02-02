from invoke import Collection, Context, task  # type: ignore

from . import docusaurus, linter, schemas

ns = Collection()

ns.add_collection(linter)
ns.add_collection(docusaurus)
ns.add_collection(schemas)


@task(name="lint")
def lint_all(context: Context) -> None:
    linter.lint_all(context)


@task(name="format")
def format(context: Context) -> None:
    linter.format(context)


# @task(name="docusaurus")
# def docusaurus(context: Context) -> None:
#     docusaurus.docusaurus(context)


ns.add_task(lint_all)
ns.add_task(format)
# ns.add_task(docusaurus)

from invoke import Collection  # type: ignore

from . import docs, docusaurus, linter, schemas

ns = Collection()

ns.add_collection(Collection.from_module(linter))
ns.add_collection(Collection.from_module(docusaurus))
ns.add_collection(Collection.from_module(schemas))
ns.add_collection(Collection.from_module(docs))

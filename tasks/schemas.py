import copy
import os
from collections import defaultdict, deque
from pathlib import Path

import yaml  # type: ignore
from invoke import Context, task  # type: ignore

METADATA_FILE = Path(__file__).parent.parent.resolve() / ".metadata.yml"
# Flag if we need to test experimental section or not
TEST_EXPERIMENTAL = os.getenv("TEST_EXPERIMENTAL", None)


def _load_extension(context: Context, path: Path) -> None:
    # Make sure it's a dir
    if os.path.isdir(path):
        print("#" * 80)
        print(f"🏗️  Loading `{path}`")

        # Load extensions
        context.run(f"infrahubctl schema load {path}")
        print("#" * 80)


def _load_yaml_metadata():
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# Build the dependency `graph`
# i.e. `extension_abc` => list of all extensions **depending** on it
# Build `all_extensions` list
# i.e. `extension_abc` => list of all dependencies
def _build_dependency_graph(metadata):
    graph = defaultdict(list)  # Graph of dependencies
    all_extensions = defaultdict(dict)  # Dict of all extension with dependencies
    for key, value in metadata.items():
        dependencies = value.get("dependencies", [])
        graph[key] = list(dependencies)  # key: [dependencies]
        all_extensions[key] = list(dependencies)
    # Ensure 'base' is present as a dummy node
    if "base" not in graph:
        graph["base"] = []
        all_extensions["base"] = []
    return graph, all_extensions


# Topological sort to determine a safe load order
def _resolve_load_order(graph, all_extensions):
    all_exts = copy.deepcopy(all_extensions)
    order = []  # List to store the final load order
    queue = deque([node for node, deps in all_exts.items() if not deps])

    # While we have something to proceed
    while queue:
        # Pick first element in the queue and add it to the result
        current = queue.popleft()
        order.append(current)

        # Remove 'current' from the dependencies of all other nodes
        for node in all_exts:
            if current in all_exts[node]:
                all_exts[node].remove(current)
                # If it happens the current was the last needed for a given
                if not all_exts[node]:
                    # We add it to the queue to be proceed!
                    queue.append(node)

    if len(order) != len(all_exts):
        # Remove debugging output, just raise error
        raise ValueError("Cycle detected in dependency graph!")

    return order


def load_order(include_experimental: bool = False) -> list[str]:
    """Return the schema paths to load, in an order that respects dependencies.

    Each entry is a directory relative to the repository root. The dummy `base`
    node loads the `base/` directory. Keys in `.metadata.yml` that are not
    directories, such as `base/dcim`, are not loadable on their own and are left out.
    Experimental schemas are included only when `include_experimental` is true.
    """
    metadata = _load_yaml_metadata()
    graph, all_extensions = _build_dependency_graph(metadata)
    repository_root = METADATA_FILE.parent
    return [
        entry
        for entry in _resolve_load_order(graph, all_extensions)
        if (include_experimental or not entry.startswith("experimental/"))
        and (repository_root / entry).is_dir()
    ]


@task
def load_all_schemas(context: Context) -> None:
    # Load each extension respecting dependencies, skipping experimental ones unless the flag is set
    for extension in load_order(include_experimental=bool(TEST_EXPERIMENTAL)):
        _load_extension(context, Path(extension))

    print("All good! ✨")

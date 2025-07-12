import copy
import os
from collections import defaultdict, deque
from pathlib import Path

import yaml  # type: ignore
from invoke import Context, task  # type: ignore

# If no version is indicated, we will take the latest
CURRENT_DIRECTORY = Path(__file__).parent.resolve()
MAIN_DIRECTORY_PATH = Path(__file__).parent
DOCUMENTATION_DIRECTORY = CURRENT_DIRECTORY.parent.resolve() / "docs"
METADATA_FILE = CURRENT_DIRECTORY.parent / ".metadata.yml"
# Flag if we need to test experimental section or not
TEST_EXPERIMENTAL = os.getenv("TEST_EXPERIMENTAL", None)


def _load_extension(context: Context, path: Path) -> None:
    # Make sure it's a dir
    # TODO: here if in extensions folder we have a dir without schema it will fail
    if os.path.isdir(path):
        print("#" * 80)
        print(f"🏗️  Loading `{path}`")

        # Load extensions
        # TODO: Maybe improve what we return here...
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
    load_order = []  # List to store the final load order
    queue = deque([node for node, deps in all_exts.items() if not deps])

    # While we have something to proceed
    while queue:
        # Pick first element in the queue and add it to the result
        current = queue.popleft()
        load_order.append(current)

        # Remove 'current' from the dependencies of all other nodes
        for node in all_exts:
            if current in all_exts[node]:
                all_exts[node].remove(current)
                # If it happens the current was the last needed for a given
                if not all_exts[node]:
                    # We add it to the queue to be proceed!
                    queue.append(node)

    if len(load_order) != len(all_exts):
        # Remove debugging output, just raise error
        raise ValueError("Cycle detected in dependency graph!")

    return load_order


@task
def load_all_schemas(context: Context) -> None:
    # Parse metadata file
    metadata = _load_yaml_metadata()

    # Build dependency graph
    graph, all_extensions = _build_dependency_graph(metadata)

    # Determine the correct order to load extensions
    load_order = _resolve_load_order(graph, all_extensions)

    # Load each extension respecting dependencies
    for extension in load_order:
        # If it's experimental extension and flag is false we skip
        if extension.startswith("experimental/") and not TEST_EXPERIMENTAL:
            continue

        _load_extension(context, Path(extension))

    print("All good! ✨")

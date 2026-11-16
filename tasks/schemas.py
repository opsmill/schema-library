import copy
import os
import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path

import yaml  # type: ignore
from infrahub_sdk.schema import validate_schema
from infrahub_sdk.yaml import SchemaFile
from invoke import Context, task  # type: ignore

REPOSITORY_ROOT = Path(__file__).parent.parent.resolve()
METADATA_FILE = REPOSITORY_ROOT / ".metadata.yml"
# Folders of published schemas. `experimental/` is deliberately not validated.
VALIDATED_FOLDERS = ("base", "extensions")
SCHEMA_SUFFIXES = {".yml", ".yaml"}
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

    # Load each extension respecting dependencies, skipping experimental ones unless the flag is set
    for extension in load_order:
        if extension.startswith("experimental/") and not TEST_EXPERIMENTAL:
            continue
        _load_extension(context, Path(extension))

    print("All good! ✨")


@dataclass(frozen=True)
class Finding:
    """One problem found in a schema file."""

    path: Path
    message: str


def validate_schema_files(root: Path) -> list[Finding]:
    """Validate every schema file under `base/` and `extensions/` of `root`.

    Errors and warnings are both returned as findings. Every problem in every
    file is reported, in path order.
    """
    findings: list[Finding] = []
    files = sorted(
        path
        for folder in VALIDATED_FOLDERS
        for path in (root / folder).rglob("*")
        if path.is_file() and path.suffix in SCHEMA_SUFFIXES
    )
    for file_path in files:
        relative = file_path.relative_to(root)
        for schema_file in SchemaFile.load_file_from_disk(path=file_path):
            if not schema_file.valid or not schema_file.content:
                findings.append(
                    Finding(relative, schema_file.error_message or "Invalid YAML file")
                )
                continue
            result = validate_schema(schema=schema_file.payload)
            findings.extend(Finding(relative, error.message) for error in result.errors)
            findings.extend(
                Finding(relative, f"Warning: {warning.message}")
                for warning in result.warnings
            )
    return findings


def _escape_annotation(value: str) -> str:
    """Escape a value for a GitHub workflow command."""
    return value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def format_annotation(finding: Finding) -> str:
    return f"::error file={_escape_annotation(finding.path.as_posix())}::{_escape_annotation(finding.message)}"


@task
def validate(context: Context) -> None:  # pylint: disable=unused-argument
    """Validate every schema in `base/` and `extensions/` without starting Infrahub."""
    findings = validate_schema_files(REPOSITORY_ROOT)
    for finding in findings:
        print(format_annotation(finding))
    if findings:
        files = len({finding.path for finding in findings})
        print(f"Found {len(findings)} problem(s) in {files} file(s).")
        sys.exit(1)
    print("All schemas are valid.")

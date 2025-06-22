import os
from collections import defaultdict, deque
from pathlib import Path
import copy

import yaml  # type: ignore
from invoke import Context, task  # type: ignore

# If no version is indicated, we will take the latest
VERSION = os.getenv("INFRAHUB_VERSION", None)
DOCKER_PROJECT = os.getenv("INFRAHUB_BUILD_NAME", "schema-library-ci")
COMPOSE_COMMAND = f"curl https://infrahub.opsmill.io/{VERSION if VERSION else ''} | sed 's/8000:8000/0:8000/' | docker compose -p {DOCKER_PROJECT} -f -"  # noqa: line-too-long
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
def start(context: Context) -> None:
    context.run(f"{COMPOSE_COMMAND} up -d --wait")


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


@task
def destroy(context: Context) -> None:
    context.run(f"{COMPOSE_COMMAND} down -v")


@task
def stop(context: Context) -> None:
    context.run(f"{COMPOSE_COMMAND} down")


def format_table(headers: list, rows: list):
    """Generate a Markdown table."""

    def escape_markdown(text: str) -> str:
        # Escape special markdown characters
        special_chars = [
            "|",
            "_",
            "*",
            "`",
            "[",
            "]",
            "(",
            ")",
            "#",
            "+",
            "-",
            ".",
            "!",
            "$",
            "<",
            ">",
        ]

        for char in special_chars:
            text = text.replace(char, f"\\{char}")
        return text

    table = f"\n| {' | '.join(headers)} |\n"
    table += f"| {' | '.join(['-' * len(header) for header in headers])} |\n"
    for row in rows:
        escaped_row = [escape_markdown(cell) for cell in row]
        table += f"| {' | '.join(escaped_row)} |\n"
    return table


def format_data(header: str, data: dict):
    if header == "choices":
        choices = [choice.get("name", "") for choice in data.get(header, [])]
        choices_str = ", ".join(choices)
        return f"`{choices_str}`"

    return str(data.get(header, ""))


def generate_table_data(data: list):
    headers = []
    for attr in data:
        for k in attr.keys():
            if k not in headers:
                headers.append(k)

    rows = []
    for attr in data:
        row = [format_data(header, attr) for header in headers]
        rows.append(row)

    return headers, rows


def generate_node_data(node: dict):
    node_markdown = []
    node_markdown.append(f"#### {node.get('name')}\n")
    if node.get("description"):
        node_markdown.append(f"- **Description:** {node.get('description')}")
    if node.get("label"):
        node_markdown.append(f"- **Label:** {node.get('label', '')}")
    if node.get("icon"):
        node_markdown.append(f"- **Icon:** {node.get('icon', '')}")
    if node.get("menu_placement"):
        node_markdown.append(f"- **Menu Placement:** {node.get('menu_placement', '')}")
    node_markdown.append(
        f"- **Include in Menu:** {'✅' if node.get('include_in_menu') else '❌'}\n"
    )
    if node.get("order_by") or node.get("uniqueness_constraints"):
        node_markdown.append("#### Ordering and Constraints\n")
        node_markdown.append(f"- **Order By:**{', '.join(node.get('order_by', []))}")
        node_markdown.append(
            f"- **Uniqueness Constraints:**{', '.join([' + '.join(c) for c in node.get('uniqueness_constraints', [])])}\n"
        )

    if attributes := node.get("attributes", []):
        node_markdown.append("##### Attributes")
        attribute_headers, attribute_rows = generate_table_data(attributes)
        node_markdown.append(format_table(attribute_headers, attribute_rows))

    if relationships := node.get("relationships", []):
        node_markdown.append("#### Relationships")
        relationship_headers, relationship_rows = generate_table_data(relationships)
        node_markdown.append(format_table(relationship_headers, relationship_rows))
    return node_markdown


def handle_generics(generics):
    content = ["### Generics\n"]
    for generic in generics:
        content.extend(generate_node_data(generic))
    return content


def handle_nodes(nodes):
    content = ["### Nodes\n"]
    for node in nodes:
        content.extend(generate_node_data(node))
    return content


def handle_extensions(extensions):
    content = ["### Extensions\n"]
    for node in extensions.get("nodes", []):
        content.append(f"#### {node.get('kind', '')}\n")
        if attributes := node.get("attributes", []):
            content.append("#### Attributes")
            headers, rows = generate_table_data(attributes)
            content.append(format_table(headers, rows))
        if relationships := node.get("relationships", []):
            content.append("#### Relationships")
            headers, rows = generate_table_data(relationships)
            content.append(format_table(headers, rows))
    return content


def generate_readme(schema, extension_dir: Path) -> list:
    schema_definition_files = {}
    for yml_file in extension_dir.glob("*.yml"):
        with open(yml_file, "r", encoding="utf-8") as f:
            schema_definition_files[yml_file.stem] = yaml.safe_load(f)

    description = schema.get("description", "")
    content = [
        f"## {schema.get('name', '')}\n",
        f"{description}\n" if not description.endswith("\n") else description,
    ]

    if dependencies := schema.get("dependencies", []):
        content.append(f"- **Dependencies:** `{', '.join(dependencies)}`")

    if attribution := schema.get("attribution", []):
        content.append(f"- **Attribution**: {attribution}\n")

    for _, file_values in schema_definition_files.items():
        content.append(f"- **Version:** {file_values['version']}\n")

        if generics := file_values.get("generics", []):
            content.extend(handle_generics(generics))

        if nodes := file_values.get("nodes", []):
            content.extend(handle_nodes(nodes))

        if extensions := file_values.get("extensions", []):
            content.extend(handle_extensions(extensions))

    # Write README.md
    readme_path = extension_dir / "README.md"
    # Ensure the parent directory exists

    os.makedirs(readme_path.parent, exist_ok=True)
    with open(readme_path, "w", encoding="utf-8") as f:
        f.writelines("\n".join(content))

    return content


def generate_toc(schema, base_path, extensions_path, experimental_path):
    toc = ["# Schema Library Documentation\n"]
    toc.append("## Base\n")
    toc.append("| name | description |")
    toc.append("| ---- | ----------- |")
    for key in sorted(schema.keys()):
        if key.startswith("base/"):
            name = key.split("/", 1)[1]
            desc = schema[key].get("description", "")
            toc.append(f"| [{name}](#{name}) | {desc} |")
    toc.append("\n## Extensions\n")
    toc.append("| name | description |")
    toc.append("| ---- | ----------- |")
    for entry in sorted(os.listdir(extensions_path)):
        ext_path = Path(extensions_path) / entry
        if ext_path.is_dir():
            desc = ""
            if str(ext_path) in schema and "description" in schema[str(ext_path)]:
                desc = schema[str(ext_path)]["description"]
            toc.append(f"| [{entry}](#{entry}) | {desc} |")
    toc.append("\n## Experimental\n")
    toc.append("| name | description |")
    toc.append("| ---- | ----------- |")
    for entry in sorted(os.listdir(experimental_path)):
        exp_path = Path(experimental_path) / entry
        if exp_path.is_dir():
            desc = ""
            if str(exp_path) in schema and "description" in schema[str(exp_path)]:
                desc = schema[str(exp_path)]["description"]
            toc.append(f"| [{entry}](#{entry}) | {desc} |")
    return "\n".join(toc) + "\n"


def process_schema_directories(schema, directories_to_parse):
    all_content = []
    for directory in directories_to_parse:
        for entry in os.listdir(directory):
            if os.path.isdir(directory / entry):
                path = directory / entry
                try:
                    content = generate_readme(schema[str(path)], path)
                    all_content.extend(content)
                except KeyError:
                    print(f"Schema `{path}` is not added to the .metadata.yml file")
    return all_content


@task
def build(context: Context) -> None:
    """Generate README.md files for all schema extensions"""
    print("Building schema README.md files...")
    directories_to_parse = [
        Path("./extensions"),
        Path("./experimental"),
    ]
    schema_docs_dir = DOCUMENTATION_DIRECTORY / "docs"
    consolidated_doc = schema_docs_dir / "schema-library.mdx"
    all_content = []
    all_content.append(
        "---\ntitle: Schema Library Documentation\n---\n<!-- markdownlint-disable-file MD025 -->\n"
    )
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)
    base_path = Path("./base")
    for key in sorted(schema.keys()):
        if key.startswith("base/"):
            name = key.split("/", 1)[1]
            yml_path = base_path / f"{name}.yml"
            if yml_path.exists():
                content = generate_readme(schema[key], base_path)
                all_content.extend(content)
    toc = generate_toc(schema, base_path, "./extensions", "./experimental")
    all_content.insert(1, toc)
    all_content.extend(process_schema_directories(schema, directories_to_parse))
    with open(consolidated_doc, "w", encoding="utf-8") as f:
        f.write("\n".join(all_content))

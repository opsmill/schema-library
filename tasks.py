import os
from pathlib import Path
import yaml # type: ignore
from collections import OrderedDict
from invoke import Context, task  # type: ignore

# If no version is indicated, we will take the latest
VERSION = os.getenv("INFRAHUB_VERSION", None)
DOCKER_PROJECT = os.getenv("INFRAHUB_BUILD_NAME", "schema-library-ci")
COMPOSE_COMMAND = f"curl https://infrahub.opsmill.io/{VERSION if VERSION else ''} | sed 's/8000:8000/0:8000/' | docker compose -p {DOCKER_PROJECT} -f -"  # noqa: line-too-long
MAIN_DIRECTORY_PATH = Path(__file__).parent
METADATA_FILE = ".metadata.yml"

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

    # FIXME: Find a more efficient way to deal with dependencies that doesn't
    # require developer to explicitly maintain it

    # First/second loop: here we allow to fail so it will load as much as it can
    print("Loading all extensions once ...")
    _parse_and_load_extensions(context, extensions_path, True)

    print("Loading all extensions second time ...")
    _parse_and_load_extensions(context, extensions_path, True)

    # Third loop: all the dependencies are loaded it MUST work
    print("Loading all extensions third time ...")
    _parse_and_load_extensions(context, extensions_path, True)

    # FIXME: If we have 4 degrees of dependencies it won't work
    print("All good!")


@task
def destroy(context: Context) -> None:
    context.run(f"{COMPOSE_COMMAND} down -v")


@task
def stop(context: Context) -> None:
    context.run(f"{COMPOSE_COMMAND} down")


def generate_readme(schema, extension_dir: Path) -> None:
    schema_definition_files = {}
    for yml_file in extension_dir.glob("*.yml"):
        with open(yml_file, "r", encoding="utf-8") as f:
            schema_definition_files[yml_file.stem] = yaml.safe_load(f)

    content = [
        f"# {schema.get('name', '')}\n",
        f"{schema.get('description', '')}\n",
    ]

    if dependencies := schema.get("dependencies", []):
        content.append(f"Dependencies: `{', '.join(dependencies)}`\n")

    if attribution := schema.get("attribution", []):
        content.append(f"Attribution: {attribution}\n")

    def format_table(headers: list, rows: list):
        """Generate a Markdown table."""
        table = f"\n| {' | '.join(headers)} |\n"
        table += f"| {' | '.join(['-' * len(header) for header in headers])} |\n"
        for row in rows:
            table += f"| {' | '.join(row)} |\n"
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
        node_markdown.append(f"### {node.get('name')}\n")
        if node.get("description"):
            node_markdown.append(f"- **Description:** {node.get('description')}")
        if node.get("label"):
            node_markdown.append(f"- **Label:** {node.get('label', '')}")
        if node.get("icon"):
            node_markdown.append(f"- **Icon:** {node.get('icon', '')}")
        if node.get("menu_placement"):
            node_markdown.append(
                f"- **Menu Placement:** {node.get('menu_placement', '')}"
            )
        node_markdown.append(
            f"- **Include in Menu:** {'✅' if node.get('include_in_menu') else '❌'}\n"
        )
        if node.get("order_by") or node.get("uniqueness_constraints"):
            node_markdown.append("\n#### Ordering and Constraints")
            node_markdown.append(
                f"- **Order By:** {', '.join(node.get('order_by', []))}"
            )
            node_markdown.append(
                f"- **Uniqueness Constraints:** {', '.join([' + '.join(c) for c in node.get('uniqueness_constraints', [])])}"
            )
        # node_markdown.append("---\n")

        if attributes := node.get("attributes", []):
            node_markdown.append("#### Attributes")
            attribute_headers, attribute_rows = generate_table_data(attributes)
            node_markdown.append(format_table(attribute_headers, attribute_rows))

        if relationships := node.get("relationships", []):
            node_markdown.append("#### Relationships")
            relationship_headers, relationship_rows = generate_table_data(relationships)
            node_markdown.append(format_table(relationship_headers, relationship_rows))
        return node_markdown

    for _, file_values in schema_definition_files.items():
        content.append("## Overview\n")
        content.append(f"- **Version:** {file_values['version']}\n")

        if generics := file_values.get("generics", []):
            content.append("## Generics\n")
            for generic in generics:
                content.extend(generate_node_data(generic))

        if nodes := file_values.get("nodes", []):
            content.append("## Nodes\n")
            for node in nodes:
                content.extend(generate_node_data(node))

        if extensions := file_values.get("extensions", []):
            content.append("## Extensions")
            for node in extensions.get("nodes", []):
                content.append(f"### {node.get('kind', '')}")

                if attributes := node.get("attributes", []):
                    content.append("#### Attributes")
                    headers, rows = generate_table_data(attributes)
                    content.append(format_table(headers, rows))

                if relationships := node.get("relationships", []):
                    content.append("#### Relationships")
                    headers, rows = generate_table_data(relationships)
                    content.append(format_table(headers, rows))

    # Write README.md
    readme_path = extension_dir / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.writelines("\n".join(content))


@task
def build(context: Context) -> None:
    """Generate README.md files for all schema extensions"""
    print("Building schema README.md files...")
    directories_to_parse = [
        Path("./extensions"),
        Path("./experimental"),
    ]

    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)

    # Build Readme for base schemas
    base_path = Path("./base")
    generate_readme(schema[str(base_path)], base_path)

    for directory in directories_to_parse:
        for entry in os.listdir(directory):
            if os.path.isdir(directory / entry):
                path = directory / entry
                # print(path)
                try:
                    generate_readme(schema[str(path)], path)
                except KeyError:
                    print(f"Schema `{path}` is not added to the {METADATA_FILE} file")


@task
def format(context: Context) -> None:
    """Run RUFF to format all Python files."""

    exec_cmds = ["ruff format .", "ruff check . --fix"]
    with context.cd(MAIN_DIRECTORY_PATH):
        for cmd in exec_cmds:
            context.run(cmd)


@task
def lint_yaml(context: Context) -> None:
    """Run Linter to check all Python files."""
    print(" - Check code with yamllint")
    exec_cmd = "yamllint ."
    with context.cd(MAIN_DIRECTORY_PATH):
        context.run(exec_cmd)

@task
def lint_mypy(context: Context) -> None:
    """Run Linter to check all Python files."""
    print(" - Check code with mypy")
    exec_cmd = "mypy --show-error-codes ."
    with context.cd(MAIN_DIRECTORY_PATH):
        context.run(exec_cmd)


@task
def lint_ruff(context: Context) -> None:
    """Run Linter to check all Python files."""
    print(" - Check code with ruff")
    exec_cmd = "ruff check ."
    with context.cd(MAIN_DIRECTORY_PATH):
        context.run(exec_cmd)


@task(name="lint")
def lint_all(context: Context) -> None:
    """Run all linters."""
    sort_metadata(context)
    lint_yaml(context)
    lint_ruff(context)
    lint_mypy(context)

def sort_dict(d):
    """
    Recursively sort a dictionary by keys.
    """
    if isinstance(d, dict):
        return OrderedDict(sorted((k, sort_dict(v)) for k, v in d.items()))
    if isinstance(d, list):
        return [sort_dict(item) for item in d]
    return d

class PreserveLiteralStyleDumper(yaml.SafeDumper):
    """
    Custom Dumper to preserve the literal style for multiline strings.
    """

    def increase_indent(self, flow=False, indentless=False):
        return super(PreserveLiteralStyleDumper, self).increase_indent(flow, False)

    def represent_scalar(self, tag, value, style=None):
        if "\n" in value:  # If the string contains newlines, use literal style
            style = "|"
        return super().represent_scalar(tag, value, style=style)

@task(name="sort-metadata")
def sort_metadata(context: Context) -> None:
    print(f" - Sort {METADATA_FILE}")
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = yaml.safe_load(f)

    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(metadata, f, Dumper=PreserveLiteralStyleDumper, default_flow_style=False, sort_keys=True, allow_unicode=True)

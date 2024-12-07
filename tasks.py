import os
from pathlib import Path
import yaml

from invoke import Context, task  # type: ignore

# If no version is indicated, we will take the latest
VERSION = os.getenv("INFRAHUB_VERSION", None)
DOCKER_PROJECT = os.getenv("INFRAHUB_BUILD_NAME", "schema-library-ci")
COMPOSE_COMMAND = f"curl https://infrahub.opsmill.io/{VERSION if VERSION else ''} | sed 's/8000:8000/0:8000/' | docker compose -p {DOCKER_PROJECT} -f -"

def generate_readme_for_extension(extension_dir: Path) -> None:
    """Generate README.md for a schema extension directory."""

    # Find schema description file
    schema_description_file = next(extension_dir.glob("*.schema.yml"), None)
    if not schema_description_file:
        return

    # Load schema file
    with open(schema_description_file) as f:
        schema = yaml.safe_load(f)

    # Load all other schema definition yml files
    schema_definition_files = {}
    for yml_file in extension_dir.glob("*.yml"):
        if yml_file != schema_description_file:
            with open(yml_file) as f:
                schema_definition_files[yml_file.stem] = yaml.safe_load(f)

    # Generate README content
    content = [
        f"# {extension_dir.name}\n\n",
        f"{schema.get('spec', {}).get('description', '')}\n"
    ]

    # Add generics
    content.append("\n## Generics\n")
    generics = []
    for yml in schema_definition_files.values():
        if "generics" in yml:
            content.extend("\n")
            for generic in yml["generics"]:
                generics.append(generic["name"])
    content.extend([f"- {generic}\n" for generic in generics])

    # Add nodes
    content.append("\n## Nodes\n")
    nodes = []
    for yml in schema_definition_files.values():
        if "nodes" in yml:
            content.extend("\n")
            for node in yml["nodes"]:
                nodes.append(node["name"])
    content.extend([f"- {node}\n" for node in nodes])

    # Add dependencies
    content.append("\n## Dependencies\n\n")
    deps = schema.get("spec", {}).get("dependencies", [])
    content.extend([f"- {dep}\n" for dep in deps])

    # Write README.md
    readme_path = extension_dir / "README.md"
    with open(readme_path, "w") as f:
        f.writelines(content)

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


@task
def build(context: Context) -> None:
    """Generate README.md files for all schema extensions"""
    print("Building schema README.md files...")
    directories_to_parse = [
        Path("./extensions"),
        Path("./experimental"),
    ]

    for dir in directories_to_parse:
        for entry in os.listdir(dir):
            if os.path.isdir(dir / entry):
                generate_readme_for_extension(dir / entry)

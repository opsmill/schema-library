import re
import sys
from collections import defaultdict
from pathlib import Path

import jinja2
import yaml  # type: ignore
from invoke import Context, task  # type: ignore

CURRENT_DIRECTORY = Path(__file__).parent.resolve()
DOCUMENTATION_DIRECTORY = CURRENT_DIRECTORY.parent / "docs"
METADATA_FILE = CURRENT_DIRECTORY.parent / ".metadata.yml"


def _sanitize_description(desc):
    if not isinstance(desc, str):
        return desc
    return desc.replace("\n", " ").replace("  ", " ").strip()


def _normalize_anchor(name: str) -> str:
    """Normalize a string to match Docusaurus/GitHub anchor links."""

    anchor = name.strip().lower()
    anchor = anchor.replace("_", "-").replace(" ", "-")
    anchor = re.sub(r"[^a-z0-9\-]", "", anchor)
    return anchor


def _generate_toc_content(metadata) -> defaultdict[str, list]:
    """Based on the metadata, generate the Table of Content for the reference page."""

    result = defaultdict(list)
    # {folder: [{name, anchor, description}, ...]}
    # e.g. {"base": [{"name": "DCIM", "anchor": "dcim", "description": "This contains ..."}]}

    # Loop through the metadata and create a dictionary with the structure
    for key in metadata:
        # TODO: Handle the case where we can't split the key
        current_item = {
            "name": metadata[key].get("name"),
            "anchor": _normalize_anchor(key.split("/")[1]),
            "description": _sanitize_description(metadata[key].get("description", "")),
        }

        result[key.split("/")[0]].append(current_item)

    # Sort the items in each folder by name
    for folder, items in result.items():
        result[folder] = sorted(items, key=lambda x: x["name"].lower())

    return result


def _generate_schema_reference_content(metadata) -> list[dict]:
    """Generate the schema reference content based on the metadata and schema file content."""

    result: list[dict] = []

    # Loop through the metadata
    for key in metadata:
        # Populate the current item with metadata
        current_schema = {
            "name": metadata[key].get("name", ""),
            "description": metadata[key].get("description", ""),
            "attribution": metadata[key].get("attribution", ""),
            "dependencies": metadata[key].get("dependencies", []),
        }

        extension_dir = Path(key)

        # If it's part of base folder, we assume the yml file is named after the key
        # e.g. base/organization => base/organization.yml
        if key.startswith("base/"):
            yml_file = extension_dir.with_suffix(".yml")
        else:
            # Find the yml file in the directory
            # FIXME: Maybe support .yaml as well?
            yml_files = list(extension_dir.glob("*.yml")) + list(
                extension_dir.glob("*.yaml")
            )

            # If more than one yml file is found it should fail
            if len(yml_files) != 1:
                raise FileNotFoundError(
                    f"Expected exactly one .yml file in {extension_dir}, found {len(yml_files)}"
                )
            yml_file = yml_files[0]  # TODO: Could be improved

        # Now load the schema file
        with open(yml_file, "r", encoding="utf-8") as f:
            schema_definition = yaml.safe_load(f)

            # Extract nodes, generics, and extensions if present
            for section in ["nodes", "generics", "extensions"]:
                current_schema[section] = schema_definition.get(section, [])
            result.append(current_schema)

    return result


def _generate_extensions_reference_documentation() -> None:
    """Generate reference page for all extensions."""

    template_file = DOCUMENTATION_DIRECTORY / "_templates" / "reference.j2"
    output_file = DOCUMENTATION_DIRECTORY / "docs" / "reference" / "extensions.mdx"

    print("Generating reference file...")

    # Open the metadata file
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = yaml.safe_load(f)

    # Generate data for the Table of Content
    toc_content = _generate_toc_content(metadata)

    # Generate data for the schema reference
    schema_content = _generate_schema_reference_content(metadata)

    # Load the template file
    if not template_file.exists():
        print(f"Unable to find the template file at {template_file}")
        sys.exit(-1)

    template_text = template_file.read_text(encoding="utf-8")

    # Render the template
    environment = jinja2.Environment(trim_blocks=True)
    template = environment.from_string(template_text)
    rendered_file = template.render(toc=toc_content, schemas=schema_content)

    # Write the rendered file to the output location
    output_file.write_text(rendered_file, encoding="utf-8")
    print(f"Docs saved to: {output_file}")


@task
def generate(context: Context) -> None:
    """Generate all documentation output from code."""
    _generate_extensions_reference_documentation()


@task
def install(context: Context) -> None:
    """Install documentation dependencies."""
    exec_cmd = "npm install"

    with context.cd(DOCUMENTATION_DIRECTORY):
        output = context.run(exec_cmd)

    if output is None or output.exited != 0:
        sys.exit(-1)


@task
def build(context: Context) -> None:
    """Build documentation website."""
    exec_cmd = "npm run build"

    with context.cd(DOCUMENTATION_DIRECTORY):
        output = context.run(exec_cmd)

    if output is None or output.exited != 0:
        sys.exit(-1)


@task
def serve(context: Context) -> None:
    """Run documentation server in development mode."""

    exec_cmd = "npm run serve"

    with context.cd(DOCUMENTATION_DIRECTORY):
        context.run(exec_cmd)

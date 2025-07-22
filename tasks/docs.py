import sys
from collections import defaultdict
from pathlib import Path

import jinja2
import yaml  # type: ignore
from invoke import Context, task  # type: ignore

CURRENT_DIRECTORY = Path(__file__).parent.resolve()
DOCUMENTATION_DIRECTORY = CURRENT_DIRECTORY.parent / "docs"
METADATA_FILE = CURRENT_DIRECTORY.parent / ".metadata.yml"
TEMPLATE_DIRECTORY = DOCUMENTATION_DIRECTORY / "_templates"
REFERENCE_DIRECTORY = DOCUMENTATION_DIRECTORY / "docs" / "reference"


def _sanitize_description(desc):
    if not isinstance(desc, str):
        return desc
    return desc.replace("\n", " ").replace("  ", " ").strip()


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
            "link": "./reference/" + key.split("/")[1] + ".mdx",
            "description": _sanitize_description(metadata[key].get("description", "")),
        }

        result[key.split("/")[0]].append(current_item)

    # Sort the items in each folder by name
    for folder, items in result.items():
        result[folder] = sorted(items, key=lambda x: x["name"].lower())

    return result


def _generate_schema_reference_content(schema_key: str, schema_metadata: dict) -> dict:
    """Generate the schema reference content based on the metadata and schema file content."""

    # Populate the current item with metadata
    schema_data = {
        "name": schema_metadata.get("name", ""),
        "description": schema_metadata.get("description", ""),
        "attribution": schema_metadata.get("attribution", ""),
    }

    # Compute link for dependencies
    schema_data["dependencies"] = []
    if "dependencies" in schema_metadata:
        for dep in schema_metadata["dependencies"]:
            if dep == "base":
                link = "dcim"  # TODO: This is a hack, should be improved ... maybe merging all base references
            else:
                link = dep.split("/")[1]
            schema_data["dependencies"].append({"name": dep, "link": link})

    extension_dir = Path(schema_key)

    # If it's part of base folder, we assume the yml file is named after the key
    # e.g. base/organization => base/organization.yml
    if schema_key.startswith("base/"):
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
            schema_data[section] = schema_definition.get(section, [])

        # Add the code section
        schema_data["code"] = yaml.dump(schema_definition, sort_keys=False)

        # Return the data structure
        return schema_data


def _generate_home_page_documentation() -> None:
    """Generate home page of the doc site."""

    template_file = TEMPLATE_DIRECTORY / "home_page.j2"
    output_file = DOCUMENTATION_DIRECTORY / "docs" / "home.mdx"

    print("Generating reference file...")

    # Open the metadata file
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = yaml.safe_load(f)

    # Generate data for the available schemas
    toc_content = _generate_toc_content(metadata)

    # Load the template file
    if not template_file.exists():
        print(f"Unable to find the template file at {template_file}")
        sys.exit(-1)

    template_text = template_file.read_text(encoding="utf-8")

    # Render the template
    environment = jinja2.Environment(trim_blocks=True)
    template = environment.from_string(template_text)
    rendered_file = template.render(toc=toc_content)

    # Write the rendered file to the output location
    output_file.write_text(rendered_file, encoding="utf-8")
    print(f"Docs saved to: {output_file}")


def _generate_per_extension_documentation() -> None:
    """Generate per extension doc page."""
    template_file = TEMPLATE_DIRECTORY / "schema_reference.j2"

    print("Generating per extension doc...")

    # Load the template file
    if not template_file.exists():
        print(f"Unable to find the template file at {template_file}")
        sys.exit(-1)

    template_text = template_file.read_text(encoding="utf-8")

    # Render the template
    environment = jinja2.Environment(trim_blocks=True)
    template = environment.from_string(template_text)

    # Open the metadata file
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = yaml.safe_load(f)

    # Loop over the schema list and generate the content
    for key in metadata:
        # Render page for each extension
        schema_data: dict = _generate_schema_reference_content(key, metadata[key])
        rendered_file = template.render(schema=schema_data)

        # Write the rendered file to the output location
        output_file: Path = REFERENCE_DIRECTORY / f"{key.split('/')[1]}.mdx"
        output_file.write_text(rendered_file, encoding="utf-8")
        print(f"Docs saved to: {output_file}")

        # Write also the doc in each extension folder
        if not key.startswith("base/"):
            readme_content: str = f"# {key.split('/')[1]}\n\nPlease refer to the [reference page](https://docs.infrahub.app/schema-library/reference/{key.split('/')[1]}) for the corresponding documentation.\n"
            output_readme: Path = CURRENT_DIRECTORY.parent / key / "README.md"
            output_readme.write_text(readme_content, encoding="utf-8")
            print(f"Docs saved to: {output_readme}")

    # Finnaly write the base readme
    base_readme_content: str = "# Base\n\nPlease refer to the [reference page](https://docs.infrahub.app/schema-library/reference/dcim) for the corresponding documentation.\n"
    base_output_readme: Path = CURRENT_DIRECTORY.parent / "base" / "README.md"
    base_output_readme.write_text(base_readme_content, encoding="utf-8")
    print(f"Docs saved to: {base_output_readme}")


@task
def generate(context: Context) -> None:
    """Generate all documentation output from code."""
    _generate_home_page_documentation()
    _generate_per_extension_documentation()


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

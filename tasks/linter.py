from pathlib import Path
import yaml  # type: ignore
from collections import OrderedDict
from invoke import Context, task  # type: ignore

CURRENT_DIRECTORY = Path(__file__).resolve()
DOCUMENTATION_DIRECTORY = CURRENT_DIRECTORY.parent / "docs"
MAIN_DIRECTORY_PATH = Path(__file__).parent
METADATA_FILE = ".metadata.yml"


@task(name="format_code")
def format_code(context: Context) -> None:
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
        return super().increase_indent(flow, False)

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
        f.write("---\n# yamllint disable rule:line-length\n")
        yaml.dump(
            metadata,
            f,
            Dumper=PreserveLiteralStyleDumper,
            default_flow_style=False,
            sort_keys=True,
            allow_unicode=True,
        )

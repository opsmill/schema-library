from collections import OrderedDict
from pathlib import Path

import yaml  # type: ignore
from invoke import Context, task  # type: ignore

CURRENT_DIRECTORY = Path(__file__).resolve()
DOCUMENTATION_DIRECTORY = CURRENT_DIRECTORY.parent / "docs"
MAIN_DIRECTORY_PATH = Path(__file__).parent.parent
METADATA_FILE = ".metadata.yml"


@task(name="format")
def format_code(context: Context) -> None:
    """Run RUFF to format all Python files."""
    exec_cmds = ["ruff format .", "ruff check . --fix"]
    with context.cd(MAIN_DIRECTORY_PATH):
        for cmd in exec_cmds:
            context.run(cmd)


@task(name="yaml")
def lint_yaml(context: Context) -> None:
    """Run yamllint to check all YAML files."""
    print(" - Check code with yamllint")
    exec_cmd = "yamllint -s ."
    with context.cd(MAIN_DIRECTORY_PATH):
        context.run(exec_cmd)


@task(name="markdown")
def lint_markdown(context: Context) -> None:
    """Run markdownlint to check all Markdown files."""
    print(" - Check code with markdownlint")
    exec_cmd = "markdownlint '**/*.md' '**/*.mdx'"
    with context.cd(MAIN_DIRECTORY_PATH):
        context.run(exec_cmd)


@task(name="mypy")
def lint_mypy(context: Context) -> None:
    """Run mypy to check all Python files."""
    print(" - Check code with mypy")
    exec_cmd = "mypy --show-error-codes ."
    with context.cd(MAIN_DIRECTORY_PATH):
        context.run(exec_cmd)


@task(name="ruff")
def lint_ruff(context: Context) -> None:
    """Run ruff check on all Python files."""
    print(" - Check code with ruff")
    exec_cmd = "ruff check ."
    with context.cd(MAIN_DIRECTORY_PATH):
        context.run(exec_cmd)


@task(name="ruff-format")
def lint_ruff_format(context: Context) -> None:
    """Run ruff format check on all Python files."""
    print(" - Check formatting with ruff format")
    exec_cmd = "ruff format --check --diff ."
    with context.cd(MAIN_DIRECTORY_PATH):
        context.run(exec_cmd)


@task(name="pylint")
def lint_pylint(context: Context) -> None:
    """Run pylint on all Python files."""
    print(" - Check code with pylint")
    exec_cmd = "pylint --ignore .venv ."
    with context.cd(MAIN_DIRECTORY_PATH):
        context.run(exec_cmd)


@task(name="python")
def lint_python(context: Context) -> None:
    """Run all Python linters (ruff, ruff format, mypy, pylint)."""
    lint_ruff(context)
    lint_ruff_format(context)
    lint_mypy(context)
    lint_pylint(context)


@task(name="lint")
def lint_all(context: Context) -> None:
    """Run all linters."""
    sort_metadata(context)
    lint_markdown(context)
    lint_yaml(context)
    lint_python(context)


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

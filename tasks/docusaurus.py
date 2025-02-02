import sys
from pathlib import Path
from invoke import Context, task # type: ignore

CURRENT_DIRECTORY = Path(__file__).parent.resolve()
DOCUMENTATION_DIRECTORY = CURRENT_DIRECTORY.parent / "docs"


@task
def docs(context: Context) -> None:
    """Build documentation website."""
    exec_cmd = "npm run build"

    with context.cd(DOCUMENTATION_DIRECTORY):
        output = context.run(exec_cmd)

    if output.exited != 0:
        sys.exit(-1)

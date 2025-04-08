from pathlib import Path

import typer
from typing_extensions import Annotated

from midivis.analyse import analyse_files
from midivis.play import play_many
from midivis.utils import set_verbosity

app = typer.Typer()


@app.command()
def play(
    files: Annotated[list[Path], typer.Argument(exists=True, dir_okay=False)],
    verbosity: Annotated[int, typer.Option("--verbose", "-v", count=True)] = 0,
):
    set_verbosity(verbosity)
    play_many(files)


@app.command()
def analyse(
    base_path: Annotated[Path, typer.Argument(exists=True, dir_okay=True)],
    verbosity: Annotated[int, typer.Option("--verbose", "-v", count=True)] = 0,
):
    set_verbosity(verbosity)
    analyse_files(base_path=base_path)


if __name__ == "__main__":
    app()

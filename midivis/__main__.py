from pathlib import Path

import typer

from midivis.analyse import analyse_files
from midivis.play import play_many

app = typer.Typer()


@app.command()
def play(files: list[Path], debug: bool = False):
    if debug:
        pass
    play_many(files)


@app.command()
def analyse(base_path: Path, debug: bool = False):
    analyse_files(base_path=base_path)


if __name__ == "__main__":
    app()

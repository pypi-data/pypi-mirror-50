from pathlib import Path
from typing import List

import click


@click.command()
@click.argument("list_of_files", type=str)
def from_list(list_of_files):
    list_of_files = list_of_files.split(" ")
    click.echo(f"Looking for files: {list_of_files}")
    cwd = Path.cwd()

    list_of_files = list(cwd.glob("*.*"))
    click.echo(f"Files in dir: {[f.name for f in list_of_files]}")

    result = []
    for filename in list_of_files:
        if not bool([f for f in list_of_files if filename in f.name]):
            result.append(filename)

    click.echo(f"Missing files: {result}")


if __name__ == "__main__":
    from_list()

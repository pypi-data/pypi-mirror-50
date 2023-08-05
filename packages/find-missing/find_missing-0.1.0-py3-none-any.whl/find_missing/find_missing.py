from pathlib import Path
from typing import List

import click


@click.command()
@click.argument("lst", type=str)
def from_list(lst):
    lst = lst.split(" ")
    click.echo(f"Looking for files: {lst}")
    cwd = Path.cwd()

    list_of_files = list(cwd.glob("*.*"))
    click.echo(f"Files in dir: {[f.name for f in list_of_files]}")

    result = []
    for filename in lst:
        if not bool([f for f in list_of_files if filename in f.name]):
            result.append(filename)

    click.echo(f"Missing files: {result}")


if __name__ == "__main__":
    from_list()

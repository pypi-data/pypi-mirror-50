import re
from pathlib import Path

import click


@click.command()
@click.argument("list_of_files", type=str)
def main(list_of_files):
    list_of_files = re.findall(r"\w+", list_of_files)
    click.echo(f"Looking for files: {list_of_files}")
    cwd = Path.cwd()

    files_in_folder = [f for f in list(cwd.glob("*.*")) if f.is_file()]
    # click.echo(f"Files in dir: {[f.name for f in files_in_folder]}")

    result = []
    for filename in list_of_files:
        if not bool([f for f in files_in_folder if filename in f.name]):
            result.append(filename)
    if result:
        click.echo("\n".join(result))


if __name__ == "__main__":
    main()

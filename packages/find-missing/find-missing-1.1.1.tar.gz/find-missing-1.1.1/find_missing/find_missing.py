import re
from pathlib import Path

import click


@click.command()
@click.option("--exact/--not-exact", default=False)
@click.argument("list_of_files", type=str)
def main(list_of_files, exact: bool):
    list_of_files = re.findall(r"[A-Za-z\d.\-_]+", list_of_files)
    # click.echo(f"Looking for files: {list_of_files}")
    cwd = Path.cwd()

    files_in_folder = [f for f in list(cwd.glob("*.*")) if f.is_file()]
    # click.echo(f"Files in dir: {[f.name for f in files_in_folder]}")

    if not exact:
        result = find_partial_match(list_of_files, files_in_folder)
    else:
        result = find_exact_match(list_of_files, files_in_folder)

    if result:
        click.echo("\n".join(result))
    else:
        click.echo("All here!")


def find_partial_match(list_of_files, files_in_folder):
    result = []
    for filename in list_of_files:
        if not bool([f for f in files_in_folder if filename in f.name]):
            result.append(filename)
    return result


def find_exact_match(list_of_files, files_in_folder):
    result = []
    for filename in list_of_files:
        if not bool(
            [
                f
                for f in files_in_folder
                if filename == f.name or filename == f.name.split(".")[0]
            ]
        ):
            result.append(filename)
    return result


if __name__ == "__main__":
    main()

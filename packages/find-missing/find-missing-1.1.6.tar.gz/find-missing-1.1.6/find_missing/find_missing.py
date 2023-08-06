import re
from pathlib import Path

import click


@click.command()
@click.option('-e/-p', "--exact/--partial", default=False)
@click.option('-v/-s', '--verbose/--silent', default=False)
@click.argument("list_of_files", type=str)
def main(list_of_files, exact: bool, verbose: bool):
    list_of_files = re.findall(r"[A-Za-z\d.\-_]+", list_of_files)

    if verbose:
        click.echo(f"Looking for files: {list_of_files}. Exact mode: {exact}")
    cwd = Path.cwd()

    files_in_folder = [f for f in list(cwd.glob("*.*")) if f.is_file()]

    if verbose:
        click.echo(f"Files in dir: {[f.name for f in files_in_folder]}")

    if not exact:
        result = find_partial_match(list_of_files, files_in_folder)
    else:
        result = find_exact_match(list_of_files, files_in_folder)

    if verbose:
        click.echo(f'\nFound {len(result)} missing files:')

    if result:
        click.echo("\n".join(result))
    elif not result and verbose:
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

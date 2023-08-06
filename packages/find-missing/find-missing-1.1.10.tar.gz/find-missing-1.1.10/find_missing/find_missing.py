import re
from pathlib import Path

import click


@click.command()
@click.option("-e/-p", "--exact/--partial", default=False)
@click.option("-v/-s", "--verbose/--silent", default=False)
@click.option("-d/-f", "--dirs/--files-only", default=False)
@click.argument("list_of_files", type=str)
def main(list_of_files, exact: bool, verbose: bool, dirs: bool):
    list_of_files = re.findall(r"[A-Za-z\d.\-_]+", list_of_files)

    if verbose:
        click.echo(f'Verbose mode: True. Exact mode: {exact}. Include directories: {dirs}')
        click.echo(
            f"Looking for files: {', '.join(list_of_files)}"
        )
    cwd = Path.cwd()

    if not dirs:
        files_in_folder = [f for f in list(cwd.glob("*.*")) if f.is_file()]
    else:
        files_in_folder = [
            f for f in list(cwd.glob("*.*")) if f.is_file() or f.is_dir()
        ]

    if verbose:
        dir_content = sorted([f'{f.name}/' for f in files_in_folder if f.is_dir()])
        file_content = sorted([f'{f.name}' for f in files_in_folder if f.is_file()])
        dir_content.extend(file_content)
        representation = '\n\t...\n\t' + '\n\t'.join(dir_content)
        click.echo(f'Directory content:{representation}')

    if not exact:
        result = find_partial_match(list_of_files, files_in_folder)
    else:
        result = find_exact_match(list_of_files, files_in_folder)

    if verbose:
        click.echo(f"\nFound {len(result)} missing files:")

    if result:
        click.echo("\n".join(result))
    elif not result and verbose:
        click.echo("All here!")


def find_partial_match(list_of_files, files_in_folder):
    result = []
    for filename in list_of_files:
        if not bool([f for f in files_in_folder if filename.lower() in f.name.lower()]):
            result.append(filename)
    return result


def find_exact_match(list_of_files, files_in_folder):
    result = []
    for filename in list_of_files:
        if not bool(
            [
                f
                for f in files_in_folder
                if filename.lower() == f.name.lower() or filename.lower() == f.name.split(".")[0].lower()
            ]
        ):
            result.append(filename)
    return result


if __name__ == "__main__":
    main()

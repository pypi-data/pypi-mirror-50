"""Toml Sort CLI"""

import click

from . import TomlSort


def get_help() -> str:
    """Get the help string for the current click context"""
    ctx = click.get_current_context()
    help_message = ctx.get_help()
    ctx.exit()
    return help_message


@click.command()
@click.option(
    "-o",
    "--output",
    type=click.File("w"),
    default="-",
    show_default=True,
    help="The output filepath. Choose stdout with '-'.",
)
@click.option(
    "-i",
    "--ignore-non-tables",
    is_flag=True,
    help="Only sort top-level Tables / Arrays of Tables",
)
@click.option(
    "-s",
    "--super-tables",
    is_flag=True,
    help="Include 'Super Tables' in the output",
)
@click.argument("filename", type=click.File("r"), default="-")
@click.version_option()
def cli(output, ignore_non_tables, filename, super_tables) -> None:
    """Sort toml file FILENAME, saving results to a file, or stdout (default)

    FILENAME a filepath or standard input (-)

    Examples:

        Read from stdin, write to stdout:

            cat input.toml | toml-sort

        Read from file on disk, write to file on disk:

            toml-sort -o output.toml input.toml

        Read from file on disk, write to stdout

            toml-sort input.toml

        Read from stdin, write to file on disk

            cat input.toml | toml-sort -o output.toml

        Only sort the top-level tables / arrays of tables

            cat input.toml | toml-sort -i

        Include Super Tables

            cat input.toml | toml-sort -s
    """
    if filename.isatty():
        click.echo(get_help())
        return

    only_sort_tables = bool(ignore_non_tables)
    include_super_tables = bool(super_tables)
    toml_content = filename.read()
    sorted_toml = TomlSort(
        toml_content, only_sort_tables, include_super_tables
    ).sorted()
    output.write(sorted_toml)

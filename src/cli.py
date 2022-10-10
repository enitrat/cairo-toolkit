import sys
import os
import click
import traceback

from typing import List
from starkware.cairo.lang.version import __version__
from logic import check_files, generate_interfaces, get_contracts_from_protostar, print_version, generate_ordered_imports


@click.group()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def cli():
    pass


@click.command()
@click.option("--files", '-f', multiple=True, default=[], help="File paths")
@click.option('--protostar', '-p', is_flag=True, help='Uses `protostar.toml` to get file paths')
@click.option('--directory', '-d', help='Output directory for the interfaces. If unspecified, they will be created in the same directory as the contracts')
def generate(protostar: bool, directory: str, files: List[str]):
    if protostar:
        protostar_path = os.path.join(os.getcwd(), "protostar.toml")
        files = get_contracts_from_protostar(protostar_path)

    sys.exit(generate_interfaces(directory, files))


@click.command()
@click.option("--files", multiple=True, default=[], help="Contracts to check")
@click.option('--protostar', '-p', is_flag=True, help='Uses `protostar.toml` to get file paths')
@click.option('--directory', '-d', help='Directory of the interfaces to check. Interfaces must be named `i_<contract_name>.cairo`')
def check(protostar: bool, directory: str, files: List[str]):
    if protostar:
        protostar_path = os.path.join(os.getcwd(), "protostar.toml")
        files = get_contracts_from_protostar(protostar_path)
    sys.exit(check_files(directory, files))


@click.command()
@click.option("--files", '-f', multiple=True, default=[], help="File paths")
def order_imports(directory: str, files: List[str]):

    sys.exit(generate_ordered_imports(directory, files))

cli.add_command(generate)
cli.add_command(check)
cli.add_command(order_imports)

def main():
    cli()


if __name__ == "__main__":
    sys.exit(main())

import argparse
import sys
import os
import toml
import traceback

from typing import Callable

from starkware.cairo.lang.compiler.ast.module import CairoFile, CairoModule
from starkware.cairo.lang.compiler.parser import parse_file
from starkware.cairo.lang.version import __version__

from starknet_interface_generator.generator import Generator


def get_contracts_from_protostar(protostar_path: str):
    config = toml.load(protostar_path)
    contracts = config['protostar.contracts']
    contracts_paths = [contract[0] for contract in contracts.values()]
    return contracts_paths


def cairo_interface_generator(cairo_parser: Callable[[str, str], CairoFile], description: str):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-v", "--version", action="version",
                        version=f"%(prog)s {__version__}")
    parser.add_argument("files", metavar="file", type=str,
                        nargs="*", help="File names")
    parser.add_argument("--protostar", action='store_true')
    parser.add_argument("-d", "--directory", type=str)
    args = parser.parse_args()

    if args.protostar:
        protostar_path = os.path.join(os.getcwd(), "protostar.toml")
        files = get_contracts_from_protostar(protostar_path)
    else:
        files = args.files

    for path in files:
        contract_file = open(path).read()
        dirpath, filename = os.path.split(path)
        contract_name = filename.split(".")[0]
        newfilename = f"i_" + filename
        newpath = os.path.join(args.directory or dirpath, newfilename)

        try:

            # Generate the AST of the cairo contract, visit it and generate the interface
            contract = CairoModule(
                cairo_file=cairo_parser(contract_file, filename),
                module_name=path,
            )

            generator = Generator(contract_name)
            contract_interface_str = generator.generate_contract_interface(
                contract)

            # Generate the AST from the cairo interface, format it, and write it to a file
            contract_interface = CairoModule(
                cairo_file=cairo_parser(contract_interface_str, newfilename),
                module_name=path,
            )
            formatted_interface = contract_interface.format()

        except Exception as exc:
            print(exc, file=sys.stderr)
            return 1

        print(f"Generating interface {newpath}")
        open(newpath, "w").write(formatted_interface)

    return 0


def main():
    def cairo_parser(code, filename): return parse_file(
        code=code, filename=filename)

    return cairo_interface_generator(
        cairo_parser=cairo_parser, description="A tool to automatically generate the interface of a cairo contract."
    )


if __name__ == "__main__":
    sys.exit(main())

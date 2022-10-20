# Cairo-toolkit

A set of useful tools for cairo / starknet development.

- Generate / check the interfaces corresponding to your Starknet contracts.
- Easily order your imports

## Installation

`pip install cairo-toolkit`

## Usage

```
cairo-toolkit [OPTIONS] COMMAND [ARGS]...

Options:
  --version
  --help     Show this message and exit.

Commands:
  check-interface
  generate-interface
  order-imports
```

### Generate interfaces

```
Usage: cairo-toolkit generate-interface [OPTIONS]

Options:
  -f, --files TEXT      File paths
  -p, --protostar       Uses `protostar.toml` to get file paths
  -d, --directory TEXT  Output directory for the interfaces. If unspecified,
                        they will be created in the same directory as the
                        contracts
  --help                Show this message and exit.
```

### Check existing interfaces

```
Usage: cairo-toolkit check-interface [OPTIONS]

Options:
  --files TEXT          Contracts to check
  -p, --protostar       Uses `protostar.toml` to get file paths
  -d, --directory TEXT  Directory of the interfaces to check. Interfaces must
                        be named `i_<contract_name>.cairo`
  --help                Show this message and exit.
```

### Ordering imports in existing file

```
Usage: cairo-toolkit order-imports [OPTIONS]

Options:
  -d, --directory TEXT  Directory with cairo files to format
  -f, --files TEXT      File paths
  -i, --imports TEXT    Imports order
  --help                Show this message and exit.
```

## Example

Generate interfaces for the contracts in `contracts/` and put them in `interfaces/`:

```
find contracts/ -iname '*.cairo' -exec cairo-toolkit generate-interface --files {} \;
```

Check the interface for `test/main.cairo` against the interface `i_main.cairo` in interfaces/:

```
cairo-toolkit check-interface --files test/main.cairo -d interfaces
```

Order imports for all cairo files under `test`

```
cairo-toolkit order-imports -d test
```

## Protostar

You can use cairo-toolkit in a protostar project.
This can be paired with a github action to automatically generate the interfaces for the contracts
that specified inside the `protostar.toml` file.

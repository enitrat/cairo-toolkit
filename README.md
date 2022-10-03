# Starknet interface generator

Generate / check the interfaces corresponding to your Starknet contracts.

## Installation

`pip install starknet-interface-generator`

## Usage

Options :

### Generate interfaces

```
Usage: starknet-interface-generator generate [OPTIONS]

Options:
  --files TEXT          File paths
  -p, --protostar       Uses `protostar.toml` to get file paths
  -d, --directory TEXT  Output directory for the interfaces. If unspecified,
                        they will be created in the same directory as the
                        contracts
  --help                Show this message and exit.
```

### Check existing interfaces

```
starknet-interface-generator check [OPTIONS]

Options:
  --files TEXT          Contracts to check
  -p, --protostar       Uses `protostar.toml` to get file paths
  -d, --directory TEXT  Directory of the interfaces to check. Interfaces must
                        be named `i_<contract_name>.cairo`
  --help                Show this message and exit.
```

## Example

Generate interfaces for the contracts in `contracts/` and put them in `interfaces/`:

```
find contracts/ -iname '*.cairo' -exec starknet-interface-generator generate --files {} \;
```

Check the interface for `test/main.cairo` against the interface `i_main.cairo` in interfaces/:

```
starknet-interface-generator check --files test/main.cairo -d interfaces
```

## Protostar

You can use starknet-interface-generator in a protostar project.
This can be paired with a github action to automatically generate the interfaces for the contracts
that specified inside the `protostar.toml` file.

`starknet-interface-generator [generate||check] --protostar`

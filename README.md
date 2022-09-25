# Starknet interface generator

Generate the interfaces corresponding to your Starknet contracts.

## Dependencies

- cairo-lang

## Installation

`pip install starknet-interface-generator`

## Usage

`starknet-interface-generator file_path [-d output_directory] [-o filename]`

## Example

`i_main` inside the interfaces directory was generated with this command :

```
starknet-interface-generator test/main-cairo -d interfaces -o i_main
```

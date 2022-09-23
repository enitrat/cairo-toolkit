# Cairo interface generator

Generate the interfaces corresponding to your Cairo contracts

## Dependencies
- cairo-lang

## Installation
`pip install cairo-interface-generator`

## Usage
```python cairo_interface.py file_path [-d output_directory] [-o filename]```


## Example
`i_main` inside the interfaces directory was generated with this command : 
```
cairo-interface-generator test/main-cairo -d interfaces -o i_main
```
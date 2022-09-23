# Cairo interface generator

Generate the corrsponding interfaces of your Cairo contracts.

## Dependencies
- cairo-lang

## Installation
`pip install cairo-interface-generator`

## Usage
```python cairo_interface.py file_path [-d output_directory] [-o filename]```


## Example
`i_main` inside the interfaces directory was generated with this command : 
```python cairo_interface.py src/main.cairo -o i_main -d interfaces```
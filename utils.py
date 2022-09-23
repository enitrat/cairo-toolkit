
# Write a function that returns a camelCase string from a snake_case string.
def to_camel_case(string: str) -> str:
    return "".join(word.title() for word in string.split("_"))

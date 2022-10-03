
def to_camel_case(string: str) -> str:
    return "".join(word.title() for word in string.split("_"))

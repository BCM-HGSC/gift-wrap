_MAP = {
    "y": True,
    "yes": True,
    "t": True,
    "true": True,
    "on": True,
    "1": True,
    "n": False,
    "no": False,
    "f": False,
    "false": False,
    "off": False,
    "0": False,
}


def strtobool(value) -> bool:
    """Converts string to bool"""
    try:
        return _MAP[str(value).lower()]
    except KeyError as e:
        raise ValueError(f'"{value}" is not a valid bool value') from e

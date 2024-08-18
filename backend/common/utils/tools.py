from typing import Any, List


def parse_list(v: Any) -> List[str] | str:
    """
    Parse a value to list.

    Parameters
    ----------
    v: Any
        the value to parse

    Returns
    -------
    list[str] | str
    """
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise (ValueError(v))

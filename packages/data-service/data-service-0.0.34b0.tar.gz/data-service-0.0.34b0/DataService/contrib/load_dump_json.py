import json
import typing

T = typing.TypeVar("T")

def load_json(path: str, verbose=True) -> T:
    if verbose:
        print("load from path: {}".format(path))
    with open(path, encoding="utf-8") as file:
        data = json.load(file)
    return data


def dump_json(data, path, verbose=True, **kwargs) -> bool:
    if verbose:
        print("save to path: {}".format(path))
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=1, **kwargs)
    except Exception as e:
        print("error: {}".format(e))
        return False
    return True

from types import SimpleNamespace

def dict_to_obj(data):
    if isinstance(data, dict):
        return SimpleNamespace(**{k: dict_to_obj(v) for k, v in data.items()})
    elif isinstance(data, list):
        return [dict_to_obj(item) for item in data]
    else:
        return data
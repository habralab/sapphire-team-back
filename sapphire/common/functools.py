from functools import reduce


def get_nested(storage: dict, *keys):
    return reduce(
        lambda value, key: value.get(key, {}) if isinstance(value, dict) else None,
        keys,
        storage,
    )

def get_filter_by_args(model_class, dic_args: dict):
    filters = []
    for key, value in dic_args.items():  # type: str, any
        if key.endswith('__min'):
            key = key[:-5]
            filters.append(getattr(model_class, key) >= value)
        elif key.endswith('__max'):
            key = key[:-5]
            filters.append(getattr(model_class, key) <= value)
        else:
            filters.append(getattr(model_class, key).like(f'%{value}%'))

    return filters


def to_dict(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(
                    convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return d

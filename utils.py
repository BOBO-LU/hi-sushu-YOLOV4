def upsert(d: dict, label: str, value: int = 1):

    d.setdefault(label, 0)
    d[label] += value

    return d

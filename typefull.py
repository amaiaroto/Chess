def get_nested_type(obj):
    t = type(obj)

    if t in (int, str, float, bool, type(None)):
        return t.__name__

    if t is tuple:
        types = ", ".join(get_nested_type(item) for item in obj)
        return f"tuple[{types}]"

    # Handle lists: return list<type> if homogeneous, else list<unknown>
    if t is list:
        if not obj:
            return "list[empty]"

        elem_types = set(get_nested_type(item) for item in obj)
        if len(elem_types) == 1:
            return f"list[{elem_types.pop()}]"
        return "list[unknown]"

    if t is dict:
        if not obj:
            return "dict[empty]"
        key_types = set(get_nested_type(k) for k in obj.keys())
        val_types = set(get_nested_type(v) for v in obj.values())
        kt = key_types.pop() if len(key_types) == 1 else "unknown"
        vt = val_types.pop() if len(val_types) == 1 else "unknown"
        return f"dict[{kt}, {vt}]"

    return t.__name__

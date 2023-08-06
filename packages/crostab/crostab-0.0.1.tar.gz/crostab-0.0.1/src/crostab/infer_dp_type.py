def infer_dp_type(some):
    if isinstance(some, str):
        if some.isnumeric():
            return 'str_num'
        else:
            return 'str'
    else:
        return type(some).__name__

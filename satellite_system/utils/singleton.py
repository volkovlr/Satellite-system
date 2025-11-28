def singleton(cls):
    _instances = {}

    def return_obj(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]
    return return_obj
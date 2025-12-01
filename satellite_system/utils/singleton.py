def singleton(cls):
    """Collect all instances of 'singleton' classes

    Returns:
        _type_
    """
    _instances = {}

    def return_obj(*args, **kwargs):
        """Create and return single object of some class

        Returns:
            _type_
        """
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]
    return return_obj
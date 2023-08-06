def _write(_path, _content):
    """

    Parameters
    ----------
    _path : str
    _content : str
    """
    with open(_path, "w+") as f:
        f.write(_content)

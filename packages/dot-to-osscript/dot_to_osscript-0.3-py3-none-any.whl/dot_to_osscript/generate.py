import re
from os import path, environ
from ._read import _read
from ._write import _write


def _concat_values(value_a, value_b, unix_var=True):
    """

    Parameters
    ----------
    value_a : str
    value_b : str
    unix_var : bool

    Returns
    -------
    str
    """
    if unix_var:
        return value_a + ":" + value_b
    else:
        return value_a + ";" + value_b


def _env_sh(_dict, path_append=True):
    """
    Parameters
    ----------
    _dict : dict

    Returns
    -------
    str
    """
    text = ""
    for k, v in _dict.items():
        if path_append and k == "PATH":
            text += k + "=\"" + "$PATH:" + v + "\"\n"
        else:
            text += k + "=\"" + v + "\"\n"
    return text


def _env_ps(_dict, path_append=True):
    """
    Parameters
    ----------
    _dict : dict

    Returns
    -------
    str
    """
    text = ""
    for k, v in _dict.items():
        if path_append and re.search('path', k, re.IGNORECASE):
            text += "Set-Variable" + \
                    " -Name \'" + "Path" + "\'" + \
                    " -Value \'" + "$env:Path;" + v + "\'" + \
                    " -Scope \'Global\';" + \
                    " Write-Output \"%s=%s\"\n" % (k, v)
        else:
            text += "Set-Variable" + \
                    " -Name \'" + k + "\'" + \
                    " -Value \'" + v + "\'" + \
                    " -Scope \'Global\';" + \
                    " Write-Output \"%s=%s\"\n" % (k, v)

    return text


def from_dotenv(ps=False, sh=False, env_file="./.env", path_append=True):
    d = _read(env_file)
    if d:
        if ps:
            _write(".env.ps1", _env_ps(d, path_append=path_append))
        if sh:
            _write(".env.sh", _env_sh(d, path_append=path_append))

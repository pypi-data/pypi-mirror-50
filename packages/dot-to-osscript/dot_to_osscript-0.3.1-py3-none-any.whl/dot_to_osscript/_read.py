from os import path


def _read(file_path):
    d = {}
    try:
        # with open(path.realpath(file_path), "r") as f:
        with open(file_path, "r") as f:
            for l in f.readlines():
                parts = l.split("=", maxsplit=1)
                if parts:
                    var = parts[0].strip()
                    val = parts[1].strip()
                    val = val.strip("\'")
                    val = val.strip("\"")
                    d.update({var: val})
        return d
    except Exception as e:
        return None

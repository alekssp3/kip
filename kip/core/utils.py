from pathlib import Path


def make_absolute(app_path, path):
    if not Path(path).is_absolute():
        return Path(app_path).joinpath(path)
    return Path(path)
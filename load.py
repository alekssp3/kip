from pathlib import Path
from kip.utils.Errors import NotAFileError

def load(filename, mode='text'):
    file = Path(filename)
    if not file.exists():
        raise FileNotFoundError
    if not file.is_file():
        raise NotAFileError
    with open(filename, 'rb') as f:
        if mode == 'raw':
            data = f.read()
        else:
            data = [line.strip() for line in f.readlines()]
    return data

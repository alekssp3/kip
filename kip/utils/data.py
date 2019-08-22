from .Errors import WrongTypeError, NotAFileError
from pathlib import Path


def save(what=None, filename=None):
    """
    :param filename:
    :type what: list
    """
    if not isinstance(what, (list, tuple, dict)):
        raise WrongTypeError
    if filename is None:
        filename = input('Input file name: ')
    with open(filename, 'w', encoding='utf-8') as f:
        for i in what:
            f.write(str(i) + '\n')


def load(filename, mode='text'):
    """
    :param filename:
    """
    file = Path(filename)
    if not file.exists():
        print(f'File {file} not found')
        raise FileNotFoundError
    if not file.is_file():
        print(f'{file} is not file')
        raise NotAFileError
    with open(filename, 'r', encoding='utf-8') as f:
    # with open(filename, 'r') as f:
        if mode == 'raw':
            data = f.read()
        else:
            data = [line.strip() for line in f.readlines()]
    return data

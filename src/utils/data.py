from .Errors import WrongTypeError


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


def load(filename='', mode='text'):
    if filename == "":
        filename = input('Input file name: ')
    with open(filename, 'r', encoding='utf-8') as f:
        if mode == 'raw':
            data = f.read()
        else:
            data = [line.strip() for line in f.readlines()]
    return data

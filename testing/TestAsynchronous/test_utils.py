import time


def timeit(foo):
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = foo(*args, **kwargs)
        end = time.monotonic()
        print('Execution time: {} ms'.format(int(end * 1000 - start * 1000)))
        return result
    return wrapper


def RoundRobin(init=[]):
    tasks = None or init
    while tasks:
        task = tasks.pop(0)
        try:
            yield next(task)
            tasks.append(task)
        except StopIteration:
            if not tasks:
                break

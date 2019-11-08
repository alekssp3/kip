import requests
import asyncio
from time import time


file = 'file-1573211536.3653588.txt'


def load(filename=None):
    if filename is not None:
        with open(filename, 'r') as file:
            yield from file.readlines()


async def ping(url):
    # print(f'Work with {url}')
    return requests.get(url)


def main():
    loop = asyncio.get_event_loop()
    tasks = [ping(i) for i in load(file)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == "__main__":
    start = time()
    main()
    print(time() - start)

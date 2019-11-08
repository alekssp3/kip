# import requests
from requests_html import AsyncHTMLSession
# import asyncio
from time import time


file = 'file-1573211536.3653588.txt'


def load(filename=None):
    if filename is not None:
        with open(filename, 'r') as file:
            yield from file.readlines()


def ping_creator(session, url):
    async def inner():
        print(f'Work with {url}')
        r = await session.get(url)
        return r
    return inner


async def ping(session, url):
    # print(f'Work with {url}')
    r = await session.get(url)
    return r


def main():
    # loop = asyncio.get_event_loop()
    # tasks = [ping(i) for i in load(file)]
    # loop.run_until_complete(asyncio.wait(tasks))
    # loop.close()
    session = AsyncHTMLSession()
    tasks = [ping_creator(session, url) for url in load(file)]
    session.run(*tasks)


if __name__ == "__main__":
    start = time()
    main()
    print(time() - start)

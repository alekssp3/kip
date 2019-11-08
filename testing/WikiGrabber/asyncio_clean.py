# import requests
from requests_html import AsyncHTMLSession
# import asyncio
from time import time
import os
import sys
# sys.path.insert(0, os.path.abspath(os.getcwd()))
# from grabber2 import create_file_from_list


#file = 'file-1573211536.3653588.txt'

file = 'width1.txt'

RESULTS = []


def create_file_from_list(data, filename=None):
    '''Create text file from data'''
    filename = filename or 'file-{}.txt'.format(time())
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('\n'.join(i for i in data))


def load(filename=None):
    if filename is not None:
        with open(filename, 'r') as file:
            yield from file.readlines()


def ping_creator(session, url):
    async def inner():
        try:
            print(f'Work with {url}')
            r = await session.get(url)
            links = r.html.absolute_links
            RESULTS.extend(links)
            # print(len(links))
        except:
            pass
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
    print(len(RESULTS))
    create_file_from_list(RESULTS)

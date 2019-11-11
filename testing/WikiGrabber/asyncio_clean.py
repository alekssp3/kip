from requests_html import AsyncHTMLSession
from time import time

file = 'width1.txt'

RESULTS = set()
FILTER = ('jpeg', 'jpg', 'png', 'ogg', 'ogv', 'mp3', 'mp4', 'pdf')


def create_file_from_list(data, filename=None):
    '''Create text file from data'''
    filename = filename or 'file-{}.txt'.format(time())
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('\n'.join(i for i in data))


def load(filename=None):
    if filename is not None:
        with open(filename, 'r', encoding='utf-8') as file:
            yield from file.readlines()


def ping_creator(session, url):
    async def inner():
        try:
            # print(f'Work with {url}')
            r = await session.get(url)
            links = r.html.absolute_links
            RESULTS.update(links)
        except Exception as e:
            print(f'Faled with url {url}')
            print(e)
            pass
    return inner


def filtered_url(url):
    for f in FILTER:
        if url.endswith('.' + f) or url.startswith('#'):
            return False
    return True


def main():
    session = AsyncHTMLSession()
    working_list = set([i for i in load(file)])
    print(f'Len of working list {len(working_list)}')
    tasks = [ping_creator(session, url) for url in working_list if filtered_url(url)]
    session.run(*tasks)


if __name__ == "__main__":
    start = time()
    main()
    print(time() - start)
    print(len(RESULTS))
    create_file_from_list(RESULTS)

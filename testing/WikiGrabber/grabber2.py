from time import time
import requests_html


TASKS = [(r'https://en.wikipedia.org/wiki/Main_Page', 2)]
DONE = set()


class Grabber():
    '''Grab page from Wikipedia.org'''
    def __init__(self, **kwargs):
        self.session = requests_html.AsyncHTMLSession()
        self.url = kwargs['url']
        self.width = kwargs['width']
        self.run()

    async def get_session(self):
        s = await self.session.get(self.url)
        return s

    def run(self):
        self.session.run(self.get_session)


def main():
    '''Main function'''
    while TASKS:
        url, width = TASKS.pop(0)
        if url not in DONE and width > 0:
            DONE.add(url)
            grabber = Grabber(url=url, width=width)
            grabs = grabber.grab()
            print(f'Len: {len(grabs)} from {url=}')
            for link in grabs:
                TASKS.append((link, width-1))


def create_file_from_list(data, filename=None):
    '''Create text file from data'''
    filename = filename or 'file-{}.txt'.format(time())
    with open(filename, 'w') as file:
        file.write('\n'.join(i for i in data))


if __name__ == "__main__":
    main()

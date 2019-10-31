import re
from time import time
import requests


class Grabber():
    '''Grab page from Wikipedia.org'''
    def __init__(self, **kwargs):
        self.pattern = r'<a\s.*?href="(.+?)".*?>(.+?)</a>'
        # self.pattern = r'<a\s.*?href="(.+?)".*</a>'
        self.url = kwargs['url']

    def get_regexp(self, pattern=None):
        '''Return regex object'''
        pattern = pattern or self.pattern
        regexp = re.compile(pattern)
        return regexp

    def grab(self):
        '''Grab text from regex object'''
        if self.url is None:
            return None
        return self.get_regexp().findall(requests.get(self.url).text)


def main():
    '''Main function'''
    grabber = Grabber(url='https://en.wikipedia.org/wiki/Main_Page')
    grabs = grabber.grab()
    print(f'Len: {len(grabs)}')
    create_file('\n'.join('\t'.join((i[0], i[1])) for i in grabs))


def create_file(data, filename=None):
    '''Create text file from data'''
    filename = filename or 'file-{}.txt'.format(time())
    with open(filename, 'w') as file:
        file.write(data)


if __name__ == "__main__":
    main()

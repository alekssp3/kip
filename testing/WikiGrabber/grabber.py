import re
import requests
from time import time

class Grabber():
    def __init__(self, *args, **kwargs):
        self.pattern = r'<a\s.*?href="(.+?)".*?>(.+?)</a>'
        # self.pattern = r'<a\s.*?href="(.+?)".*</a>'
        self.url = kwargs['url']

    def get_regexp(self, pattern=None):
        pattern = pattern or self.pattern
        regexp = re.compile(pattern)
        return regexp

    def grab(self):
        if self.url is None:
            return
        return self.get_regexp().findall(requests.get(self.url).text)


def main():
    grabber = Grabber(url='https://en.wikipedia.org/wiki/Main_Page')
    grabs = grabber.grab()
    print(f'Len: {len(grabs)}')
    # create_file('\n'.join('\t'.join((i[0], i[1])) for i in grabs))
    


def create_file(data, filename=None):
    filename = filename or 'file-{}.txt'.format(time())
    with open(filename, 'w') as file:
        file.write(data)


if __name__ == "__main__":
    main()


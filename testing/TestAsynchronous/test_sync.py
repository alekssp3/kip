import re
import time
import requests
from test_utils import timeit


URL = 'https://en.wikipedia.org/wiki/Main_Page'
TASKS = []
RESULT = set()
RESPONSE = []


def get_response(url):
    RESPONSE.append(requests.get(url))


def get_url_text():
    RESPONSE.pop(0).text


def grab_all_links(text):
    pattern = r'<a\s.*?href="(.+?)".*?>(.+?)</a>'
    regexp = re.compile(pattern)
    links = (i[0] for i in regexp.findall(text))
    return links


def get_url_from_link(url, link):
    if link.startswith('#'):
        out = url + link
    elif link.startswith('//'):
        out = url.split('/')[0] + link
    elif link.startswith('/'):
        out = '/'.join(url.split('/')[:3]) + link
    else:
        out = link
    return out


def start():
    # start_time = time.monotonic()
    url, depth = TASKS.pop(0)
    if url not in RESULT:
        RESULT.add(url)
    get_response(url)
    text = get_url_text()
    for t in text:
        links = grab_all_links(t)
        for link in links:
            cur_url = get_url_from_link(url, link)
            if cur_url not in RESULT:
                RESULT.add(cur_url)
                if depth - 1 > 0:
                    TASKS.append((cur_url, depth - 1))


def async_start():
    pass


@timeit
def main():
    TASKS.append((URL, 1))
    while TASKS:
        start()
    print(f'Len: {len(RESULT)}')


if __name__ == "__main__":
    main()

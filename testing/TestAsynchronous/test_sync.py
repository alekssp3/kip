import re
import time
import requests

URL = 'https://en.wikipedia.org/wiki/Main_Page'
TASKS = []
RESULT = set()
RESPONSE = []


def timeit(foo):
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = foo(*args, **kwargs)
        end = time.monotonic()
        print(end * 1000 - start * 1000)
        return result
    return wrapper


def get_response(url):
    return RESPONSE.append(requests.get(url))


def get_url_text():
    yield RESPONSE.pop(0).text


def grab_all_links(text):
    pattern = r'<a\s.*?href="(.+?)".*?>(.+?)</a>'
    regexp = re.compile(pattern)
    links = (i[0] for i in regexp.findall(text))
    for i in links:
        yield i


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


@timeit
def main():
    TASKS.append((URL, 2))
    while TASKS:
        start()
    print(f'Len: {len(RESULT)}')


if __name__ == "__main__":
    main()

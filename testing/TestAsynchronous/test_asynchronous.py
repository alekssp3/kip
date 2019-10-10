from time import time
import re
import requests
# from bs4 import BeautifulSoup, SoupStrainer

url='https://en.wikipedia.org/wiki/Main_Page'


# def get_response(url):
#     _resp = requests.get(url)
#     if _resp:
#         return _resp


# def get_soup(response):
#     if response is not None:
#         return BeautifulSoup(response.content, 'html.parser', parse_only=SoupStrainer('a'))


# def get_links_with_soup(soup):
#     out = []
#     for link in soup:
#         if link.has_attr('href'):
#             out.append(link['href'])
#     return out


def get_links_with_re(text):
    # its like bs without bs ^_^
    pattern = r'<a\s.*?href="(.+?)".*?>(.+?)</a>'
    # only 272 links
    # pattern = r'<a href="(.+?)">'
    # only 11 links
    # pattern = r'<a href="([^"]+)">'
    regexp = re.compile(pattern)
    return regexp.findall(text)
    

def simple_foo():
    # response = get_response(url)
    # soup = get_soup(response)
    # links = get_links_with_soup(soup)
    # for link in links:
    #     print(link)
    # print(f'Len of links list: {len(links)}')
    pass


def simple_async_foo():
    pass


def main():
    start1 = time()
    simple_foo()
    end1 = time()
    print(f'simple foo: {end1 - start1}')
    start2 = time()
    # simple_async_foo
    end2 = time()
    print(f'simple async foo: {end2 - start2}')


if __name__ == '__main__':
    # main()
    response = requests.get(url)
    links = get_links_with_re(response.text)
    
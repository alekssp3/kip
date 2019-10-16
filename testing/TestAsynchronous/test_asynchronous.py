from time import time
import re
import requests
from multiprocessing import Process

url='https://en.wikipedia.org/wiki/Main_Page'
links_to_prepare = []
links_to_work = []
links_all_done = []
links_buffer = set()
errors = []

def get_links_with_re(text):
    pattern = r'<a\s.*?href="(.+?)".*?>(.+?)</a>'
    regexp = re.compile(pattern)
    return [i[0] for i in regexp.findall(text)]


def get_normal_link(link):
    if link.startswith('http'):
        return link
    elif link.startswith('//'):
        return links_all_done[0].split('/')[0] + link
    elif link.startswith('/'):
        return '/'.join(links_all_done[0].split('/')[:3]) + link
    else:
        return links_all_done[0] + link


def worker():
    while True:
        if links_to_work:
            link, weidth = links_to_work.pop(0)
            if link in links_buffer:
                continue
            elif weidth < 1:
                links_all_done.append(link)
                continue
            else:
                links_buffer.add(link)
                links_to_prepare.append(link)
                response = requests.get(link)
                # print('after response')
                if response:
                    # for l in get_links_with_re(response.text):
                        # links_to_work.append((get_normal_link(l), weidth-1))
                    links_to_work.extend([(get_normal_link(l), weidth-1) for l in get_links_with_re(response.text)])
                    # print('after adding')
                else:
                    errors.append((link, weidth))
        else:
            print('All done.')
            break


def main():    
    links_to_work.append((url, 1))
    worker()

if __name__ == '__main__':
    main()
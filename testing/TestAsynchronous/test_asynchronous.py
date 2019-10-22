import re
import requests
from datetime import datetime

URL = 'https://en.wikipedia.org/wiki/Main_Page'
TASKS = []
RESULT = []


def grab_all_urls(url):
    response = requests.get(url)
    if response:
        pattern = r'<a\s.*?href="(.+?)".*?>(.+?)</a>'
        regexp = re.compile(pattern)
        links = (i[0] for i in regexp.findall(response.text))
        for link in links:
            if link.startswith('#'):
                out = url + link
            elif link.startswith('//'):
                out = url.split('/')[0] + link
            elif link.startswith('/'):
                out = '/'.join(url.split('/')[:3]) + link
            else:
                out = link
            if out not in RESULT:
                yield out


def event_loop():
    while TASKS:
        url, depth = TASKS.pop(0)
        if url not in RESULT:
            RESULT.append(url)
        urls = grab_all_urls(url)
        for cur_url in urls:
            RESULT.append(cur_url)
            if depth - 1 > 0:
                TASKS.append((cur_url, depth - 1))


if __name__ == '__main__':
    TASKS.append((URL, 1))
    start = datetime.now()
    event_loop()
    print(f'Time: {datetime.now() - start}')
    print(f'Len: {len(RESULT)}')


# инициируем очередь чтения новой ссылкой и глубиной сканирования
# пока в очереди есть ссылки
#     вынуть ссылку из очереди
#     отправить запрос 
#     прочитать ответ
#     распарсить ответу
#     привести ссылки из ответа в нормальный вид
#     поместить нормализованные ссылки в очередь
import requests
from re import compile
from time import time


TASKS = []
RESULTS = set()
EXTENTIONS = 'pfd png jpg jpeg avi ogg'.split()


class Task:
    pass


def create_task(*args, **kwargs):
    task = Task()
    for arg in args:
        if str(type(Task())) in str(arg.__class__):
            task.__dict__.update(arg.__dict__)
            break
    task.__dict__.update(kwargs)
    TASKS.append(task)


def grab_links(text):
    pattern = r'<a\s.*?href="(.+?)".*?>(.+?)</a>'
    regexp = compile(pattern)
    links = (i[0] for i in regexp.findall(text))
    return links


def task_info(task):
    print(f'Job: {task.job}')
    print('Params:')
    for i in task.__dict__:
        if i not in 'job':
            print(f' {i} : {task.__dict__[i]}')


def normalize_link(url, link):
    if link.startswith('#'):
        out = url + link
    elif link.startswith('//'):
        out = url.split('/')[0] + link
    elif link.startswith('/'):
        out = '/'.join(url.split('/')[:3]) + link
    else:
        out = link
    return out


def jobs_manager():
    task = TASKS.pop(0)
    task_info(task)
    if task.job == 'request':
        if task.url not in RESULTS and task.depth > 0:
            create_task(task, job='filter')
    if task.job == 'filter':
        ext = task.url.split('.')[-1]
        if ext.lower() not in EXTENTIONS:
            create_task(task, job='response', ext=ext)
    if task.job == 'response':
        response = requests.get(task.url)
        create_task(task, job='grab_links', response=response)
    if task.job == 'grab_links':
        links = grab_links(task.response.text)
        for link in links:
            create_task(task, job='normalize', link=link)
    if task.job == 'normalize':
        norm = normalize_link(task.url, task.link)
        create_task(task, job='result', normalized=norm)
    if task.job == 'result':
        RESULTS.add(task.normalized)
        depth = task.depth - 1
        create_task(job='request', depth=depth, url=task.normalized)


def main():
    start = time()
    create_task(job='request', url='https://en.wikipedia.org/wiki/Main_Page', depth=2)
    while TASKS:
        jobs_manager()
    stop = time()
    print(f'RESULTS LEN: {len(RESULTS)}')
    print(f'Time: {stop-start}')


if __name__ == '__main__':
    main()

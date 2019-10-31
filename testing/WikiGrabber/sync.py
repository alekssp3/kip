import requests


TASKS = []
RESULTS = []

class Task:
    def __init__(self, *args, **kwargs):
        self.do = kwargs['do']
        self.params = kwargs['params']


# task1 = Task(do='request', params={'url':'https://en.wikipedia.org/wiki/Main_Page', 'depth':1})
# TASKS.append(task1)


def create_task(**kwargs):
    TASKS.append(Task(**kwargs))


create_task(do='request', params={'url':'https://en.wikipedia.org/wiki/Main_Page', 'depth':1})

    
def jobs_manager():
    task = TASKS.pop(0)
    job = task.do
    params = task.params
    print(f'Job: \n {job}')
    print('Params:')
    for i in params:
        print(f' {i}: {params[i]}')
    if job == 'request':
        if params['url'] not in RESULTS and params['depth'] > 0:
            create_task(do='response', params=params)
    if job == 'response':
        url = params['url']
        params['text'] = requests.get(url)
        create_task(do='grab_links', params=params)
    if job == 'grab_links':
        create_task(do='normalize_links', params=params)
    if job == 'normalize_links':
        create_task(do='result', params=params)
    if job == 'result':
        url = params['url']
        RESULTS.append(url)
        params['depth'] = params['depth'] - 1
        create_task(do='request', params=params)
        

def main():
    while TASKS:
        jobs_manager()

if __name__ == '__main__':
    main()

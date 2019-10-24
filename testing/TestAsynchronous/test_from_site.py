import asyncio
import requests


urls = ['http://www.google.com', 'http://www.yandex.ru', 'http://www.python.org']


async def call_url(urls):
    while urls:
        url = urls.pop(0)
        print('Starting {}'.format(url))
        response = requests.get(url)
        data = response.text()
        print('{}: {} bytes: {}'.format(url, len(data), data))
        return data


async def main():
    task1 = asyncio.create_task(call_url(urls))

    await asyncio.gather(task1)


if __name__ == "__main__":
    asyncio.run(main())
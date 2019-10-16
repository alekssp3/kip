import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    # await say_after(1, 'hello')
    # await say_after(3, 'world')
    # await say_after(2, 'Some else')
    tasks = []
    tasks.append(asyncio.create_task(say_after(1, 'hello')))
    tasks.append(asyncio.create_task(say_after(8, 'world')))
    tasks.append(asyncio.create_task(say_after(5, 'some else')))

    for t in tasks:
        await t

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
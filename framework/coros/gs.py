import asyncio
import random

async def my_coro(id):
    process_time = random.randint(1,5)
    await asyncio.sleep(process_time)
    print(f'Coroutine {id}, has completed after {process_time} seconds')
    return f"{id}"

async def first_coro():
    while True:
            await asyncio.sleep(2)
            print('first_coro')

async def second_coro():
    while True:
            await asyncio.sleep(2)
            print('second_coro')

async def main():
    tasks = [asyncio.ensure_future(my_coro(i)) for i in range(10,0, -1)]
    await asyncio.gather(*tasks)
    for t in tasks:
        print(t.result())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())

    asyncio.ensure_future(first_coro())
    asyncio.ensure_future(second_coro())
    loop.run_forever()
import asyncio

def process_all(tasks):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    return loop.run_until_complete(asyncio.gather(*[task for task in tasks]))
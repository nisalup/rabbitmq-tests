import asyncio

from new_task import new_task

QUEUE_NAME = "B"

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(new_task(QUEUE_NAME))

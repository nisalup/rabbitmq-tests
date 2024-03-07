import aio_pika
import asyncio

QUEUE_NAMES = ["A", "B"]

async def callback(message: aio_pika.abc.AbstractIncomingMessage):
    origin_queue = {message.routing_key}

    print(f"{origin_queue} [x] Received {message.body.decode()}")
    await asyncio.sleep(message.body.count(b'.'))
    print(f"{origin_queue} [x] Done")
    await message.ack()

async def worker():
    connection = await aio_pika.connect_robust(
        host="localhost"
    )
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    for queue_name in QUEUE_NAMES:
        locals()[f'queue_{queue_name}'] = await channel.declare_queue(queue_name, durable=True, auto_delete=False)
        await locals()[f'queue_{queue_name}'].consume(callback)
        print(f"{queue_name} [*] Waiting for messages. To exit press CTRL+C")

    await asyncio.Future()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(worker())

import asyncio
import aio_pika
import sys

EXCHANGE_NAME = "requests_handler"

QUEUE_NAMES = ["A", "B"]

async def new_task(queue_name=QUEUE_NAMES[0]):
    connection = await aio_pika.connect_robust(
                    host="localhost"
                )
    channel = await connection.channel()

    queue = await channel.declare_queue(queue_name, durable=True, auto_delete=False)

    exchange = await channel.declare_exchange(
        EXCHANGE_NAME,
        durable=True,
        auto_delete=False
    )

    message = bytes(''.join(sys.argv[1:]) or ".", encoding='utf8')

    await exchange.publish(
        aio_pika.Message(body=message,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        ),
        routing_key=queue.name
    )
    print(f"{queue_name} [x] Sent {message}")
    await connection.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(new_task())

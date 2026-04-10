import asyncio
import json
import random
from datetime import datetime, timezone

from aiokafka import AIOKafkaProducer


async def produce_market_ticks() -> None:
    producer = AIOKafkaProducer(bootstrap_servers="localhost:9092")
    await producer.start()
    try:
        while True:
            event = {
                "symbol": random.choice(["AAPL", "TSLA", "NVDA", "MSFT"]),
                "price": round(random.uniform(90, 500), 2),
                "volume": random.randint(100, 5000),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            await producer.send_and_wait("market-ticks", json.dumps(event).encode("utf-8"))
            await asyncio.sleep(0.01)
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(produce_market_ticks())

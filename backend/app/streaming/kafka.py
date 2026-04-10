from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from aiokafka import AIOKafkaProducer
from tenacity import retry, stop_after_attempt, wait_fixed


@dataclass
class TradeEvent:
    order_id: str
    symbol: str
    side: str
    quantity: float
    price: float
    model_score: float
    risk_score: float


class KafkaTradeProducer:
    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self._producer: AIOKafkaProducer | None = None

    async def start(self) -> None:
        self._producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        await self._producer.start()

    async def stop(self) -> None:
        if self._producer:
            await self._producer.stop()

    @retry(wait=wait_fixed(0.02), stop=stop_after_attempt(3))
    async def publish(self, event: TradeEvent) -> None:
        if not self._producer:
            raise RuntimeError("Producer not started")
        payload = json.dumps(asdict(event)).encode("utf-8")
        await self._producer.send_and_wait(self.topic, payload)

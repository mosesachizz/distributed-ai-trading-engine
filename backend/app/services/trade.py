from __future__ import annotations

import time
from datetime import datetime, timezone
from uuid import uuid4

from app.schemas.trade import TradeRequest, TradeResponse
from app.services.ml import LSTMPredictor
from app.services.risk import AdaptiveRiskEngine
from app.streaming.kafka import KafkaTradeProducer, TradeEvent


class TradeOrchestrator:
    def __init__(
        self,
        risk_engine: AdaptiveRiskEngine,
        model: LSTMPredictor,
        producer: KafkaTradeProducer,
    ) -> None:
        self.risk_engine = risk_engine
        self.model = model
        self.producer = producer

    async def execute(self, request: TradeRequest) -> TradeResponse:
        started = time.perf_counter()
        rsi = 48.5
        volatility = 0.18
        model_score = self.model.predict_edge(request.price, rsi, volatility)
        risk_score = self.risk_engine.calculate_risk_score(
            quantity=request.quantity,
            price=request.price,
            rsi=rsi,
            volatility=volatility,
        )
        accepted = model_score >= 0.35 and not self.risk_engine.should_block(risk_score)
        order_id = str(uuid4())
        event = TradeEvent(
            order_id=order_id,
            symbol=request.symbol,
            side=request.side.value,
            quantity=request.quantity,
            price=request.price,
            model_score=model_score,
            risk_score=risk_score,
        )
        await self.producer.publish(event)
        latency_ms = (time.perf_counter() - started) * 1000
        if latency_ms > 50:
            accepted = False
        return TradeResponse(
            accepted=accepted,
            order_id=order_id,
            model_score=model_score,
            risk_score=risk_score,
            created_at=datetime.now(timezone.utc),
        )

from app.core.config import get_settings
from app.services.ml import LSTMPredictor
from app.services.risk import AdaptiveRiskEngine
from app.services.trade import TradeOrchestrator
from app.streaming.kafka import KafkaTradeProducer

settings = get_settings()
producer = KafkaTradeProducer(settings.kafka_bootstrap_servers, settings.kafka_order_topic)
risk_engine = AdaptiveRiskEngine(settings.risk_max_notional, settings.risk_max_daily_loss)
model = LSTMPredictor(settings.model_path)
orchestrator = TradeOrchestrator(risk_engine=risk_engine, model=model, producer=producer)


def get_trade_orchestrator() -> TradeOrchestrator:
    return orchestrator

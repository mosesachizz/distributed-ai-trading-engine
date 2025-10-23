"""
Entry point for the Distributed AI Trading Engine.
"""

import asyncio
import uvicorn
from src.core.trade_engine import TradeEngine
from src.core.risk_manager import RiskManager
from src.core.market_data import MarketData
from src.streaming.kafka_consumer import MarketDataConsumer
from src.utils.config import Config
from src.utils.logger import setup_logger

async def main():
    """Initialize and start the trading engine."""
    logger = setup_logger(__name__)
    config = Config()
    
    # Initialize components
    market_data = MarketData()
    risk_manager = RiskManager(
        max_position=config.get("risk.max_position", 10000.0),
        volatility_threshold=config.get("risk.volatility_threshold", 0.05)
    )
    trade_engine = TradeEngine(
        model_path=config.get("model.path", "models/trading_model.h5"),
        risk_manager=risk_manager,
        market_data=market_data
    )
    
    # Start Kafka consumer
    consumer = MarketDataConsumer(
        bootstrap_servers=config.get("kafka.bootstrap_servers", "localhost:9092"),
        topic=config.get("kafka.topic", "market-data"),
        callback=trade_engine.execute_trade
    )
    
    # Start trading engine and API
    try:
        logger.info("Starting trading engine and API...")
        trade_engine.start()
        consumer_task = asyncio.create_task(asyncio.to_thread(consumer.start))
        api_task = asyncio.create_task(
            uvicorn.run(
                "src.api.trade_api:app",
                host="0.0.0.0",
                port=8000,
                reload=False
            )
        )
        await asyncio.gather(consumer_task, api_task)
    except Exception as e:
        logger.error("Application failed: %s", str(e))
        raise

if __name__ == "__main__":
    asyncio.run(main())
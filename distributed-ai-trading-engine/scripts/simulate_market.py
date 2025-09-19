"""
Script to simulate market data and send to Kafka.
"""

import time
import random
import numpy as np
from src.streaming.kafka_producer import MarketDataProducer
from src.utils.logger import setup_logger
from src.utils.config import Config

def simulate_market_data():
    """Simulate market data and send to Kafka."""
    logger = setup_logger(__name__)
    config = Config()
    producer = MarketDataProducer(
        bootstrap_servers=config.get("kafka.bootstrap_servers", "localhost:9092"),
        topic=config.get("kafka.topic", "market-data")
    )
    
    logger.info("Starting market data simulation...")
    price = 100.0  # Starting price
    price_history = [price]
    
    while True:
        # Simulate price movement
        price *= (1 + np.random.normal(0, 0.01))
        price_history.append(price)
        if len(price_history) > 50:
            price_history.pop(0)
        
        # Calculate features
        volume = random.randint(500, 5000)
        volatility = np.std(price_history[-20:]) / np.mean(price_history[-20:]) if len(price_history) >= 20 else 0.01
        sma = np.mean(price_history[-20:]) if len(price_history) >= 20 else price
        rsi = 50.0
        if len(price_history) >= 14:
            deltas = np.diff(price_history[-14:])
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            avg_gain = np.mean(gains)
            avg_loss = np.mean(losses) + 1e-10
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
        
        market_data = {
            "symbol": "AAPL",
            "price": round(price, 2),
            "volume": volume,
            "volatility": round(volatility, 3),
            "sma": round(sma, 2),
            "rsi": round(rsi, 2)
        }
        producer.send(market_data)
        logger.debug("Simulated market data: %s", market_data)
        time.sleep(0.1)  # Simulate 100ms intervals

if __name__ == "__main__":
    simulate_market_data()
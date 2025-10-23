"""
Kafka consumer for real-time market data streaming.
Integrates with the trading engine for trade execution.
"""

import logging
from kafka import KafkaConsumer
from typing import Callable
import json
from ..utils.logger import setup_logger

class MarketDataConsumer:
    """Consumes market data from Kafka and processes it."""
    
    def __init__(self, bootstrap_servers: str, topic: str, callback: Callable):
        """Initialize the Kafka consumer.
        
        Args:
            bootstrap_servers (str): Kafka server addresses.
            topic (str): Kafka topic to subscribe to.
            callback (Callable): Function to process market data.
        """
        self.logger = setup_logger(__name__)
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset="latest",
            value_deserializer=lambda x: json.loads(x.decode("utf-8"))
        )
        self.callback = callback
        self.logger.info("Kafka consumer initialized for topic: %s", topic)

    def start(self):
        """Start consuming market data from Kafka."""
        self.logger.info("Starting Kafka consumer...")
        try:
            for message in self.consumer:
                market_data = message.value
                self.logger.debug("Received market data: %s", market_data)
                self.callback(market_data)
        except Exception as e:
            self.logger.error("Kafka consumer error: %s", str(e))
            raise
"""
Kafka producer for sending market data to the trading engine.
"""

import logging
import json
from kafka import KafkaProducer
from ..utils.logger import setup_logger

class MarketDataProducer:
    """Produces market data to Kafka topics."""
    
    def __init__(self, bootstrap_servers: str, topic: str):
        """Initialize the Kafka producer.
        
        Args:
            bootstrap_servers (str): Kafka server addresses.
            topic (str): Kafka topic to publish to.
        """
        self.logger = setup_logger(__name__)
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        self.topic = topic
        self.logger.info("Kafka producer initialized for topic: %s", topic)

    def send(self, market_data: dict):
        """Send market data to Kafka topic.
        
        Args:
            market_data (dict): Market data to publish.
        """
        try:
            self.producer.send(self.topic, market_data)
            self.producer.flush()
            self.logger.debug("Sent market data to Kafka: %s", market_data)
        except Exception as e:
            self.logger.error("Failed to send market data: %s", str(e))
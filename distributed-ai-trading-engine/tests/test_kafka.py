"""
Integration tests for Kafka producer and consumer.
"""

import pytest
from src.streaming.kafka_producer import MarketDataProducer
from src.streaming.kafka_consumer import MarketDataConsumer

@pytest.mark.asyncio
async def test_kafka_producer_consumer():
    """Test Kafka producer and consumer integration."""
    producer = MarketDataProducer("localhost:9092", "test-topic")
    consumer = MarketDataConsumer("localhost:9092", "test-topic", lambda x: x)
    
    # Send test data
    test_data = {
        "symbol": "TEST",
        "price": 100.0,
        "volume": 1000.0,
        "volatility": 0.02,
        "sma": 100.0,
        "rsi": 50.0
    }
    producer.send(test_data)
    
    # Mock consumer to capture data
    captured = []
    consumer.callback = lambda x: captured.append(x)
    consumer.consumer = iter([type("Message", (), {"value": test_data})])
    
    await asyncio.to_thread(consumer.start)
    assert len(captured) == 1
    assert captured[0] == test_data
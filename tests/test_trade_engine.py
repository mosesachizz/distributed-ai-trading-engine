"""
Unit tests for the TradeEngine class.
"""

import pytest
import numpy as np
from src.core.trade_engine import TradeEngine
from src.core.risk_manager import RiskManager
from src.core.market_data import MarketData
from src.utils.metrics import MetricsCollector

@pytest.fixture
def trade_engine():
    """Fixture for TradeEngine instance."""
    risk_manager = RiskManager()
    market_data = MarketData()
    return TradeEngine("models/trading_model.h5", risk_manager, market_data)

def test_execute_trade_valid(trade_engine):
    """Test trade execution with valid market data."""
    market_data = {
        "symbol": "AAPL",
        "price": 150.0,
        "volume": 1000.0,
        "volatility": 0.02,
        "sma": 148.0,
        "rsi": 50.0
    }
    trade = trade_engine.execute_trade(market_data)
    assert trade is not None
    assert trade["symbol"] == "AAPL"
    assert trade["action"] in ["buy", "sell"]
    assert trade_engine.metrics.trade_execution_count > 0

def test_execute_trade_invalid_risk(trade_engine, mocker):
    """Test trade rejection due to high risk."""
    mocker.patch.object(RiskManager, "evaluate_risk", return_value=False)
    market_data = {
        "symbol": "AAPL",
        "price": 150.0,
        "volume": 1000.0,
        "volatility": 0.1,
        "sma": 148.0,
        "rsi": 80.0
    }
    trade = trade_engine.execute_trade(market_data)
    assert trade is None
    assert trade_engine.metrics.trade_rejection_count > 0
"""
Unit tests for the RiskManager class.
"""

import pytest
from src.core.risk_manager import RiskManager

@pytest.fixture
def risk_manager():
    """Fixture for RiskManager instance."""
    return RiskManager(max_position=10000.0, volatility_threshold=0.05)

def test_evaluate_risk_valid(risk_manager):
    """Test risk evaluation with valid data."""
    prediction = [0.7]
    market_data = {"volatility": 0.02, "rsi": 50.0}
    assert risk_manager.evaluate_risk(prediction, market_data) is True

def test_evaluate_risk_high_volatility(risk_manager):
    """Test risk evaluation with high volatility."""
    prediction = [0.7]
    market_data = {"volatility": 0.1, "rsi": 50.0}
    assert risk_manager.evaluate_risk(prediction, market_data) is False

def test_evaluate_risk_extreme_rsi(risk_manager):
    """Test risk evaluation with extreme RSI."""
    prediction = [0.7]
    market_data = {"volatility": 0.02, "rsi": 80.0}
    assert risk_manager.evaluate_risk(prediction, market_data) is False

def test_calculate_position_size(risk_manager):
    """Test position size calculation."""
    market_data = {"volatility": 0.02}
    position_size = risk_manager.calculate_position_size(market_data)
    assert position_size == 9800.0  # 10000 * (1 - 0.02)